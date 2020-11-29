from ._error import NotInstalled
from ._grid import grid, random_grid
from ._base import memlist, memfile, memstdout

try:
    from memo._http import memweb
except ModuleNotFoundError:
    memweb = NotInstalled("memweb", "httpx")

try:
    from memo._wandb import memwandb
except ModuleNotFoundError:
    memwandb = NotInstalled("memwandb", "wandb")


__version__ = "0.1.0"
__all__ = [
    "grid",
    "random_grid",
    "memlist",
    "memfile",
    "memstdout",
    "memweb",
    "memwandb",
]
