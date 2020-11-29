from functools import wraps

import httpx


def memweb(url):
    """
    Remembers input/output of a function by sending it over http to an endpoint.

    Arguments:
        filepath: path to write data to
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with httpx.Client() as client:
                _ = client.post(url, data={**kwargs, **result})
            return result

        return wrapper

    return decorator
