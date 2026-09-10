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

## Section 2.1 — Running Local LLMs with Ollama

A new section of the course begins here, shifting from cloud-hosted models (OpenAI, Anthropic, Google) to running models **locally, for free**, using **Ollama** — available for macOS, Linux, and Windows from ollama.com.

### Why this matters, cost-wise
The lecture contrasts this directly against OpenAI's API pricing page — every model call to a hosted API (OpenAI, Anthropic, Google Gemini) costs money per million tokens, for both input and output. Running a model locally through Ollama skips that entirely — no sign-up, no per-token billing, no API key needed.

*In plain terms: this matters even more for *evaluation* work specifically (the whole subject of this course) than for casual chatting — evaluating a model properly means running it against many test cases, often repeatedly as you iterate on prompts (exactly what Section 1.4's Workbench demo showed). That's a lot of API calls adding up fast if each one costs money; running locally makes heavy, repeated evaluation runs effectively free.*

### What's on Ollama's model library
Ollama's models page lists essentially every popular open model — DeepSeek R1, Llama 3.2, Mistral, Qwen 2.5, Phi-4, and more — each available at different parameter sizes. Models can also be filtered by *purpose*: general chat, **embedding** models, **vision** models, and — notably — models with **tool support** (needed for building agents), e.g. Llama 3.3 70B is flagged as tool-capable.

*In plain terms: this is the exact same tool already used hands-on earlier in this session — every one of the `smolagents` and `shoe_store_agent.py`/`rag_app.py` scripts in this repo already runs on Ollama, using `llama3.2:1b`. This lecture is really just formalizing something already set up and working in this project. The "tool support" filter is worth remembering for later: not every local model is built to reliably call tools/functions — that's exactly the gap that made `llama3.2:1b` shaky in the earlier smolagents dry-run (Course 1 discussion), so a model explicitly tagged "tool support" would likely behave more reliably for agentic tasks.*

### Setup note
The instructor has Ollama already installed and asks students to install it before the next lecture, since it'll be used starting there.

*In plain terms: nothing to do here — Ollama's already installed and working in this environment (confirmed earlier: `ollama list` shows `llama3.2:1b` and `nomic-embed-text` already pulled).*

---

## Section 2.2 — Choosing a Model Size: Parameters, Hardware, and Trade-offs

### Bigger parameter count = bigger file, more hardware needed
On Ollama's model page, most models offer a dropdown of parameter sizes — e.g. DeepSeek R1 ranges from 7B all the way up to 671B. Size scales fast: a 7B model is about 4.7GB, while the 671B version needs roughly 404GB of storage. More parameters means a more complex transformer model, which needs more processing power (CPU/GPU/RAM) and heavier quantization support to actually run.

*In plain terms: "parameters" are still the model's learned settings (first mentioned back in Course 1, Section 3.3, discussing Llama 3.2's 1B/3B vs 11B/90B lineup) — this lecture just puts real numbers on what that size difference costs in disk space and hardware.*

### Head count and head count (KV) — model internals shown per size
Each model listing also shows its **quantization version** and **head count** (and a separate "head count KV") — roughly, how many parallel "attention heads" the model uses internally. These numbers scale with model size: a 7B model might show ~28 head count, while DeepSeek R1's 671B version jumps to 128 head count and 128 head count KV.

*In plain terms: "heads" here is the exact same concept as the attention visualization seen all the way back in Course 1, Section 2.1 (the BertViz-style grid of Layers × Heads) — this lecture is showing that real number as a concrete spec you can check per model, not just an abstract diagram. More heads generally means the model can track more distinct kinds of relationships between words at once — part of why bigger models are more capable, and heavier to run.*

### Practical hardware guidance
Realistically, most machines can't handle the largest models (671B, 70B, even 32B). The lecture suggests capping expectations around **8B–14B** parameters for typical hardware. The instructor's own machine (Apple M1 Max, 64GB RAM) handles inference well; a typical Windows machine might be limited closer to 8B. For anyone wanting to run bigger local models, a dedicated Nvidia GPU helps — an RTX 3080 (or 2080) is a reasonable choice; a 4090 works but is expensive.

**The trade-off to remember:** smaller models are what's actually runnable on modest hardware, but they give less predictable/reliable output than larger ones.

*In plain terms — an honest, useful connection to this session's own earlier work: every script already built in this repo (`shoe_store_agent.py`, `rag_app.py`, and all the `smol_agent_*.py` scripts) runs on `llama3.2:1b` — a **1-billion-parameter** model, smaller than even the 7B–8B floor this lecture recommends as a practical minimum. That directly explains why the earlier smolagents custom-tool dry-run struggled (the model kept trying to write its own `import requests` instead of reliably using the given tool) — it wasn't a setup bug, it's exactly the "smaller = less predictable/reliable tool-use" trade-off this lecture is describing, now with a concrete real-world example already lived through in this same session.*

### Architecture isn't just about size
Comparing two different model families at similar/larger sizes shows the internal architecture isn't just a bigger version of the same thing: Llama 3.1's 405B version (243GB) shows a head count of 128 but a head count KV of only 8 — quite different from DeepSeek R1's 671B version (128 and 128). Different model families make different architectural trade-offs, not just "more of the same" as they scale up.

---

## Section 2.3 — Hands-On: Pulling and Running Models via the Ollama CLI, and Seeing Model Size Actually Matter

### The basic commands
- `ollama list` — shows every model already downloaded on the machine.
- `ollama run <model>:<size>` — pulls the model first if it isn't already downloaded (the lecture compares this directly to `docker pull` from Docker Hub — same idea, downloading an "image" for a model instead of a container), then drops you into an interactive prompt to chat with it, just like ChatGPT's interface.
- `/bye` — quits the current running model's prompt.

### Demo 1: a small, old model gives a completely wrong answer
Running `ollama run qwen:1.8b` (Qwen 1.5 series, 1.8B parameters, from Alibaba Cloud) and asking a normal question ("how are you doing?") works fine — a generic, reasonable chatbot reply. But asking it to **"write a Selenium C#/.NET code for the google.com website"** produces output that isn't Selenium code at all — it writes unrelated `HttpClient`/SSL-protocol style C# code, nothing like what was asked for.

