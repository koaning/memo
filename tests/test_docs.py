import pathlib

import exdown
import pytest
import textwrap

from memo import memlist, memfunc, memfile, memwandb, memweb

files = [str(p) for p in pathlib.Path("docs").glob("*.md")] + ["readme.md"]
functions = [memlist, memfunc, memfile]


@pytest.mark.parametrize("fpath", files)
def test_markdown_files(fpath):
    for string, lineno in exdown.extract(fpath, syntax_filter="python"):
        try:
            exec(string, {"__MODULE__": "__main__"})
        except Exception:
            print(f"{fpath} (line {lineno}):\n```\n{string}```")
            raise


@pytest.mark.parametrize("func", functions)
def test_docstrings(func, tmp_path):
    with open(f"{tmp_path}/supertmp.md", "w") as handle:
        handle.write(textwrap.dedent(func.__doc__))
    for string, lineno in exdown.extract(f"{tmp_path}/supertmp.md", syntax_filter="python"):
        try:
            exec(string, {"__MODULE__": "__main__"})
        except Exception:
            print(f"{func} (line {lineno}):\n```\n{string}```")
            raise
