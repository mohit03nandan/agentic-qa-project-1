"""
Phase 2, Week 7 - DeepEval hands-on: 5 golden test cases against a live local LLM.

How to run:
    deepeval test run test_llm_qa.py

What this does, in plain terms:
1. For each question below, we actually call the local model (via Ollama) to get
   a live answer - we are testing the real model, not a hardcoded string.
2. We compare that live answer against an "expected_output" (our golden answer key)
   using two metrics:
   - AnswerRelevancyMetric: does the answer actually address the question asked?
   - GEval (Correctness): does the answer match the expected answer in meaning?
"""

import ollama
import pytest
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric, GEval
from deepeval.models import OllamaModel
from deepeval.test_case import LLMTestCase, SingleTurnParams

MODEL = "llama3.2:1b"

# The same local model, used here as the "judge" for the LLM-as-a-judge metrics below.
judge_model = OllamaModel(model=MODEL, base_url="http://localhost:11434", temperature=0)

# Your golden dataset: 5 questions where you already know the correct answer.
GOLDENS = [
    {
        "input": "What is the capital of Japan?",
        "expected_output": "The capital of Japan is Tokyo.",
    },
    {
        "input": "What is 9 times 6?",
        "expected_output": "9 times 6 is 54.",
    },
    {
        "input": "Who wrote the play Romeo and Juliet?",
        "expected_output": "William Shakespeare wrote Romeo and Juliet.",
    },
    {
        "input": "What gas do humans breathe in to survive, mainly?",
        "expected_output": "Humans mainly breathe in oxygen to survive.",
    },
    {
        "input": "Is the Great Wall of China visible from the Moon with the naked eye?",
        "expected_output": "No, the Great Wall of China is not visible from the Moon with the naked eye - this is a common myth.",
    },
]


def ask_model(question: str) -> str:
    """Calls the local Ollama model and returns its live answer."""
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": question}],
    )
    return response["message"]["content"]


correctness_metric = GEval(
    name="Correctness",
    criteria="Correctness - determine if the actual output is factually correct and matches the meaning of the expected output.",
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
        SingleTurnParams.EXPECTED_OUTPUT,
    ],
    model=judge_model,
)

answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.5, model=judge_model)


@pytest.mark.parametrize("golden", GOLDENS)
def test_golden_qa(golden):
    live_answer = ask_model(golden["input"])
    test_case = LLMTestCase(
        input=golden["input"],
        actual_output=live_answer,
        expected_output=golden["expected_output"],
    )
    assert_test(test_case, [answer_relevancy_metric, correctness_metric])
