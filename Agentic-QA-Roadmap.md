# Agentic QA Roadmap

*A 22-week, phase-by-phase path from automation testing to professional agentic AI testing.*

Check items off as you go (most editors and GitHub render `- [ ]` as clickable checkboxes).

---

## Phase 0 — Mental Model Shift (Week 1)

Understand why testing probabilistic systems differs from testing deterministic ones before touching any tool.

- [ ] Read Anthropic's prompt engineering guide
- [ ] Read OpenAI's prompt engineering guide
- [ ] Write 5 bullet points on how LLM testing differs from traditional automation, in your own words

---

## Phase 1 — LLM & Gen AI Fundamentals (Weeks 2–4)

Build the conceptual base — tokens, embeddings, sampling, hallucination — that every later testing decision rests on.

**Week 2**
- [ ] Complete "ChatGPT Prompt Engineering for Developers" (DeepLearning.AI)
- [ ] Learn tokens & context windows — explain why long chats get "forgotten"

**Week 3**
- [ ] Complete "How Transformers Work" (conceptual, no math)
- [ ] Learn embeddings & vector similarity search basics
- [ ] Learn temperature, top-p, and sampling — why identical prompts give different outputs

**Week 4**
- [ ] Complete "Building Systems with the ChatGPT API" (DeepLearning.AI)
- [ ] Learn the difference between fine-tuning, RAG, and prompting
- [ ] Learn common hallucination causes and patterns
- [ ] Summarize: what would you flag as a "bug" in a model response, and why?

---

## Phase 2 — Gen AI Testing Fundamentals (Weeks 5–8)

Learn the new defect taxonomy and evaluation techniques, then write your first real LLM test suites.

**Week 5**
- [ ] Study the defect taxonomy: hallucination, bias, toxicity, injection, inconsistency, context loss, PII leakage, refusal errors
- [ ] Read about BLEU/ROUGE and why they fail on open-ended text

**Week 6**
- [x] Learn the LLM-as-a-judge evaluation technique
- [x] Learn how to build a golden dataset of input/expected-output pairs
- [x] Install Promptfoo and run your first config-driven test suite

**Week 7**
- [x] Install DeepEval and write pytest-style LLM assertions
- [x] Build 5 golden test cases against a live LLM (local model via Ollama, no cloud API needed)

**Week 8**
- [x] Install Giskard and run a vulnerability scan (note: Giskard v3 replaced `scan()` with scenario-based checks - used the current API to run a real prompt-injection probe instead)
- [x] **Project 1:** full test suite covering correctness, hallucination detection, and 5-run consistency
- [x] Push Project 1 to a public GitHub repo &rarr; https://github.com/mohit03nandan/agentic-qa-project-1

---

## Phase 3 — RAG Systems Testing (Weeks 9–10)

Test retrieval-augmented pipelines stage by stage — most "AI chatbot" features you'll meet in the wild are RAG.

**Week 9**
- [x] Learn the RAG pipeline: query → embed → retrieve → inject context → generate
- [x] Learn RAGAS metrics: faithfulness, answer relevance, context precision/recall

**Week 10**
- [x] Tracing: built a small RAG app with each stage printed/visible by hand (query → embed → retrieve → inject → generate) — LangSmith/TruLens skipped in favor of manual tracing to avoid another dependency rabbit hole
- [x] Test a sample RAG app stage by stage: retrieval, then relevance, then faithfulness
- [x] Documented one retrieval bug (missed the "Final Sale" exception doc) and, more importantly, a judge-reliability bug (context recall judge hallucinated a missing fact as present)

---

## Phase 4 — Agentic AI Concepts (Weeks 11–14)

Learn how agents plan, call tools, and remember — you can't test a structure you don't understand.

**Week 11**
- [x] Learn what separates an "agent" from a chatbot: planning, autonomy, multi-step reasoning
- [x] Learn the ReAct (reason + act) loop pattern

**Week 12**
- [x] Learn tool/function calling mechanics — how an agent picks a tool and its arguments
- [x] Learn memory types: short-term, long-term (vector store), episodic

**Week 13**
- [x] Learn multi-agent orchestration and delegation patterns
- [x] Learn the basics of MCP (Model Context Protocol)

