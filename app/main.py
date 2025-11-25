import sys
import os
import subprocess

def find_executable(file: str) -> str|None:
    path_list = os.environ.get('PATH', '').split(os.pathsep)

    for directory in path_list:
        file_path = f"{directory}/{file}"
        
        if os.path.isfile(file_path):
            if os.access(file_path, os.X_OK):
                return file_path


def main():
    while True:
        recognized = ("echo", "exit", "type")
        sys.stdout.write("$ ")
        command = input("")
        if command == "exit":
            break
        parts = command.split(" ")
        if parts[0] == "echo":
            print(f"{" ".join(parts[1:])}")
        elif parts[0] == "type":
            if parts[1] in recognized:
                print(f"{parts[1]} is a shell builtin")
            else:
                executable = find_executable(parts[1])
                if executable:
                    print(f"{parts[1]} is {executable}")
                else:
                    print(f"{parts[1]} not found")
        else:
            executable = find_executable(parts[0])
            if executable:
                result = subprocess.run(parts, capture_output=True, text=True, check=True)
                print(f"Program was passed {len(parts)} args (including program name).")
                for i, arg in enumerate(parts):
                    print(f"Arg #{i}{":" if i != 0 else ""}{" (program name):" if i == 0 else ""} {arg}")
                print(result.stdout, end="")
            else:
                print(f"{command}: command not found")

if __name__ == "__main__":
    main()
