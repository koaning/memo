## Do I really need to output a dictionary? 

It's an opinionated packages but we thinkg it's neater that way. 
You'll usually want to have a name attached to column names in 
a dataframe and functions can have multiple outputs.  

## Can I add a progress bar? 

We don't offer a progress bar natively in this library, but nothing is stopping you
from using [rich](https://github.com/willmcgugan/rich) or 
[tqdm](https://github.com/tqdm/tqdm) for this. 

### Rich Demo 

```python
import numpy as np
from rich.progress import Progress

from memo import memlist, memfile, grid, capture_time

data = []


@memfile(filepath="results.jsonl")
@memlist(data=data)
@capture_time(time_taken=True)
def birthday_experiment(class_size, n_sim):
    """Simulates the birthday paradox. Vectorized = Fast!"""
    sims = np.random.randint(1, 365 + 1, (n_sim, class_size))
    sort_sims = np.sort(sims, axis=1)
    n_uniq = (sort_sims[:, 1:] != sort_sims[:, :-1]).sum(axis = 1) + 1
    proba = np.mean(n_uniq != class_size)
    return {"est_proba": proba}


settings = list(grid(class_size=range(5, 50), n_sim=[100, 10_000, 1_000_000]))


with Progress() as progress:
    task = progress.add_task("[green]Processing...", total=len(settings))

    for setting in settings:
        birthday_experiment(**setting)
        progress.update(task, advance=1)
```

### Tqdm Demo 

```python
import numpy as np
import tqdm

from memo import memlist, memfile, grid, capture_time

data = []


@memfile(filepath="results.jsonl")
@memlist(data=data)
@capture_time(time_taken=True)
def birthday_experiment(class_size, n_sim):
    """Simulates the birthday paradox. Vectorized = Fast!"""
    sims = np.random.randint(1, 365 + 1, (n_sim, class_size))
    sort_sims = np.sort(sims, axis=1)
    n_uniq = (sort_sims[:, 1:] != sort_sims[:, :-1]).sum(axis = 1) + 1
    proba = np.mean(n_uniq != class_size)
    return {"est_proba": proba}


settings = list(grid(class_size=range(5, 50), n_sim=[100, 10_000, 1_000_000]))

for setting in tqdm.tqdm(settings):
    birthday_experiment(**setting)
```