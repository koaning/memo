from functools import wraps

import wandb


def memwandb(project, **config):
    """
    Remembers input/output of a function by sending it to wandb.

    Warning:
        To use this tool, you may need to install extra dependencies.

        ```
        pip install memo[wandb]
        ```

    Arguments:
        project: name of the wandb project you want to send to
        config: optional extra keyword arguments to send along

    Usage:

    ```python
    import os
    from memo import wemwandb, time_taken

    # You probably want to run with this setting to prevent a
    # whole lot of output suddenly appearing.
    os.environ["WANDB_SILENT"] = "true"

    data = []


    @memwandb(project="birthday")
    @time_taken()
    def birthday_experiment(class_size, n_sim):
        sims = np.random.randint(1, 365 + 1, (n_sim, class_size))
        sort_sims = np.sort(sims, axis=1)
        n_uniq = (sort_sims[:, 1:] != sort_sims[:, :-1]).sum(axis = 1) + 1
        proba = np.mean(n_uniq != class_size)
        return {"est_proba": proba}

    settings = grid(class_size=range(2, 40), n_sim=[1_000, 10_000, 100_000, 1_000_000])
    for setting in settings:
        birthday_experiment(**setting)
    ```
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import logging

            logger = logging.getLogger("wandb")
            logger.setLevel(logging.ERROR)
            wandb.init(project=project)
            wandb.config = config
            result = func(*args, **kwargs)
            wandb.log({**kwargs, **result})
            return result

        return wrapper

    return decorator
