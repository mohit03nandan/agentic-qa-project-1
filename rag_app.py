"""
Phase 3, Week 10 - a small real RAG app, tested stage by stage.

Scenario: a support bot for an online shoe store, backed by a tiny
document library. We trace every stage by hand (query -> embed ->
retrieve -> inject context -> generate) so each one is visible and
testable on its own - this is what "tracing" means in practice, even
without a dedicated tracing dashboard like LangSmith/TruLens.

How to run:
    python rag_app.py
"""

import numpy as np
import ollama

EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "llama3.2:1b"

# The document library. Note doc 4 is a real exception to the refund policy -
# deliberately worded differently from the question, to see if retrieval finds it.
DOCS = [
    "Shipping takes 3 to 5 business days for standard delivery.",
    "Refunds are accepted within 30 days of purchase. The item must be unworn and in its original box.",
    "Members of our loyalty program earn 1 point for every dollar spent.",
    "Items marked as 'Final Sale' cannot be returned or exchanged, no exceptions.",
]

QUESTION = "What's your refund policy for shoes that don't fit?"

# What a fully correct answer would need to cover, for scoring purposes.
REFERENCE_ANSWER = (
    "You can return shoes within 30 days if they are unworn, but items marked "
    "'Final Sale' cannot be returned or exchanged under any circumstances."
)

TOP_K = 1  # deliberately narrow, to see if this misses the Final Sale exception


def embed(text: str) -> np.ndarray:
    response = ollama.embed(model=EMBED_MODEL, input=text)
    return np.array(response["embeddings"][0])


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def main():
    print(f"STAGE 1 - QUERY:\n  {QUESTION}\n")

    query_vec = embed(QUESTION)
    print(f"STAGE 2 - EMBED:\n  query turned into a {len(query_vec)}-number vector\n")

    doc_vecs = [embed(doc) for doc in DOCS]
    scored = sorted(
        zip(DOCS, doc_vecs),
        key=lambda pair: cosine_similarity(query_vec, pair[1]),
        reverse=True,
    )
    print("STAGE 3 - RETRIEVE (all docs, ranked by similarity):")
    for doc, vec in scored:
        print(f"  {cosine_similarity(query_vec, vec):.3f}  {doc}")
    retrieved = [doc for doc, _ in scored[:TOP_K]]
    print(f"\n  -> Top {TOP_K} retrieved and passed to the model:")
    for doc in retrieved:
        print(f"     - {doc}")
    print()

    context_block = "\n".join(retrieved)
    prompt = (
        f"Using ONLY the following store policy text, answer the customer's question. "
        f"If the policy text does not fully answer it, say what it does cover.\n\n"
        f"Policy text:\n{context_block}\n\n"
        f"Customer question: {QUESTION}"
    )
    print(f"STAGE 4 - INJECT CONTEXT:\n  (prompt built with the {TOP_K} retrieved doc(s) above)\n")

    response = ollama.chat(model=CHAT_MODEL, messages=[{"role": "user", "content": prompt}])
    answer = response["message"]["content"]
    print(f"STAGE 5 - GENERATE:\n  {answer}\n")

    print("=" * 60)
    print("Saved for scoring in rag_eval.py:")
    print(f"  retrieved_contexts = {retrieved!r}")
    print(f"  response = {answer!r}")


if __name__ == "__main__":
    main()
