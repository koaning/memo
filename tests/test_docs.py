import pathlib

import pytest

from mktestdocs import check_md_file, check_docstring
from memo import memlist, memfunc, memfile, time_taken, grid, random_grid

files = [str(p) for p in pathlib.Path("docs").glob("*.md")] + ["README.md"]
functions = [memlist, memfunc, memfile, time_taken, grid, random_grid]


@pytest.mark.parametrize("fpath", files)
def test_files_good(fpath):
    check_md_file(fpath=fpath)


@pytest.mark.parametrize("func", functions, ids=lambda d: d.__name__)
def test_docstrings(func):
    check_docstring(func)
