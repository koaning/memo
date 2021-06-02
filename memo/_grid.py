import random
import itertools as it


def grid(shuffle=True, progbar=None, **kwargs):
    """
    Generates a grid of settings.

    Arguments:
        kwargs: the name of parameter is the key while the values represent items to iterate over

    Example

    ```python
    from memo import grid

    settings = grid(a=[1,2], b=[1, 2], shuffle=False)
    expected = [
        {'a': 1, 'b': 1},
        {'a': 1, 'b': 2},
        {'a': 2, 'b': 1},
        {'a': 2, 'b': 2}
    ]
    assert settings == expected
    ```
    """
    settings = [
        dict(zip(kwargs.keys(), d)) for d in it.product(*[v for v in kwargs.values()])
    ]
    if progbar:
        raise DeprecationWarning(
            "`progbar` is deprecated, use a `from memo import Runner` to get a progbar."
        )
    if shuffle:
        random.shuffle(settings)
    return settings


def random_grid(n=30, **kwargs):
    """
    Generates a random grid settings.

    Arguments:
        kwargs: the name of parameter is the key while the values represent items to iterate over

    Example

    ```python
    from memo import random_grid

    settings = random_grid(n=30, a=[1,2], b=[1, 2])
    assert len(settings) == 30
    ```
    """
    return [{k: random.choice(v) for k, v in kwargs.items()} for _ in range(n)]
