import sys

commands = []

def main():
    # TODO: Uncomment the code below to pass the first stage
    command = input("$ ")
    if command not in commands:
        print(f"{command}: command not found")


if __name__ == "__main__":
    main()
