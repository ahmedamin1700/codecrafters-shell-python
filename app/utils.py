import os


def find_executable(program: str) -> str | None:
    """
    Searches for an executable in user's PATH.

    Args:
        program (str): program to find in PATH.

    Returns:
        str|None: executable path for the mentioned program if found.
    """
    path_list = os.environ.get("PATH", "").split(os.pathsep)

    for directory in path_list:
        file_path = f"{directory}/{program}"

        if os.path.isfile(file_path):
            if os.access(file_path, os.X_OK):
                return file_path


def find_executables_in_path(prefix: str):
    executables = set()
    path_list = os.environ.get("PATH", "").split(os.pathsep)

    for directory in path_list:
        if os.path.isdir(directory):
            files = os.listdir(directory)
            for filename in files:
                if filename.startswith(prefix):
                    full_path = f"{directory}/{filename}"
                    if os.access(full_path, os.X_OK):
                        executables.add(filename)
    return executables


def parse_command_line(line: str) -> list[str]:
    """
    Parses a command line string, handling quotes and collapsing
    unquoted whitespace.
    """
    args = []
    current_arg = ""
    quote_state = None
    is_escaped = False

    for char in line:
        if is_escaped:
            if quote_state == "double" and char not in ('"', "\\", "$"):
                current_arg += f"\\{char}"
                is_escaped = False
                continue
            current_arg += char
            is_escaped = False
            continue
        elif char == "\\":
            if quote_state == "single":
                current_arg += char
            else:
                is_escaped = True
                continue
        elif char == "'":
            if quote_state == "double":
                current_arg += char
            elif quote_state == None:
                quote_state = "single"
            else:
                quote_state = None

        elif char == '"':
            if quote_state == "double":
                quote_state = None
            elif quote_state == "single":
                current_arg += char
            else:
                quote_state = "double"

        elif char == " ":
            if quote_state == None:
                if current_arg:
                    args.append(current_arg)
                    current_arg = ""
            else:
                current_arg += char

        else:
            current_arg += char

    if current_arg:
        args.append(current_arg)

    return args
