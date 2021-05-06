## Base Scenario

Let's say you're running a simulation, or maybe a machine learning experiment. Then you
might have code that looks like this;

```python
import numpy as np

def birthday_experiment(class_size, n_sim=10_000):
    """Simulates the birthday paradox. Vectorized = Fast!"""
    sims = np.random.randint(1, 365 + 1, (n_sim, class_size))
    sort_sims = np.sort(sims, axis=1)
    n_uniq = (sort_sims[:, 1:] != sort_sims[:, :-1]).sum(axis = 1) + 1
    return np.mean(n_uniq != class_size)

results = [birthday_experiment(s) for s in range(2, 40)]
```

This example sort of works, but how would we now go about plotting our results? If you want
to plot the effect of `class_size` and the simulated probability then it'd be do-able. But things
get tricky if you're also interested in seeing the effect of `n_sim` as well. The input of the
simulation isn't nicely captured together with the output of the simulation.

## Decorators

The idea behind this library is that you can rewrite this function, only slightly, to make
all of this data collection a whole log simpler.

```python
import numpy as np
from memo import memlist

data = []

@memlist(data=data)
def birthday_experiment(class_size, n_sim):
    """Simulates the birthday paradox. Vectorized = Fast!"""
    sims = np.random.randint(1, 365 + 1, (n_sim, class_size))
    sort_sims = np.sort(sims, axis=1)
    n_uniq = (sort_sims[:, 1:] != sort_sims[:, :-1]).sum(axis = 1) + 1
    return {"est_proba": np.mean(n_uniq != class_size)}

for size in range(2, 40):
    for n_sim in [1000, 10000, 100000]:
        birthday_experiment(class_size=size, n_sim=n_sim)
```

The `data` object now represents a list of dictionaries that have `"n_sim"`, `"class_size"`
and `"est_proba"` as keys. You can easily turn these into a pandas DataFrame if you'd like
via `pd.DataFrame(data)`.

## Logging More

The `memlist` decorate takes care of all data collection. It captures all keyword
arguments of the function as well as the dictionary output of the function. This
then is appended this to a list `data`. Especially when you're iteration on your
experiments this might turn out to be a lovely pattern.

For example, suppose we also want to log how long the simulation takes;

```python
import time
import numpy as np
from memo import memlist

data = []

@memlist(data=data)
def birthday_experiment(class_size, n_sim):
    """Simulates the birthday paradox. Vectorized = Fast!"""
    t1 = time.time()
    sims = np.random.randint(1, 365 + 1, (n_sim, class_size))
    sort_sims = np.sort(sims, axis=1)
    n_uniq = (sort_sims[:, 1:] != sort_sims[:, :-1]).sum(axis = 1) + 1
    proba = np.mean(n_uniq != class_size)
    t2 = time.time()
    return {"est_proba": proba, "time": t2 - t1}

for size in range(2, 40):
    for n_sim in [1000, 10000, 100000]:
        birthday_experiment(class_size=size, n_sim=n_sim)
```

## Power

The real power of the library is that you can choose not only to log to
a list. You can just as easily write to a file too!

```python
import time
import numpy as np
from memo import memlist, memfile

data = []

@memfile(filepath="results.json")
@memlist(data=data)
def birthday_experiment(class_size, n_sim):
    """Simulates the birthday paradox. Vectorized = Fast!"""
    t1 = time.time()
    sims = np.random.randint(1, 365 + 1, (n_sim, class_size))
    sort_sims = np.sort(sims, axis=1)
    n_uniq = (sort_sims[:, 1:] != sort_sims[:, :-1]).sum(axis = 1) + 1
    proba = np.mean(n_uniq != class_size)
    t2 = time.time()
    return {"est_proba": proba, "time": t2 - t1}

for size in range(2, 40):
    for n_sim in [1000, 10000, 100000]:
        birthday_experiment(class_size=size, n_sim=n_sim)
```

## Utilities

The library also offers utilities to make the creation of these grids even easier. In particular;

- We supply a grid generation mechanism to prevent a lot of for-loops.
- We supply a `@capture_time` so that you don't need to write that logic yourself.

```python
import numpy as np
from memo import memlist, memfile, grid, time_taken

data = []

@memfile(filepath="results.json")
@memlist(data=data)
@time_taken()
def birthday_experiment(class_size, n_sim):
    """Simulates the birthday paradox. Vectorized = Fast!"""
    sims = np.random.randint(1, 365 + 1, (n_sim, class_size))
    sort_sims = np.sort(sims, axis=1)
    n_uniq = (sort_sims[:, 1:] != sort_sims[:, :-1]).sum(axis = 1) + 1
    proba = np.mean(n_uniq != class_size)
    return {"est_proba": proba}

for settings in grid(class_size=range(2, 40), n_sim=[1000, 10000, 100000]):
    birthday_experiment(**settings)
```

## Parallel

If you have a lot of simulations you'd like to run, it might be helpful to
run them in parallel. That's why this library also hosts a `Runner` class
that can run your functions on multiple CPU cores.

```python
import numpy as np

from memo import memlist, memfile, grid, time_taken, Runner

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

settings = list(grid(class_size=range(20, 30), n_sim=[100, 10_000, 1_000_000], progbar=False))

# To Run in parallel
runner = Runner(backend="threading", n_jobs=-1)
runner.run(func=birthday_experiment, settings=settings)
```

## More features

These decorators aren't performing magic, but my experience has been
that these decorators make it more fun to actually log the results of experiments.
It's nice to be able to just add a decorator to a function and not have to
worry about logging the statistics.

The library also offers extra features to make things a whole _log_ simpler.

- `memweb` sends the json blobs to a server via http-post requests
- `memfunc` sends the data to a callable that you supply, like `print`
- `random_grid` generates a randomized grid for your experiments
