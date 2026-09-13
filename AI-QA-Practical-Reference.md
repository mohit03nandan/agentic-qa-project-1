# AI/LLM Testing — Practical Reference for QA

One dense page instead of three long ones. Organised by **what you actually do at work**, not by course order.

Detail lives in:
- [Agentic-QA-Revision-Notes.md](Agentic-QA-Revision-Notes.md) — the 22-week roadmap, concepts + real hands-on findings
- [Course-1-GenAI-Testing-Notes.md](Course-1-GenAI-Testing-Notes.md) — using Gen AI to *help you* test
- [Course-2-LLM-Testing-DeepEval-RAGAS-Notes.md](Course-2-LLM-Testing-DeepEval-RAGAS-Notes.md) — testing AI systems with DeepEval/RAGAS

Sections marked **[GAP]** aren't in any of those — they're things real AI QA work needs that the courses skipped.

---

## 1. What actually changes vs. normal QA

| Normal software | AI system |
|---|---|
| Same input → same output | Same input → **different output every run** |
| Bug traces to a line of code | "Bug" could be prompt, retrieval, model, or the judge |
| Pass/fail is binary | Pass/fail is a **score vs. a threshold you chose** |
| Test data is fixed | Correct answer may be a *range* of acceptable answers |
| You test the code | You test **behaviour**, and the code didn't even change |

**The one sentence version:** you stop asserting equality and start scoring behaviour, which means *you* now own the definition of "good enough."

---

## 2. Three system types — and what breaks in each

### A. Plain LLM app (prompt in → text out)
**Breaks as:** hallucination, ignoring instructions, wrong tone/format, bias/toxicity, inconsistency between runs.
**Test:** Answer Relevancy, Prompt Alignment (did it follow the instruction, not just answer well), Correctness, Bias/Toxicity.

### B. RAG app (retrieve docs → answer from them)
**Four independent failure points** — this is the most useful RAG idea to hold onto:

| Stage | What breaks | Metric that catches it |
|---|---|---|
| Chunking | Info split badly, context severed | (indirect — shows up as bad retrieval) |
| Embedding/indexing | Right doc exists but never surfaces | Contextual **Recall** |
| Retrieval ranking | Junk ranked above the good chunk | Contextual **Precision** |
| Generation | Right docs retrieved, answer still ignores them | **Faithfulness** / Contextual Relevancy |

**Why it matters:** "the bot gave a wrong answer" is not a bug report. *Which of the four* is the bug report.