### Demo 2: a stronger, reasoning-capable model gets it right
Switching to `ollama run deepseek-r1:8b` (already downloaded) and asking the *exact same* Selenium question produces a completely different result: DeepSeek R1 is a **reasoning model**, so it visibly writes out its "thinking" process first (working through what's being asked) before producing an answer — and this time, the generated Selenium C#/.NET code is actually correct and would run in a real IDE.

*In plain terms — this is Section 2.2's "smaller model = less predictable output" point, now proven with a real side-by-side example instead of just stated as a rule: same exact question, same task type (Selenium code generation, the same kind of task shown working fine with ChatGPT back in Course 1's Sections 2.2 and 3.2) — a small, older 1.8B model produced completely wrong, unusable output, while a larger, newer, reasoning-capable 8B model got it right. This directly explains (and validates) what was already observed hands-on earlier in this very session: the smolagents custom-tool dry-run used `llama3.2:1b` — even smaller than this failing 1.8B example — and it likewise produced unreliable, incorrect behavior (trying to `import requests` instead of using the given tool, then confidently reporting an unverified "200" status). Same underlying cause, two independent real examples of it now.*

*Touchpoint — "reasoning model" and visible "thinking": this is the same idea flagged back in Course 1, Section 1.4 (Claude 3.7 Sonnet's optional "thinking"/reasoning-budget setting in Anthropic's Workbench) — some models are specifically built to work through a problem step-by-step before answering, rather than jumping straight to a response, and that extra step visibly correlates with getting a harder task (like generating correct code) right.*

### The bigger point
Once a model is downloaded, it runs entirely offline — no internet connection needed at all for inference. But which model you choose clearly matters: a bigger/more capable (or more reasoning-oriented) model gives meaningfully better, more reliable answers than a small one, even for the exact same question.

---

## Section 2.4 — Nicer Chat Interfaces for Local Models: Msty and GPT4All

*(Note: this lecture's captions came through in Portuguese — notes below are translated/cleaned up, not transcribed.)*

After running models via the raw Ollama CLI (Section 2.3), this lecture shows friendlier, ChatGPT-like desktop UIs for the same local models — a quick taste before a later, deeper LangChain-based chatbot-building course.

### Two tools shown
- **Msty** (msty.app) — a chat interface for local models. Auto-detects every model already installed via Ollama (it picked up the 8B DeepSeek R1 model, plus others already on the machine, without extra setup). Also supports uploading documents, pasting YouTube links, and uploading images (for vision-capable models) to ask questions against them.
- **GPT4All** (gpt4all.io) — already covered hands-on back in Course 1, Section 3.2. Mentioned again here as supporting the R1 model too, with the same "visible thinking" behavior for reasoning models.

*In plain terms: Msty and GPT4All solve the same problem — a nicer, ChatGPT-style window for models you're already running locally through Ollama, so you don't have to work entirely from a terminal prompt.*

### Demo: proving the answer really is fully local
In Msty, DeepSeek R1 is selected and asked to convert Selenium code to Playwright for `eaapp.somee.com` — the same practice site used repeatedly throughout Course 1. Before hitting send, **the machine's internet connection is turned off**, to prove the response comes entirely from the local model with nothing sent anywhere. It still works — DeepSeek R1 visibly "thinks" through the problem, then writes out the conversion.

*In plain terms: this is a genuinely convincing, hands-on proof of the exact privacy claim from Course 1, Section 3.1 ("no internet required, nothing leaves your machine") — not just a marketing tagline this time, but demonstrated by literally disabling the network and getting a correct answer anyway.*

### What's next
The course flags that Ollama will be used again soon, once the course starts working with **LangChain** — matching the "Course 3" pointer already noted in this file's Section 1.2 (the instructor's separate "Build and Test AI Agent, Chatbots and RAGs with Ollama and Local LLM" course, listed in [Udemy-Course-Sequence.md](Udemy-Course-Sequence.md)).

---

## Section 2.5 — Ollama CLI Deep Dive: Managing Models Like Docker Containers

