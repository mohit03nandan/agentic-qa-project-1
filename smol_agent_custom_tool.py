"""
smolagents #3 - a custom tool built with @tool, aimed at a QA-flavoured task.

Point of this one: this is the interesting one for the agentic-QA roadmap -
a hand-written tool (check_url_status) that gives the agent a "hand" to
actually check something in the real world, instead of only generating
text. eaapp.somee.com is the same practice site used throughout
Course-1-GenAI-Testing-Notes.md (Sections 2.2, 3.2, 4.2-4.6).

Compare this to shoe_store_agent.py's hand-rolled ReAct loop (THINK ->
ACT -> OBSERVE) - smolagents gives you that same loop for free, and the
"ACT" step is real Python code the model writes, not a fixed JSON schema.

Same local Ollama model as the other smol_agent_*.py scripts.

How to run:
    python smol_agent_custom_tool.py
"""

import requests
from smolagents import CodeAgent, LiteLLMModel, tool

MODEL_ID = "ollama_chat/llama3.2:1b"
OLLAMA_API_BASE = "http://localhost:11434"


def get_model() -> LiteLLMModel:
    return LiteLLMModel(
        model_id=MODEL_ID,
        api_base=OLLAMA_API_BASE,
        api_key="ollama",
        num_ctx=8192,
    )


@tool
def check_url_status(url: str) -> str:
    """
    Checks if a URL is reachable and returns its HTTP status code.

    Args:
        url: the full URL to check, including http:// or https://
    """
    try:
        response = requests.get(url, timeout=10)
        return f"{url} responded with HTTP status {response.status_code}"
    except requests.RequestException as exc:
        return f"{url} could not be reached: {exc}"


def main():
    model = get_model()
    agent = CodeAgent(tools=[check_url_status], model=model)

    result = agent.run("Check if http://eaapp.somee.com is up, and tell me the status code.")
    print(f"\nFINAL ANSWER: {result}")


if __name__ == "__main__":
    main()
