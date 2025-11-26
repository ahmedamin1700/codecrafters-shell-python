import sys
import os
import subprocess
import readline

from app.completer import Completer
from app.utils import find_executable, parse_command_line


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
            return  # 'type' with no argument does nothing

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

        completer = Completer(self._builtins.keys())
        readline.set_completer(completer.completer)
        readline.set_completer_delims("\t \n;")

        if "libedit" in readline.__doc__:
            # Use 'bind ^I rl_complete' for libedit
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            # Use 'tab: complete' for GNU readline
            readline.parse_and_bind("tab: complete")

        while True:
            sys.stdout.write("$ ")
            sys.stdout.flush()  # Ensure the prompt appears before input

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