*(Note: this lecture's captions also came through in Portuguese — notes below are translated/cleaned up.)*

### The commands
- `ollama` (with no arguments) — lists every available subcommand.
- `ollama rm <model>` — deletes a downloaded model from the machine (confirmed afterward with `ollama list`, which no longer shows it).
- `ollama show <model>` — prints detailed metadata about a specific model: its architecture, parameter count/support, **context length**, **embedding length**, quantization, and which capabilities (e.g. tool support, vision) it has.

### The mental model: "Ollama is Docker, for LLMs"
The lecture draws this comparison directly — pulling, running, listing, removing, and inspecting a model with Ollama maps one-to-one onto pulling, running, listing, removing, and inspecting a container with Docker. Same lifecycle, different subject (a model instead of a container image).

*In plain terms: if Docker commands are already familiar, Ollama's command set should feel immediately intuitive — `ollama pull`/`run` ≈ `docker pull`/`run`, `ollama rm` ≈ `docker rm`, `ollama show` ≈ `docker inspect`.*

*Touchpoint — "context length": this is the same setting already used hands-on in this very session — the `smol_agent_*.py` scripts (Course 1) explicitly set `num_ctx=8192` when configuring `llama3.2:1b` through LiteLLM, specifically because Ollama's default context length (2048) is too small for agentic tasks. `ollama show` is exactly where you'd go to check what a given model's default context length actually is, before deciding whether to override it.*

### What's next
The course is about to start combining Ollama-run local models with **LangChain**, moving from "just chatting with a local model" toward actually building an LLM application on top of one.

---

## Section 2.6 — Ollama as an API Server (Section Wrap-up)

### Running Ollama as a service
`ollama serve` starts Ollama running as a background API server, listening on **port 11434**. (If it's already running as a persistent service, trying this again just reports the address is already bound — which is the normal, expected state.) This port is what upcoming sections will use to talk to the local model programmatically, instead of typing into a chat prompt by hand.

### Testing the API directly
- `http://localhost:11434/api/generate` (a simple check) confirms Ollama is running.
- The real work happens by **POST**ing to that `/api/generate` endpoint with a JSON body containing `model` and `prompt`. Demoed in Postman: `model: llama3.2`, `prompt: "Why is sky blue?"` — sent as a POST request, and a real answer comes back.
- By default, the response **streams** back one word/token at a time (useful for a live-typing chat UI feel). Setting `"stream": false` in the request body instead returns the whole answer in a single chunk.

*In plain terms — this closes a loop already relevant to this repo's own code: `shoe_store_agent.py`, `rag_app.py`, and `smol_agent_basic.py`/`smol_agent_websearch.py`/`smol_agent_custom_tool.py` (all from earlier in this session) call Ollama through the Python `ollama` library or through LiteLLM's `api_base="http://localhost:11434"`. Both are just convenient wrappers around exactly this same REST API — `ollama.chat(...)` under the hood is making the same kind of POST request to `/api/generate` (or the chat-equivalent endpoint) demonstrated here directly in Postman. Nothing new is being introduced technically; this lecture is just showing the raw HTTP layer that all of that existing code has been quietly sitting on top of the whole time.*

### Section wrap-up
This closes out the Ollama section. From the next section onward, the course moves to actually *building* something on top of a locally-running LLM — using these APIs together with **LangChain**.

---

## Section 3.1 — LLM Testing, Mapped onto Traditional Software Testing

A new section begins here — this is where the course starts actually using **DeepEval**. Before writing any code, this lecture deliberately maps LLM testing onto the traditional testing vocabulary a software test engineer already knows, so the DeepEval code that follows lands on familiar ground rather than feeling like an entirely new discipline.

### Definition
LLM testing = evaluating an LLM's output to make sure it meets specific criteria (accuracy, coherence, fairness, safety) for its intended purpose.

### The core difference from traditional testing
In traditional software, outcomes are predictable and a bug can usually be traced back to a specific block of code. LLMs behave like a **black box** with an effectively infinite range of possible inputs and outputs — there's no single line of code to point at when something goes wrong.

### Mapping LLM testing onto the four traditional testing types

**1. Unit testing → single-response evaluation**
Traditional unit testing checks the smallest testable piece of an application. For an LLM, that's evaluating one response to one input against a clearly defined expectation — exactly the "capital of New Zealand → Wellington" example used repeatedly earlier in this course. Simple, clear, pass/fail.

**2. Functional testing → task-level proficiency across many inputs**
Traditional functional testing verifies an entire user flow (e.g. logging in end-to-end). LLM functional testing instead checks how well the model performs *a specific task* — like text summarization — across a wide *range* of different inputs, not just one flow.

*In plain terms: it's less "does this one screen work" and more "does this one capability (summarizing) hold up across many different documents/questions," since there's no fixed "flow" to click through in an LLM app the way there is in a traditional UI.*

**3. Regression testing → same test cases, every iteration**
Run the same set of test cases every time a change is made, to catch breaking changes. The advantage of using quantitative metrics for this: you can set a clear **threshold** for what counts as "broken," and track how performance drifts across iterations over time.

*In plain terms — an important nuance: an LLM regression test doesn't need the exact same wording every single run to "pass" — it needs the same **meaning/context** to hold. If the response keeps landing on the same underlying answer (even phrased differently), that's fine. If the context keeps shifting or the model starts hallucinating, *that's* a real regression, even if no code changed — because the "code" here is really the prompt + model + surrounding data, any of which can drift.*

**4. Responsibility testing → not part of traditional testing at all**
This one has no real traditional-testing equivalent: testing the LLM's output against **responsible-AI metrics** — bias, toxicity, fairness — regardless of what task is being performed. Already touched on in Section 1.5 (Bias Detection), but worth noting here explicitly as its own category, since nothing like it exists in classic software QA.

### Why this framing matters
The metrics already covered across earlier sections (answer relevancy, tool/function-calling accuracy, contextual precision/recall, and so on — Sections 1.1, 1.3, 1.5) are the actual mechanics that implement these four categories. This lecture's job was just to line them up against a mental model already familiar from ordinary QA work, before the course starts writing real DeepEval code in the next lecture.

---

## Section 3.2 — The Non-Traditional Approach: LLM-Specific Metrics

Having mapped LLM testing onto traditional testing categories (Section 3.1), this lecture turns to the metrics side — evaluating an LLM (whether it's a raw model, an AI agent, a chatbot, a RAG system, or a fine-tuned model) always needs a different toolkit than unit/integration/regression testing alone.

### Statistical NLP metrics — named, but explicitly out of scope for this course
Three classic statistical evaluation metrics get named:
- **BLEU** (Bilingual Evaluation Understudy)
- **ROUGE** (Recall-Oriented Understudy for Gisting Evaluation)
- **METEOR** (Metric for Evaluation of Translation with Explicit Ordering)

These matter mainly when **fine-tuning** a model — checking how closely its output overlaps, word-for-word, with reference translations/summaries. The instructor has a separate course specifically on fine-tuning with Hugging Face that covers these in depth; this course intentionally skips them.

*In plain terms: this closes a loop from Section 1.1 — BLEU and ROUGE were already named there under "traditional metrics" (word-order/structure comparison against a reference). This lecture is just confirming explicitly: those are for fine-tuning work, not for the kind of application-level LLM testing this course focuses on.*

### The metrics this course actually cares about
- **Answer Relevancy** — does the output address the given input informatively and concisely? (Already named in Section 1.5; will get its own code-based deep dive soon.)
- **Prompt Alignment** — does the output actually follow the instructions given in the prompt template? (A newly named metric here — distinct from just "is the answer relevant," this checks whether the model *obeyed the instructions themselves*, e.g. format, constraints, or structure requested in the prompt.)
- **Correctness** — is the output actually correct.
- **Hallucination** — does the output contain fake/made-up information, or is it accurate?
- **Contextual Relevancy, Contextual Recall** — already covered in Section 1.5's RAG-metrics breakdown.

*In plain terms: "Prompt Alignment" vs. "Answer Relevancy" is a subtle but useful distinction — Relevancy asks "is this a good, on-topic answer," while Alignment asks "did it actually follow the specific instructions I gave it" (e.g. Course 1's Section 4.4 example of asking for "just the code block, no extra text" — a good, correct answer that ignores that formatting instruction would fail Prompt Alignment even while passing Answer Relevancy).*

### What's next
The next lecture returns to **LLM-as-a-judge** (first introduced in Section 1.3) with more depth on how it makes evaluating against metrics like these practical.

---

## Section 3.3 — LLM as a Judge, in Depth

This lecture is the conceptual anchor for the entire rest of this section: **almost every metric this course is about to write code for actually runs on "LLM as a judge" under the hood.**

### The mechanism
An LLM is used to assess the output of another LLM-based application — a chatbot, Q&A system, AI agent, or RAG system, doesn't matter which. A common real-world pattern: use a *more capable* model as the judge to evaluate the output of an application built on a *smaller* one (e.g. using DeepSeek to judge output produced by a Qwen 2.5-based app). The judge model is given a specific prompt asking it to rate generated content against predefined criteria — effectively acting as an autonomous evaluator, with no human needed to review each output.

### Why this approach wins
1. **Cost** — avoids the high cost of having humans manually review every LLM output.
2. **Speed and scale** — enables rapid, consistent, scalable evaluation, especially for outputs too large for a person to realistically review one by one.
3. **Quality** — G-Eval (an LLM-as-judge-based metric) is explicitly said to outperform the statistical tools from Section 3.2 (BLEU, ROUGE, METEOR) at actually judging output quality.

*In plain terms: this directly answers a natural question raised back in Section 1.3 — LLM-as-judge isn't just "the lazy middle option" between human grading and code-based grading, it's presented here as genuinely *more accurate* than the older statistical approach, on top of being cheaper and faster than human review.*

### The big reveal: both DeepEval and RAGAS run on this
Nearly every metric already covered in this course is, under the hood, implemented via LLM-as-a-judge in both tools:
- **DeepEval** — uses **G-Eval** as its general-purpose judge-based metric; and for RAG metrics (answer relevancy, faithfulness, contextual relevancy, contextual precision, contextual recall) and agentic metrics (task completion, tool correctness), all of it runs through an LLM acting as judge. Same story for hallucination and bias detection.
- **RAGAS** — the exact same pattern: answer relevancy, faithfulness, contextual relevancy, toxicity detection, bias detection — all LLM-as-judge based.

*In plain terms: this is the thread tying together nearly everything covered so far in this course — Section 1.3's metric list, Section 1.5's deep dive (answer relevancy, contextual precision/relevancy, tool selection, bias detection, function accuracy), and Section 3.2's "metrics this course cares about" — every one of those, once real code gets written, will turn out to be "ask a judge LLM to score this," not a hand-written scoring formula. Worth keeping in mind going forward: whenever the DeepEval/RAGAS code calls a metric by name, there's an LLM quietly making that judgment call behind the scenes — which also means the judge LLM's own reliability/quality matters for how trustworthy the evaluation result actually is.*

### What's next
Starting the next lecture, the course begins working through each evaluation metric one at a time, actually writing the code — applying everything covered theoretically across this section so far.

---

## Section 3.4 — First DeepEval Code: Answer Relevancy, Using an OpenAI Key

The first real hands-on DeepEval code. Even though this course is generally about local LLMs, the instructor deliberately starts with an **OpenAI API key** first — because in many real companies, teams use a paid OpenAI key rather than a local model, so it's worth seeing both ways.

### Setting up the OpenAI key
Two ways shown:
1. **Export it directly in the terminal:** get the key from platform.openai.com (login → Settings → API Keys → create/copy a secret key), then `export OPENAI_API_KEY=<key>`.
2. **Use a `.env` file instead:** create a `.env` file containing `OPENAI_API_KEY=<key>`, then in code, use `python-dotenv`'s `load_dotenv()` to load it in.

*In plain terms: this repo already follows exactly the second pattern — `.env` (gitignored) already holds keys like `ANTHROPIC_API_KEY`, and `python-dotenv` is already installed and used the same way in `browser_use_basic.py`.*

### The first DeepEval test — Answer Relevancy
The test builds an `LLMTestCase` with three pieces:
- **`input`** — "Who is the current president of the United States of America?"
- **`actual_output`** — the response being evaluated
- **`retrieval_context`** — "Joe Biden serves as the current president of America" (used here as the test's ground truth for this demo, regardless of real-world accuracy)

Then it measures the **Answer Relevancy** metric against those three pieces.

**First run:** `actual_output` set to Joe Biden (matching the given context) → relevancy score comes back **1.0** (pass). Confirmed working both inside the notebook and as a standalone `test.py` run from the terminal (`python3 test.py`), visibly calling GPT-4 behind the scenes to do the judging.

**Second run:** `actual_output` changed to "In 2025, the president of the United States is Donald Trump" → the test **fails**, score **0.0** — because that answer doesn't align with the `retrieval_context` given in the test case.

*In plain terms — the single most important thing to take from this demo: Answer Relevancy here is checking whether the output aligns with the **context provided in the test case**, not whether it's factually true in the real world. Joe Biden isn't marked "correct" because he's actually the real president — he's correct *because that's what the test case's `retrieval_context` says*. This is exactly Section 1.3's abstract "golden data" idea, now seen as a real, literal field (`retrieval_context`) in DeepEval's actual test case API — the ground truth is whatever you feed the test, and the metric checks alignment against that, not against the real world.*

### What's next
This lecture was just a first working example to prove the pipeline runs end-to-end; the next lecture goes back and explains the actual code (the `LLMTestCase` structure, how metrics get measured) in proper detail.

---

## Section 3.5 — Contextual Precision, Full Code Walkthrough, and a Key Lesson: Different Metrics Need Different Fields

### A glimpse of how many metrics DeepEval actually has
Typing `deepeval.metrics.` and letting autocomplete list options reveals far more than just Answer Relevancy — Image Editing metrics, Knowledge Retention, Conversation Relevancy, Multimodal Faithfulness, Conversational G-Eval, and many more. The course won't dive into all of them immediately — just building up one at a time, starting simple.

### Writing a Contextual Precision test, step by step
1. **Imports:** `from deepeval.test_case import LLMTestCase` and `from deepeval.metrics import ContextualPrecisionMetric` — same pattern as any Python library import (compared here to `using` in C# or `import` in Java/JavaScript).
2. **Instantiate the metric:** `contextual_precision_metric = ContextualPrecisionMetric()`.
3. **Build the test case:** `LLMTestCase(input=..., actual_output=..., retrieval_context=...)`.
   - `input`: "Who is the current president of USA in 2024?"
   - `actual_output`: "Donald Trump"
   - `retrieval_context`: "Donald Trump serves as the current president of America" (deliberately made to *match* this time, unlike Section 3.4's mismatched Biden/Trump example)
4. **Measure it:** `contextual_precision_metric.measure(test_case=test_case)` (there's also an async `a_measure()`, not used here).
5. **Read the results:** `.score`, `.success`, `.score_breakdown` (breakdown comes back `None` here since there's only a single score to report).

### `LLMTestCase`'s full set of parameters
Hovering over `LLMTestCase` reveals it accepts far more than the three fields used so far: `input`, `actual_output`, `expected_output`, `context`/`retrieval_context`, additional metadata, comments, **`tools_called`**, **`expected_tools`**, `reasoning`, `name`, and more.

*In plain terms: this is Section 1.3's abstract test-case shape (input, golden data, model output, tool output, score) now shown as the real, concrete parameter list of an actual class — and it directly explains where Section 1.5's agentic metrics come from: `tools_called` vs. `expected_tools` is precisely what Tool Selection Accuracy and Function/Argument Accuracy compare against, as real fields on the same test case object used for every other metric.*

*Also worth remembering: these are hardcoded placeholder values for the demo. In a real pipeline, `actual_output` would come from your actual LLM/agent/RAG system's live response, and `retrieval_context` would come from wherever that system actually retrieved its context from — a vector database for a RAG system (this repo's own `rag_app.py` is exactly that kind of pipeline), an agent's tool-call results for an AI agent, or the LLM's own response for a plain model.*

### The key lesson: a missing required field fails loudly, not silently
Running the test *without* `expected_output` fails immediately with a clear error: **"Missing test case parameter... Expected output cannot be None for ContextualPrecisionMetric."** Unlike Section 3.4's Answer Relevancy metric (which only needed input/actual_output/retrieval_context), **Contextual Precision additionally requires `expected_output`** to have anything to measure precision against.

Adding `expected_output = "Donald Trump is the current president of USA"` and re-running fixes it: `score = 1.0`, `success = True`, `score_breakdown = None`.

*In plain terms: the practical takeaway here matters more than this specific example — **every metric has its own required fields**, and DeepEval fails fast and tells you exactly what's missing rather than silently returning a meaningless score. Good habit going forward: check what a given metric actually needs before assuming the same three fields work everywhere.*

### Not yet recorded anywhere
This test ran entirely locally — nothing was pushed to DeepEval's cloud dashboard, **Confident AI** (previewed briefly back in Course 2, Section 1.6, as confident-ai.com). Recording results there for historical tracking/dashboards is what the next lecture covers.

---

## Section 3.6 — From `.measure()` to `evaluate()`: Pushing Results to Confident AI

### A disclaimer worth remembering
The instructor notes this section (and a couple more) got **re-recorded** because DeepEval shipped major breaking changes (moving from roughly v2 to v3.35 at recording time) — new UI, and two entirely new test case types added mid-course. Worth keeping in mind generally: DeepEval is a fast-moving library, and code/APIs from any tutorial (this course included) can drift from whatever version is actually installed.

*In plain terms — this isn't abstract: exactly this kind of version drift is what caused the debugging earlier in this session's own notebook work. This repo's `myenv` venv has DeepEval 4.2.2 (newer even than this lecture's 3.35), and its `OllamaModel`/config-routing behaved differently from what an older version would expect — the same "breaking changes across versions" pattern flagged here, just experienced firsthand.*

### `.measure()` vs. `evaluate()`
Everything done so far (Sections 3.4–3.5, and the two answer-relevancy/contextual-precision runs earlier in this session) used a metric's `.measure()` method directly — DeepEval calls this the **"standalone"** way, because it runs entirely locally and never pushes anything to DeepEval's cloud dashboard, **Confident AI** (first mentioned in Section 1.6).

The `evaluate()` function instead:
- Sends results to the Confident AI portal.
- Returns far richer reporting than `.measure()`'s plain score/success output.

### The code change
Minimal — swap the metric's own `.measure(test_case=...)` call for DeepEval's top-level `evaluate()` function:
```python
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

test_case = LLMTestCase(
    input="Who is the current president of the United States of America?",
    actual_output="Joe Biden",
    retrieval_context=["Joe Biden serves as the current president of America"]
)

evaluate(test_cases=[test_case], metrics=[AnswerRelevancyMetric()])
```
Note both `test_cases` and `metrics` are **lists (plural)** — `evaluate()` is built to run *multiple* test cases against *multiple* metrics in one call, not just one at a time.

### New test case types (added since the original recording)
Beyond `LLMTestCase` (used throughout so far), two more now exist:
- **`ConversationalTestCase`** — for testing chatbots across a multi-turn conversation, not just one input/output pair.
- **`MLLMTestCase`** — for multimodal LLMs (image/video/audio capability, not just text).

*In plain terms — MLLM ties directly back to Course 1's Section 3.3 (Llama 3.2's multimodal 11B/90B models): this is the DeepEval-side test case for evaluating exactly that kind of model, once it needs to handle more than plain text.*

### What shows up in the Confident AI portal
Running the same Answer Relevancy test through `evaluate()` instead of `.measure()` produces, in the dashboard:
- An **eval insight** panel suggesting next actions (e.g. logging hyperparameters).
- A model overview of the test run.
- The full test case (input, actual output, retrieval context) laid out clearly.
- The **score and threshold** (default threshold shown: 0.5) — success/failure is threshold-based, not just "score exists."
- A **natural-language explanation** of *why* that score was given (e.g. "the answer was fully relevant and directly addressed the question, with no irrelevant information").
- **Run duration** and which model did the judging (GPT-4.1 at recording time).
- **Cost** — the actual dollar amount spent on that evaluation's API calls.
- A historical view — each run becomes one point that builds into a trend/graph over time as more evaluations accumulate.

*In plain terms: the cost-tracking feature is a direct, concrete payoff of Section 1.3's "cost savings" benefit and Section 2.1's "local models save money" point — seeing an actual dollar figure per evaluation run is what makes it obvious just how quickly LLM-as-judge evaluation costs can add up at scale with a paid API, and why a local judge model (as already set up and working in this session, via Ollama) avoids that cost entirely.*

*Also worth noting: this repo's `.env.local` already holds a `CONFIDENT_API_KEY` (found and gitignored earlier in this session) — meaning Confident AI is already set up and ready to actually try hands-on here, if wanted.*

---

## Section 3.7 — Multiple Test Cases, A/B Comparison, and a Genuinely Important Nuance About Answer Relevancy

### Running two test cases at once
A second `LLMTestCase` gets added — `input="Who built the GPT models?"`, `actual_output="OpenAI"`, `retrieval_context=["OpenAI built the GPT models"]` — and both test cases are passed into the same `evaluate(test_cases=[test_case_1, test_case_2], metrics=[...])` call. (The lecture flags again that hardcoding `actual_output` is only for learning the mechanics — in a real pipeline it would come from an actual LLM/RAG/agent response, as already noted in Section 3.5.)

### The Compare Test Results page
Confident AI's dashboard includes a **Compare Test Results** view — an A/B-style comparison between different evaluation runs over time. Comparing a run with only 1 test case against one with 2 test cases isn't a clean apples-to-apples comparison, so the lecture deliberately sets up a fairer side-by-side next.

### A revealing experiment: does Answer Relevancy really only check the given context?
This is the most important part of the lecture, and it **refines** something stated back in Section 3.4:

- Test: `input="Who built the GPT model?"`, `actual_output="OpenAI"` — but this time `expected_output` and `retrieval_context` were deliberately set to **wrong/misleading** values: `"Cloud Anthropic built the GPT model"`. Result: **the test still passes**, Answer Relevancy stays high.
- Then the `input` was changed to `"Who built the Claude model?"` (still `actual_output="OpenAI"`). Result: **the test now fails**, score drops to 0.

*In plain terms — why this matters: Section 3.4 said Answer Relevancy checks alignment with "the context provided in the test case," not real-world truth. This lecture shows that's not the whole picture — the **judge LLM's own background knowledge** also plays a real role. In the first case, even though the fed-in context/expected-output was wrong, the judge model (GPT-4.1) "knew" from its own training that OpenAI actually built GPT, and scored the answer as relevant anyway. Only once the *question itself* changed to something where "OpenAI" is genuinely the wrong answer (Claude was built by Anthropic, not OpenAI) did the judge correctly fail it — using its own knowledge, not just the fabricated context it was handed. **The honest takeaway: for well-known facts, a capable judge LLM can catch a wrong answer even if the test case's own supplied context tries to mislead it — but this isn't something to rely on. It's a property of how good/knowledgeable the specific judge model happens to be for that particular fact, not a guarantee of the metric itself.** For genuinely obscure or company-specific facts the judge model has no training knowledge of, the metric would likely lean on the given context, closer to the simpler framing from Section 3.4.*

### Comparison only works with `evaluate()`, not `.measure()`
The A/B comparison view visibly highlights the change between runs (a metric flipping from a passing 1 down to a failing 0) — and this comparison capability is exclusive to the `evaluate()` + Confident AI workflow. The standalone `.measure()` method (Sections 3.4–3.5) has no equivalent — no history, no run-to-run comparison, since nothing gets recorded anywhere.

### What's next: handling many test cases (datasets)
Two test cases hardcoded inline clearly doesn't scale to real LLM application testing, which needs many. The next lecture covers building an actual **dataset** of test cases, rather than writing each one by hand inline.

---

## Section 3.8 — Goldens and Datasets: Separating the "Truth Set" from the Test Run

### What a "golden" actually is
In DeepEval, an evaluation **dataset** is a collection of **goldens**. A golden is a *precursor* to a test case — at evaluation time, every golden in a dataset gets converted into an actual `LLMTestCase` before the evaluation runs against it.

### Why not just use test cases directly?
The core distinction: a **golden** holds information that should stay fixed/permanent — a genuine "ground truth" record, meant to be stored safely once and reused. A **test case** is comparatively volatile — its `actual_output` in particular changes every time the real LLM/RAG/chatbot it's testing produces a fresh response.

*In plain terms — a relatable analogy from ordinary test automation: a golden is like a **test data fixture** (a fixed input + expected value you keep in a file, that shouldn't casually change), while a test case is like **one actual test run/result** built from that fixture at execution time. You keep the fixture stable and trustworthy; the actual execution result is naturally different every time the system under test runs.*

### Building a golden and a dataset in code
New imports: `from deepeval.dataset import EvaluationDataset, Golden`.

```python
golden = Golden(
    input="Who is the current president of the United States of America?",
    expected_output="Joe Biden",
    context=["Joe Biden serves as the current president of America"]
)

dataset = EvaluationDataset()
dataset.add_golden(golden)
```

**One key naming difference to remember:** `LLMTestCase` uses `retrieval_context`, but `Golden` uses just `context` — same underlying idea, different field name.

`Golden` accepts largely the same shape as `LLMTestCase` — optional `actual_output`, `expected_output`, `context`, `tools_called`/`expected_tools`, plus `source_file`, custom column key-values, and `expected_outcomes` (specifically for conversational goldens). `EvaluationDataset` starts empty (`EvaluationDataset()`), and `add_golden()` can add a golden directly from the class, or bulk-import many at once from a **CSV or JSON file** — and can even accept full test cases or conversational goldens directly, not just plain goldens.

*In plain terms: right after adding a golden, the dataset shows **0 test cases** but does hold the golden data — the golden→test-case conversion is a separate step that happens later, at actual evaluation time (covered in the next lecture). This is the concrete, coded version of the "golden data" idea already introduced back in Section 1.3.*

### Another disclaimer about breaking changes
The instructor again flags this specific area (`EvaluationDataset`) as one of the most heavily changed parts of DeepEval since the course was first recorded — enough that students had complained the original lectures felt obsolete, prompting this re-recording.

### What's next
The next lecture picks up from here — actually converting these goldens into test cases and running an evaluation against them.

---

## Section 3.9 — Converting Golden → Test Case, and Two Real Live Bugs

### The conversion code
Picking up from Section 3.8's dataset of goldens, each golden gets turned into a real `LLMTestCase` and added back into the dataset:
```python
for golden in dataset.goldens:
    test_case = LLMTestCase(
        input=golden.input,
        expected_output=golden.expected_output,
        retrieval_context=golden.context,
        actual_output="Joe Biden"  # has to be supplied separately - see below
    )
    dataset.add_test_case(test_case)

evaluate(test_cases=dataset.test_cases, metrics=[AnswerRelevancyMetric()])
```
Note `dataset.test_cases` is used directly as the list passed into `evaluate()` — no need to manually build an array, since the dataset already collects them.

### Bug #1: `dataset.golden` → should be `dataset.goldens`
The first attempt used the singular `golden` and hit an error — the dataset's actual attribute is the **plural** `goldens`. A simple typo, but a good reminder to check the exact API rather than guess from how the class name reads.

### Bug #2: "actual output cannot be None" — and *why* that's expected
The second, more instructive error: `actual_output` was missing. This isn't an oversight to just patch around — it's the **direct, hands-on confirmation of Section 3.8's whole point**: a `Golden` deliberately does *not* carry `actual_output`, because that value is supposed to come from the real system under test (an LLM call, a RAG pipeline, a chatbot, an agent) at evaluation time — not from the static "truth set." Since there's no real application wired up yet in this demo, `actual_output="Joe Biden"` gets hardcoded manually as a stand-in.

*In plain terms: this error is the golden/test-case split actually doing its job — it's forcing you to explicitly decide where the real, live output comes from, rather than silently letting a fixed value pass as if it were a real response.*

### Bug #3 (not named as one, but worth flagging): stale data from re-running cells
Re-running the golden→test-case conversion cell multiple times (while debugging bugs #1 and #2) caused the dataset to accumulate leftover, incomplete test cases from the earlier failed attempts. The fix was re-running the dataset-creation cell from scratch to get a clean dataset before the evaluation would actually pass.

*In plain terms — this maps directly onto Jupyter-notebook debugging in general, not just DeepEval specifically: notebook cells share state across re-runs, so a half-fixed bug can leave stale objects (like a partially-built dataset) sitting around even after the code itself looks correct. This is the exact same category of issue as this session's own earlier DeepEval/Ollama debugging — a kernel restart was needed there too, for a similar reason (stale config not being picked up).*

### The payoff: it works, and shows up on the historical graph
Once fixed, the evaluation runs successfully and pushes to Confident AI — the test case passes. Going back to the evaluation history view (first seen in Section 3.6/3.7), there's a visible **dip** in the trend line from the earlier failed attempts during debugging — a real, honest record of the mistakes made along the way, not just the final clean result.

---

## Section 3.10 — Scaling Up: Pushing a Golden Dataset to Confident AI for Reuse

### The real-world problem
One hardcoded golden is fine for learning, but real projects need thousands of them — and the same golden data often needs to be reused across *multiple different evaluations, or even multiple projects/teams*. Storing them as a big local JSON blob inside one test file doesn't solve that reuse problem; what's needed is one **central place** to store goldens.

### Confident AI's Datasets feature
The Confident AI portal has a dedicated **Datasets** tab, supporting both single-turn (plain Q&A-style) and multi-turn (conversational) datasets — goldens can be added there directly through the UI, tagged, assigned to teams, and filtered by properties like golden ID or a "finalized" tag.

*Practical note: the free tier only allows one dataset at a time — the instructor deletes a manually-created UI dataset here specifically to instead demonstrate the code-driven approach below, which is the more realistic workflow anyway.*

### Building goldens from a plain data array, in a loop
Instead of one hardcoded `Golden`, this starts from a plain Python list — simulating data handed over by a data engineer:
```python
test_data = [
    {"input": "Who is the current president of America?", "expected_output": "Joe Biden"},
    {"input": "Who introduced the GPT model?", "expected_output": "OpenAI"}
]

goldens = []
for data in test_data:
    golden = Golden(input=data["input"], expected_output=data["expected_output"])
    goldens.append(golden)
```

### Building the dataset — and a shorthand
Rather than calling `add_golden()` once per item (Section 3.8's approach), `EvaluationDataset` can take the whole `goldens` list directly:
```python
new_dataset = EvaluationDataset(goldens=goldens)
```

### Pushing it to Confident AI
```python
new_dataset.push(alias="test golden dataset", overwrite=True)
```
- `alias` — the name the dataset gets in the Confident AI portal.
- `overwrite` (defaults to `False`) — set to `True` so re-running this push **updates** the existing dataset instead of duplicating every record each time the script runs again.

Running this opens the Confident AI portal directly, showing both goldens now stored centrally — the president question paired with "Joe Biden," and the GPT question paired with "OpenAI."

*In plain terms: `overwrite=True` here is the same idempotency concern that matters in any real pipeline or CI script — without it, re-running the same push repeatedly would just keep piling up duplicate records instead of cleanly updating the same dataset. And this repo already has a `CONFIDENT_API_KEY` sitting in `.env.local` (found and gitignored earlier in this session), so this exact push-to-cloud workflow is genuinely ready to try hands-on if wanted.*

### What's next
The next lecture covers the other half of this workflow: **pulling** a dataset back down from Confident AI (instead of rebuilding it from scratch every time) to actually run an evaluation against it.

---

## Section 3.11 — Pulling a Dataset Back, a Mock App, and a Surprising Answer Relevancy Result

### Pulling the dataset back down
To actually round-trip the workflow, the dataset gets pulled into a **fresh variable** (not the one used to push it, which already holds the data locally and would make the pull pointless to demonstrate):
```python
cloud_dataset = EvaluationDataset()
cloud_dataset.pull(alias="test golden dataset")
```
After this, `cloud_dataset.goldens` holds the two records fetched live from Confident AI.

### Building a tiny mock app (since two goldens now need two different answers)
Section 3.9's approach of hardcoding one `actual_output = "Joe Biden"` doesn't work anymore — the dataset now has two different questions needing two different correct answers. A minimal stand-in "application" is written instead:
```python
def mock_llm_app(input):
    if input == 1:
        return "Joe Biden"
    elif input == 2:
        return "OpenAI"
```
A simple counter (starting at 1, incremented each loop iteration) drives which branch fires for each golden as the loop converts goldens into test cases, using this mock app's return value as `actual_output`.

*In plain terms: this is a deliberately bare-bones stand-in for what would, in a real system, be an actual call to your LLM/RAG pipeline/agent — the same idea flagged back in Section 3.5 about where `actual_output` is really supposed to come from. This repo's own `rag_app.py`/`shoe_store_agent.py` are exactly the kind of real application that would eventually replace a mock function like this.*

### The real payoff: editing ground truth centrally, without touching code
With test cases built and `evaluate(test_cases=cloud_dataset.test_cases, metrics=[AnswerRelevancyMetric()])` passing, the golden's `expected_output` for the president question gets edited **directly in the Confident AI web UI** — changed from "Joe Biden" to "Donald Trump" — with zero code changes.

**Expectation:** re-running the exact same evaluation code should now fail, since the mock app still returns "Joe Biden" while the golden now expects "Donald Trump."

**What actually happened: the test still passed.**

### Why — a genuinely important nuance about Answer Relevancy
The instructor's explanation: this test case was never given a `retrieval_context`. **Answer Relevancy doesn't actually compare `actual_output` against `expected_output` at all** — it only checks whether the actual output is a relevant answer to the *input question itself*. "Joe Biden" is still a perfectly relevant-sounding answer to "who is the president," regardless of what the golden's `expected_output` field currently says — so the metric has no reason to fail it.

*In plain terms — this refines something already flagged in Section 3.7: there, the judge model's own knowledge was shown to matter alongside supplied context. This goes a step further — for Answer Relevancy specifically, `expected_output` isn't even part of what the metric checks by default, when there's no `retrieval_context` tying things together. That kind of "does the actual output match the expected/golden answer" comparison belongs to other metrics — Contextual Precision (Section 3.5) explicitly required `expected_output` to function at all, which is a strong hint it's actually being used there for comparison, unlike here. The lecture defers a full explanation to the upcoming RAG-focused sections, where `retrieval_context` gets used properly.*

### The bigger picture
Despite this particular metric quirk, the workflow itself is the real point: centralizing goldens in Confident AI means **non-engineers on a team can edit ground-truth data directly through a UI**, and the exact same evaluation code automatically picks up whatever the current cloud data says — no code redeploy needed just to update test expectations.

---

## Section 3.12 — Course Errata: `deepeval set-ollama` Syntax Changed

A short instructor note posted ahead of the next lecture (which covers using local models like DeepSeek R1 as the evaluation judge instead of OpenAI): the CLI command shown in the recorded video,
```
!deepeval set-ollama deepseek-r1:8b
```
breaks on current DeepEval v4.x. The fix is one extra flag:
```
!deepeval set-ollama --model deepseek-r1:8b
```
The instructor already patched this in the course's Section 3 source code, but flags it explicitly since — as already disclaimed several times across this section (3.6, 3.8) — DeepEval keeps shipping breaking changes, and more are expected as the course continues.

*In plain terms: this is the exact same command already used successfully, hands-on, earlier in this session — `deepeval set-ollama --model=llama3.2:1b` (with an `=` instead of a space) worked correctly when fixing the notebook's OpenAI rate-limit issue. Both the `--model X` and `--model=X` forms are standard for this kind of CLI flag, so either works — this errata is just confirming the flag needs to be named explicitly (`--model`), not passed as a bare positional argument like the original recording showed.*

---

## Section 3.13 — Switching the Evaluation Judge from OpenAI to a Local Ollama Model

### The command
Inside a notebook cell, prefixing a shell command with `!` runs it directly (standard Jupyter syntax — not Python code):
```
!deepeval set-ollama --model deepseek-r1:8b
```
The instructor picks **DeepSeek R1 8B** specifically for being lighter/more performant on his machine, after considering alternatives — including **gpt-oss** (OpenAI's own open-weight model family, offered in a 20B-parameter size among others, also pullable via Ollama).

### What this actually changes, under the hood
Running the command updates the same `.deepeval/.deepeval` config file already fixed by hand earlier in this session, setting:
- `LOCAL_MODEL_NAME` → `deepseek-r1:8b`
- `LOCAL_MODEL_BASE_URL` → the local Ollama endpoint
- `USE_LOCAL_MODEL` → `YES`
- `USE_AZURE_OPENAI` → `No`
- `LOCAL_MODEL_API_KEY` → `ollama`

(The same config folder separately holds the Confident AI API key/config, from Section 1.6/3.10's Confident AI setup.)

*In plain terms — this closes the loop on the debugging done earlier in this very session: fixing the notebook's OpenAI `RateLimitError` involved manually working out and setting almost this exact same set of keys (`LOCAL_MODEL_NAME`, `LOCAL_MODEL_BASE_URL`, `USE_LOCAL_MODEL`, `LOCAL_MODEL_API_KEY`) by hand, one at a time, through trial and error. This lecture is the "official" version of that same fix — confirming the manual config edits done earlier were exactly right, just arrived at by reverse-engineering rather than by running the documented CLI command.*

### What's next
Once this is set, the next lecture actually runs an evaluation using this local model as the judge, instead of OpenAI.

---

## Section 3.14 — Running Local, Hitting a Different Kind of Quota, and Closing Out DeepEval Basics

### Same code, zero cost this time
With the local model configured (Section 3.13), the *exact same* existing `evaluate()` code runs unchanged — no code edits needed — but now judges with DeepSeek R1 8B via Ollama instead of GPT-4.1. Cost for this run: nothing.

### A different free-tier limit shows up: Confident AI's own run cap
Running it hits a message: **"only ten runs are allowed every week. Upgrade to our starter plan to unlock unlimited evaluations."** This isn't a cloud-LLM-API cost limit (that's already zero with a local judge) — it's **Confident AI's own dashboard quota**, capping free-tier accounts at 10 evaluation runs per week, regardless of which model is doing the judging.

**Workaround shown:** manually delete old/unneeded runs from the Confident AI history to free up quota within the weekly cap — the instructor deletes enough runs to get back down with a few remaining for the rest of the demo, rather than upgrading to a paid plan.

*In plain terms — this is a genuinely useful distinction to keep straight, since it's easy to assume "local model = fully free, no limits." There are actually **two separate quota systems** in play here: (1) the LLM provider's own usage limits (OpenAI's paid API, or a local model's total freedom from that), and (2) Confident AI's own reporting/dashboard quota, which caps free-tier *runs*, independent of what model did the judging. Switching to a local judge solves problem #1 but does nothing for problem #2 — this repo's own `.env.local` already holds a `CONFIDENT_API_KEY`, so this exact 10-runs/week ceiling would apply if evaluate() calls get run from here too.*

### Confirming it worked
After freeing up quota, the run succeeds, and the dashboard's "View full details" panel now shows the evaluation model as **DeepSeek R1 8B (Ollama)** instead of GPT — everything else about the report looks and works the same as the OpenAI-judged runs before it.

### Going forward: mostly local, but not dogmatically so
From here, the course will lean on the local LLM as judge by default — but explicitly *not* exclusively. The instructor flags that for RAG-related evaluation specifically, a local model might not be capable enough, and the course will "hop" back to a cloud model (GPT) when that's genuinely needed.

*In plain terms: this is a balanced, practical stance rather than an absolutist "always local" rule — pick the judge model based on whether the task actually needs the extra capability, the same "smaller model = less reliable for harder tasks" trade-off already seen concretely in Sections 2.3 (Qwen 1.8B vs. DeepSeek R1 8B on Selenium code) and this session's own live debugging (Contextual Precision failing on `llama3.2:1b` with an "invalid JSON" error until a more capable local model was used).*

### Section wrap-up
This closes out the DeepEval basics section — everything needed to get started (metrics, `.measure()` vs. `evaluate()`, goldens/datasets, pushing/pulling from Confident AI, local vs. cloud judges) has now been covered. The next section moves from hardcoded/mock outputs to evaluating a **real** LLM application with DeepEval.

---

*(Next section's notes get appended below as more transcripts/screenshots come in.)*
