![](docs/header.png)

## Installation 

```
pip install memo
```

## Documentation

The documentation can be found [here]().

## Usage

Here's an example of utility functions provided by our library. 

```python
import numpy as np 
from memo import memlist, memfile, grid, time_taken

data = []

@memfile(filepath="results.jsonl")
@memlist(data=data)
@time_taken()
def birthday_experiment(class_size, n_sim):
    """Simulates the birthday paradox. Vectorized = Fast!"""
    sims = np.random.randint(1, 365 + 1, (n_sim, class_size))
    sort_sims = np.sort(sims, axis=1)
    n_uniq = (sort_sims[:, 1:] != sort_sims[:, :-1]).sum(axis = 1) + 1
    proba = np.mean(n_uniq != class_size)
    return {"est_proba": proba}

for settings in grid(class_size=[5, 10, 20, 30], n_sim=[1000, 1_000_000]):
    birthday_experiment(**settings)
```

The decorators `memlist` and `memfile` are making sure that the keyword arugments and 
dictionary output of the `birthday_experiment` are logged. The contents of the `results.jsonl`-file
and the `data` variable looks like this; 

```
{"class_size": 5, "n_sim": 1000, "est_proba": 0.024, "time_taken": 0.0004899501800537109}
{"class_size": 5, "n_sim": 1000000, "est_proba": 0.027178, "time_taken": 0.19407916069030762}
{"class_size": 10, "n_sim": 1000, "est_proba": 0.104, "time_taken": 0.000598907470703125}
{"class_size": 10, "n_sim": 1000000, "est_proba": 0.117062, "time_taken": 0.3751380443572998}
{"class_size": 20, "n_sim": 1000, "est_proba": 0.415, "time_taken": 0.0009679794311523438}
{"class_size": 20, "n_sim": 1000000, "est_proba": 0.411571, "time_taken": 0.7928380966186523}
{"class_size": 30, "n_sim": 1000, "est_proba": 0.703, "time_taken": 0.0018239021301269531}
{"class_size": 30, "n_sim": 1000000, "est_proba": 0.706033, "time_taken": 1.1375510692596436}
```

The nice thing about being able to log results to a file or to the web is that 
you can also more easily parallize your jobs!

## Features 

This library also offers decorators to pipe to other sources. 

- `memlists` sends the json blobs to a list
- `memfile` sends the json blobs to a file 
- `memweb` sends the json blobs to a server via http-post requests
- `memfunc` sends the data to a callable that you supply, like `print`
- `grid` generates a convenient grid for your experiments
- `random_grid` generates a randomized grid for your experiments
- `time_taken` also logs the time the function takes to run

Check the API docs [here](https://koaning.github.io/memo/util.html) for more information on 
how these work. 
