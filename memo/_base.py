
import orjson
from typing import Callable, List
from types import GeneratorType
from functools import wraps
from joblib import Parallel, delayed, parallel_backend
import joblib.parallel
from rich.progress import Progress
import time


def mempar(*args, progbar=True, **kwargs):
    """Wraps joblib's Parallel for easy parallelization
    @mempar will parrallelize any function that is wrapped with @memlist
    The function to be parrellized must be called with an interable containing
    key : value pairs that match the original signature of the function (see example).


    # Arguments:
        *args : passes through all positional arguments to parrallel_backend context manager
        progbar: bool Display progress bar. Defaults to True
        **kwargs : passes through all keyword arguments to parrallel_backend context manager

    # Raises:
        TypeError : if iterable_ is anything other than list, tuple, or a generator
    # Example:
    ```python
    from memo import memlist, grid, mempar
    data = []
    @mempar(backend="threading", n_jobs=-1)
    @memlist(data=data)
    def birthday_experiment(class_size, n_sim):
        sims = np.random.randint(1, 365 + 1, (n_sim, class_size))
        sort_sims = np.sort(sims, axis=1)
        n_uniq = (sort_sims[:, 1:] != sort_sims[:, :-1]).sum(axis=1) + 1
        proba = np.mean(n_uniq != class_size)
        return {"est_proba": proba}

    g = grid(
        progbar=False, class_size=[5, 10, 20, 30, 40], n_sim=[1000, 1_000_000, 50, 200]
    )

    birthday_experiment(g)
    ```
    """

    def decorator(func):
        @wraps(func)
        def wrapper(
            iterable_,
        ):

            if not isinstance(iterable_, (list, tuple, set, GeneratorType)):
                raise TypeError(f"Type {type(iterable_)} not supported")
            elif progbar and not isinstance(iterable_, GeneratorType):
                total = len(iterable_)
                with Progress() as progress:
                    task = progress.add_task("[red]Mempar....", total=total)

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
                            progress.update(task, completed=self.parallel.n_completed_tasks, refresh=True)
                            with self.parallel._lock:
                                if self.parallel._original_iterator is not None:
                                    self.parallel.dispatch_next()

                    joblib.parallel.BatchCompletionCallBack = BatchCompletionCallBack
                    with parallel_backend(*args, **kwargs):
                        Parallel(require="sharedmem")(
                            delayed(func)(**settings) for settings in iterable_
                        )
            else:
                with parallel_backend(*args, **kwargs):
                    Parallel(require="sharedmem")(
                        delayed(func)(**settings) for settings in iterable_
                    )

        return wrapper

    return decorator


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
