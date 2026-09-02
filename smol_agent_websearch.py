"""
smolagents #2 - agent with a built-in tool: WebSearchTool.

Point of this one: watch the agent decide FOR ITSELF when it needs to
search the web vs. when it can just answer directly, then use the search
result to build its final answer. This is the "Tooling" spectrum point
from Course-1-GenAI-Testing-Notes.md Section 6.3 - giving an LLM access
to an outside resource, rather than only its own training knowledge.

Same local Ollama model as smol_agent_basic.py - fully offline/free.
Note: llama3.2:1b is a small model and can be shaky at agentic tool-use.
If results look confused, this is expected for a 1B model - see the
README note about trying a stronger model.

How to run:
    python smol_agent_websearch.py
"""

from smolagents import CodeAgent, LiteLLMModel, WebSearchTool

MODEL_ID = "ollama_chat/llama3.2:1b"
OLLAMA_API_BASE = "http://localhost:11434"


def get_model() -> LiteLLMModel:
    return LiteLLMModel(
        model_id=MODEL_ID,
        api_base=OLLAMA_API_BASE,
        api_key="ollama",
        num_ctx=8192,
    )


def main():
    model = get_model()
    agent = CodeAgent(tools=[WebSearchTool()], model=model)

    result = agent.run("What is the latest stable version of Playwright?")
    print(f"\nFINAL ANSWER: {result}")


if __name__ == "__main__":
    main()
