# smolagents experiments

Three small, standalone scripts to get a rough, hands-on feel for
[smolagents](https://github.com/huggingface/smolagents) (Hugging Face's
"agents that think in Python code" library) — following on from
Course-1-GenAI-Testing-Notes.md Section 6.3 (the AI agents ethics/risk deep
dive) and the "LLM vs. agent" discussion in this same session.

## Setup already done

- Installed: `pip install 'smolagents[toolkit,litellm]'`
- Model backend: your existing local **Ollama** setup (`llama3.2:1b`), the
  same model already used by `shoe_store_agent.py` and `rag_app.py` — so
  these run fully offline, free, no API key needed.
- Note: pip flagged some version conflicts with `deepeval`/`instructor`
  (they pin an older `openai` package) after installing smolagents' deps.
  `import deepeval` and `import instructor` both still succeeded when
  tested, so nothing looked broken — but if a deepeval/instructor script
  misbehaves later, this install is the first place to check
  (`pip install "openai<2.0.0"` would roll that piece back).

## The 3 scripts

1. **`smol_agent_basic.py`** — no tools at all. Just watch a `CodeAgent`
   solve "sum 1 to 10" and print the actual Python code it writes and runs
   at each step, before giving a final answer.
2. **`smol_agent_websearch.py`** — adds the built-in `WebSearchTool()`.
   Watch the agent decide *for itself* whether it needs to search before
   answering.
3. **`smol_agent_custom_tool.py`** — a hand-written `@tool`
   (`check_url_status`) that lets the agent actually check a real URL's
   HTTP status. Points at `eaapp.somee.com`, the same practice site used
   throughout the course notes (Sections 2.2, 3.2, 4.2–4.6) — so this is
   the closest one to an actual "agentic QA" mini-tool.

Run any of them directly:
```
python smol_agent_basic.py
python smol_agent_websearch.py
python smol_agent_custom_tool.py
```

## What to notice while running these

- Every step, smolagents prints the **real Python code** the LLM decided
  to write and execute — this is the "CodeAgent" idea from Section 6.3's
  agentic-level table (the model writes code, rather than filling in a
  fixed JSON tool-call schema).
- `llama3.2:1b` is a *small* model — smolagents' own docs admit it's "a bit
  weak for agentic behaviours." If output looks confused or it takes a
  few retries, that's the model, not a setup problem. Since `.env` already
  has `ANTHROPIC_API_KEY` configured for other work in this repo, a much
  stronger option is one line away:
  ```python
  from smolagents import LiteLLMModel
  import os
  model = LiteLLMModel(model_id="anthropic/<model-id>", api_key=os.environ["ANTHROPIC_API_KEY"])
  ```
  Swap this in place of `get_model()`'s return value in any script to compare.
  Check LiteLLM's [supported Anthropic model IDs](https://docs.litellm.ai/docs/providers/anthropic)
  for the exact current `<model-id>` string to use — don't guess it.
- Compare `smol_agent_custom_tool.py` to `shoe_store_agent.py`: the second
  one hand-rolls the THINK → ACT → OBSERVE loop with a raw `ollama.chat`
  call and a manual dispatch table; smolagents gives you that same loop
  "for free," with the model writing real code for the ACT step instead of
  a fixed JSON tool call.

## Where this could go next

- Add 2–3 more small tools (e.g. read a local JSON test-data file, run a
  fake "execute test" function) and give one agent all of them — see how
  it decides which tool to use for which part of a task.
- Try the same task on the local `llama3.2:1b` model vs. a cloud model via
  `ANTHROPIC_API_KEY` and compare how reliably each one picks the right
  tool — a good hands-on illustration of Section 6.3's "Accuracy" and
  "Consistency" values.
