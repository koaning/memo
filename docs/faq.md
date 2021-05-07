## Do I really need to output a dictionary? 

It's an opinionated packages but we think it's neater that way. 
You'll usually want to have a name attached to column names in 
a dataframe and functions can have multiple outputs.  

## Can I add a progress bar? 

You get a progress bar if you're using a `Runner`

### Demo 

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
    n_uniq = (sort_sims[:, 1:] != sort_sims[:, :-1]).sum(axis = 1) + 1
    proba = np.mean(n_uniq != class_size)
    return {"est_proba": proba}


settings = grid(class_size=range(20, 30), n_sim=[100, 10_000, 1_000_000])

# This runner comes with a progress bar
runner = Runner(backend="threading", n_jobs=1)
runner.run(func=birthday_experiment, settings=settings)
```

## Can I get amazing visualisations? 

Sure, but they won't be supplied by this package. Instead we might
recommend checking out [hiplot](https://github.com/facebookresearch/hiplot).
It gives a pretty parallel coordinates from jupyter notebook.

If you've got a list with dictionaries you can run;

```
import hiplot as hip
data = [{'dropout':0.1, 'lr': 0.001, 'loss': 10.0, 'optimizer': 'SGD'},
        {'dropout':0.15, 'lr': 0.01, 'loss': 3.5, 'optimizer': 'Adam'},
        {'dropout':0.3, 'lr': 0.1, 'loss': 4.5, 'optimizer': 'Adam'}]
hip.Experiment.from_iterable(data).display()
```

You can read in a file locally as well. 

```
import pandas as pd
import hiplot as hip
df = pd.read_json("collected-data.jsonl", lines=True)
data = df.to_dict(orient='records')

hip.Experiment.from_iterable(data).display()
```
