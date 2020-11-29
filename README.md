> **IMPORTANT** This repository is a work-in-progress.

# memo

Decorators that help you remember.


## Installation 

```python
pip install memo
```

## Usage

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

# `data` is now a list of dictionaries 
# these have`n_sim`, `class_size` and `est_proba` as keys
# can easily be turned into a dataframe via `pd.DataFrame(data)`
```

The `memlist` decorate takes care of all data collection. It captures all keyword
arguments of the function as well as the dictionary output of the function. This 
then is appended this to a list `data`. Especially when experiments become larger 
this turned out to be a lovely pattern such that I didn't need to worry about logging 
stats anymore. For example, suppose we also want to log how long the simulation takes;

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

Note how little we need to change! 

## Utilities

We offer some utilities to make some of this easy though. In particular; 

- We supply a grid generation mechanism to prevent a lot of for-loops. 
- We supply a `@capture_time` so that you don't need to write that logic yourself.

```python
import numpy as np 
from memo import memlist, grid, capture_time

data = []

@memlist(data=data)
@capture_time(time_taken=True, time_start=True)
def birthday_experiment(class_size, n_sim):
    """Simulates the birthday paradox. Vectorized = Fast!"""
    sims = np.random.randint(1, 365 + 1, (n_sim, class_size))
    sort_sims = np.sort(sims, axis=1)
    n_uniq = (sort_sims[:, 1:] != sort_sims[:, :-1]).sum(axis = 1) + 1
    proba = np.mean(n_uniq != class_size)
    return {"est_proba": proba}

for settings in grid(size=range(2, 40), n_sim=[1000, 10000, 100000]):
    birthday_experiment(**settings)
```

## Alternatives 

This library also offers decorators to pipe to other sources. 

- `memfile` sends the json blobs to a file 
- `memweb` sends the json blobs to a server via http-post requests
- `memstdout` sends the data to stdout, or a callable that you define
- `memwand` sends the json blobs to a [weights and biases](https://wandb.ai/) endpoint

The nice thing about being able to log results to a file or to the web is that 
you can also more easily parallize your jobs. 

## Utilities 

This library also offers some extra utilities to make it easy to collect logs from these sorts
of grids. 

- `grid`: generates a grid on your behalf 
- `random_grid`: generates a random grid on your behalf 
- `ignore_error`: allows underlying function to ignore errors
- `timeit`: also captures the time taken
