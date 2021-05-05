import pytest
from memo import memlist, Runner, grid


@pytest.mark.parametrize(
    "kw",
    [{"backend": "loky"}, {"backend": "threading"}, {"backend": "multiprocessing"}],
)
def test_base_multiple_calls(kw):
    data = []
    g = [{"a": 1}] * 100

    @memlist(data=data)
    def count_values(n_jobs=-1, **kwargs):
        return {"sum": sum(kwargs.values())}

    runner = Runner(**kw)
    runner.run(func=count_values, settings=g, progbar=True)
    assert len(data) == len(g)


@pytest.mark.parametrize(
    "kw",
    [{"backend": "loky"}, {"backend": "threading"}, {"backend": "multiprocessing"}],
)
def test_keys_included(kw):
    data = []
    g = [{"a": 3, "b": 4, "c": 5}]

    @memlist(data=data)
    def count_values(**kwargs):
        return {"sum": sum(kwargs.values())}

    runner = Runner(n_jobs=-1, **kw)
    runner.run(func=count_values, settings=g, progbar=True)
    assert len(data) == 1
    assert all([k in data[0].keys() for k in g[0].keys()])


@pytest.mark.parametrize(
    "kw",
    [{"backend": "loky"}, {"backend": "threading"}, {"backend": "multiprocessing"}],
)
def test_base_args_included(kw):
    data = []

    @memlist(data=data)
    def count_values(a, b, **kwargs):
        return {"sum": sum(kwargs.values())}

    g = [{"a": 1, "b": 2, "c": 1}, {"a": 1, "b": 2, "c": 1}]
    runner = Runner(n_jobs=-1, **kw)
    runner.run(func=count_values, settings=g, progbar=True)
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

        @memlist(data=data)
        def count_values(**kwargs):
            return {"sum": sum(kwargs.values())}

        count_values(g)
        runner = Runner(backend="threading", workers=-1)
        runner.run(func=count_values, settings=g, progbar=True)


def test_generator_progbar_warning():
    data = []
    g = (s for s in grid(class_size=[5, 6], n_sim=[1000, 1_000_000]))

    with pytest.warns(
        UserWarning, match="Progress bar not supported for generator settings"
    ):

        @memlist(data=data)
        def count_values(**kwargs):
            return {"sum": sum(kwargs.values())}

        runner = Runner(backend="threading", n_jobs=-1)
        runner.run(func=count_values, settings=g, progbar=True)
