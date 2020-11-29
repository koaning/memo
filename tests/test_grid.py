from memo import grid


def test_grid():
    inputs = [i for i in grid(a="abc", b="abcd")]
    assert len(inputs) == 12
    assert all(["a" in i for i in inputs])
    assert all(["b" in i for i in inputs])
