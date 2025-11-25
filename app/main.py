import sys
import os
import subprocess

def find_executable(program: str) -> str|None:
    """
    Searches for an executable in user's PATH.

    Args:
        program (str): program to find in PATH.

    Returns:
        str|None: executable path for the mentioned program if found.
    """
    path_list = os.environ.get('PATH', '').split(os.pathsep)

    for directory in path_list:
        file_path = f"{directory}/{program}"
        
        if os.path.isfile(file_path):
            if os.access(file_path, os.X_OK):
                return file_path

def parse_command_line(line: str) -> list[str]:
    """
    Parses a command line string, handling single quotes and collapsing
    unquoted whitespace.
    """
    args = []
    current_arg = ""
    is_in_quotes = False

    for char in line:
        if char == "'":
            # Toggle the quoting state. Don't add the quote to the argument.
            is_in_quotes = not is_in_quotes
        
        elif char == ' ' and not is_in_quotes:
            # This is a separator for arguments.
            # If we have a current argument built up, finish it.
            if current_arg:
                args.append(current_arg)
                current_arg = ""
            # If current_arg is already empty (e.g., multiple spaces),
            # this does nothing, effectively collapsing the spaces.
            
        else:
            # This is a normal character, either because it's not a space
            # or because it's a space inside quotes.
            current_arg += char
            
    # After the loop, there might be a final argument left over.
    if current_arg:
        args.append(current_arg)
        
    return args

class Shell:
    def __init__(self):
        self._builtins = {
            "exit": self._handle_exit,
            "echo": self._handle_echo,
            "type": self._handle_type,
            "pwd": self._handle_pwd,
            "cd": self._handle_cd,
        }

    def _handle_exit(self, args: list[str]) -> None:
        """Handler for the 'exit' command."""
        if args and args[0] == 0:
            sys.exit(0)
        else:
            sys.exit(0)
    
    def _handle_echo(self, args):
        """Handler for the 'echo' command."""
        print(" ".join(args))

    def _handle_type(self, args):
        """Handler for the 'type' command."""
        if not args:
            return # 'type' with no argument does nothing

        cmd_to_check = args[0]
        if cmd_to_check in self._builtins:
            print(f"{cmd_to_check} is a shell builtin")
        else:
            executable = find_executable(cmd_to_check)
            if executable:
                print(f"{cmd_to_check} is {executable}")
            else:
                print(f"{cmd_to_check}: not found")

    def _handle_pwd(self, args):
        print(os.getcwd())

    def _handle_cd(self, args):
        path = args[0]
        try:
            if path == "~":
                home = os.getenv("HOME")
                os.chdir(home)
            else:
                os.chdir(path)
        except FileNotFoundError:
            print(f"cd: {path}: No such file or directory")

    def _execute_external(self, parts):
        """Handler for executing external commands."""
        command = parts[0]
        executable = find_executable(command)
        
        if executable:
            # The shell's only job is to run the command.
            # The external program will handle printing its own output.
            subprocess.run(parts)
        else:
            print(f"{command}: command not found")
    
    def run(self):
        """The main loop of the shell."""
        while True:
            sys.stdout.write("$ ")
            sys.stdout.flush() # Ensure the prompt appears before input
            
            command_line = input()
            if not command_line:
                continue

            parts = parse_command_line(command_line)
            command = parts[0]
            args = parts[1:]

            # The dispatcher logic starts here
            if command in self._builtins:
                # If it's a built-in, call its handler method.
                self._builtins[command](args)
            else:
                # Otherwise, treat it as an external command.
                self._execute_external(parts)

if __name__ == "__main__":
    # To run the shell, create an instance and call its run method.
    shell = Shell()
    shell.run()
