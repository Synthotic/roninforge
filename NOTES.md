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
