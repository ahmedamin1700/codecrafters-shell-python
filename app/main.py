import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    while True:
        sys.stdout.write("$ ")
        command = input("")
        if command == "exit":
            break
        parts = command.split(" ")
        if parts[0] == "echo":
            print(f"{" ".join(parts[1:])}")
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
