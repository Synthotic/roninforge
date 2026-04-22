# Tool base class / interface
import io
import contextlib
from abc import ABC, abstractmethod

# --- blueprint - every tool must implement run() ---

class Tool(ABC):
    name = ""               # tool name child will set
    description = ""       # tool description child will set
   
    @abstractmethod        # child must implement run()
    def run(self, args):
        pass                # child fills this in

# --- read file tool - specific tool implementation ---

class ReadFileTool(Tool):
    name = "read_file"
    description = "Read the file and return contents"

    def run(self, args):
        try:    
            with open(args["path"]) as f:   # opens file 
                return f.read()             # returns contents of file
        except FileNotFoundError:
            return f"File not found: {args['path']}"  # handle errors
        except Exception as e:
            return f"Error reading file: {e}"                        # catch crashes

# --- tool executes python code - specific tool implementation ---

class RunCodeTool(Tool):
    name = "run_code"
    description = "Execute the code and returns output"

    def run(self, args):
        buffer = io.StringIO()                          # fake file in memory
        try:
            with contextlib.redirect_stdout(buffer):    # send prints to buffer
                exec(args["code"])                      # run the code
            return buffer.getvalue()                    # return what was printed
        except Exception as e:
            return f"Error: {e}"                        # catch crashes


    
    
               

