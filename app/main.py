import sys

commands = []

def CommandParse(commandString: str):
    
    try:
        
        command = commandString[0]
        args = commandString[1:]

        if len(args) > 1:
            args = " " +  " ".join(args)
    
    except:
        command = commandString[0]
    return command,args



def main():
    # TODO: Uncomment the code below to pass the first stage
    
    command_input = input("$ ")
    command_input = command_input.split(" ")
    command,args = CommandParse(command_input)
    if command_input in commands and args:
        eval(f"{command} {args}")

    else:
        print(f"{command}: command not found")


if __name__ == "__main__":
    main()
