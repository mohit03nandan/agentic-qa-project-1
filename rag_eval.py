"""
Phase 3, Week 10 - scoring the RAG app from rag_app.py, RAGAS-style.

Note: the `ragas` pip package hit a real dependency conflict on this machine
(it needs an older langchain-core than another already-installed package
needs - a very common problem in the LangChain ecosystem). Rather than fight
version pinning further, this script implements the same three ideas
directly as plain judge prompts to our local model. This is actually a good
thing to see: RAGAS's metrics ARE just structured LLM-judge prompts under
the hood - there's no magic inside the library.

How to run:
    python rag_eval.py
"""

import ollama

JUDGE_MODEL = "llama3.2:1b"

USER_INPUT = "What's your refund policy for shoes that don't fit?"
RESPONSE = "The policy text does not cover refunds for shoes that don't fit."
RETRIEVED_CONTEXTS = [
    "Refunds are accepted within 30 days of purchase. The item must be unworn and in its original box.",
]

# The reference answer, broken into its individual factual claims by hand -
# this is what RAGAS's context recall does automatically under the hood.
REFERENCE_CLAIMS = [
    "Shoes can be returned within 30 days if they are unworn.",
    "Items marked 'Final Sale' cannot be returned or exchanged.",
]


def ask_judge(question: str) -> str:
    result = ollama.chat(model=JUDGE_MODEL, messages=[{"role": "user", "content": question}])
    return result["message"]["content"].strip()


def check_faithfulness() -> str:
    prompt = (
        f"Context:\n{RETRIEVED_CONTEXTS[0]}\n\n"
        f"Claim: \"{RESPONSE}\"\n\n"
        "Does the claim ONLY state things that are directly supported by the context, "
        "with nothing made up or added? Answer with just YES or NO, then a one-sentence reason."
    )
    return ask_judge(prompt)


def check_context_precision() -> str:
    prompt = (
        f"Question: {USER_INPUT}\n"
        f"Retrieved passage: \"{RETRIEVED_CONTEXTS[0]}\"\n\n"
        "Is this passage relevant and useful for answering the question? "
        "Answer with just YES or NO, then a one-sentence reason."
    )
    return ask_judge(prompt)


def check_context_recall() -> list[tuple[str, str]]:
    results = []
    for claim in REFERENCE_CLAIMS:
        prompt = (
            f"Retrieved context:\n{RETRIEVED_CONTEXTS[0]}\n\n"
            f"Fact that a full answer should include: \"{claim}\"\n\n"
            "Is this fact present in the retrieved context above? "
            "Answer with just YES or NO, then a one-sentence reason."
        )
        results.append((claim, ask_judge(prompt)))
    return results


def main():
    print("FAITHFULNESS - did the answer stick to the retrieved text?")
    print(f"  {check_faithfulness()}\n")

    print("CONTEXT PRECISION - was what got retrieved actually relevant?")
    print(f"  {check_context_precision()}\n")

    print("CONTEXT RECALL - did retrieval capture every fact a full answer needed?")
    recall_results = check_context_recall()
    covered = 0
    for claim, verdict in recall_results:
        print(f"  Fact: {claim}\n    -> {verdict}")
        if verdict.strip().upper().startswith("YES"):
            covered += 1
    print(f"\n  Recall score: {covered}/{len(REFERENCE_CLAIMS)} required facts were actually retrieved")


if __name__ == "__main__":
    main()
