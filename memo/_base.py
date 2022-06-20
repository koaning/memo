import orjson
import pathlib
from typing import Callable, List
from functools import wraps


def _contains(kwargs, datalist):
    """Checks if certain keyword arguments appear in the datalist."""
    for item in datalist:
        try:
            match = all([kwargs[k] == item[k] for k in kwargs.keys()])
        except KeyError:
            # If there is a key-error then we have a keyword argument
            # that we did not search over earlier. So we must run!
            return False
        if match:
            return True
    return False


def memlist(data: List, skip: bool = False):
    """
    Remembers input/output of a function in python list.

    Arguments:
        data: a list to push received data into
        skip: skips the calculation if kwargs appear in data already

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
            # We might be able to skip if the parameters
            # already appear in the dataset.
            if skip and _contains(kwargs, data):
                return None
            data.append({**kwargs, **result})
            return result

        return wrapper

    return decorator


def memfile(filepath: str, skip: bool = False):
    """
    Remembers input/output of a function in a jsonl file on disk.

    Arguments:
        filepath: path to write data to
        skip: skips the calculation if kwargs appear in data already

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
            if skip:
                if pathlib.Path(filepath).exists():
                    with open(filepath, "r") as f:
                        datalist = [orjson.loads(line) for line in list(f)]
                else:
                    datalist = []
            with open(filepath, "a") as f:
                if skip and _contains(kwargs, datalist):
                    return None
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
