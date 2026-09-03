"""
browser-use #1 - the simplest possible browser agent.

Point of this one: unlike smol_agent_*.py (which only ever "thought" in
text or called a tiny hand-written tool), this agent actually controls a
real Chrome browser - navigating, reading the page, clicking, typing -
driven entirely by an LLM interpreting the plain-English `task` below.

Uses the existing ANTHROPIC_API_KEY already set up in .env for this repo
(the local llama3.2:1b model that struggled with the smolagents custom-tool
run is expected to struggle even more here - this agent has to reason over
full page content/screenshots, a much harder job than one tool call).

How to run:
    python browser_use_basic.py
"""

import asyncio

from browser_use import Agent, ChatAnthropic
from dotenv import load_dotenv

load_dotenv()


async def main():
    llm = ChatAnthropic(model="claude-sonnet-5", temperature=0.0)
    task = "Go to http://eaapp.somee.com and tell me the page title and the text on the main login/visit button."
    agent = Agent(task=task, llm=llm)
    history = await agent.run(max_steps=15)
    print(f"\nFINAL RESULT: {history.final_result()}")


if __name__ == "__main__":
    asyncio.run(main())
