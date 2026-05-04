import json        # parse JSON

def extract_json(text):
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == 0:
        return None
    return text[start:end]


def run(provider,messages, tools, system_prompt, max_steps):
    for step in range(max_steps):
        reply = provider.complete(messages, system_prompt)  # get reply from model
        print(f"Step {step}: {reply[:200]}")

        try:
            clean = extract_json(reply)
            if clean is None:
                return "No JSON found in reply: " + reply
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



