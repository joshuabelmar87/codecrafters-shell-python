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
def parse_command(input_line: str) -> list[str]:
    """
    Parse a shell command line using regex, handling single quotes correctly.

    Rules:
    - Characters inside single quotes (') are treated literally.
    - Spaces inside quotes are preserved.
    - Adjacent quoted/unquoted strings are concatenated.
    - Quotes themselves are removed.
    - Outside quotes, whitespace separates arguments.
    """
    # Match either:
    #   1. A single-quoted string (content only, quotes discarded)
    #   2. A sequence of non-whitespace, non-quote characters
    token_re = re.compile(r"'([^']*)'|([^\s']+)")

    matches = token_re.findall(input_line)

    # findall returns tuples: (quoted_content, unquoted_content)
    # One of them is always empty
    tokens = [q if q else u for q, u in matches]

    # Concatenate adjacent tokens that had no whitespace between them
    # (the regex already splits on whitespace, so we just need to join
    # consecutive matches that were next to each other without space)
    # Because the regex consumes the input sequentially and whitespace
    # is the only separator, the list already has correct argument boundaries.
    # Adjacent quoted/unquoted pieces that touch (e.g. 'hello''world')
    # appear as consecutive tokens with no space between them in the original,
    # but findall still produces separate matches. We therefore merge them.

    if not tokens:
        return []

    # Re-scan to merge adjacent tokens that were not separated by whitespace
    result = []
    last_end = 0
    pos = 0

    for match in token_re.finditer(input_line):
        start, end = match.span()
        content = match.group(1) if match.group(1) is not None else match.group(2)

        # If there was only whitespace (or nothing) between previous token and this one,
        # and the previous result exists, we may need to concatenate
        if result and start == last_end:
            result[-1] += content
        else:
            result.append(content)

        last_end = end

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
    result = parse_command(commandString) 
    try:
        
        command = result[0]
        args = result[1:]
   
    except:
        command = result[0]
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
