import random
import itertools as it


def grid(**kwargs):
    for c in it.product(*[v for v in kwargs.values()]):
        yield {k: v for k, v in zip(kwargs.keys(), c)}


def random_grid(n=30, **kwargs):
    for i in range(n):
        yield {k: random.choice(v) for k, v in kwargs.items()}
