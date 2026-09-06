# Course 2 — Path to AI QA Engineer (DeepEval, RAGAS, HF Evaluate, Local LLMs)

Official course title (confirmed from the Udemy player UI): *"2026 - Path to AI QA Engineer to test LLMs and AI Apps using DeepEval, RAGAs and HF Evaluate with Local LLMs like Ollama"* (4.4★, 819 ratings, 7,807 students, 14.5 hours total, last updated June 2026).

A new, separate course from [Course-1-GenAI-Testing-Notes.md](Course-1-GenAI-Testing-Notes.md) — this one is about *testing/evaluating* LLM applications specifically (using DeepEval, RAGAS, and other tools, working with Ollama and local models), rather than using Gen AI to help write tests.

Notes captured from lecture transcripts/screenshots, section by section, cleaned up into plain English (not a word-for-word transcript).

---

## Section 1.1 — Welcome, and Why Do We Even Need to Evaluate an LLM?

### The basic flow
A user sends a prompt to an LLM — could be a local model, or a cloud one like ChatGPT or DeepSeek — and the LLM sends back a response. Simple enough. But the real question this course is built around is: **how do we know if that response is actually correct?**
- If you already know the right answer, checking is easy — just compare.
- If you *don't* already know the right answer, it gets tricky — and this is where most real usage actually lives.

### Example 1: A simple factual question — easy to verify
Asking "What is the capital of New Zealand? Just give the city name" gets back "Wellington." Easy to check — it's a known, verifiable fact.

### Example 2: Summarizing a document — harder to verify
Upload a whole document and ask for a summary. Now checking the answer requires you to actually understand the document yourself first, so you can judge whether the summary is fair and accurate. This is where "the QA hat" has to come on — it's not a one-glance check anymore.

### Example 3: Asking for code — looks right, but might not actually work
Ask DeepSeek for a C#/.NET Playwright test, and it hands back a code block that *looks* correct. But running it in a real IDE might reveal it's broken. Point the error back out to the model, and it apologizes and fixes it. This is the clearest example in the lecture: **an LLM's output can look confident and correct while still being wrong** — you don't find out until you actually run/verify it.

### The core lesson
LLM output is never guaranteed to be 100% accurate. That's the entire reason evaluation exists as a discipline — you can't just trust a response because it *sounds* right; you need a structured way to check it.

---

## What Is "LLM Evaluation"?

### Benchmarks and datasets
LLMs are typically evaluated using standardized datasets designed to test performance across different task types, such as:
- Text summarization (the document example above)
- Open-book question answering (the "capital of New Zealand" example)
- Code generation (the Playwright example)
- Language understanding

These datasets act as a common benchmark — a fair way to compare different models against each other, and to see how well a model handles real-world tasks, not just cherry-picked easy questions.

### Evaluation metrics — two broad categories

**1. Traditional metrics** — compare the LLM's generated text against a known correct answer, called the **ground truth** (or *reference*). These metrics mostly look at word order and structure. Examples: exact match, BLEU score, ROUGE, F1 score. Commonly used for summarization and translation tasks.

*In plain terms: this is "actual vs. expected" testing, just like normal software testing — you need a correct/expected answer (the ground truth) prepared ahead of time, and then you score how closely the model's actual answer matches it.*

**2. Non-traditional metrics** — use semantic understanding (does it *mean* the same thing, not just use the same words) or even use another model's judgement to score the output. These can work *with or without* a reference answer. Examples: embedding similarity, perplexity, and **LLM-based scoring** (using an LLM to judge/score another LLM's output). Especially useful when fine-tuning a model and checking how well the fine-tuning worked.

*In plain terms: "LLM-based scoring" is the "LLM as judge" idea — instead of a human or a rigid word-matching formula, you use a second LLM to read the answer and score its quality. This is the more flexible, more human-like way of grading answers where there's no single "correct" wording to match against.*

