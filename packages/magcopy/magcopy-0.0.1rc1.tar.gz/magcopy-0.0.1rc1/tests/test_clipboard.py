import pytest
from pathlib import Path
from magcopy import InvalidPathError, ACTION_FILE, CLIPBOARD_FILE
from magcopy.clipboard import (
    add_to_clipboard,
    get_action,
    read_from_clipboard,
    read_all_from_clipboard,
)


@pytest.fixture
def cleanup_clipboard_files():
    # Clean up clipboard files after each test
    yield
    ACTION_FILE.unlink(missing_ok=True)
    CLIPBOARD_FILE.unlink(missing_ok=True)


def test_add_to_clipboard(cleanup_clipboard_files):
    path1 = Path(__file__).parent.joinpath("__init__.py").resolve()
    path2 = Path(__file__).parent.joinpath("test_clipboard.py").resolve()

    print(path2.is_file())

    add_to_clipboard("copy", path1)
    assert get_action() == "copy"
    assert read_from_clipboard() == Path(path1)
    assert read_all_from_clipboard() == [Path(path1)]

    add_to_clipboard("move", path2)
    assert get_action() == "move"
    assert read_from_clipboard() == Path(path2)
    assert read_all_from_clipboard() == [Path(path2), Path(path1)]


def test_add_to_clipboard_invalid_path(cleanup_clipboard_files):
    with pytest.raises(InvalidPathError):
        add_to_clipboard("copy", "nonexistent_file.txt")


def test_read_from_clipboard(cleanup_clipboard_files):
    path = Path(__file__).parent.joinpath("__init__.py").resolve()
    add_to_clipboard("copy", path)

    assert read_from_clipboard() == Path(path)


def test_read_all_from_clipboard(cleanup_clipboard_files):
    path1 = Path(__file__).parent.joinpath("__init__.py").resolve()
    path2 = Path(__file__).parent.joinpath("test_clipboard.py").resolve()
    add_to_clipboard("copy", path1)
    add_to_clipboard("move", path2)

    assert read_all_from_clipboard() == [Path(path2), Path(path1)]


def test_get_action(cleanup_clipboard_files):
    assert get_action() == ""  # No action initially

    add_to_clipboard("copy", Path(__file__).resolve())
    assert get_action() == "copy"

    add_to_clipboard("move", Path(__file__).parent.resolve())
    assert get_action() == "move"
