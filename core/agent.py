import json        # parse JSON

def extract_json(text):
    start = text.find("{")  # find first {
    end = text.rfind("}") + 1 # find last }
    if start == -1 or end == 0: # if no JSON found
        return None # return None if no JSON found  
    return text[start:end] # return JSON


def trim_messages(messages, max_tokens=3000): # trim messages to max tokens
    def count_tokens(msgs): # count tokens in messages
        total = 0 # total tokens
        for msg in msgs: # iterate over messages
            total += len(msg["content"]) // 4 # 4 characters per token
        return total # return total tokens

    while count_tokens(messages) > max_tokens and len(messages) > 1: # while messages are too long
        messages.pop(0) # remove first message
    
    return messages # return trimmed messages


def run(provider,messages, tools, system_prompt, max_steps):
    for step in range(max_steps):   # iterate over max steps
        messages = trim_messages(messages) # trim messages to max tokens
        reply = provider.complete(messages, system_prompt)  # get reply from model
        print(f"Step {step}: {reply[:200]}") # print first 200 characters of reply

        try:
            clean = extract_json(reply) # extract JSON from reply
            if clean is None: # if no JSON found
                return reply # return reply if no JSON found
            parsed = json.loads(clean)  # parse JSON
        except json.JSONDecodeError:  # handle errors
            return "Invalid JSON: " + clean     # handle errors                


        if "tool" in parsed:  # if tool is in parsed
            tool_name = parsed["tool"]  # get tool name
            if tool_name in tools:  # if tool is in tools
                result = tools[tool_name].run(parsed["args"])  # run tool
                messages.append({"role": "assistant", "content": reply})  # add assistant message
                messages.append({"role": "user", "content": result})  # add user message
            else:
                return "Tool not found: " + tool_name  # handle errors

        elif "response" in parsed:  # if response is in parsed
            return parsed["response"]  # return response

    return "Max steps reached without a response"  # handle errors



