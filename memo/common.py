import time
import datetime as dt
from functools import wraps


def capture_time(time_taken=True, start_time=True, end_time=True):
    """
    Adds additional time-based information to output.

    Arguments:
        time_taken: add how long it took to calculate
        start_time: add datetime-string of when the function got called
        end_time: add datetime-string of when the function got called
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tic = time.time()
            start = str(dt.datetime.now())
            result = func(*args, **kwargs)
            toc = time.time()
            end = str(dt.datetime.now())
            if time_taken:
                result = {**result, "time_taken": toc - tic}
            if start_time:
                result = {**result, "start_time": start}
            if end_time:
                result = {**result, "end_time": end}
            return result

        return wrapper

    return decorator
