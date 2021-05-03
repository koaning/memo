import orjson
from typing import Callable, Dict, List, Iterable, Optional
from types import GeneratorType
from functools import wraps
from joblib import Parallel, delayed, parallel_backend
import joblib.parallel
from rich.progress import Progress
import time
import warnings


class Runner():
    """Run functions in parallel with joblib
        joblib has 3 standard options for backends. 2 process based {"loky", "multiprocessing"}
        and 1 thread based {"threading"}. Depending on the function you wish to run one approach
        may be considerably faster than another. See links for more details

        The other important argument is the number of jobs `n_jobs` which dictates the
        number of cpu cores for proecess based backends or number of threads for thread
        based backend. You can pass -1 to use all cores available or the number
        you'd like to run e.g n_jobs=2. Be aware that over-subscription of CPU resources
        e.g n_jobs=32 on a 6 core processer will adversely affect performance
        See links for more details

        All keyword arguments during instantiaition will pass through to `parallel_backend`

        Notes
        joblib can also attach to third party backends such as Ray or Apache spark,
        however that functionality has not yet been tested

        Links
        https://joblib.readthedocs.io/en/latest/parallel.html
    """

    def __init__(self, *args, backend: Optional[str] = 'loky', n_jobs: Optional[int] = None, **kwargs, ):
        self.args = args
        self.kwargs = kwargs
        self.backend = backend
        self.n_jobs = n_jobs

    def _run(self, func: Callable, settings: Iterable[Dict]) -> None:
        """run the parallel backend
            Private. All arguments passed through run method
        """
        try:
            with parallel_backend(*self.args, self.backend, self.n_jobs, **self.kwargs):
                Parallel(require="sharedmem")(
                    delayed(func)(**settings) for settings in settings
                )
        except TypeError as e:  # Help for the User as the traceback is not helpful when keyword argument is wrong
            import sys
            raise type(e)(str(e) + "\nCheck that arguments to Runner() are correct").with_traceback(sys.exc_info()[2])

    def run(self, func: Callable, settings: Iterable[Dict], progbar: bool = True) -> None:
        """Run function with joblibs parallel backend

        Args:
            func (Callable): The function to be run in parallel. 
            settings (Iterable): An Iterable of Key-value pairs. 
            progbar (bool, optional): Show progress bar. Defaults to True.

        Raises:
            TypeError: When **kwargs doesn't match signature of `parallel_backend`
        """
        if not isinstance(settings, (list, tuple, set, GeneratorType)):  # check settings is iterable
            raise TypeError(f"Type {type(settings)} not supported")
        elif progbar and not isinstance(settings, GeneratorType):
            total = len(settings)
            with Progress() as progress:
                task = progress.add_task("[red]Runner....", total=total)

                class BatchCompletionCallBack(object):

                    def __init__(self, dispatch_timestamp, batch_size, parallel):
                        self.dispatch_timestamp = dispatch_timestamp
                        self.batch_size = batch_size
                        self.parallel = parallel

                    def __call__(self, out):
                        self.parallel.n_completed_tasks += self.batch_size
                        this_batch_duration = time.time() - self.dispatch_timestamp

                        self.parallel._backend.batch_completed(self.batch_size,
                                                               this_batch_duration)

                        self.parallel.print_progress()
                        # Update progress bar
                        progress.update(task, completed=self.parallel.n_completed_tasks, refresh=True)
                        with self.parallel._lock:
                            if self.parallel._original_iterator is not None:
                                self.parallel.dispatch_next()
                # Monkey patch
                joblib.parallel.BatchCompletionCallBack = BatchCompletionCallBack
                self._run(func, settings)
        else:
            if isinstance(settings, GeneratorType):
                warnings.warn("Progress bar not supported for generator settings")
            self._run(func, settings)


def memlist(data: List):
    """
    Remembers input/output of a function in python list.

    Arguments:
        data: a list to push received data into

    Example

    ```python
    from memo import memlist

    data = []

    @memlist(data=data)
    def simulate(a, b):
        return {"result": a + b}

    # The `@memlist` decorator will allow the inputs/outputs to
    # be saved in the provided `data` list.
    for a in range(5):
        for b in range(10):
            simulate(a=a, b=b)

    assert len(data) == 50

    # If we keep running more loops the list will grow.
    for a in range(6, 10 + 1):
        for b in range(11, 20 + 1):
            simulate(a=a, b=b)

    assert len(data) == 100
    ```
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            data.append({**kwargs, **result})
            return result

        return wrapper

    return decorator


def memfile(filepath: str):
    """
    Remembers input/output of a function in a jsonl file on disk.

    Arguments:
        filepath: path to write data to

    ```python
    from memo import memfile

    @memfile(filepath="tmpfile.jsonl")
    def simulate(a, b):
        return {"result": a + b}

    for a in range(5):
        for b in range(10):
            simulate(a=a, b=b)
    ```
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filepath, "a") as f:
                ser = orjson.dumps(
                    {**kwargs, **result},
                    option=orjson.OPT_NAIVE_UTC | orjson.OPT_SERIALIZE_NUMPY,
                )
                f.write(ser.decode("utf-8") + "\n")
            return result

        return wrapper

    return decorator


def memfunc(callback: Callable):
    """
    Remembers input/output of a function by printing.

    Arguments:
        callback: callback function that receives a dictionary with logged info

    ```python
    from memo import memfunc, memlist

    data = []

    @memlist(data=data)
    @memfunc(callback=print)
    def simulate(a, b):
        return {"result": a + b}

    for a in range(5):
        for b in range(10):
            simulate(a=a, b=b)

    # You should now see print statements, and this holds:
    assert len(data) == 50
    ```
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            callback({**kwargs, **result})
            return result

        return wrapper

    return decorator
