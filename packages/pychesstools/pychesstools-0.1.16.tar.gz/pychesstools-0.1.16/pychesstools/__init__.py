"""A game of chess."""

from importlib.metadata import PackageNotFoundError, version
from importlib.util import find_spec
from pathlib import Path

__version__: str | None

try:
    __version__ = version("pychesstools")
except PackageNotFoundError:
    __version__ = None

__WORKING_DIRECTORY__ = Path(__file__).parent
__RICH_AVAILABLE__ = bool(find_spec("rich"))
