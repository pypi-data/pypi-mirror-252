import shutil
from pathlib import Path
from magcopy import (
    Actions,
    InvalidActionError,
    InvalidPathError,
    OutputIsNonDirectoryError,
    PathLike,
)
from magcopy.clipboard import clear_clipboard, get_action, read_from_clipboard


def __copy(input_path: Path, output_path: Path) -> None:
    if output_path.is_file():
        raise OutputIsNonDirectoryError(
            f"Destination '{output_path}' is a file, not a directory."
        )

    if input_path.is_file():
        shutil.copy(input_path, output_path)
        print(f'File successfully copied to "{output_path}".')

    elif input_path.is_dir():
        shutil.copytree(input_path, output_path.joinpath(input_path.name))
        print(f'Folder successfully copied to "{output_path}".')


def __move(input_path: Path, output_path: Path):
    if output_path.is_file():
        raise OutputIsNonDirectoryError(
            f"Destination '{output_path}' is a file, not a directory."
        )

    if input_path.is_file():
        shutil.move(input_path, output_path)
        print(f'File successfully moved to "{output_path}".')

    elif input_path.is_dir():
        shutil.move(input_path, output_path.joinpath(input_path.name))
        print(f'Folder successfully moved to "{output_path}".')


def paste(path: PathLike):
    input_path = read_from_clipboard()
    output_path = Path(path) if isinstance(path, str) else path
    action = get_action()

    if not output_path.is_file() and not output_path.is_dir():
        raise InvalidPathError("Error: Please provide a valid path.")

    if action == Actions.COPY:
        __copy(input_path, output_path)
    elif action == Actions.MOVE:
        __move(input_path, output_path)
    else:
        raise InvalidActionError(f"Error: Unknown or invalid action '{action}'")

    clear_clipboard()
