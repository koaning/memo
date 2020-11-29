import json
from functools import wraps

from .error import NotInstalled

try:
    from memo.http import memweb
except ModuleNotFoundError:
    memweb = NotInstalled("memweb", "httpx")

try:
    from memo.wandb import memwandb
except ModuleNotFoundError:
    memwandb = NotInstalled("memwandb", "wandb")


def memlist(data):
    """
    Remembers input/output of a function in python list.

    Arguments:
        data: a list to push received data into
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            data.append({**kwargs, **result})
            return result

        return wrapper

    return decorator


def memfile(filepath):
    """
    Remembers input/output of a function in a jsonl file on disk.

    Arguments:
        filepath: path to write data to
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filepath, "a") as f:
                f.write(json.dumps({**kwargs, **result}) + "\n")
            return result

        return wrapper

    return decorator


def memstdout(print_fn=print):
    """
    Remembers input/output of a function by printing.

    Arguments:
        print_fn: option to overwrite the print_fn that is used, this allows you to attach a logger instead
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print_fn({**kwargs, **result})
            return result

        return wrapper

    return decorator
