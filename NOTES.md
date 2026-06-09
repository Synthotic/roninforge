# roninforge — Notes, Bugs & Changes

## Format

- `[BUG]` — identified issue
- `[FIX]` — applied fix
- `[CHANGE]` — intentional design or behavior change
- `[DECISION]` — architectural or product decision worth remembering

---

## Log

### 2026-04-01

- `[CHANGE]` Renamed `model.py` → `model_access.py`; introduced `ModelAccess` ABC and `OllamaAccess` provider
- `[DECISION]` `ModelProvider` abstraction is the freemium boundary — local Ollama (free), API-backed models (Pro)
- `[DECISION]` No LangChain — minimal deps, full code ownership

---

### 2026-04-06

- `[CHANGE]` Implemented `core/agent.py` — ReAct-style agent loop (`run()`)
- `[DECISION]` Tool calling uses structured JSON (`{"tool": ..., "args": ...}` / `{"response": ...}`) rather than Ollama's native tool-call API — keeps `ModelAccess.complete()` returning a plain string, provider-agnostic
- `[DECISION]` `provider` is injected as a parameter to `run()`, not instantiated inside the loop — clean separation between agent logic and model provider
- `[FIX]` Added `try/except json.JSONDecodeError` — agent exits gracefully if model returns malformed JSON (strict for now, may revisit once Qwen output shape is confirmed)
- `[BUG]` Known gap: if Qwen outputs preamble text before JSON, `json.loads` will fail — deferred until model is wired up

---

### 2026-04-10

- `[DECISION]` `Tool` owns its own name, description, and `run()` — self-contained, not defined per-pack
- `[DECISION]` Pack YAML lists which tools to load by name — the pack selects the toolset, each tool describes itself
- `[DECISION]` Tool descriptions live on the `Tool` class so the agent can build the system prompt dynamically from whatever tools are loaded — no duplication across packs
- Next: implement `tool.py` — `Tool` base class with `name`, `description`, and `run(args)`; then `registry.py` to load/look up tools by name

---

### 2026-04-12

- `[CHANGE]` Implemented `core/tool.py` — `Tool` ABC with `name`, `description`, and abstract `run(args)`
- `[CHANGE]` Added `ReadFileTool` and `RunCodeTool` as first concrete tools
- `[BUG]` `ReadFileTool` has no error handling — uncaught exception if path doesn't exist, deferred
- `[DECISION]` `exec()` in `RunCodeTool` is intentional — local-first tool, trusted input only
- `[FIX]` Fixed indentation error in `RunCodeTool.run()` — `buffer` had 9 spaces instead of 8
- Next: `registry.py` — load and look up tools by name
- Next: `Fix error handling for ReadFileTool

---

### 2026-04-22

- `[FIX]` `ReadFileTool` error handling implemented — catches `FileNotFoundError` and general `Exception` (deferred from 2026-04-12)
- `[BUG]` `registry.py` — bare `from tool import ...` will break depending on invocation context. Should be `from .tool import ...` (relative) or `from core.tool import ...` (absolute)
- `[BUG]` `registry.py` — silent skip when a pack lists an unknown tool name; agent may expect a tool that never loaded. Consider warning or raising on unknown names
- `[BUG]` `registry.py` — no error handling on `open(f"packs/{pack_name}.yaml")` — uncaught `FileNotFoundError` if pack doesn't exist
- Next: fix above three `registry.py` bugs

---

### 2026-05-02

- `[FIX]` Fixed indentation error in `agent.py` lines 17-19 — `clean`, `if clean is None`, and `return` were dedented out of the `try` block, causing `IndentationError`
- `[CHANGE]` Agent end-to-end run confirmed working — successfully scanned `main.py` and returned security issue analysis via Qwen2.5-Coder 7B Q4
- `[DECISION]` `agent.py` returns raw model reply if no JSON found (line 19) — intentional fallback for when Qwen doesn't follow the structured format
- `[FIX]` `extract_json()` in `agent.py` resolves the known gap (2026-04-06) — strips preamble text before JSON so `json.loads` no longer fails on model output with leading text
- Next: fix three `registry.py` bugs logged 2026-04-22

---

### 2026-05-06

- `[CHANGE]` Added `trim_messages()` to `agent.py` — trims message history to stay under `max_tokens=3000` (default), estimates token count at 4 chars/token, drops oldest messages first
- `[DECISION]` Dropping from the front is intentional for now — may lose original user instruction in long runs, acceptable at this stage

---

### 2026-05-13

- `[CHANGE]` Added `archive` global list — trimmed messages are saved here instead of discarded
- `[CHANGE]` Added `extract_tags()` — strips stopwords, extracts keywords from a message for later retrieval
- `[CHANGE]` Added `recall()` — searches archive for messages with overlapping tags, injects top 2 matches into conversation window each step
- `[FIX]` Fixed `imimport json` typo on line 1 — would have caused `SyntaxError`
- Next: interactive mode

---

### 2026-06-08

- `[CHANGE]` Added interactive mode to `main.py` — `while True` loop with `input()`, appends user messages to `messages`, prints agent reply each turn; `exit`/`quit` to stop
- `[BUG]` Response loop issue — deferred, will fix later

---