### C. Agent (LLM + tools + loop)
**Breaks as:** wrong tool picked, right tool + wrong arguments, right tools + wrong order, infinite loop, task abandoned halfway, excessive agency (did something it shouldn't).
**Test:** Tool Correctness, argument accuracy, trajectory evaluation, task completion, loop detection.

---

## 3. Metrics cheat-sheet

| Metric | Catches | Needs | LLM-judged? |
|---|---|---|---|
| Answer Relevancy | Off-topic / padded answers | input, actual_output | Yes |
| Prompt Alignment | Ignored your instructions | input, actual_output | Yes |
| Faithfulness | Answer contradicts retrieved docs | actual_output, retrieval_context | Yes |
| Contextual Precision | Junk ranked above good chunks | + expected_output | Yes |
| Contextual Recall | Needed info never retrieved | + expected_output | Yes |
| Contextual Relevancy | Answer ignores what was retrieved | retrieval_context | Yes |
| Hallucination | Invented facts | context | Yes |
| Bias / Toxicity | Unsafe or skewed output | actual_output | Yes |
| **Tool Correctness** | Wrong tool called | tools_called, expected_tools | **No — deterministic** |
| Task Completion | Gave up / didn't finish | trajectory | Yes |
| G-Eval (custom) | Anything you can describe in English | whatever you specify | Yes |

**Three traps worth memorising:**
1. **Answer Relevancy does NOT check `expected_output`.** It only asks "is this a relevant answer to the question." A confidently wrong answer can score 1.0.
2. **Scoring direction isn't universal.** Higher is better for relevancy; for bias-type metrics lower can mean better. Always verify on a known-bad example before trusting a metric.
3. **Tool Correctness ignores call *order* by default.** Fine for one tool, dangerous for a multi-step agent where order is the policy (e.g. look up the order *before* refunding it).

---

## 4. Anatomy of a test

```
Golden (stable truth)          Test case (per run)
---------------------          -------------------
input                     →    input
expected_output           →    expected_output
context                   →    retrieval_context   ← from the REAL retriever
                               actual_output       ← from the REAL system
                               tools_called        ← from the REAL agent
                               → score vs threshold
```

- **Golden** = the fixed truth set. Store centrally (Confident AI dataset, or a JSON/CSV in repo). Non-engineers can edit these.
- **Test case** = one execution. `actual_output`, `retrieval_context`, `tools_called` must come from the *live* system — hardcoding them means you're testing nothing.
- **Threshold** = your call, not the tool's. The score doesn't change when you move it; only pass/fail does.

---

## 5. LLM-as-a-judge — and its limits

Nearly every metric above is "hand a rubric to a second LLM and ask it to score." That's why:
- Scores **drift between identical runs** — the judge is itself non-deterministic.
- A **weak judge model produces garbage** (small models fail to emit valid JSON, or miss the point entirely).
- The judge's **own knowledge leaks in** — it may pass an answer because it happens to know it's true, regardless of your supplied context.

**[GAP] Who tests the judge?**
Before trusting a metric in a pipeline, calibrate it:
1. Build ~10 examples you already know the verdict for (5 clearly good, 5 clearly bad).
2. Run the metric. Does it agree with you?
3. Run the same set 3× — how much does the score move? That variance is your **noise floor**; your threshold must sit outside it.
4. Re-calibrate when you change judge model. A judge swap is a breaking change, not a config tweak.

---

## 6. **[GAP]** When a test fails — triage order

Don't report "AI is wrong." Work down this list:

1. **Is it just noise?** Re-run 3×. If it flips around the threshold, it's variance, not a bug → widen the threshold or fix the noise floor.
2. **Is the judge wrong?** Read the judge's `reason` field. If the reasoning is nonsense, the metric is the bug.
3. **Is the test wrong?** Missing `retrieval_context`, stale `expected_output`, wrong required field. (Very common.)
4. **Is it the prompt?** Vague instructions produce hedging/deflection. Tighten and re-run — this fixes a surprising share of "model is broken" reports.
5. **RAG: which stage?** Print the retrieved chunks. If the right chunk isn't there → retrieval/indexing bug. If it's there and the answer ignores it → generation bug.
6. **Agent: which step?** Print the trajectory. Wrong tool / wrong args / wrong order / never terminated.
7. **Only now** is it a genuine model-quality issue.

---

## 7. **[GAP]** Running evals in CI/CD

The honest problems: evals are **slow**, **non-deterministic**, and **cost money or CPU**. So:

- **Tier your suite.** Smoke set (~10 cases, deterministic metrics only — tool correctness, format/schema checks) on every PR. Full set nightly. Expensive red-team/adversarial suite weekly.
- **Prefer deterministic checks where possible** — schema valid, required tool called, PII absent, latency under X, cost under Y. These are fast and never flake.
- **Gate on aggregates, not single cases.** "Pass rate ≥ 90% across 50 cases" is stable. "This one case must score ≥ 0.8" will flake forever.
- **Pin the judge model version.** Otherwise a silent provider update rewrites your baselines overnight.
- **Budget the run.** Track tokens/cost per suite execution; a runaway eval suite is a real bill.
- **Store every run.** Trend lines matter more than any single run's verdict.

---

## 8. **[GAP]** Designing the test set

- **Start from real user queries**, not invented ones. Pull from logs/support tickets where possible.
- **Cover the shapes, not just the topics:** happy path, ambiguous phrasing, out-of-scope question ("I don't know" is a correct answer — test that it says so), adversarial/injection, empty/garbage input, very long input, multi-turn follow-up.
- **Paraphrase robustness:** the same intent worded 3 ways should behave the same. This is where agents break most often.
- **Keep goldens small and stable.** 30 well-chosen cases beat 300 noisy ones.
- **Synthetic generation** (RAGAS can generate test sets from your documents) is good for *volume*, but human-review the generated goldens before they become truth.

---

## 9. **[GAP]** Writing this up for non-QA people

Nobody outside QA knows what "0.62 contextual precision" means. Translate:

- **Bad:** "Faithfulness scored 0.4."
- **Good:** "In 4 of 10 billing questions, the bot stated a refund window that does not appear anywhere in our policy docs. Risk: customers act on wrong information."

Set acceptance criteria *with* the product owner **before** testing, in their language:
- What must never happen (hard fail — e.g. invents a policy, leaks PII, calls the refund tool unprompted)?
- What's acceptable degradation (soft — e.g. slightly verbose answers)?
- What pass rate ships? 90%? 99%? For which category?

---

## 10. Security testing — the short version

Full detail in the roadmap notes (Weeks 18–19). Minimum bar for any AI feature:

- **Direct prompt injection** — "ignore previous instructions..."
- **Indirect injection** — malicious text hidden in a *retrieved document* or web page the agent reads. This is the one people forget, and RAG/agents are wide open to it.
- **Jailbreaks** — roleplay/hypothetical framings to bypass rules.
- **Data exfiltration** — can it be coaxed into revealing its system prompt, other users' data, or internal docs?
- **Excessive agency** — can it be talked into calling a destructive tool it shouldn't (refund, delete, send email)?
- **PII leakage** — in outputs *and* in what gets sent to a third-party API.

Treat any of these succeeding as a **hard fail**, not a score.

---

## 11. Non-functional checks that are actually test criteria

| Check | Why |
|---|---|
| Latency p95 (not average) | One slow tail request ruins UX; averages hide it |
| Cost per request / per task | Directly ships to the invoice; regressions are silent |
| Token usage regression | A prompt tweak can double cost with no visible output change |
| Loop/step cap | An agent that never terminates burns money in production |
| Drift over time | Same test, same prompt, worse score next month = provider changed the model |

---

## 12. Tools — one line each

| Tool | Use it for |
|---|---|
| **DeepEval** | Pytest-style LLM assertions, custom metrics (G-Eval), agent tool-correctness |
| **RAGAS** | RAG-specific metrics, synthetic test-set generation from your docs |
| **Promptfoo** | Fast side-by-side prompt/model comparison, `--repeat` for consistency runs |
| **Giskard** | Scanning for injection/bias/robustness vulnerabilities |
| **HF `evaluate`** | Classic statistical scores (BLEU/ROUGE) — only really for fine-tuning work |
| **Ollama** | Running models locally: free, private, no quota — costs you CPU/time instead |
| **LangSmith / Langfuse** | Tracing multi-step agent runs; essential for debugging trajectories |
| **Confident AI** | Hosted dashboards/history for DeepEval (free tier is capped per week) |

---

## 13. If you remember only five things

1. **Score, don't assert.** And *you* own the threshold.
2. **Re-run before you report.** Non-determinism looks exactly like a bug.
3. **Localise the failure** — chunking / retrieval / generation / tool / args / judge — before calling it a model problem.
4. **The judge is a system under test too.** Calibrate it against known answers.
5. **Some failures are never "a low score"** — injection, PII leakage, unauthorised tool calls are hard fails.
