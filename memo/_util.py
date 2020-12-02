import time
from functools import wraps


def time_taken(minutes=False, rounding=2):
    """
    Adds additional time-based information to output.

    Arguments:
        minutes: log minutes instead of seconds
        rounding: number of decimals to round the timing to

    Example:

    ```python
    import numpy as np

    from memo import memlist, grid, time_taken

    data = []


    @memlist(data=data)
    @time_taken()
    def birthday_experiment(class_size, n_sim):
        sims = np.random.randint(1, 365 + 1, (n_sim, class_size))
        sort_sims = np.sort(sims, axis=1)
        n_uniq = (sort_sims[:, 1:] != sort_sims[:, :-1]).sum(axis = 1) + 1
        proba = np.mean(n_uniq != class_size)
        return {"est_proba": proba}


    settings = grid(class_size=range(5, 50), n_sim=[100, 10_000, 1_000_000])

    for setting in settings:
        birthday_experiment(**setting)
    ```
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tic = time.time()
            result = func(*args, **kwargs)
            toc = time.time()
            time_total = toc - tic
            if minutes:
                time_total = time_total / 60
            result = {**result, "time_taken": round(time_total, rounding)}
            return result

        return wrapper

    return decorator
