import json                        # lets us parse JSON strings into dictionaries

archive = []                       # empty list that stores old messages when they get trimmed
                                   # lives outside any function so all functions can access it

# --- TAGGER: pulls keywords from a message ---

def extract_tags(text):            # takes any string, returns a list of keywords
    stopwords = {"the", "a", "is", "it", "to", "and", "of", "in", "for", "on", "that", "this", "with"}
                                   # common words we don't care about
    words = text.lower().split()   # lowercase everything, split into a list of words
    tags = [w for w in words if w not in stopwords and len(w) > 3]
                                   # keep words that aren't stopwords and are longer than 3 characters
    return list(set(tags))         # set() removes duplicates, list() converts back to a list

# --- JSON EXTRACTOR: finds JSON inside messy model output ---

def extract_json(text):            # takes raw model reply, returns just the JSON part
    start = text.find("{")         # find position of first {
    end = text.rfind("}") + 1      # find position of last }, +1 to include it
    if start == -1 or end == 0:    # no { or } found at all
        return None                # give up, no JSON here
    return text[start:end]         # slice out just the JSON part

# --- TRIMMER: keeps conversation under the token limit ---

def trim_messages(messages, max_tokens=3000):  # takes message list and a size limit

    def count_tokens(msgs):        # helper function, only exists inside trim_messages
        total = 0                  # start counter at zero
        for msg in msgs:           # loop through each message
            total += len(msg["content"]) // 4  # characters divided by 4 = rough token count
        return total               # give back the total

    while count_tokens(messages) > max_tokens and len(messages) > 1:
                                   # keep looping while: over the limit AND more than 1 message left
        old = messages.pop(0)      # remove the oldest message from the list
        old["tags"] = extract_tags(old["content"])  # tag it with keywords before archiving
        archive.append(old)        # save it to the archive so we can recall it later

    return messages                # give back the trimmed list

# --- RETRIEVER: searches archive for relevant old messages ---

def recall(current_message, max_recalls=2):  # takes current message text, returns up to 2 old messages
    current_tags = extract_tags(current_message)  # get keywords from current message
    scored = []                    # empty list to hold matches with their scores
    for msg in archive:            # loop through every archived message
        overlap = len(set(current_tags) & set(msg["tags"]))
                                   # & finds tags that appear in BOTH lists
                                   # len counts how many matches
        if overlap > 0:            # at least one keyword matched
            scored.append((overlap, msg))  # save the score and the message as a pair
    scored.sort(reverse=True)      # sort by score, highest first
    return [msg for _, msg in scored[:max_recalls]]
                                   # return just the messages (not scores) for top 2 matches
                                   # _ means "I don't need this value" (the score)

# --- AGENT LOOP: the brain that ties everything together ---

def run(provider, messages, tools, system_prompt, max_steps):
                                   # provider = model connection
                                   # messages = conversation so far
                                   # tools = dictionary of available tools
                                   # system_prompt = personality/instructions
                                   # max_steps = safety limit on loops

    for step in range(max_steps):  # loop up to max_steps times

        recalled = recall(messages[-1]["content"])
                                   # search archive for anything related to the latest message
                                   # messages[-1] means "last item in the list"
        messages = trim_messages(messages)
                                   # put recalled messages at the front of the conversation
        contexts = recalled + messages
                                   # make sure total size is under the limit
        reply = provider.complete(contexts, system_prompt)
                                   # send to model, get response
        print(f"Step {step}: {reply[:200]}")
                                   # debug: show first 200 chars of what the model said

        try:                       # try this, if it crashes go to except
            clean = extract_json(reply)      # pull JSON out of the reply
            if clean is None:                # no JSON found at all
                return reply                 # model just talked, return it as the answer
            parsed = json.loads(clean)       # turn JSON string into a dictionary
        except json.JSONDecodeError:         # JSON was found but it's broken
            return "[AGENT ERROR] Could not parse JSON: " + clean  # return error with what we tried to parse

        if "tool" in parsed:                 # model wants to use a tool
            tool_name = parsed["tool"]       # which tool
            if tool_name in tools:           # does it exist?
                result = tools[tool_name].run(parsed["args"])  # run it
                messages.append({"role": "assistant", "content": reply})
                                             # add model's request to conversation
                messages.append({"role": "user", "content": result})
                                             # add tool result to conversation
                                             # loop continues — model sees the result next turn
            else:
                return "Tool not found: " + tool_name  # tool doesn't exist, bail out

        elif "response" in parsed:           # model has the final answer
            return parsed["response"]        # return it, loop stops

    return "Max steps reached without a response"  # used all steps, never got an answer



