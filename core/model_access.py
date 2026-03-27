import requests                                    # makes HTTP calls
from abc import ABC, abstractmethod                # abstract base class tools

# --- blueprint - every provider must implement complete() ---

class ModelAccess(ABC):
    @abstractmethod
    def complete(self, messages, system_prompt):    # chat history + instructions
        pass                                       # children fill this in

# --- ollama provider - talks to local model ---

class OllamaAccess(ModelAccess):
    def __init__(self, model, url):                # setup - runs on creation
        self.model = model                         # which model to hit
        self.url = url                             # where ollama lives

    def complete(self, messages, system_prompt):   # the actual API call
        full_messages = [{"role": "system", "content": system_prompt}] + messages  # inject system prompt first
        payload = {
            "model": self.model,                   # stored from __init__
            "messages": full_messages              # system + conversation
        }
        response = requests.post(self.url + "/api/chat", json=payload)  # send to ollama
        result = response.json()                   # parse what comes back
        return result["message"]["content"]        # grab just the text

# --- test it locally - won't run on import ---

if __name__ == "__main__":
    model = "qwen2.5-coder:7b-instruct-q4_K_M"
    url = "http://localhost:11434"
    provider = OllamaAccess(model, url)

    messages = [{"role": "user", "content": "Hello"}]
    reply = provider.complete(messages, "You are a helpful assistant")
    print(reply)