### Tools mentioned for doing this
- **Hugging Face's `evaluate`** — a library/method that makes running these evaluations on a model's output straightforward.
- **DeepEval** — has a *huge* number of built-in metrics available (the lecture shows VS Code's autocomplete listing dozens: answer relevancy, conversational metrics, RAG metrics, multimodal metrics, and many more). This course will only cover a handful of the most important ones in upcoming lectures, not the entire list.

---

## Section 1.2 — Understanding Types of AI Applications

Before evaluation can be discussed properly, this lecture steps back to cover *what kinds* of AI applications actually exist — since the way you'd test a chatbot is different from how you'd test an AI agent or a RAG system.

### What counts as "an AI application"
An AI application is any software program that uses AI techniques to perform tasks that would normally need human intelligence — learning, reasoning, problem-solving, perception, language understanding, decision-making.

That covers a lot of ground. Some categories named: chatbots, AI agents, AI in software automation testing, RAG (retrieval-augmented generation), AI for web scraping/data extraction, and AI applied to healthcare, defense, education, farming, robotics, and more. Basically every industry is now trying to bolt AI onto its products ("the AI race"). What makes this possible is that models like ChatGPT are **general-purpose** — one model, usable for almost any task — which is the real shift LLMs brought since 2022.

This course focuses on three of these types in particular: **chatbots**, **AI agents**, and **RAG**.

### Type 1: Chatbots
The simplest category — you ask, it answers. Already seen in Section 1.1 ("capital of New Zealand" → "Wellington"). A few more examples of just how flexible one general-purpose model can be:
- Ask it to "explain the speed of light like a kindergarten teacher," and it adjusts its tone/style to match.
- Ask for Selenium C#/.NET code with dependency injection, and it can even give back **two different versions side by side**, asking which one you prefer — feeding your choice back to refine future responses.

*In plain terms: that "pick which response you prefer" feature is the same A/B response-comparison UI already seen and noted in Course 1's notes (Section 4.4, "You're giving feedback on a new version of ChatGPT") — it's OpenAI quietly collecting human preference data to improve the model, not something specific to this course.*

### Type 2: AI Agents
An AI agent is a program/system that lets an LLM reach *outside* itself — searching the live web, writing better code with more context, and so on — instead of only answering from what it memorized during training.

**Demo:** Ask ChatGPT "who won the 2024 US presidential election" *without* web search enabled, and (because that's recent, real-world information) the answer won't be reliable. Turn web search on, and it visibly goes and searches (citing sources like Wikipedia and a news site), then gives an accurate, current answer. Notice: for the earlier Selenium-code or speed-of-light questions, it never needed to search — the model already "knew" those from training. It only reaches for a tool when its own frozen knowledge isn't enough.

**A second demo drives the same point home from the other direction:** the exact same 2024-election question, asked to a *local* model (Qwen 2.5, no tools attached) — it correctly says (based on its training cutoff of October 2023) that the election hasn't happened yet, because it has no way to know otherwise. Only once that model is "fused" with an agent that has a search/Wikipedia tool does it correctly report the actual outcome.

*In plain terms: this is exactly the "LLM vs. agent" distinction already worked through hands-on with smolagents and browser-use — a plain LLM only knows what it learned during training and has no way to check anything happening after its cutoff date; an agent adds tools (like web search) that let it reach outside that frozen knowledge and get a real, current answer. Same idea, now shown with a concrete "who won the election" example instead of an abstract explanation.*

### Type 3: RAG (Retrieval-Augmented Generation)
RAG retrieves data from an external source — a PDF, a document, an Excel sheet, scraped web data — and feeds it to the LLM as context, so the answer is grounded in that specific source rather than only general training knowledge.

**Demo:** Upload the "Attention Is All You Need" paper (the foundational research paper behind the Transformer architecture that modern LLMs are built on) as a source, then ask "What is attention?" — the answer comes back clearly grounded in that paper's actual content. Ask the *same* question in a brand-new chat, with no PDF attached, and the answer is noticeably different — now it's coming from the model's general training knowledge instead of that specific document.

**How the RAG pipeline actually works, step by step:**
1. Documents get extracted and split into smaller chunks.
2. Each chunk is turned into an embedding (a vector) and stored in a vector database.
3. At question time, the system finds the chunks most semantically similar to the question.
4. Those retrieved chunks, plus the original question, are handed to the LLM to generate the final answer.

Companies use this pattern to point an LLM at their own large pile of internal documents (PDFs, docs, spreadsheets) so employees can get answers grounded in company-specific knowledge, not just generic answers.

*In plain terms: this is the same Retrieval → Augmented → Generation breakdown already covered in Course 1's notes (Section 4.6) — chunking and embeddings/vector stores are just the concrete "how" behind the "Retrieval" step of that R-A-G acronym. And the "upload a PDF, get grounded answers" demo here is the same pattern as NotebookLM (Course 1, Section 4.5) and GPT4All's LocalDocs (Course 1, Section 3.2) — three different products, same underlying idea.*

### A pointer to a related course
The instructor references a separate course of theirs — "Build and Test AI Agent, Chatbots and RAGs with Ollama and Local LLM" — which covers building these systems (chatbots, RAG apps, tool-calling AI agents) using LangChain in more depth.

*In plain terms: this matches "Course 3" in [Udemy-Course-Sequence.md](Udemy-Course-Sequence.md) — good confirmation that these courses are meant to build on each other in roughly the planned order.*

### Why this matters for testing
The whole point of this lecture: chatbots, AI agents, and RAG systems are architecturally different (a chatbot just answers; an agent reaches for tools; a RAG system retrieves and grounds its answers in documents), so testing/evaluating each of them well requires understanding which type you're actually dealing with — covered starting in the next lecture.

---

## Section 1.3 — Basics of LLM Evaluation with Prompts

### Why prompting and evaluation go hand in hand
A quote cited from an Anthropic Cloud Solution Architect sets up this whole lecture: **not being able to measure how well your model performs is the biggest blocker to actually using LLMs in production** — and it's exactly what keeps prompting "an art instead of a science." Doing evaluation work upfront costs time initially, but saves much more time later and gets a better product out sooner.

*In plain terms: "evals" (evaluations) and prompting aren't separate activities — you can't reliably improve a prompt without a way to measure whether the new version is actually better, and you can't evaluate meaningfully without decent prompts to test in the first place.*

### Why teams skip this anyway
Two honest reasons given: many people are simply unfamiliar with how LLM evaluation works, and it's unclear *how* to actually implement it. As a result, evaluation often gets skipped entirely — the lecture compares this directly to how unit testing gets skipped at a lot of companies under time pressure.

### The benefits of doing it properly
- Iterative prompt improvement (you can only iterate confidently once you can measure the difference)
- Quality assurance both before and after deployment
- Objective comparison between different models
- Cost savings (catching problems before they reach production, and not over-paying for capability you don't need)

### The evaluation workflow, step by step
1. **Write test cases** — multiple prompts, plus their expected outputs.
2. **Send the prompt** to the LLM.
3. **Run evaluation tools** against the result — this is where DeepEval, RAGAS, Hugging Face `evaluate`, and similar tools come in (the whole reason this course exists).
4. Once the results meet expectations, **deploy to production**.

### What an LLM "test case" actually contains
This isn't classical software testing, so the shape of a test case is a bit different. It typically holds:
- **Input data** — what you actually asked the LLM (the prompt).
- **Golden data** — the expected/correct result (also called the **ground truth**). This term comes up constantly in RAGAS/DeepEval-style tooling — worth remembering.
- **Model output** — the actual response, whether it came from a plain LLM, an AI application, or a RAG system.
- **Tool output / tool selection** — if the system is an AI agent, you also check whether it picked the *right* tool for the job, not just whether the final answer looked fine.
- **Score** — the evaluation result itself.

*In plain terms: this "golden data" is exactly the same idea as `REFERENCE_ANSWER` already used in this repo's own `rag_app.py` (Phase 3 of the roadmap) — a pre-written correct answer the actual output gets scored against. Same concept, just introduced here with its more common industry name.*

### The three types of evaluation

**1. Human-based (human-graded) evaluation**
A person — ideally a subject-matter expert, not just any tester — reviews the model's output and scores it. Best for subjective or nuanced judgment calls. Example given: if an LLM recommends a medicine, a doctor can recognize that a differently-worded but chemically-equivalent answer is still correct, whereas a software tester without medical knowledge might wrongly mark it "failed" just because it didn't match the expected wording exactly.

**2. Code-based (code-graded) evaluation**
A programmatic, rule-based check — comparing output against expected values in code. Works well when the correct answer is unambiguous and objective (a specific number, an exact string). This is the main style behind Hugging Face's `evaluate` library.

**3. LLM-based evaluation ("LLM as a judge")**
Uses a *second* LLM to evaluate the first LLM's output. This is presented as the sweet spot between the other two: it handles subjective, nuanced judgment better than rigid code-based checks, while being much faster and more scalable than paying humans to review every single output. **This is the approach DeepEval and RAGAS lean on most**, and the one this course will spend the most time on.

*In plain terms: this directly extends the "non-traditional metrics" mentioned back in Section 1.1 ("LLM-based scoring") — now given its proper name, "LLM as a judge," plus the reasoning for why it's the practical middle ground.*

### What "LLM as a judge" can actually score
A long list of metric categories that DeepEval/RAGAS implement using this approach:
- General-purpose: **G-Eval**, **DAG**
- RAG-specific: answer relevancy, faithfulness, contextual precision, contextual recall, contextual relevancy
- Agentic: task completion, tool correctness/tool completion
- Conversational: bias, toxicity, summarization quality, prompt/hallucination detection

*In plain terms: don't worry about memorizing this whole list yet — the lecture flags it as a preview, and says only a handful of these will actually get covered in depth in upcoming DeepEval-focused sections. Worth noting: "tool correctness" (checking an agent picked the *right* tool) connects straight back to the "AI Agent & Model Testing" category flagged in Course 1's TestSprite notes (Section 7.2) — evaluating an agent's tool-use decisions, not just its final answer, is treated as its own distinct thing to test.*

---

## Section 1.4 — Hands-On: Human-Graded Evaluation Using Anthropic's Workbench

This lecture demos the first of the three evaluation types from Section 1.3 — **human-based evaluation** — using Anthropic's **Workbench** (part of the Anthropic Console; OpenAI has an equivalent). A general-purpose model is used throughout (Claude 3.7 Sonnet, the latest at recording time), not a custom fine-tuned one.

### Setting up the prompt
The Workbench lets you configure a model, variables, tools, and example inputs for one prompt, plus settings like temperature, max tokens, and (for reasoning models like Claude 3.7 Sonnet) a "thinking"/reasoning token budget.

The demo prompt gives Claude a role and a job:
> "You are a skilled QA engineer, especially in automation testing. Your job is to convert Selenium test code to Playwright, for any given language (C#, Java, TypeScript, JavaScript). If you see an unsupported language, add a comment saying Playwright doesn't support that language binding yet."

Two **input variables** are defined using `{{double braces}}` — one for the source code itself, one for what language it's written in. Workbench turns each variable into its own fillable field, forming the actual "test case" input.

### First run
Real Selenium sample code is pulled from the ExecuteAutomation GitHub repo (Java), pasted into the source-code variable, with `language = Java`. Running the prompt produces working Playwright code, complete with comments mapping Selenium concepts to Playwright ones (e.g. "this is the Chrome-driver equivalent," "this is a browser context, similar to a browser session").

*In plain terms: this is the same Selenium→Playwright idea already covered conceptually (Course 1, Section 5.1's point that LLMs already "understand" popular automation frameworks) — now seen concretely converting real, non-trivial test code from one framework to another, not just generating a fresh test from scratch.*

### The human-grading part
Workbench's **Evaluate** tab lets you manage several test cases for one prompt, see each one's model output, and — the actual human-grading step — assign your own **rating** to how good that output is (e.g. "very good"). You can also view the exact prompt that produced it.

### Iterating the prompt (version 2) — and a concrete token-savings result
A second version of the prompt makes the role even more senior/specific ("expert QA engineer and automation architect who provides automation test solutions") and adds an explicit instruction: *"do not include a lot of text apart from the code block."* Result: the output gets much less cluttered (no long explanatory comments), and **output tokens dropped from ~643 to ~300+** for the same conversion task.

*In plain terms: this is a very concrete example of Section 1.3's "prompting and evaluation go hand in hand" point — the only reason this improvement is visible and provable at all is because both prompt versions were run through the same test case and compared side by side. It's also a direct real-world instance of the "cost savings" benefit listed in Section 1.3: fewer output tokens for an equally-correct answer means a cheaper API call, at scale.*

### Generating more test cases, and comparing versions
- **Generate test case** (inside Evaluate) — lets the AI itself write a *new* test case for the same prompt (e.g. auto-generating a Python source-code example, changing the language variable to Python), instead of you writing every test case by hand.
- **Add comparison** — lines up outputs from two prompt versions side by side, along with the human ratings already given each (e.g. version 2 rated "very good" → a 4/5, version 3 rated "excellent" → a 5/5), then lets you **run remaining** to execute every test case against every compared prompt version at once.

*In plain terms: this is Section 1.3's abstract test-case structure (input, golden data, model output, score) made completely concrete — here, "input" is the source code + language variables, "model output" is the generated Playwright code, and "score" is literally the human-assigned rating (4, 5, etc.) sitting right next to it.*

### Adding a tool changes the output — not just adds a step
Workbench has a (preview) **Tools** option — custom tools, plus a built-in **web search** tool (configurable to allow/block specific domains, or the whole web). Re-running the *exact same* Selenium→Playwright prompt after adding the web search tool produced a noticeably more sophisticated result: instead of a flat, one-off code conversion, Claude now generated a full **Page Object Model** structure — separate classes for the Home Page, Login Page, and Employee List page, each with its own methods — much closer to how a real automation engineer would actually structure the code.

*In plain terms: this is a strong, concrete demonstration of what Course 1's Section 3.2 flagged as the Page Object pattern, and what this course's own Section 1.2 called an "AI agent" (a model reaching outside itself with a tool) — giving the model one extra tool (web search) measurably changed the *quality and structure* of its output, not just how it arrived there. No MCP server tool support yet in Workbench at time of recording, but the lecture expects that's coming.*

### One more capability, mentioned but not demoed
Workbench also supports adding further back-and-forth "message pairs" to a test case — building out a multi-turn conversation (a follow-up question after the assistant's reply, then another, and so on) to evaluate chain-of-thought-style interactions, not just single-turn prompts.

---

## Section 1.5 — Understanding Evaluation Metrics (in more depth)

A closer look at some of the metrics first previewed in Section 1.3's list — not every tool implements every metric (e.g. hallucination detection isn't universal across tools), but these are the ones that show up most often.

- **Answer Relevancy** — does the response actually address the user's query? This applies just as much to a fine-tuned model as to a plain application calling an LLM.
- **Contextual Relevancy** — in a RAG system, does the final *response* actually align with the context that was retrieved for it?
- **Contextual Precision** — a related but different check: how *precise* is the retrieved context itself (not the final response) — i.e., did the RAG system actually pull the right chunks, before the LLM even generates an answer from them?

  *In plain terms: Relevancy vs. Precision here is checking two separate failure points in a RAG pipeline (Course 1, Section 4.6 / this course's Section 1.2) — Precision asks "did we retrieve the right documents?", Relevancy asks "given what was retrieved, did the answer actually use it properly?" A RAG system can fail at either step independently — retrieve the wrong chunks (precision problem) or retrieve the right chunks but still generate an answer that ignores them (relevancy problem).*

- **Tool Selection Accuracy** — for a chatbot/agent, did it pick the *appropriate* tool/action for the given input? Called out as increasingly critical as an application scales from one or two tools to potentially hundreds or thousands (a mix of external and internal tools, some of which may even call other tools).

  *In plain terms: this is the same "tool correctness" idea flagged in Section 1.3's metric list, and it directly echoes the Workbench demo from Section 1.4 — adding the web search tool changed Claude's output entirely (to a full Page Object Model). At scale, with many tools available, checking that the *right* tool got picked for the job becomes its own dedicated testing concern, separate from whether the final answer was good.*

- **Bias Detection** — checks whether a model's response reveals bias baked in from its training data. Example given: asking "will boys get higher marks than girls?" — if the model answers "yes," that's not some universal truth, it's a sign the model was trained on data where boys happened to score higher, and it wrongly generalized that pattern into a rule.

  *In plain terms: this metric isn't checking "is the answer factually wrong" in the normal sense — it's checking whether the model is presenting a skewed pattern from its training data as if it were a general truth.*

- **Function/Argument Accuracy** — assesses whether the correct *arguments* (parameters) are being passed into a function or API call made by a chatbot/agent. If the arguments are wrong, the function call itself fails or returns nothing useful, and the whole response falls apart even if the *right* tool was chosen.

  *In plain terms: this is a level deeper than Tool Selection Accuracy — even if the agent picks the correct tool, it still has to fill in that tool's inputs correctly (e.g. calling `check_url_status` with a garbled or wrong URL would technically be "the right tool, wrong argument"). Both checks matter, and they catch different bugs.*

---

## Section 1.6 — Evaluation Libraries Overview: DeepEval, RAGAS, OpenAI Evals, Galileo, HF Evaluate

Five tools dominate the LLM-evaluation space right now: **DeepEval**, **RAGAS**, **OpenAI Evals**, **Galileo**, and **Hugging Face Evaluate**. All still evolving, each with its own strengths — this lecture is a quick tour before going deeper into individual tools later.

### OpenAI Evals
A framework for evaluating LLM applications/systems, with a built-in registry of ready-made evals covering different dimensions of OpenAI's own models, plus the ability to write custom evals for your own use case.

*In plain terms — the key limitation: OpenAI Evals is tightly built around OpenAI's own models (GPT-4.5, GPT-4.1, the "o" reasoning models). It works great if that's what you're using, but isn't the right tool if you want to evaluate other vendors' models or local models — which is this whole course's angle (testing with Ollama/local LLMs). That's the likely reason this course leans toward RAGAS/DeepEval instead.*

### RAGAS
Open-source, built specifically to "supercharge" evaluation of LLM applications — uses state-of-the-art LLM-assisted methods (i.e., the "LLM as a judge" idea from Section 1.3) to score performance with automated metrics. Notably, it can evaluate pipelines built with frameworks like LlamaIndex **without needing a hand-labeled evaluation dataset** prepared in advance.

*In plain terms: "without needing a hand-labeled dataset" is a big deal — normally you'd need someone to write out a bunch of golden/expected answers by hand (Section 1.3's "golden data") before you can evaluate anything. RAGAS can generate synthetic evaluation data itself, cutting out a lot of that manual prep work.*

### DeepEval
Open-source framework for building, testing, and monitoring LLM applications, with a large set of evaluation metrics/tools. Its own positioning: **"similar to Pytest, but specialized for unit-testing LLM outputs."** It bundles in recent research-backed metrics — G-Eval, hallucination detection, answer relevance, RAGAS-style metrics, and more.

*In plain terms: the Pytest comparison is the single most useful mental model here — if you already know how to write a Pytest assertion (`assert result == expected`), DeepEval is aiming to give you that same familiar workflow, except the "assertion" is really an LLM-judged metric checking something fuzzier than exact equality (like "was this answer relevant" or "did this hallucinate").*

Both RAGAS and DeepEval also come with their own observability features — visual dashboards to compare your dataset against actual model responses, rather than just raw pass/fail text output.

### Galileo
Positioned as an enterprise-grade generative-AI evaluation *and* observability platform — does what DeepEval/RAGAS do, but goes further with three categories on its site: **Evaluate**, **Observe**, and **Protect**.
- **Observe** — a LangSmith-style dashboard showing how the LLM calls different tools during testing (deep visibility into tool-use behavior, connecting to Section 1.5's "Tool Selection Accuracy" concern).
- **Protect** — an active **guardrail**: if a hallucination is detected, Galileo can intercept the response *before* it ever reaches the user, and serve a corrected/safe response instead of the flawed one.

*In plain terms: this is an important distinction from the other tools — DeepEval/RAGAS are mainly for testing/evaluating during development (did this response pass or fail our check), while Galileo's "Protect" feature works at production runtime, actively blocking a bad response in real time rather than just reporting on it afterward. Worth remembering as "test-time evaluation" vs. "runtime guardrail" — two different jobs, even though the underlying detection technique (hallucination scoring) may be similar.*

---

*(Next section's notes get appended below as more transcripts/screenshots come in.)*
