# Entry point — loads a pack and runs the agent
import yaml
from core.model_access import OllamaAccess
from core.registry import load_tools
from core.agent import run

# 1. Load the pack
with open("packs/secdev/pack.yaml") as f:
    pack = yaml.safe_load(f)    # load pack

# 2. create the provider
provider = OllamaAccess("qwen2.5-coder:7b-instruct-q4_K_M", "http://localhost:11434")

# 3. load the tools
tools = load_tools("secdev")    

# 4. conversation history
messages = []

# 5. interactive loop
while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Shutting down...")
        break
    messages.append({"role": "user", "content": user_input})
    reply = run(provider, messages, tools, pack["system_prompt"], 10)
    print(f"\nAgent: {reply}")