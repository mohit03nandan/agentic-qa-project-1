"""
smolagents #1 - the simplest possible agent: no tools at all.

Point of this one: see the CodeAgent loop with nothing else going on.
Watch the console output - smolagents prints the actual Python code the
LLM writes and runs at each step, before printing the final answer. That
"the agent writes and runs real code" behaviour is the "CodeAgent" idea
from Course-1-GenAI-Testing-Notes.md Section 6.3 (agentic level table).

Uses the same local Ollama model already set up for shoe_store_agent.py /
rag_app.py, so this runs fully offline, free, no API key needed.

How to run:
    python smol_agent_basic.py
"""

from smolagents import CodeAgent, LiteLLMModel

MODEL_ID = "ollama_chat/llama3.2:1b"
OLLAMA_API_BASE = "http://localhost:11434"


def get_model() -> LiteLLMModel:
    return LiteLLMModel(
        model_id=MODEL_ID,
        api_base=OLLAMA_API_BASE,
        api_key="ollama",  # LiteLLM wants something here even though Ollama ignores it
        num_ctx=8192,  # Ollama's default (2048) is too small for agentic tasks
    )


def main():
    model = get_model()
    agent = CodeAgent(tools=[], model=model)

    result = agent.run("Calculate the sum of numbers from 1 to 10")
    print(f"\nFINAL ANSWER: {result}")


if __name__ == "__main__":
    main()
