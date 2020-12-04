from memo import grid, random_grid


def test_grid():
    inputs = [i for i in grid(a="abc", b="abcd")]
    assert len(inputs) == 12
    assert all(["a" in i for i in inputs])
    assert all(["b" in i for i in inputs])


def test_random_grid():
    inputs = [i for i in random_grid(n=10, a="abc", b="abcd")]
    assert len(inputs) == 10
    assert all(["a" in i for i in inputs])
    assert all(["b" in i for i in inputs])
