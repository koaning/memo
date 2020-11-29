# memo

Decorators that help you remember.

## Installation 

```python
pip install memo
```

## Usage

Let's say you're running a simulation, or maybe a machine learning experiment. Then you've
probably gotten a function that handles all the logic and a list comprehension like below; 

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

This sort of works, but only because the example is simple. If you'd be interested in also 
seeing the effect of `n_sim` then you'd need to write a lot of logic to capture the data
in the right way.

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

The idea is that `memlist` captures all keyword arguments of the function as well as 
the dictionary output of the function and then appends this to a list. Especially 
when experiments become larger this turned out to be a lovely pattern such that I didn't
need to worry about logging stats anymore. 

## Alternatives 

This library also offers decorators to pipe to other sources. 

- `memfile` sends the json blobs to a file 
- `memweb` sends the json blobs to a server via http-post requests
- `memstdout` sends the data to stdout, or a callable that you define
- `memwand` sends the json blobs to a [weights and biases](https://wandb.ai/) endpoint

## Utilities 

This library also offers some extra utilities to make it easy to collect logs from these sorts
of grids. 

- ``