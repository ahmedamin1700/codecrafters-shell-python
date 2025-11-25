import sys


def main():
    while True:
        recognized = ("echo", "exit")
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
                print(f"{parts[1]} not found")
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
