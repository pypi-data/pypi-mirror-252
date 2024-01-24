import sys
from magcopy import Actions, InvalidPathError, clipboard
from magcopy.path import paste

usage = """\
Usage: magcopy <action> <path/file>

Actions:
    copy   - Copy folder or file to clipboard
    move   - Add folder or file to clipboard to move
    paste  - Paste folder or file from clipboard to current folder or specified folder

Options:
    --help  - Display this usage message.

Note:
    This program does not alter the contents of the system's default clipboard. It maintains its own clipboard for managing copied and moved items.

Example:
    magcopy copy /path/to/source/folder
    magcopy paste /path/to/destination/folder

    magcopy move /path/to/source/file
    magcopy paste /path/to/destination/folder

    magcopy copy /path/to/source/file --clip
"""


def get_arg_path() -> str:
    if len(sys.argv) == 0:
        print("Error: Please provide the path for the file or folder.")
        sys.exit(1)

    return sys.argv.pop(0)


def execute_path_action(action: str) -> None:
    path = get_arg_path()

    try:
        clipboard.add_to_clipboard(action, path)
    except InvalidPathError as error:
        print(error)
        sys.exit(1)


sys.argv = sys.argv[1:]

clip_flag = "--clip" in sys.argv
if clip_flag:
    sys.argv.pop(sys.argv.index("--clip"))

if "--help" in sys.argv or len(sys.argv) == 0:
    print(usage)
    sys.exit(0)

command = sys.argv.pop(0)
if command == "copy":
    execute_path_action(Actions.COPY)

elif command == "move":
    execute_path_action(Actions.MOVE)

elif command == "paste":
    path = get_arg_path()

    paste(path)

else:
    print(
        f"Error: Unknown or invalid command '{command}'. Use 'magcopy --help' to view the usage guide."
    )
    sys.exit(1)
