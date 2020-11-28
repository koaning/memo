from functools import wraps

import wandb


def memwandb(project, **config):
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
