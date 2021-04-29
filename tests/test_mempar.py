import pytest
from memo import memlist, mempar


@pytest.mark.parametrize("kw", [{"backend": "loky", "n_jobs": -1}, {"backend": "threading", "n_jobs": -1}, {"backend": "multiprocessing", "n_jobs": -1}])
def test_base_multiple_calls(kw):
    data = []
    g = [{"a": 1}] * 100

    @mempar(**kw)
    @memlist(data=data)
    def count_values(**kwargs):
        return {"sum": sum(kwargs.values())}

    count_values(g)
    assert len(data) == len(g)


@pytest.mark.parametrize("kw", [{"backend": "loky", "n_jobs": -1}, {"backend": "threading", "n_jobs": -1}, {"backend": "multiprocessing", "n_jobs": -1}])
def test_keys_included(kw):
    data = []
    g = [{"a": 3, "b": 4, "c": 5}]

    @mempar(**kw)
    @memlist(data=data)
    def count_values(**kwargs):
        return {"sum": sum(kwargs.values())}

    count_values(g)

    assert len(data) == 1
    assert all([k in data[0].keys() for k in g[0].keys()])


@pytest.mark.parametrize("kw", [{"backend": "loky", "n_jobs": -1}, {"backend": "threading", "n_jobs": -1}, {"backend": "multiprocessing", "n_jobs": -1}])
def test_base_args_included(kw):
    data = []

    @mempar(**kw)
    @memlist(data=data)
    def count_values(a, b, **kwargs):
        return {"sum": sum(kwargs.values())}

    count_values([{"a": 1, "b": 2, "c": 1}, {"a": 1, "b": 2, "c": 1}])
    assert len(data) == 2
    assert data[0]["a"] == 1
    assert data[0]["b"] == 2
    assert data[0]["c"] == 1
    assert data[1]["a"] == 1
    assert data[1]["b"] == 2
    assert data[1]["c"] == 1


def test_raises_type_error():
    data = []
    g = {"a": 3, "b": 4, "c": 5}

    with pytest.raises(TypeError):
        @mempar(backend="threading", n_jobs=-1)
        @memlist(data=data)
        def count_values(**kwargs):
            return {"sum": sum(kwargs.values())}

        count_values(g)
