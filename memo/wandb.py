from functools import wraps

import wandb


def memwandb(project, **config):
    """
    Remembers input/output of a function by sending it to wandb.

    Arguments:
        project: name of the wandb project you want to send to
        config: optional extra keyword arguments to send along
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            wandb.init(project=project)
            wandb.config = config
            result = func(*args, **kwargs)
            wandb.log({**kwargs, **result})
            return result

        return wrapper

    return decorator
