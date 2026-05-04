# Tool registry — loads and registers tools for the agent
import yaml   # load YAML files
from core.tool import ReadFileTool, RunCodeTool # import tools

TOOL_MAP = {
    "read_file": ReadFileTool,  
    "run_code": RunCodeTool # more tools can be added here
}

#---  load tools from pack.yaml file ---
def load_tools(pack_name):
    with open(f"packs/{pack_name}/pack.yaml") as f: # load pack
        pack = yaml.safe_load(f) # load pack

    tools = {} # empty dictionary to store tools
    for name in pack["tools"]: # iterate over tools in pack
            if name in TOOL_MAP: # if tool is in TOOL_MAP
                tools[name] = TOOL_MAP[name]() # add tool to list
    return tools # return dictionary of tools
       