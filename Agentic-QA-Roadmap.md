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
- [ ] Push Project 1 to a public GitHub repo

---

## Phase 3 — RAG Systems Testing (Weeks 9–10)

Test retrieval-augmented pipelines stage by stage — most "AI chatbot" features you'll meet in the wild are RAG.

**Week 9**
- [ ] Learn the RAG pipeline: query → embed → retrieve → inject context → generate
- [ ] Learn RAGAS metrics: faithfulness, answer relevance, context precision/recall

**Week 10**
- [ ] Set up tracing with LangSmith or TruLens
- [ ] Test a sample RAG app stage by stage: retrieval, then relevance, then faithfulness
- [ ] Document one retrieval bug and one faithfulness bug you found

---

## Phase 4 — Agentic AI Concepts (Weeks 11–14)

Learn how agents plan, call tools, and remember — you can't test a structure you don't understand.

**Week 11**
- [ ] Learn what separates an "agent" from a chatbot: planning, autonomy, multi-step reasoning
- [ ] Learn the ReAct (reason + act) loop pattern

**Week 12**
- [ ] Learn tool/function calling mechanics — how an agent picks a tool and its arguments
- [ ] Learn memory types: short-term, long-term (vector store), episodic

**Week 13**
- [ ] Learn multi-agent orchestration and delegation patterns
- [ ] Learn the basics of MCP (Model Context Protocol)

**Week 14**
- [ ] **Project 2:** build a simple 2–3 tool agent with LangGraph or CrewAI

---

## Phase 5 — Agentic AI Testing (Weeks 15–20)

The specialization itself: trajectory evaluation, tool-call correctness, and adversarial red-teaming of autonomous systems.

**Week 15**
- [ ] Learn trajectory/path evaluation — judging the steps, not just the final answer
- [ ] Learn tool-selection correctness testing

**Week 16**
- [ ] Learn task completion / goal success rate measurement across repeated runs
- [ ] Learn multi-turn coherence and state-tracking testing

**Week 17**
- [ ] Learn loop/deadlock detection and cost-per-task tracking
- [ ] Wire up LangSmith tracing on your Project 2 agent

**Week 18**
- [ ] Study the OWASP Top 10 for LLM Applications until you can recite it
- [ ] Learn direct and indirect prompt injection techniques

**Week 19**
- [ ] Learn jailbreak probing methodology
- [ ] Learn excessive-agency and data-exfiltration risks
- [ ] Learn structured red-teaming methodology

**Week 20**
- [ ] **Project 3 (portfolio piece):** full agent test suite — functional, trajectory, tool-call accuracy, adversarial resistance, cost/latency, regression

---

## Phase 6 — Production & Non-Functional Concerns (Weeks 21–22)

Round out with the concerns that only show up once an agent is live: cost, latency, drift.

**Week 21**
- [ ] Learn load/performance testing for LLM APIs — latency percentiles, streaming, rate limits
- [ ] Learn cost/token-usage regression testing

**Week 22**
- [ ] Learn A/B testing across prompts and model versions
- [ ] Learn production monitoring and behavioral drift detection

---

## Proof of Work (Ongoing — start as soon as Project 1 exists)

What actually gets you hired. Don't wait until week 22 to start these.

- [ ] Keep a public GitHub repo of your agent-testing framework, updated as you learn
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
