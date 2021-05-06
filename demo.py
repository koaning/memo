from memo import Runner
import numpy as np
import ray
from memo import memlist, memfile, grid, time_taken

data = []


@memfile(filepath="results.jsonl")
@memlist(data=data)
@time_taken()
def birthday_experiment(class_size, n_sim):
    """Simulates the birthday paradox. Vectorized = Fast!"""
    sims = np.random.randint(1, 365 + 1, (n_sim, class_size))
    sort_sims = np.sort(sims, axis=1)
    n_uniq = (sort_sims[:, 1:] != sort_sims[:, :-1]).sum(axis=1) + 1
    proba = np.mean(n_uniq != class_size)
    return {"est_proba": proba}


for setting in grid(class_size=range(20, 30), n_sim=[100, 10_000, 1_000_000]):
    birthday_experiment(**setting)


# To Run in parallel

data = []
ray.init(address='auto', _redis_password='5241590000000000')

settings = list(grid(class_size=range(20, 30), n_sim=[100, 10_000, 1_000_000], progbar=False))
runner = Runner(backend="ray", n_jobs=-1)
runner.run(func=birthday_experiment, settings=settings)
