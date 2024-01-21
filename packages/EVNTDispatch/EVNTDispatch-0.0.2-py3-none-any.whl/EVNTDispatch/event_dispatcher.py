import asyncio
import functools
import logging
import os

from asyncio import AbstractEventLoop, Task, Future
from typing import Callable, Any, Set, List, Dict, Union, Coroutine, Tuple, Generator, Iterable, Awaitable

from .event_listener import EventListener, Priority
from .pevent import PEvent
from .event_type import EventType
from .executor import Executor
from .utils import does_event_type_match
from .c_logger import CLogger


class EventDispatcher:
    """
    EventDispatcher handles event listeners, triggers events, and manages asynchronous execution of listeners.
    """
    UNLIMITED_RESPONDERS = -1

    def __init__(
            self,
            max_executor_workers: int = -1,
            debug_mode: bool = False,
    ):
        """
        Initialize the EventDispatcher.
        :param debug_mode: Enable debug mode for logging.
        :param max_executor_workers: The maximum number of workers for the underlying executor.
                                     Defaults to -1 which uses the available logical CPU count.
        """
        self.debug_mode = debug_mode

        self._listeners: Dict[str, List['EventListener']] = {}
        self._sync_canceled_future_events: Dict[str, int] = {}
        self._busy_listeners: Set[Coroutine] = set()

        # Event loop and related components
        self._event_queue_manager_task: Task = None  # noqa
        self._event_loop: AbstractEventLoop = None  # noqa
        self._event_queue = asyncio.Queue()
        self._queue_empty_event = asyncio.Event()  # Event signaling an empty queue

        # Dictionary to hold running tasks
        self._running_tasks: Dict[str, List[Union[Task, Future]]] = {}
        self._running_scheduled_tasks: List[Union[Task, Future]] = []
        self._time_until_final_task = 0  # Time until the final task is complete

        # Flags for controlling event dispatch and queue status
        self._cancel_events = False
        self._is_queue_primed = False
        self._is_event_loop_running = False
        self._had_error = False

        # Determine the total number of workers based on available logical cores
        cpu_count = os.cpu_count()
        total_logical_cores = cpu_count if cpu_count else 1
        total_workers = max_executor_workers if max_executor_workers != -1 else total_logical_cores

        self._executor = Executor(max_workers=total_workers)
        self._logger = CLogger('dispatcher', logging.INFO, {logging.StreamHandler(): logging.INFO})

    @property
    def is_queue_empty(self) -> bool:
        """
        Check if the event queue is empty.

        :return: True if the event queue is empty, False otherwise.
        """
        return self._event_queue.empty()

    @property
    def queue_size(self) -> int:
        """
        Get the size of the event queue.

        :return: The number of events in the queue.
        """
        return self._event_queue.qsize()

    def start(self, loop: AbstractEventLoop = None) -> None:
        """
        Start the event loop if not already running.

        :param loop: The event loop to use. If not provided, try to get the existing loop.
                    If all fails it creates a new event loop.
        """
        if not self._is_event_loop_running:
            self._event_loop = self._get_event_loop(loop)
            self._event_queue_manager_task = self._event_loop.create_task(self._event_loop_runner())
            self._is_event_loop_running = True

    async def close(self, wait_for_scheduled_tasks: bool = True) -> None:
        """
        Close the event loop and wait for queued and scheduled events to be processed.

        :param wait_for_scheduled_tasks: Flag to indicate whether to wait for scheduled tasks to complete.
        """
        if self._is_queue_primed:
            # Wait for all events in the queue to be processed
            await self._queue_empty_event.wait()
        else:
            # If no events have been placed in the queue, cancel the task to avoid indefinite waiting
            self._event_queue_manager_task.cancel('Canceling queue manager due to no events to process')

        if wait_for_scheduled_tasks:
            # Calculate the time left until the final task is complete
            final_task_complete_time = self._time_until_final_task - self._event_loop.time()
            # Ensure the value is positive or zero(z)
            z_final_task_complete_time = final_task_complete_time if final_task_complete_time > 0 else 0
            await asyncio.sleep(z_final_task_complete_time)

            await asyncio.gather(*self._running_scheduled_tasks)

        # all futures and tasks that have been created are collected here
        waitables_collection: Dict[AbstractEventLoop, List[Union[Task, Future]]] = {}

        # here we collect all the running tasks (async Events)
        for _, running_tasks in self._running_tasks.items():
            for task in running_tasks:
                if task.cancelled() or task.done():
                    continue
                loop = task.get_loop()

                if waitables_collection.get(loop):
                    waitables_collection[loop].append(task)
                else:
                    waitables_collection[loop] = [task]

        # wait for the completion of the varius tasks and futures running based on their loop
        for loop, waitables in waitables_collection.items():
            results = await asyncio.gather(*waitables, return_exceptions=True)
            for result in results:
                if isinstance(result, BaseException):
                    self._log_exception(result)

        self._executor.shutdown()

        self._is_event_loop_running = False

    def add_listener(self, event_name: str, listener: Callable, priority: Priority = Priority.NORMAL,
                     allow_busy_trigger: bool = True, event_type: EventType = EventType.Base) -> None:
        """
        Add a listener to the event.

        :param event_type: the type of event to respond to, EventType.Base responds to all types
        :param allow_busy_trigger: allow the listener to be trigger even if it's still running
        :param event_name: Name of the event.
        :param listener: Callable object representing the listener function.
        :param priority: Priority of the listener.
        """
        if callable(listener):
            self._register_event_listener(event_name, listener, priority, allow_busy_trigger, event_type)
            self._sort_listeners(event_name)
        else:
            raise ValueError("Listener must be callable (a function or method).")

    def remove_listener(self, event_name: str, callback: Callable) -> None:
        """
        Remove a listener from the event.

        :param event_name: Name of the event.
        :param callback: Callable object representing the listener function.
        """
        self.remove_listeners(event_name, (callback,))

    def remove_listeners(self, event_name: str, callbacks_to_remove: Iterable[Callable]) -> None:
        """
        Remove a group a listeners from the event.

        :param event_name: Name of the event.
        :param callbacks_to_remove: A collection of callable objects to remove
        """
        event_listeners = self._listeners.get(event_name)

        for listener in event_listeners:
            if listener.callback in callbacks_to_remove:
                event_listeners.remove(listener)

    def schedule_task(self, func: Union[Callable[..., None], Callable[..., Awaitable[None]]], exec_time: float,
                      *args: List) -> None:
        """
        Schedule a task to be executed after a specified time.

        Args:
            func (Union[Callable[..., None], Callable[..., Awaitable[None]]]): The function or coroutine to be scheduled.
            exec_time (float): The time delay (in seconds) before executing the task.
            *args: Additional arguments to be passed to the function or coroutine.

        Raises:
            Exception: If no event loop is running.
            ValueError: If `func` is not a callable.

        Returns:
            None
        """
        if not self._is_event_loop_running:
            raise Exception("No event loop running")

        if not callable(func):
            raise ValueError(f"({func}), must be a callable")

        if asyncio.iscoroutinefunction(func):
            time_handler = self._event_loop.call_later(exec_time, self._schedule_coroutine, func, *args)
        else:
            time_handler = self._event_loop.call_later(exec_time, self._schedule_func, func, *args)

        self._time_until_final_task = time_handler.when()

    def _schedule_coroutine(self, coro: Callable[..., Awaitable[None]], *args: List) -> None:
        """
        Internal method to schedule the execution of a coroutine after a specified time.

        Args:
            coro (Callable[..., Awaitable[None]]): The coroutine to be scheduled.
            *args: Additional arguments to be passed to the coroutine.

        Returns:
            None
        """

        async def wrapper():
            await coro(*args)

        task = self._event_loop.create_task(wrapper())

        self._running_scheduled_tasks.append(task)

        cleanup = functools.partial(self._clean_up_scheduled_task, task)

        task.add_done_callback(cleanup)

    def _schedule_func(self, func: Callable[..., None], *args: List) -> None:
        """
        Internal method to schedule the execution of a function after a specified time.

        Args:
            func (Callable[..., None]): The function to be scheduled.
            *args: Additional arguments to be passed to the coroutine.

        Returns:
            None
        """

        future = self._executor.submit(func, *args, is_scheduled_task=True)

        wrapped_future = asyncio.wrap_future(future, loop=self._event_loop)

        self._running_scheduled_tasks.append(wrapped_future)

        cleanup = functools.partial(self._clean_up_scheduled_task, wrapped_future)

        wrapped_future.add_done_callback(cleanup)

    def cancel_future_sync_event(self, event_name: str) -> None:
        """
        Cancel future occurrences of a synchronous event.

        This method increments the cancellation count for a specific synchronous event (`event_name`). It keeps track of
        the number of times the event has been canceled to prevent its future execution based on the cancellation count.

        If the event has already been canceled at least once, this method increments the cancellation count. Otherwise,
        it initializes the count to 1.

        :param event_name: The name or identifier of the synchronous event to cancel.
        """
        if self._sync_canceled_future_events.get(event_name):
            self._sync_canceled_future_events[event_name] += 1
        else:
            self._sync_canceled_future_events[event_name] = 1

    def cancel_event(self, event_name: str) -> None:
        """
        Cancel all running tasks associated with a specific event.

        This method cancels all running asynchronous tasks that are associated with a given event (`event_name`). It
        retrieves the tasks related to the specified event and attempts to cancel each task.

        :param event_name: The name or identifier of the event for which running asynchronous tasks should be canceled.
        """
        for task in self._running_tasks.get(event_name, []):
            try:
                task.cancel()
            except asyncio.CancelledError:
                print(f"failed to cancel task: {task.get_coro().__name__}")

    def sync_trigger(self, event: PEvent, *args, **kwargs) -> None:
        """
        Trigger the event and notify all registered listeners.

        :param event: The event to trigger.
        :param args: Additional arguments to pass to listeners.
        :param kwargs: Additional keyword arguments to pass to listeners.
        """
        if not self._is_event_loop_running:
            raise Exception("No event loop running")

        self._is_queue_primed = True
        self._event_queue.put_nowait((self._sync_trigger, event, args, kwargs))

    async def _sync_trigger(self, event: PEvent, *args, **kwargs) -> None:
        """
        Internal method to trigger the event and notify all registered listeners.

        :param event: The event to trigger.
        :param args: Additional arguments to pass to listeners.
        :param kwargs: Additional keyword arguments to pass to listeners.
        """
        if self._cancel_events or self._is_sync_event_cancelled(event):
            return

        running_futures = [
            self._run_sync_listener(listener, event, *args, **kwargs)
            for listener in self._get_listeners(event)
        ]

        results = await asyncio.gather(*running_futures, return_exceptions=True)
        for result in results:
            if isinstance(result, BaseException):
                self._log_exception(result)
                raise result

        self._run_coro_or_func(event.on_event_finish)

    async def _run_sync_listener(self, listener: EventListener, event: PEvent, *args, **kwargs):
        """
        Execute a synchronous event listener.

        This method executes a synchronous event listener represented by the provided `listener` object, passing the
        associated event (`event`) along with additional arguments and keyword arguments.

        If debug mode is enabled (`self.debug_mode`), it logs the invocation of the listener.

        :param listener: The EventListener representing the synchronous event listener function to execute.
        :param event: The event associated with the listener.
        :param args: Additional arguments to pass to the listener.
        :param kwargs: Additional keyword arguments to pass to the listener.
        """
        if self.debug_mode:
            self._log_listener_call(listener, event)

        future = self._executor.submit(listener.callback, event, *args, **kwargs)

        wrapped_future = asyncio.wrap_future(future)
        await wrapped_future

        if not wrapped_future.exception():
            self._run_coro_or_func(event.on_listener_finish)
        else:
            self._log_exception(wrapped_future.exception())
            raise wrapped_future.exception()

    async def async_trigger(self, event: PEvent, *args: Any, **kwargs: Any) -> None:
        """
        Asynchronously trigger the event and notify registered listeners.

        :param event: The event to trigger.
        :param args: Additional arguments to pass to listeners.
        :param kwargs: Additional keyword arguments to pass to listeners.
        """
        if not self._is_event_loop_running:
            raise Exception("No event loop running")

        self._is_queue_primed = True
        self._event_queue.put_nowait((self._async_trigger, event, args, kwargs))

    def async_trigger_nw(self, event: PEvent, *args: Any, **kwargs: Any) -> None:
        """
        Asynchronously trigger the event and notify registered listeners without waiting.

        :param event: The event to trigger.
        :param args: Additional arguments to pass to listeners.
        :param kwargs: Additional keyword arguments to pass to listeners.
        """
        if not self._is_event_loop_running:
            raise Exception("No event loop running")

        self._is_queue_primed = True
        self._event_queue.put_nowait((self._async_trigger, event, args, kwargs))

    async def _async_trigger(self, event: PEvent, *args: Any, **kwargs: Any) -> None:
        """
        Internal method to asynchronously trigger the event and notify registered listeners.

        :param event: The event to trigger.
        :param args: Additional arguments to pass to listeners.
        :param kwargs: Additional keyword arguments to pass to listeners.
        """
        if self._cancel_events:
            return

        callable_listeners = [
            event_listener for event_listener in self._get_listeners(event)
            if (event_listener.allow_busy_trigger or event_listener.callback not in self._busy_listeners
                or event.include_busy_listeners)
        ]

        for event_listener in callable_listeners:
            if self.debug_mode:
                self._log_listener_call(event_listener, event)
            if event_listener.callback not in self._busy_listeners:
                self._busy_listeners.add(event_listener.callback)

        tasks = [self._run_async_listener(listener, event, *args, **kwargs) for listener in callable_listeners]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # log out any errors
        for result in results:
            if isinstance(result, BaseException):
                self._log_exception(result, '_async_trigger')

        self._run_coro_or_func(event.on_event_finish)

    async def _run_async_listener(self, listener: EventListener, event: PEvent, *args, **kwargs):
        """
        Asynchronously run the specified listener for the given event.

        :param listener: The listener to run.
        :param event: The event being processed.
        :param args: Additional arguments to pass to the listener.
        :param kwargs: Additional keyword arguments to pass to the listener.
        """
        task = self._event_loop.create_task(listener.callback(event, *args, **kwargs))

        await task
        if listener.callback in self._busy_listeners:
            self._busy_listeners.remove(listener.callback)

        if task.exception():
            self._log_exception(task.exception())
            raise task.exception()
        else:
            self._run_coro_or_func(event.on_listener_finish)

    async def async_mixed_trigger(self, event: PEvent, *args, **kwargs):
        """
       Asynchronously trigger the event and notify registered sync and async listeners

       :param event: The event to trigger.
       :param args: Additional arguments to pass to listeners.
       :param kwargs: Additional keyword arguments to pass to listeners.
       """
        self._event_queue.put_nowait((self._mixed_trigger, event, args, kwargs))

    def sync_mixed_trigger(self, event: PEvent, *args, **kwargs):
        """
       Asynchronously trigger the event and notify registered sync and async listeners

       :param event: The event to trigger.
       :param args: Additional arguments to pass to listeners.
       :param kwargs: Additional keyword arguments to pass to listeners.
       """
        self._event_queue.put_nowait((self._mixed_trigger, event, args, kwargs))

    async def _mixed_trigger(self, event: PEvent, *args: Any, **kwargs: Any) -> None:
        if self._cancel_events:
            return

        self._is_queue_primed = True
        is_sync_event_cancelled = self._is_sync_event_cancelled(event)

        running_tasks = []
        for listener in self._get_listeners(event):
            if asyncio.iscoroutinefunction(listener.callback):
                task = self._event_loop.create_task(self._run_async_listener(listener, event, *args, **kwargs))
                running_tasks.append(task)
            elif not is_sync_event_cancelled:
                task = self._event_loop.create_task(self._run_sync_listener(listener, event, *args, **kwargs))
                running_tasks.append(task)

        await asyncio.gather(*running_tasks)

        self._run_coro_or_func(event.on_event_finish)

    # noinspection PyUnusedLocal
    def _remove_task_from_tracked_task(self, event: PEvent, task: Task, future: Future) -> None:
        """
        Clean up tracked tasks that have finished.

        Parameters:
        - event (PEvent): The event associated with the task.
        - task (Task): The task to clean up.
        - future (Future): The future associated with the task.

        Returns:
        None
        """
        if self._running_tasks.get(event.event_name):
            self._running_tasks[event.event_name].remove(task)

        if len(self._running_tasks.get(event.event_name, [])) == 0:
            self._running_tasks.pop(event.event_name)

    # noinspection PyUnusedLocal
    def _clean_up_scheduled_task(self, waitable: Union[Future, Task], future: Future) -> None:
        """
        Clean up a scheduled task.

        Parameters:
        - waitable (Union[Future, Task]): The scheduled task to clean up.
        - future (Future): The future associated with the scheduled task.

        Returns:
        None
        """
        try:
            self._running_scheduled_tasks.remove(waitable)
        except ValueError:
            # This error should never trigger, but just in case, catch it.
            pass

    def disable_all_events(self) -> None:
        """
        Disable all events from being triggered.
        """
        self._cancel_events = True

    def enable_all_events(self) -> None:
        """
        Enable all events to be triggered.
        """
        self._cancel_events = False

    def _get_listeners(self, event: PEvent) -> Generator[EventListener, None, None]:
        """
        Retrieve listeners associated with a specific event.

        Parameters:
        - event (PEvent): The event for which listeners are to be retrieved.

        Yields:
        EventListener: The next event listener associated with the specified event.
        """
        listeners = self._listeners.get(event.event_name, [])
        total_listeners = len(listeners)
        max_responders = min(event.max_responders, total_listeners) if event.max_responders > 0 else total_listeners

        total_responses = 0
        for listener in listeners:
            if total_responses >= max_responders:
                break

            if does_event_type_match(listener, event):
                yield listener

            total_responses += 1

    def _register_event_listener(self, event_name: str, callback: Callable, priority: Priority,
                                 allow_busy_trigger: bool = True, event_type: EventType = EventType.Base) -> None:
        """
        Register an event listener for the specified event.

        :param allow_busy_trigger: allow the listener to be trigger even if it's still running
        :param event_name: Name of the event.
        :param callback: Callable object representing the listener function.
        :param priority: Priority of the listener.
        """
        listener = EventListener(callback=callback, priority=priority, allow_busy_trigger=allow_busy_trigger,
                                 event_type=event_type)

        # if the callback is already registered in the event, return
        if listener.callback in [lstener for lstener in self._listeners.get(event_name, [])]:
            return

        if event_name in self._listeners:
            self._listeners[event_name].append(listener)
        else:
            self._listeners.update({event_name: [listener]})

    def _sort_listeners(self, event_name: str) -> None:
        """
        Sort the listeners for the specified event based on their priorities.

        :param event_name: Name of the event.
        """
        if event_name not in self._listeners:
            raise ValueError("event name not found")
        self._listeners[event_name] = sorted(self._listeners[event_name],
                                             key=lambda event_listener: event_listener.priority.value)

    def _log_listener_call(self, listener: EventListener, event: PEvent) -> None:
        """
        Log the invocation of an event listener, including whether it's synchronous or asynchronous.

        :param listener: The event listener being invoked.
        :param event: The event associated with the listener.
        """

        if listener.callback in self._busy_listeners and not event.include_busy_listeners and not listener.allow_busy_trigger:
            self._logger.info(f"skipping call to: [{listener.callback.__name__}] as it's busy")
        else:
            self._logger.info(f"[{listener.callback.__name__}] triggered from event [{event.event_name}]")

    def _log_exception(self, error: BaseException, *args) -> None:
        self._had_error = True
        self._logger.error(f'{error} | {args}')

    def _get_event_loop(self, loop: asyncio.AbstractEventLoop = None) -> AbstractEventLoop:
        """
        get the event loop, creates a new one if one isn't already running.

        Note:
            this method edits the dispatchers _event_loop attribute
        """
        if not loop:
            try:
                self._event_loop = asyncio.get_running_loop()
            except RuntimeError:
                self._event_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._event_loop)
        else:
            self._event_loop = loop

        return self._event_loop

    def _add_task_to_tracked_task(self, task: Union[Task, Future], event: PEvent) -> None:
        """
        Add a task associated with a specific event to the running tasks.

        Parameters:
        - task (Union[Task, Future]): The task or future to be added to the running tasks.
        - event (PEvent): The event associated with the task.

        Returns:
        None
        """
        if self._running_tasks.get(event.event_name):
            self._running_tasks[event.event_name].append(task)
        else:
            self._running_tasks[event.event_name] = [task]

    def _is_sync_event_cancelled(self, event: PEvent) -> bool:
        """
        Check if a synchronous event has been canceled.

        Parameters:
        - event (PEvent): The event to check for cancellation.

        Returns:
        bool: True if the event has been canceled, False otherwise.
        """
        # If the event has not been canceled at least once, return false
        if not self._sync_canceled_future_events.get(event.event_name, 0):
            return False

        self._sync_canceled_future_events[event.event_name] -= 1

        # Remove the event data from the dictionary
        if self._sync_canceled_future_events[event.event_name] < 1:
            self._sync_canceled_future_events.pop(event.event_name)

        return True

    def _run_coro_or_func(self, func: Union[Callable[..., None], Callable[..., Coroutine]], *args, **kwargs) -> None:
        if func is None:
            return

        if not callable(func):
            error = TypeError(f'{func} is not callable')
            self._log_exception(error)
            raise error

        try:
            if asyncio.iscoroutinefunction(func):
                coro = func(*args, *kwargs)
                self._event_loop.create_task(coro)
            else:
                func(*args, **kwargs)
        except Exception as e:
            self._log_exception(e, "run coro or func")

    async def _event_loop_runner(self):
        """
        Run the event loop to process queued events.
        """

        while self._is_event_loop_running:
            queue_item: Tuple[Union[Callable, Coroutine], PEvent, Any, Any] = await self._event_queue.get()
            event_executor, event, args, kwargs = queue_item

            task = self._event_loop.create_task(event_executor(event, *args, **kwargs))
            self._add_task_to_tracked_task(task, event)

            cleanup = functools.partial(self._remove_task_from_tracked_task, event, task)
            task.add_done_callback(cleanup)

            # if the queue is empty set the empty event (true)
            if self._event_queue.empty():
                self._queue_empty_event.set()
            # else clear the event (false)
            else:
                self._queue_empty_event.clear()

            self._event_queue.task_done()
