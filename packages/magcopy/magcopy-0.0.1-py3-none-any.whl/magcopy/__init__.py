from pathlib import Path
from typing import Union

PathLike = Union[str, Path]

MAX_ITEMS_IN_CLIPBOARD = 10
CLIPBOARD_FILE = Path(__file__).parent.parent.joinpath(".clipboard").resolve()
ACTION_FILE = Path(__file__).parent.parent.joinpath(".action").resolve()

__version__ = "0.0.1"


class Actions:
    COPY = "copy"
    MOVE = "move"
    PASTE = "paste"


class InvalidPathError(Exception):
    pass


class InvalidActionError(Exception):
    pass


class OutputIsNonDirectoryError(Exception):
    pass
