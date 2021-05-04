from ._error import NotInstalled
from ._grid import grid, random_grid
from ._base import memlist, memfile, memfunc
from ._runner import Runner
from ._util import time_taken

try:
    from memo._http import memweb
except ModuleNotFoundError:
    memweb = NotInstalled("memweb", "web")


__all__ = [
    "grid",
    "random_grid",
    "memlist",
    "memfile",
    "memfunc",
    "memweb",
    "time_taken",
    "Runner",
]
