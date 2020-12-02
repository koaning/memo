import time
from functools import wraps


def time_taken(minutes=False, rounding=2):
    """
    Adds additional time-based information to output.

    Arguments:
        minutes: log minutes instead of seconds
        rounding: number of decimals to round the timing to
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tic = time.time()
            result = func(*args, **kwargs)
            toc = time.time()
            time_total = toc - tic
            if minutes:
                time_total = time_total/60
            result = {**result, "time_taken": round(time_total, rounding)}
            return result

        return wrapper

    return decorator
