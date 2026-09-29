import sys
import subprocess
import os
import re

commands = {"exit":"Exit the shell","echo":"Echo the args","type":"Distinguishes type of command"}


def type(param: str):
    
    if param in commands:
        print(f"{param} is a shell builtin")
    if param not in commands:
        print(f"{param} not found")
    
        path = os.environ.get("PATH")
        dirs = path.split(os.pathsep)

        for d in path:
            if re.search(r"{param}", d):
                print(f"{param} is {d}")


            

def exit():
    sys.exit()

def echo(params : str):
    print(f"{params}")

def CommandParse(commandString: str):
    
    try:
        
        command = commandString[0]
        args = commandString[1:]

        if len(args) > 1:
            args = " ".join(args)
    
    except:
        command = commandString[0]
    return command,args



def main():
    while True:    
        command_input = input("$ ")
        command_input = command_input.split(" ")
        command,args = CommandParse(command_input)
        match command.lower():
            
            case cmd  if cmd in commands.keys() and len(args) >= 1:
                args = "".join(args)
                eval(f"{command}(\"{args}\") ")

            case cmd if cmd not in commands.keys():
                print(f"{command}: command not found")
        
            case cmd if cmd in commands.keys() and len(args) == 0:
                eval(f"{command}()")


if __name__ == "__main__":
    main()
