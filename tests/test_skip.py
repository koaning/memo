import pytest
from memo._base import _contains

true_pairs = [
    ([{"a": 1}], {"a": 1}),
    ([{"a": 1}, {"a": 2}], {"a": 1}),
    ([{"a": 1, "b": 2}], {"a": 1, "b": 2}),
]


@pytest.mark.parametrize("pairs", true_pairs)
def test_contains_true(pairs):
    datalist, kwargs = pairs
    assert _contains(kwargs=kwargs, datalist=datalist)


false_pairs = [
    ([{"a": 1}], {"a": 2}),
    ([{"a": 1}], {"a": 1, "b": 1}),
    ([{"a": 1}, {"b": 1}], {"a": 1, "b": 1}),
]


@pytest.mark.parametrize("pairs", false_pairs)
def test_contains_false(pairs):
    datalist, kwargs = pairs
    assert not _contains(kwargs=kwargs, datalist=datalist)
