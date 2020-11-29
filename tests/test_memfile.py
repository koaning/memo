import json
import pytest

from memo import memfile


def confirm_file_contents(fpath, data):
    with open(fpath, "r") as f:
        data_read = [json.loads(j) for j in f.read().split("\n") if j != ""]
    print(data_read)
    for i, d in enumerate(data_read):
        assert data[i] == d


@pytest.mark.parametrize("kw", [{"a": 1, "b": 1}, {"a": 3, "b": 4}])
def test_base_values(kw, tmp_path):
    filepath = f"{tmp_path}/file.jsonl"

    @memfile(filepath=filepath)
    def count_values(**kwargs):
        return {"sum": sum(kwargs.values())}

    count_values(**kw)

    confirm_file_contents(filepath, [{**kw, "sum": kw["a"] + kw["b"]}])


def test_base_multiple_calls(tmp_path):
    filepath = f"{tmp_path}/file.jsonl"

    @memfile(filepath=filepath)
    def count_values(**kwargs):
        return {"sum": sum(kwargs.values())}

    for i in range(1, 5):
        count_values(a=1)
        confirm_file_contents(filepath, [{"a": 1, "sum": 1}] * i)
