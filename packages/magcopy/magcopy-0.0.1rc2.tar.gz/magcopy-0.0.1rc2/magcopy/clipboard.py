from pathlib import Path
from magcopy import (
    InvalidPathError,
    PathLike,
    MAX_ITEMS_IN_CLIPBOARD,
    ACTION_FILE,
    CLIPBOARD_FILE,
)


def __create_files_if_not_exists() -> None:
    for file in [CLIPBOARD_FILE, ACTION_FILE]:
        if not file.is_file():
            file.touch()


def get_action() -> str:
    __create_files_if_not_exists()

    return ACTION_FILE.read_text(encoding="utf-8").strip().lower()


def add_to_clipboard(action: str, path: PathLike) -> None:
    __create_files_if_not_exists()

    path_obj = Path(path) if isinstance(path, str) else path
    if not path_obj.is_file() and not path_obj.is_dir():
        raise InvalidPathError("Error: Please provide a valid path.")

    clipboard_items: list[str] = [
        item.strip()
        for item in CLIPBOARD_FILE.read_text(encoding="utf-8").split("\n")
        if item != ""
    ]
    clipboard_items.insert(0, path_obj.as_posix())
    if len(clipboard_items) > MAX_ITEMS_IN_CLIPBOARD:
        clipboard_items.pop()

    CLIPBOARD_FILE.write_text("\n".join(clipboard_items), encoding="utf-8")
    ACTION_FILE.write_text(action.lower(), encoding="utf-8")


def read_from_clipboard() -> Path:
    __create_files_if_not_exists()

    clipboard_items: list[str] = [
        item.strip()
        for item in CLIPBOARD_FILE.read_text().split("\n")
        if item != ""
    ]

    return Path(clipboard_items[0])


def read_all_from_clipboard() -> list[Path]:
    __create_files_if_not_exists()

    clipboard_items: list[str] = [
        item.strip()
        for item in CLIPBOARD_FILE.read_text().split("\n")
        if item != ""
    ]

    return [Path(item) for item in clipboard_items]


def clear_clipboard():
    ACTION_FILE.write_text("")
    CLIPBOARD_FILE.write_text("")
