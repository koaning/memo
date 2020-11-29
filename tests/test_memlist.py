import pytest
from memo import memlist


@pytest.mark.parametrize("kw", [{"a": 1, "b": 1}, {"a": 3, "b": 4}])
def test_base_values(kw):
    data = []

    @memlist(data=data)
    def count_values(**kwargs):
        return {"sum": sum(kwargs.values())}

    count_values(**kw)

    assert len(data) == 1
    assert data[0]["a"] == kw["a"]
    assert data[0]["b"] == kw["b"]
    assert data[0]["sum"] == kw["a"] + kw["b"]


@pytest.mark.parametrize("kw", [{"a": 1}, {"a": 3, "b": 4}, {"a": 3, "b": 4, "c": 5}])
def test_keys_included(kw):
    data = []

    @memlist(data=data)
    def count_values(**kwargs):
        return {"sum": sum(kwargs.values())}

    count_values(**kw)

    assert len(data) == 1
    assert all([k in data[0].keys() for k in kw.keys()])


def test_base_multiple_calls():
    data = []

    @memlist(data=data)
    def count_values(**kwargs):
        return {"sum": sum(kwargs.values())}

    for i in range(1, 5):
        count_values(a=1)
        assert len(data) == i


def test_base_args():
    data = []

    @memlist(data=data)
    def count_values(a, b, **kwargs):
        return {"sum": sum(kwargs.values())}

    count_values(1, b=2, c=1)
    assert len(data) == 1
    assert data[0]["b"] == 2
    assert data[0]["c"] == 1


def test_base_args_included():
    data = []

    @memlist(data=data)
    def count_values(a, b, **kwargs):
        return {"sum": sum(kwargs.values())}

    count_values(a=1, b=2, c=1)
    assert len(data) == 1
    assert data[0]["a"] == 1
    assert data[0]["b"] == 2
    assert data[0]["c"] == 1
