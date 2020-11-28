from functools import wraps

import httpx


def memweb(url):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            _ = httpx.post(url, data={**kwargs, **result})
            return result
        return wrapper
    return decorator
