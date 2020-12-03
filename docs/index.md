<h1 style="color: black; font-size: 2em; font-weight: 800;">"a whole log simpler" ... literally!</h1>

## Installation 

You can install this package via pip;

```
pip install memo
```

You might want to install extra dependencies depending on your use-case. 

```
pip install "memo[web]"
```

## What does this package do? 

This packages contains decorators that can help you route the input/output
of functions to files/dataframes and other sources. It's useful in logging
results from simulations or machine learning experiments.

```python
import numpy as np 
from memo import memfile

@memfile(filepath="results.jsonl")
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

The decorator ensures that all the keyword arguments and dictionary 
outputs of a function are logged. To see how it works in more detail, 
check the [quickstart](/getting-started.html)

## Features 

This library also offers decorators to pipe to other sources. 

- `memlists` sends the json blobs to a list
- `memfile` sends the json blobs to a file 
- `memweb` sends the json blobs to a server via http-post requests
- `memfunc` sends the data to a callable that you supply, like `print`
- `grid` generates a convenient grid for your experiments
- `random_grid` generates a randomized grid for your experiments
- `time_taken` also logs the time the function takes to run
