"""A game of chess."""

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

__version__: str | None

try:
    __version__ = version("pychesstools")
except PackageNotFoundError:
    __version__ = None

__WORKING_DIRECTORY__ = (
    Path(__file__).parent if "__file__" in globals() else Path("pychesstools")
)
