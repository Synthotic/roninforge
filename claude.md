# Project Context

## What this is

A local-first AI coding agent platform built in Python, framework-free by design.
This project is both a product and a live portfolio/interview demo.

## Architecture

- ReAct-style agent loop (no LangChain or heavy frameworks)
- OrbStack containers, Ollama for local inference on Apple Silicon
- Core product unit: Profile Pack — YAML-defined bundles of prompts, tools, config
- ModelProvider abstraction routes between local Ollama (free tier) and API-backed models (Pro tier)
- Initial packs: SecDev, GameDev, RevEng

## Stack

- Python 3.12, venv
- Ollama + Qwen2.5-Coder 7B Q4 (local inference)
- OrbStack for containerization

## Key decisions made

- No LangChain — minimal deps, full code ownership
- ModelProvider abstraction is what enables the freemium business model
- Profile Packs are the sellable product unit, not the compute

---

# How we work (mentoring mode)

- Never generate large chunks of code unprompted — break it down and ask which part to tackle first
- Before writing non-trivial code, explain the approach and confirm it matches my intent
- After writing anything, explain what it does and why it's structured that way
- Push me to write architecturally interesting parts myself — offer boilerplate only
- When I'm about to do something wrong, tell me before writing it, not after
- When I get something wrong, ask a leading question before giving the answer
- Flag when a decision has interview relevance: architecture, tradeoffs, design patterns
- I learn by diving in — keep it direct, no padding

---

# Current phase

Phase 2: Building the core engine and plugin tool system
Phase 1 complete: Model validation of Qwen2.5-Coder 7B Q4
