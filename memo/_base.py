import orjson
from typing import Callable, List
from functools import wraps


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
