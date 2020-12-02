import random
import itertools as it


def grid(**kwargs):
    """
    Generates a grid of settings.

    Arguments:
        kwargs: the name of parameter is the key while the values represent items to iterate over

    Example

    ```python
    from memo import grid

    settings = list(grid(a=[1,2], b=[1, 2]))
    expected = [
         {'a': 1, 'b': 1},
         {'a': 1, 'b': 2},
         {'a': 2, 'b': 1},
         {'a': 2, 'b': 2}
    ]
    assert settings == expected

    def calc_sum(a, b):
        return {"c": a + b}

    for setting in settings:
        print(calc_sum(**setting))
    ```
    """
    for c in it.product(*[v for v in kwargs.values()]):
        yield {k: v for k, v in zip(kwargs.keys(), c)}


def random_grid(n=30, **kwargs):
    """
    Generates a random grid settings.

    Arguments:
        kwargs: the name of parameter is the key while the values represent items to iterate over

    Example

    ```python
    from memo import random_grid

    settings = list(random_grid(n=30, a=[1,2], b=[1, 2]))
    assert len(settings) == 30
    ```
    """
    for i in range(n):
        yield {k: random.choice(v) for k, v in kwargs.items()}
