import sys
import subprocess
import os
import re
from pathlib import Path


commands = {"exit":"Exit the shell","echo":"Echo the args","type":"Distinguishes type of command"}

def getFullPath(fileName:str):
    path_dirs = os.environ.get("PATH", "").split(os.pathsep)
    matches = []
    for directory in path_dirs:
        file_path = Path(directory) / param
        if file_path.is_file() and  os.access(file_path,os.X_OK):
            matches.append(str(file_path))
    return matches       

def type(param: str):
    
    if param in commands:
        print(f"{param} is a shell builtin")
    if param not in commands:
        path_dirs = os.environ.get("PATH", "").split(os.pathsep)
        matches = []
        for directory in path_dirs:
            file_path = Path(directory) / param
            if file_path.is_file() and  os.access(file_path,os.X_OK):
                matches.append(str(file_path))
                print(f"{param} is {file_path}")
        if len(matches) == 0:
            print(f"{param}: not found")


def runExecutable(path :Path, args:list):
    
    process = subprocess.Popen([f"{path}",[ "{args}"]])

    
def exit():
    sys.exit()

def echo(params : str):
    print(f"{params}")

def CommandParse(commandString: str):
    args = []
    try:
        
        command = commandString[0]
        args = commandString[1:].split(" ")

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
                        
            case cmd in cmd not in commands.keys():     
                if len(args) > 1:

                    process = subprocess.Popen({getFull},[{args[0:]}])
                else:
                    print(f"{command}: command not found")

            case cmd  if cmd in commands.keys() and len(args) >= 1:
                args = "".join(args)
                eval(f"{command}(\"{args}\") ")
        
            case cmd if cmd in commands.keys() and len(args) == 0:
                eval(f"{command}()")


if __name__ == "__main__":
    main()