**Week 14**
- [x] **Project 2:** build a simple 2–3 tool agent — built from scratch (no framework) using Ollama's native tool calling, to keep the ReAct loop fully visible; found 2 real bugs (malformed tool calls, and a policy-violation reasoning failure)

---

## Phase 5 — Agentic AI Testing (Weeks 15–20)

The specialization itself: trajectory evaluation, tool-call correctness, and adversarial red-teaming of autonomous systems.

**Week 15**
- [x] Learn trajectory/path evaluation — judging the steps, not just the final answer
- [x] Learn tool-selection correctness testing

**Week 16**
- [x] Learn task completion / goal success rate measurement across repeated runs
- [x] Learn multi-turn coherence and state-tracking testing

**Week 17**
- [x] Learn loop/deadlock detection and cost-per-task tracking
- [x] Tracing on Project 2 agent — already have full step-by-step ACT/OBSERVE prints in `shoe_store_agent.py` (LangSmith skipped, same reasoning as Week 10: avoids another cloud account/dependency)

**Week 18**
- [x] Study the OWASP Top 10 for LLM Applications until you can recite it
- [x] Learn direct and indirect prompt injection techniques

**Week 19**
- [x] Learn jailbreak probing methodology
- [x] Learn excessive-agency and data-exfiltration risks
- [x] Learn structured red-teaming methodology

**Week 20**
- [x] **Project 3 (portfolio piece):** full agent test suite — functional, trajectory, tool-call accuracy, adversarial resistance, cost/latency, regression (1/5 passed — real findings, including a self-contradicting adversarial failure)

---

## Phase 6 — Production & Non-Functional Concerns (Weeks 21–22)

Round out with the concerns that only show up once an agent is live: cost, latency, drift.

**Week 21**
- [x] Learn load/performance testing for LLM APIs — latency percentiles, streaming, rate limits
- [x] Learn cost/token-usage regression testing

**Week 22**
- [x] Learn A/B testing across prompts and model versions
- [x] Learn production monitoring and behavioral drift detection

**ROADMAP COMPLETE** — Phases 0–6 done, three portfolio projects built and pushed to GitHub.

---

## Proof of Work (Ongoing — start as soon as Project 1 exists)

What actually gets you hired. Don't wait until week 22 to start these.

- [x] Keep a public GitHub repo of your agent-testing framework, updated as you learn &rarr; https://github.com/mohit03nandan/agentic-qa-project-1
- [ ] Write 2–3 short case studies on defects you found through red-teaming
- [ ] Contribute a test case or issue to LangGraph or CrewAI
- [ ] Practice explaining the OWASP LLM Top 10 and trajectory evaluation out loud, unscripted

---

## Reference: New Defect Categories (vs. traditional testing)

| Category | What it means |
|---|---|
| Hallucination | Model fabricates facts, sources, or details |
| Bias & fairness | Skewed or discriminatory outputs |
| Toxicity | Harmful, offensive, or unsafe content |
| Prompt injection | Malicious input hijacks the model's instructions |
| Inconsistency | Same input, materially different output across runs |
| Context loss | Model forgets or ignores earlier instructions |
| PII leakage | Model exposes personal/sensitive data |
| Refusal errors | Over-refusing safe requests, or under-refusing unsafe ones |

## Reference: Tools by Phase

| Tool | Used for |
|---|---|
| Promptfoo | Config-driven prompt/output testing |
| DeepEval | Pytest-style LLM test assertions |
| RAGAS | RAG pipeline evaluation (faithfulness, relevance) |
| Giskard | Automated vulnerability scanning (bias, hallucination, injection) |
| LangSmith | Tracing and evaluation for LangChain/LangGraph agents |
| TruLens | RAG and LLM app tracing/evaluation |
| LangGraph / CrewAI | Building and orchestrating agents |
| OWASP LLM Top 10 | Security checklist for LLM applications |

---

*Also available as an interactive, progress-tracked page: [Agentic QA Roadmap artifact](https://claude.ai/code/artifact/97306399-e9f8-4a3e-a6e9-18bee55cd654)*
