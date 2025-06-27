import concurrent.futures
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, List, Optional, Tuple
from pokesys.config.app import APP_CONFIG
from pokesys.logger import logger


class Executor:
    """
    Pool to manage the execution of synchronous code.
    Executor distributes tasks to ThreadPool.
    """    
    _instance = None
    _lock = threading.Lock()    

    def __init__(self):
        self.num_threads = APP_CONFIG.executor_num_threads
        self.thread_pool = ThreadPoolExecutor(max_workers=self.num_threads)

    @classmethod
    def get_instance(cls):
        """Returns the singleton instance in a thread-safe manner."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def submit(self, f: Callable, *args, **kwargs):
        """
        Submits a task to the appropriate pool based on the function type.
        Returns a Future to track the result.
        """
        return self.thread_pool.submit(f, *args, **kwargs)

    def _submit_to_async_worker(self, coro):
        """Distribute a coroutine to an asynchronous worker using round-robin."""
        worker = self.async_workers[self.async_worker_index]
        self.async_worker_index = (self.async_worker_index + 1) % self.num_async_workers
        return worker.submit(coro)

    def shutdown(self):
        """Shutdown the executor, closing the pools."""
        self.thread_pool.shutdown()

    def __del__(self):
        self.shutdown()


def scatter_gather(
    to_send: List[Callable],
    args_list: Optional[List[Tuple[Any, ...]]] = None,
    kwargs_list: Optional[List[Dict[str, Any]]] = None,
    *,
    timeout: Optional[float] = None,
) -> Tuple[Any, ...]:
    """
    Sends different sets of arguments/kwargs to a list of modules (callables)
    and collects the responses.

    Each callable in `to_send` receives the positional arguments of the corresponding `tuple`
    in `args_list` and the named arguments of the corresponding `dict` in `kwargs_list`.
    If `args_list` or `kwargs_list` are not provided (or are `None`), the corresponding callables
    will be called without positional or named arguments, respectively,
    unless an empty list (`[]`) or empty tuple (`()`) is provided for a specific item.

    Args:
        to_send: List of callable objects (e.g. functions or `Module` instances).
        args_list: Optional list of tuples. Each tuple contains the positional arguments
            for the corresponding callable in `to_send`. If `None`, no positional arguments 
            are passed unless specified individually by an item in `kwargs_list`.
        kwargs_list: Optional list of dictionaries. Each dictionary contains the named arguments 
            for the corresponding callable in `to_send`. If `None`, no named arguments are passed 
            unless specified individually by an item in `args_list`.
        timeout: Maximum time (in seconds) to wait for responses.

    Returns:
        Tuple containing the responses for each callable. If an error or timeout occurs for a 
        specific callable, its corresponding response in the tuple will be `None`.

    Raises:
        TypeError: If `to_send` is not a callable list.
        ValueError: If the lengths of `args_list` (if provided) or `kwargs_list`
            (if provided) do not match the length of `to_send`.

    Examples:
        def add(x, y): return x + y
        def multiply(x, y=2): return x * y
        callables = [add, multiply, add]

        # Example 1: Using only args_list
        args = [ (1, 2), (3,), (10, 20) ] # multiply will use its default y
        results = scatter_gather(callables, args_list=args)
        print(results) # (3, 6, 30)

        # Example 2: Using args_list e kwargs_list
        args = [ (1,), (), (10,) ]
        kwargs = [ {'y': 2}, {'x': 3, 'y': 3}, {'y': 20} ]
        results = scatter_gather(callables, args_list=args, kwargs_list=kwargs)
        print(results) # (3, 9, 30)

        # Example 3: Using only kwargs_list (useful if functions have defaults or don't need positional args)
        def greet(name="World"): return f"Hello, {name}"
        def farewell(person_name): return f"Goodbye, {person_name}"
        funcs = [greet, greet, farewell]
        kwargs_for_funcs = [ {}, {'name': "Earth"}, {'person_name': "Commander"} ]
        results = scatter_gather(funcs, kwargs_list=kwargs_for_funcs)
        print(results) # ("Hello, World", "Hello, Earth", "Goodbye, Commander")
    """
    if not isinstance(to_send, list) or not all(callable(f) for f in to_send):
        raise TypeError("`to_send` must be a non-empty list of callable objects")

    executor = Executor.get_instance()
    futures = []
    for i, f in enumerate(to_send):
        args = args_list[i] if args_list and i < len(args_list) else ()
        kwargs = kwargs_list[i] if kwargs_list and i < len(kwargs_list) else {}
        futures.append(executor.submit(f, *args, **kwargs))
    
    done, _ = concurrent.futures.wait(futures, timeout=timeout)
    responses: List[Any] = []
    for FUTURE in done:
        try:
            responses.append(FUTURE.result())
        except Exception as e:
            logger.error(str(e))
            responses.append(None)
    return tuple(responses)
