import sys
import subprocess
import os
import re
from pathlib import Path
import socket
import getpass

commands = {"cd":"Changes current directory","exit":"Exit the shell","echo":"Echo the args","type":"Distinguishes type of command","pwd":"Prints current working directory"}

def cd(path = "~"):
    if os.path.isdir(os.path.expanduser(path)):
        os.chdir(os.path.expanduser(path)) 
    else:
        print(f"cd: {path}: No such file or directory")
def pwd():
    print(os.getcwd())

def getFullPath(fileName:str):
    try:
        
        path_dirs = os.environ.get("PATH", "").split(os.pathsep)
        matches = []
        for directory in path_dirs:
            file_path = Path(directory) / fileName
            if file_path.is_file() and  os.access(file_path,os.X_OK):
                matches.append(str(file_path))
        return matches[0]       
    except:
        return []

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
    if os.access(file_path, os.X_OK):    
        process = subprocess.Popen([f"{path}",[ "{args}"]])
    
def exit():
    sys.exit()

def echo(params : list):
    params="".join(params)
    print(f"{params}")

def CommandParse(commandString: str):
    args = []
    try:
        
        command = commandString[0]
        args = commandString[1:]
   
    except:
        command = commandString[0]
    return command,args

def main():
    user = getpass.getuser()
    hostname = socket.gethostname()
    while True:    
        #command_input = input(f"{user}@{hostname}:{os.getcwd()}$ ")
        command_input = input(f"$ ")
        command_input = command_input.split(" ")
        command,args = CommandParse(command_input)
        
        match command:

            case cmd if cmd  not in commands.keys():     
                if len(args) == 0:
                    try: 
                        process = subprocess.Popen(cmd)
                        process.wait()
                    except:
                        try:
                            process = subprocess.Popen(getFullPath(cmd))
                            process.wait()
                        except:
                            print(f"{cmd}: command not found")
                            main()
                            
                if len(args) >= 1:
                    try:
                        if os.access(cmd, os.X_OK):
                            process = subprocess.Popen([cmd]+args)
                            process.wait()
                        else:
                            process = subprocess.Popen([cmd]+args)
                            process.wait()
                    except:
                        print(f"{cmd}: command not found")
                else:
                    print(f"{command}: command not found")

            case cmd  if cmd in commands.keys(): 
                if len(args) >= 1:
                    args = " ".join(args)
                    eval(f"{cmd}(\"{args}\") ")
            
                if len(args) == 0:
                    eval(f"{command}()")


if __name__ == "__main__":
    main()
