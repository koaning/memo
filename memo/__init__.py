import json
from functools import wraps


def memlist(data):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            data.append({**kwargs, **result})
            return result
        return wrapper
    return decorator


def memfile(filepath):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filepath, 'a') as f:
                f.writeline(json.dumps({**kwargs, **result}))
            return result
        return wrapper
    return decorator


def memstdout(print_fn=print):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print_fn({**kwargs, **result})
            return result
        return wrapper
    return decorator
