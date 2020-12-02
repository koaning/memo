from ._error import NotInstalled
from ._grid import grid, random_grid
from ._base import memlist, memfile, memfunc
from ._util import time_taken

try:
    from memo._http import memweb
except ModuleNotFoundError:
    memweb = NotInstalled("memweb", "web")

try:
    from memo._wandb import memwandb
except ModuleNotFoundError:
    memwandb = NotInstalled("memwandb", "wandb")


__version__ = "0.1.1"
__all__ = [
    "grid",
    "random_grid",
    "memlist",
    "memfile",
    "memfunc",
    "memweb",
    "memwandb",
    "time_taken",
]
