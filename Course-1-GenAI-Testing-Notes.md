# Course 1 — Generative AI in Software Automation Testing

Udemy: https://www.udemy.com/course/generative-ai-in-software-automation-testing/

Notes captured from lecture slide screenshots, section by section, lecture by lecture.

---

## Section 1 — Introduction to the Course and Gen AI

### What is Generative AI
Generative AI refers to a class of **artificial intelligence** models designed to generate new, original content or data based on the input it receives. It can create text, images, music, and even **code**, which makes it powerful across various fields.

*In plain terms: it's AI that makes new stuff (not just retrieves existing stuff), and one of the things it can make is working code.*

### Section framing questions
- How will Gen AI help me in software testing?
- How does Gen AI generate manual test cases and automation test code?

### Various models of Gen AI
Generative AI branches into three main model families:

- **LLMs** (Large Language Models) → Text Generation, Code Generation, Chatbots
- **GANs** (Generative Adversarial Networks) → Image Generation, Deepfakes, Art Creation
- **VAEs** (Variational Autoencoders) → Data Compression, Synthetic Data Generation

*In plain terms: LLMs are the "text and code" branch (the one this course/roadmap focuses on); GANs are the "realistic image/art" branch; VAEs are more about compressing and synthesizing data.*

### Large Language Model (LLM)
- LLMs generate software code.
- They can understand and generate software code across various programming languages. This happens because LLMs are an **application** of Gen AI.
- LLMs branch into: Text Generation, Code Generation, Chatbots.

### How an LLM actually processes text (pipeline)
```
Data Source
   |
   v
Preprocessing Steps (Preprocessing <-> Tokenization loop)
   |
   v
Tokens Sequence
   |
   v
LLM Neural Network
   |
   v
Training Phase
   |
   v
Trained Neural Network
   |
   v
Text Generation or Prediction
```
*In plain terms: raw data gets cleaned and broken into tokens (matches the "tokens" concept from earlier in the roadmap), fed into a neural network, trained, and the trained network is what actually generates or predicts text.*

### Popular LLMs in the market today
1. GPT 4.0 / 4.0 Turbo — OpenAI
2. LLaMA — Meta
3. Gemini — Google
4. Claude 3.5 Sonnet — Anthropic
5. Mistral — Mistral AI

*Note: course material here reflects the LLM lineup as of when it was recorded — newer models (e.g. Claude 5 family, GPT-5.x, Gemini 3, Llama 4) have released since. Good to keep this list as a historical snapshot, not the current state of the art.*

### Applications of Gen AI in Software Testing
- **Manual Testing**
  - Manual test case generation
  - Manual test data mapping
- **Automated Software Testing and code generation**
  - AI code suggestion
  - AI code correction and code coverage
- **Test Data Generation**
- **Automated bug tracking**

### A few more concrete use cases
- **Use case #1:** Given a big Swagger document with all API definitions, Gen AI can write the API tests (e.g. with Postman or RestSharp) for you.
- **Use case #2:** For a fragile UI application, Gen AI can query the page and get locators matching the current UI before a test starts running — helping automated UI tests survive small UI changes.
- **Use case #3:** Generate test data for complex objects in a more realistic fashion (not just random/dummy values).

---

## Section 2 — Generative AI and LLMs in Practice (2.1)

### Generative AI (recap)
Generative AI refers to a class of **artificial intelligence** models designed to generate new, original content or data based on the input it receives. It can create text, images, music, and even **code**, which makes it powerful across various fields.

*In plain terms: same definition the course opened with — AI that makes new stuff, and code is one of the things it can make.*

### Large Language Model — how it fits into Gen AI
- LLMs generate software code.
- They can understand and generate software code across various programming languages. This happens because LLMs are an **application** of Gen AI.
- LLMs branch into: Text Generation, Code Generation, Chatbots.

*In plain terms: repeats the Section 1 point — LLMs are one branch of Gen AI, and code generation is just one of the things that branch can do.*

### What's happening inside an LLM — attention visualization
The slide shows a BertViz-style attention visualization: a grid of **Layers** (rows) × **Heads** (columns), where each small panel plots lines connecting words in a sentence pair (e.g. "the cat sat on the mat" / "the cat lay on the rug") to each other. Hovering a specific line (e.g. Layer 2, Head 4) highlights exactly which word is "paying attention" to which other word.

*In plain terms: this is a peek under the hood at "attention" — the mechanism an LLM uses to figure out which words in a sentence relate to each other. Each layer and "head" learns to focus on different word relationships (e.g. linking "cat" to "sat" or "lay"). This is part of the Text Generation/Prediction step from the Section 1 pipeline diagram.*

### Are these LLMs free to use?
Most LLMs offer free tiers:
1. **ChatGPT** — free model is GPT-4o mini (and GPT-4o itself for a limited number of queries)
2. **Gemini** — has a free model, plus an Advanced model for paid users
3. **Claude** — free tier gets limited queries on their advanced model

*In plain terms: all three let you try them for free, but the free tier either gives you a smaller/weaker model or caps how many times you can use the best one.*

---

## Section 2.2 — Hands-on: Asking ChatGPT to Write Test Code, and Discovering AI Testing Tools

This part of the section isn't a slide — it's a live demo of prompting ChatGPT directly, tying back to the "Automated Software Testing and code generation" use case from Section 1.

### Demo 1: Generating a Selenium test with ChatGPT
The instructor asks ChatGPT for a simple Selenium C# .NET test that logs into `http://eaapp.somee.com`. ChatGPT comes back with a plan plus a starting code skeleton:
- **Plan:** open the site → click the Login link → enter username/password → submit the form → assert the login succeeded
- **Code skeleton:** an NUnit test project referencing `OpenQA.Selenium` + `OpenQA.Selenium.Chrome`, with a `LoginTest` class holding an `IWebDriver` field and a `[SetUp]` method to prep the browser before each test

*In plain terms: eaapp.somee.com is just a small practice "dummy app" QA folks use to rehearse automation on — it's not a real product. The point of the demo isn't the app, it's that you can describe a test in plain English and the LLM hands back real, runnable scaffolding (the right imports, class structure, setup method) instead of you typing it from memory. That's Section 1's "AI code suggestion" idea, now seen actually happening.*

*Touchpoint: NUnit is a C# test framework — think of it as the C# equivalent of JUnit (Java) or pytest (Python); it's what actually runs the test and reports pass/fail. `[SetUp]` is an NUnit attribute meaning "run this before every single test" (here, to open the browser). None of that scaffolding is new or AI-specific — Gen AI is just writing the boilerplate you'd otherwise write yourself.*

### Demo 2: Asking ChatGPT for a list of AI-powered testing tools
Second prompt: get a curated list of AI-powered tools used across software testing. ChatGPT groups its answer by category, starting with **AI tools for functional & visual testing**:

1. **Testim** — end-to-end tests that use "smart locators" so they survive small UI changes; hooks into CI/CD.
2. **Applitools** — specializes in *visual* AI: compares screenshots across browsers/devices to catch visual bugs (e.g. a button that's suddenly misaligned), layered on top of Selenium/Playwright.
3. **Mabl** — cloud-based; focuses on "self-healing" tests plus spotting anomalies during CI/CD runs.
4. **Functionize** — you describe tests in plain English (NLP-based), and ML handles maintaining them and even predicting what to test next.
5. **Autify** — a low-code recorder (record your clicks) combined with AI-based locator healing, for web and mobile.
6. **TestCraft** — codeless, visual test builder for web UI that adapts automatically as the UI evolves.
7. **Testsigma** — open-source, low-code, NLP-driven; covers web, mobile, and API testing with auto-healing.
8. **AccelQ** — cloud-based, NLP-driven end-to-end testing aimed at agile teams.
9. **Katalon Studio / Platform** — listed next, cut off in the screenshot (the list kept going).

*In plain terms: almost every tool here is solving the same underlying pain — "my automated tests keep breaking because the UI changed slightly." Most attack it with some flavor of "the AI figures out what element you meant to click even though its exact ID changed" (self-healing / smart locators), or by comparing visuals instead of relying on brittle selectors. A second cluster (Functionize, Testsigma, AccelQ) layers NLP on top so you can write tests in plain English instead of code.*

*Touchpoint: "self-healing" and "smart locators" are the recurring buzzwords in this whole space — worth remembering, since they map directly to Section 1's use case #2 (fragile UI tests surviving small changes). "CI/CD integration" just means the tool can run automatically as part of your build/deploy pipeline, not only by hand.*

---

## Section 2.3 — Using ChatGPT's Deep Research to Compare Playwright vs Selenium

### Demo: asking for a tool comparison, and getting clarifying questions back
The instructor asks ChatGPT to compare Playwright and Selenium's features and how companies use them. Instead of answering immediately, ChatGPT asks back for scope first:
1. Compare the two tools specifically, or something broader?
2. A technical comparison (speed, API usability, browser support) vs. real-world company use cases vs. both?
3. Any specific industry or company size in mind (startups vs. enterprise)?

The instructor answers: both tools, both angles (technical *and* real-world usage), and specifically enterprise companies.

*In plain terms: this is "Deep Research" mode — before writing anything, the AI asks what you actually care about, the way a good analyst clarifies scope before drafting a report. It's a different pattern from a normal chat reply: instead of you having to write a longer, more detailed prompt up front, the AI narrows things down for you by asking.*

*Touchpoint: Playwright (built by Microsoft) and Selenium (the older, long-standing industry-standard framework) both do the same core job — driving a real browser from code (clicking, typing, reading the page) — which is exactly what's needed for automated web/UI testing. They compete for the same role on a test automation team.*

### The report ChatGPT builds
Once the scope is confirmed, ChatGPT doesn't just reply in a paragraph — a live "Organizing report sections" panel appears, building out a structured outline before the actual research runs:
- Introduction
- A feature-comparison table
- Deeper sections on: performance, API design, browser support, test-automation capability, programming-language support, CI/CD integration
- Enterprise adoption (how real companies actually use each tool)
- Recommendations at the end

*In plain terms: this is the AI's table of contents before it's actually gone and researched anything — similar to sketching section headers for a test plan or report before filling in the details.*

*Touchpoint: this whole exercise mirrors a real decision automation teams face — "should we build our suite on Selenium or Playwright?" The section headers it picked (CI/CD integration, language support, browser support) are the actual criteria a team would weigh in real life (e.g. Playwright leans on modern async APIs and built-in auto-waiting; Selenium has the widest browser/driver ecosystem and the longest track record). Unlike the 2.2 demo, which used Gen AI as a code generator, this demo shows Gen AI acting as a research assistant for a tooling decision.*

---

## Section 3.1 — Why Local LLMs

### The problem: every prompt leaves your machine
The section opens with a blunt reminder: anything typed into ChatGPT or Claude gets sent off to that company's servers to be processed.

*In plain terms: using these tools over the web means your prompt (and whatever data is inside it) physically travels to OpenAI's or Anthropic's infrastructure, not just "stays in the browser." That's fine for generic questions, but it matters the moment your prompt contains something you shouldn't be sharing outside your company.*

### Why that's a real problem for testers specifically
The slide lists a few concrete situations where sending prompts to the cloud becomes an issue:
- You'd rather run the LLM on your own machine than send anything to the cloud at all.
- Your test data itself is sensitive (real customer data, internal system details, credentials, etc.) — company policy won't allow sending that to a third party, even accidentally, just to get help writing a test.
- You simply use the free tier so much that you hit its daily query cap.
- So — what's the alternative?

*In plain terms: this connects straight back to Section 2.1's "free tiers have limits" note — here the course adds a second, bigger reason beyond quotas: some test data just legally/contractually can't leave the building. If your test fixtures include anything sensitive, pasting them into ChatGPT to "help write a test" is itself a data-handling risk, independent of how good the free tier is.*

### The answer: run the LLM locally
Instead of calling a cloud API, you can download an LLM and run it directly on your own computer, using tools such as:
- **GPT4All**
- **Ollama**

*In plain terms: a "local LLM" is a (usually smaller) version of a language model that runs entirely on your laptop/server — no internet call, no data leaving your machine, no per-query cap from a vendor. Tools like Ollama and GPT4All are basically the easy on-ramp for downloading and running these models yourself, instead of setting up the model infrastructure from scratch. The trade-off (not stated on this slide yet, but worth remembering) is usually less raw capability than the biggest cloud models, in exchange for privacy and no usage limits.*

---

## Section 3.2 — Demo: Installing and Using GPT4All Locally

### Downloading GPT4All
The instructor goes to the GPT4All website, which advertises itself with two taglines: "Privacy first" and "No internet required," and downloads/installs it through a normal setup wizard (a plain "Welcome" install screen, nothing testing-specific).

*In plain terms: this is the direct answer to the problem raised in 3.1 — GPT4All is a free desktop app that lets you run open-source LLMs entirely on your own computer. Installing it is just like installing any other desktop app; no special setup beyond the usual "Next → Next → Finish."*

### What the app looks like once installed
The GPT4All interface looks a lot like ChatGPT's — a chat panel, a list of past chats on the left, and a model picker at the top (the demo shows it switched between models called "Nous Hermes 2 Mistral DPO" and "Llama 3 8B Instruct"). There's also a **LocalDocs** panel on the right, where you can add your own files/folders as a "collection" (the demo shows collections named `gameofthrones` and `my_local_files`) so the model can answer using your own documents.

*In plain terms: the big difference from ChatGPT/Claude isn't the look — it's that you can swap between several different open-source models (each a separate download) instead of being locked into one vendor's model. "Llama 3 8B Instruct" means Meta's Llama 3 model at the 8-billion-parameter size — much smaller than something like GPT-4, which is exactly why it's able to run on a regular laptop instead of a data-center server.*

*Touchpoint: LocalDocs is basically "feed the model your own files so it can answer questions about them" — a simple, built-in version of a technique usually called RAG (Retrieval-Augmented Generation), where the model's answers are grounded in documents you supply rather than only in what it memorized during training. Worth remembering this name, since RAG comes up again later in more depth (see [[project_agentic_qa_learning]] roadmap).*

### Demo: generating a Selenium test locally
With the **Llama 3 8B Instruct** model selected, the instructor asks it (in a chat titled "Selenium WebDriver tests Amazon") to write a Selenium test for searching on Amazon. The local model generates a full Java test class, `AmazonSearchTest.java`, using JUnit + Selenium WebDriver:
- Imports JUnit's `Test` and Selenium's `By`, `WebDriver`, `WebElement`, `ChromeDriver`, `PageFactory`
- Creates the WebDriver and navigates to amazon.com
- Wraps the page in a Page Object class (`AmazonHomePage`) with helper methods like `setSearchInputFieldValue()` and `clickSearchButton()`
- Asserts that a search-results element becomes visible after searching

*In plain terms: this is the exact same kind of task as the ChatGPT demo in Section 2.2 (write me a Selenium test) — except this time it's running entirely offline, on a free open-source model, with nothing sent to any company's servers. It shows that local LLMs aren't just a privacy fallback with worse capability — they're genuinely capable of the same "generate a test skeleton" task, at least for a reasonably common example like this one.*

*Touchpoint: the **Page Object pattern** (`AmazonHomePage` holding the locators/actions for that page) is a standard test-automation design pattern, not something Gen AI invented — it separates "how to interact with a page" from "what the test actually checks," so if a locator changes you only fix it in one place. It's worth recognizing this pattern by name since it'll keep showing up whenever Gen AI generates automation code.*

---

## Section 3.3 — Meta's Llama 3.2: Lighter and Multimodal Local Models

### The article: Meta introduces Llama 3.2
The instructor pulls up Meta AI's official announcement for **Llama 3.2** ("Revolutionizing edge AI and vision with open, customizable models," Sept 25, 2024). The headline graphic splits the new lineup into two groups:
- **Lightweight, on-device models:** 1B and 3B (parameter count, in billions)
- **Multimodal models:** 11B and 90B

*In plain terms: "3B" means 3 billion parameters — parameters are roughly the model's "learned settings," so more of them usually means a more capable but heavier/slower model. This announcement is Meta's newer, more spread-out lineup: some versions are made deliberately small so they can run on modest hardware ("edge"/"on-device"), and some are made larger and given the extra ability to understand images, not just text ("multimodal").*

### Why this matters right after the GPT4All demo
Section 3.2's demo already ran **Llama 3 8B Instruct** locally on a laptop through GPT4All. Llama 3.2 pushes that same idea further in two directions at once: even smaller models (1B/3B) that could run on lighter hardware, or even phones, and bigger models (11B/90B) that add vision capability.

*In plain terms: this connects two ideas from earlier in the section — "run it locally for privacy" (Section 3.1) and "here's a tool to actually do that" (GPT4All, Section 3.2). Llama 3.2 shows that the *open model* side of this equation keeps improving too: smaller local models get more capable, and some now handle images.*

*Touchpoint — "on-device" vs. "edge AI": these terms both mean "runs directly on the user's own hardware (phone, laptop) instead of calling out to a cloud server" — the same privacy/no-internet-required idea from GPT4All, just Meta's framing of it from the model side rather than the app side.*

*Touchpoint — "multimodal": means the model can take more than just text as input — here, images too (a screenshot, a photo of a UI bug, a diagram). For testing specifically, this is worth flagging: a multimodal local model is what would eventually let you feed it a screenshot of a broken UI and ask "what's wrong with this page," entirely offline.*

---

## Section 4.1 — Section Title Slide: Software Automation Testing, Starting with Manual Testing

This is a divider slide marking the start of a new section, "Generative AI — Software Automation Testing," with **Manual Testing** as its first sub-topic (shown with a "manual/checklist" book icon). The right side is a decorative collage of tool logos for what's presumably coming up in this section — a few are recognizable: **Selenium** ("Se" logo), **Cypress** ("cy" logo), and what looks like **Playwright**'s theater-mask logo, alongside a few other automation/workflow-style icons.

*In plain terms: this slide is just a chapter divider, not new content by itself — but it's useful as a map. It signals the course is about to go one-by-one through the "Applications of Gen AI in Software Testing" list from Section 1 (manual testing, automated testing/code generation, test data generation, bug tracking), starting with manual testing first, and that popular automation tools (Selenium, Cypress, Playwright) will be the concrete examples used along the way.*

---

## Section 4.2 — Manual Test Scenarios: The "Just Give It a URL" Trap, and How to Fix It

### First attempt: just asking ChatGPT for test scenarios by URL
The instructor asks ChatGPT to "write manual test scenarios for the page http://eaapp.somee.com with all possible permutations and combinations." ChatGPT replies — but flags up front that it can't actually open the page, so it's guessing a generic login/registration/navigation structure instead. It then produces a long, well-organized list anyway: numbered sections like "1. Login Page Test Scenarios," split into Valid Input and Invalid Input cases (e.g. correct credentials, submitting via Enter instead of the button, empty username, empty password), continuing all the way to an "11. Security Test Scenarios" section covering SQL injection and Cross-Site Scripting (XSS) attempts, and wrapping up with a conclusion.

*In plain terms: the output looks impressively thorough — organized numbering, positive/negative/edge cases, even security scenarios — but it's all generated from ChatGPT's general knowledge of "what a typical login page probably has," not from actually looking at this specific page. It's a well-written guess.*

### The instructor calls this out directly
Next prompt: "can you access the site in the first place?" ChatGPT admits plainly that no, it can't access external websites — everything it gave was based on general web-app patterns, not this real page.

*In plain terms: this is the key lesson of the demo — a plain ChatGPT chat (without browsing/tool access turned on) cannot fetch a live URL. If you don't realize this, you might trust a confident-sounding, well-formatted answer that's actually disconnected from the real page. Always check whether the tool actually looked at your input, especially when the input is a link.*

### The fix: paste the real page source in instead of just the link
The instructor opens eaapp.somee.com (ExecuteAutomation's "EA Employee App" demo site — the same practice site used back in Section 2.2) in the browser, right-clicks to **Inspect**, then opens **View Source** to get the page's raw HTML. Back in ChatGPT, the follow-up prompt is: "Can you analyse this page source and write me all the possible manual test scenarios and make sure that you are writing the scenarios like an experienced QA Engineer" — with the copied HTML pasted alongside it.

*In plain terms: since the model can't fetch the page itself, the workaround is to hand it the page's real content directly — copy the HTML from "View Source" and paste it into the chat. Now the model has actual ground truth to reason about (real form fields, real labels, real structure) instead of a generic guess.*

*Touchpoint — View Source vs. Inspect: "Inspect" opens the browser's DevTools panel (a live, interactive view of the page, including elements added by JavaScript after load); "View Source" shows the raw HTML exactly as the server originally sent it, as one plain page. For quickly grabbing HTML to paste into a chat, View Source is the simpler of the two.*

*Touchpoint — "act like an experienced QA Engineer": this phrase is a small but deliberate prompt-engineering trick called a **persona/role prompt** — asking the model to respond *as* a specific kind of expert nudges it toward that expert's habits (e.g. thinking about edge cases and security, not just the happy path) rather than a generic answer.*

*Touchpoint: this whole exercise foreshadows a bigger idea — an LLM that genuinely *can* browse live pages (via tool use / browsing plugins, or an agent wired up to a real browser) wouldn't need this manual copy-paste workaround at all. That's the direction "agentic" testing tools go, per your 22-week agentic QA roadmap.*

---

## Section 4.3 — Refining the Output: Adding Test Data to the Scenarios

### Follow-up prompt in the same conversation
Continuing the same chat from 4.2 (where ChatGPT had analyzed the real page source), the instructor doesn't start over — they just ask a follow-up: "Can you please include the Test Datas for the above login page." ChatGPT updates the *same* scenarios with a `Test Data` field added to each one, and also adds a new "1. Page Load Scenarios" section at the top — for example:
- **Scenario 1.1 (page loads successfully):** Steps: open the login page → Test Data: N/A → Expected Result: page loads with no errors, all elements (form, fields, buttons) displayed correctly.
- **Scenario 1.2 (verify page title):** Steps: open the page, check the browser's title bar → Test Data: N/A → Expected Result: title reads "Login – Execute Automation Employee App."

*In plain terms: this is the useful part of a chat-based workflow — instead of writing one giant "perfect" prompt up front, you can iterate. Ask for a first pass, look at what's missing (here, test data), then ask it to add just that on top of what it already produced. The model remembers the full conversation, including the page source pasted earlier, so it doesn't need that context repeated.*

*Touchpoint — Test Scenario vs. Test Case: this update quietly upgrades the earlier output from *test scenarios* (a one-line idea of what to check, e.g. "invalid password shows an error") into something closer to full *test cases* (concrete Steps, Test Data, and Expected Result for each one) — that's a standard manual-testing distinction, and it's exactly what "include the test data" was really asking for, even phrased informally.*

*Touchpoint: page-load and page-title checks (Scenario 1.1–1.2 here) are basic **sanity checks** — quick, cheap tests confirming the page even loaded correctly before you bother testing its actual functionality. It's a sensible thing for the model to have added on its own once asked to think more thoroughly.*

---

## Section 4.4 — From Scenarios to Gherkin, Diagrams, and Hitting the Free-Tier Wall

### Converting scenarios into Gherkin/BDD format
Still in the same conversation, the instructor asks ChatGPT to "write all the above scenarios in the BDD Gherkin format." It rewrites a scenario (e.g. "the Salary field shouldn't accept non-numeric values") into `Given` / `When` / `Then` steps — for example, *Given the user is on the "Create New Employee" form, When the user enters "abcde" in the Salary field...* The screenshot also happens to catch ChatGPT's **A/B response-comparison UI** ("You're giving feedback on a new version of ChatGPT" — pick Response 1 or 2), which is unrelated to testing; it's just OpenAI silently testing two model variants against each other on this chat.

*In plain terms: Gherkin is a plain-English, structured way to write test scenarios using the words Given/When/Then — Given sets up the starting state, When is the action taken, Then is the expected outcome. It's the format used by BDD (Behavior-Driven Development) frameworks like Cucumber and SpecFlow, which can actually *execute* Gherkin files as automated tests, and it's also readable by non-technical stakeholders (product owners, business analysts) since it's close to plain sentences. Asking the AI to reformat scenarios it already wrote into Gherkin is a good example of "same content, different shape" — a cheap, useful follow-up prompt.*

### The "mermaid drawing" mix-up
Next prompt: "Draw a mermaid Drawing for all the scenarios listed." ChatGPT takes this completely literally and generates an illustrated image of mythical mermaid characters holding nets and treasure chests, labeled with things like "Non-Numeric Toggled Inputs," "Invalid Emails," "Overly Long," and "Boundary Testing."

*In plain terms: this is a genuinely useful cautionary example rather than a mistake to skip past. "Mermaid" (capital M, as **Mermaid.js**) is also the name of a popular tool for writing diagrams (flowcharts, sequence diagrams) as plain text — a completely different meaning from "mermaid" the sea creature. Because the prompt just said "a mermaid drawing" with no other context, the model picked the literal, much more common meaning and generated fantasy art instead of a diagram. Lesson: when you mean a specific tool or format, name it precisely — "a Mermaid.js flowchart," not just "a mermaid drawing" — otherwise the model will guess, and it'll guess based on what's statistically more common, not what you actually meant.*

### Asking for a mind map — and hitting the free-tier limit
Final prompt: "Generate a mind map drawing for the above test scenarios." This time ChatGPT produces something closer to what was intended — an illustrated mind-map-style image with a central "Web Form Test Scenarios" node branching out to categories like Validation Tests, Edge Cases, and Missing Required Fields. Right after this, ChatGPT shows a hard stop: **"You've hit the Free plan limit for GPT-4o. You need GPT-4o to continue this chat because it has images. Your limit resets after 8:33 PM."**

*In plain terms: both the "mermaid" and "mind map" outputs here are generated *pictures* (like AI art), not interactive/editable diagrams — worth noticing, since a real Mermaid.js diagram would instead be text/code that a tool renders as a clean, editable flowchart. And the quota message at the end is Section 2.1's "free tiers have limits" point happening live in the demo: this particular chat needed the paid GPT-4o model because it contains images, and the free plan's usage cap for that was reached mid-conversation — exactly the kind of situation Section 3.1 used to justify considering a local LLM instead.*

---

## Section 4.5 — NotebookLM: Grounding Test Analysis in a Real Requirements Doc

### What NotebookLM is
The instructor introduces **NotebookLM**, Google's "AI research assistant" (built on their Gemini 1.5 Pro model). You create a notebook and upload your own source documents into it; from there, NotebookLM only answers based on *those* sources, not general internet knowledge.

*In plain terms: this directly solves the exact problem hit in Section 4.2, where ChatGPT couldn't actually see the real login page and had to guess. NotebookLM flips that around — you feed it the real document (e.g. a requirements spec) up front, and everything it says afterward is grounded in that document. This is essentially a polished, ready-to-use version of the RAG idea flagged back in Section 3.2's LocalDocs touchpoint (Retrieval-Augmented Generation: answers built from documents you supply, not just the model's memory).*

### The demo notebook and its auto-generated guide
The instructor loads three sample sources: a product requirements document for a fictional cloud-based customer engagement platform called **"Project Phoenix,"** plus background material on cloud CRM software and on SaaS (Software as a Service) in general. NotebookLM immediately produces a **Notebook guide**: an auto-written summary of all three sources, a set of **suggested questions** (e.g. "What are the key features and functionalities of Project Phoenix?"), and one-click generators for a FAQ, Study Guide, Table of Contents, Timeline, or Briefing Doc. There's also an **Audio Overview** option that can generate a two-host, podcast-style spoken discussion of the sources.

*In plain terms: think of this as "upload your spec, and instantly get a study guide, an FAQ, and a list of good questions to ask about it" — useful any time you (or a whole team) need to get quickly oriented in a document nobody's fully read yet, like a fresh requirements doc before writing tests against it.*

### Asking a grounded question and getting a cited answer
The instructor clicks the suggested question about Project Phoenix's key features. NotebookLM answers with a structured breakdown — Omnichannel Communication (email/chat/SMS, chat handling up to 100 concurrent users), AI-Driven Insights and Automation, a Customer Support and Analytics Dashboard, and Third-Party Integrations — followed by risks like dependency on third-party APIs and GDPR data-privacy compliance. Every claim has a small numbered citation marker next to it, pointing back to the exact spot in the source document it came from.

*In plain terms: those citation numbers are the real payoff here — you can click through and verify "does the spec actually say this," instead of just trusting the AI's summary. For testing specifically, this is a strong starting point for requirements-based test design: the "100 concurrent users" detail is a concrete, checkable performance/load requirement, and the GDPR mention is a hint toward compliance and data-privacy test scenarios — both the kind of thing you'd want to turn into actual test cases, and both traceable back to a real requirement instead of an AI guess.*

---

## Section 4.6 — RAG, Properly Defined

This section formally names and explains the idea that's been quietly running through the course since the RAG touchpoint in Section 3.2 (GPT4All's LocalDocs) and Section 4.5 (NotebookLM).

### What is RAG?
RAG stands for **Retrieval-Augmented Generation**: a technique that combines a retrieval system (something that fetches relevant information) with a generative model (the LLM that writes the answer). The course's own definition: it's an "advanced technique... that enhances [an LLM's] capabilities by combining a retrieval system with a generative model."

*In plain terms: a plain LLM only knows what it learned during training. RAG bolts on a second step — before answering, first go fetch relevant real documents/data — so the answer can be grounded in something current and specific to you, instead of only the model's frozen training knowledge.*

### RAG Breakdown — what each letter means
- **Retrieval:** fetch information from an external and/or "static" (fixed/local) knowledge source.
- **Augmented:** combine that fetched external knowledge with the static knowledge to build up a fuller picture of information.
- **Generation:** the LLM then generates a response from that combined knowledge, aiming for accuracy and answers that fit the actual context supplied.

*In plain terms: this maps cleanly onto what was already seen in the course — Retrieval = "go grab the right chunk of the document," Augmented = "add that chunk into what the model is working with," Generation = "now write the answer using that chunk." It's the same three-step idea, just given its formal name and acronym.*

### Confirming NotebookLM and GPT4All's LocalDocs are both RAG tools
The course explicitly connects the dots: NotebookLM (Section 4.5) and GPT4All's LocalDocs feature (Section 3.2) are both named as concrete examples of RAG tools.

*In plain terms: nice confirmation that those two "grounded knowledge" features from earlier weren't just similar in spirit — they're both literally implementations of RAG, one cloud-based (NotebookLM), one local (GPT4All's LocalDocs). Same underlying technique, two different tools.*

### Other use cases of RAG — specifically for testing
Because RAG-based answers are context-aware and precise (grounded in the actual documents you feed it, rather than a generic guess), the course calls out a few testing-specific uses:
1. **Test Plan generation** (the example this course itself builds toward)
2. **Test Case generation** — once you have the actual requirements document to ground it in
3. **Test estimation**, sometimes — using historical project data as the retrieved source

*In plain terms: this is the payoff for everything covered in Section 4 so far. Section 4.2 showed the failure mode (ChatGPT guessing at a page it couldn't see) and Section 4.5 showed the fix in action (NotebookLM answering from a real requirements doc with citations) — this slide is just naming that fix as "RAG" and pointing out it generalizes beyond Q&A to generating whole test plans, test cases, and even estimates, as long as you feed it the right source documents (a spec, a requirements doc, or past project data).*

---

## Section 5.1 — Moving from Manual to Automated UI Testing with Gen AI

### Section title: "How to perform automated UI testing with the help of Gen AI?"
A new section divider, moving on from Section 4's manual-testing focus into automated UI testing — this matches the tool collage teased back on the Section 4.1 title slide (Selenium, Cypress, Playwright icons), now being addressed directly.

### LLMs already understand the popular automation frameworks
The course states that Gen AI can help with automated UI testing just as naturally as it helped with manual testing, because LLMs already "understand" (have been trained on lots of code and docs from) the popular automation frameworks:
- **Cypress**
- **Playwright**
- **Selenium**
- **TestCafe**

It also notes LLMs can help refactor existing test code, not just generate new tests.

*In plain terms: this isn't a new capability so much as a reminder — the same "write me a Selenium test" trick already demonstrated back in Sections 2.2 and 3.2 works because these frameworks are extremely well-documented and widely used in public code, so the model has seen tons of real examples of each one during training. TestCafe is the one new name here: it's another end-to-end web testing framework (Node.js-based), in the same space as Cypress and Playwright, but notable for not needing Selenium/WebDriver under the hood at all.*

*Touchpoint — "refactor" here means: take test code that already works and clean it up (better naming, removing duplication, applying patterns like Page Object) without changing its behavior. That's a distinct, and arguably more immediately useful, skill from "generate a brand-new test from scratch."*

### "Not only that" — AI-powered coding tools built into the editor
The course adds a second category: AI-powered development tools that live inside your IDE, rather than a separate chat window:
- **GitHub Copilot**
- **Tabnine**
- **Amazon CodeWhisperer**
- **Google Project IDX**

These are described as able to refactor, explain, document, and even write unit-test code.

*In plain terms: this is a genuinely different way of using Gen AI than everything shown so far in the course. ChatGPT/Claude/GPT4All are separate chat windows — you describe what you want, copy the answer, and paste it into your code. Tools like GitHub Copilot instead sit directly inside your code editor and suggest code as you type, right in context, without the copy-paste step. It's the same underlying idea (an LLM trained on code) wrapped in a much more integrated, faster workflow for day-to-day coding.*

*Touchpoint: "explain" and "document" are worth calling out specifically for testers inheriting someone else's automation suite — pointing one of these tools at an unfamiliar test file and asking it to explain what the code does, or to generate missing comments/docs, is often a faster first step than reading it line-by-line cold.*

---

## Section 5.2 — ZeroStep: AI Baked Directly into Playwright

### What ZeroStep is
The instructor visits ZeroStep's website — an npm package (`npm i @zerostep/playwright -D`) that adds an `ai()` function directly into Playwright test code, backed by GPT-3.5/GPT-4. Instead of writing a CSS selector or XPath to locate an element, you write a plain-English instruction — the example shown is `ai("Fill out the form with realistic values")` on a real form (First Name, Last Name, Street Address, City, State) — and ZeroStep's AI figures out at runtime what actions to actually take to satisfy that instruction.

*In plain terms: this is the most concrete example yet of the "LLMs understand Playwright" point from Section 5.1 — not copy-pasting AI-generated code from a chat window, but a real library that plugs the AI directly into your existing Playwright test, one line at a time if you want. The tagline "So long, selectors" is the pitch: instead of the test breaking because a `button.class-xyz` selector changed, you just describe *what* the test should do, and the AI works out *how* to do it against whatever the page currently looks like.*

*Touchpoint: this is the same "self-healing"/"smart locator" idea flagged all the way back in Section 2.2's tool roundup (Testim, Applitools, etc.) — except here it's not a separate paid platform, it's a small library bolted onto the same open-source Playwright framework you're probably already using. The site's other selling point, "without changing your development workflow," means you can adopt this gradually — sprinkle `ai()` into just the flakiest parts of a suite rather than rewriting everything at once.*

*Touchpoint: worth remembering as a trade-off to watch for — a locator is deterministic (same input, same result every time); an AI figuring out "what to click" from an instruction is not always guaranteed to be deterministic in the same way. Good to keep in mind for later when the course covers testing AI-driven systems themselves.*

---

## Section 5.3 — Auto Playwright: Another Take on AI-Driven Playwright Tests

### Setting it up
The instructor follows the GitHub README for **Auto Playwright**, an open-source package (TypeScript, 6 contributors, actively released) that adds a similar AI-powered `auto()` function to Playwright. Setup is three steps:
1. Install it: `npm install auto-playwright -D`
2. Export your own OpenAI API key as an environment variable (or put it in a `.env` file): `export OPENAI_API_KEY='sk-...'`
3. Import `auto` from `auto-playwright` alongside the normal Playwright `test`/`expect`, and call it inside a test.

*In plain terms: this is the same overall idea as ZeroStep (Section 5.2) — plain-English instructions instead of brittle selectors, built directly into Playwright — but a different, independent open-source project, and one that talks straight to your own OpenAI account rather than a separate hosted service. Practically, that means you need to hold and pay for your own OpenAI API key for this one to work.*

*Touchpoint: exporting the API key as an environment variable (rather than pasting it directly into the test code) is standard security practice — it keeps the secret out of the source code and out of git history. Worth remembering any time a tool needs a credential like this.*

### What the `auto()` function can actually do
The README example shows `auto()` handling three distinct kinds of tasks in one small test:
1. **Query data** — `auto("get the header text", { page, test })` reads plain-text content off the page.
2. **Perform an action** — `` auto(`Type "${headerText}" in the search box`, { page, test}) `` finds the right input and types into it.
3. **Assert state** — `` auto(`Is the contents of the search box equal to "${headerText}"`, { page, test }) `` returns a true/false answer, which then gets checked with a normal `expect(...).toBe(true)`.

*In plain terms: this is a nice, clear breakdown of what "AI in your test" actually means in practice — it's not just one trick (finding elements), it covers three separate jobs a normal test does anyway: reading data off the page, doing something with it, and checking the result. Here all three are driven by plain-English instructions instead of hand-written Playwright locator/action code, and the very last step still ends in an ordinary Playwright/Jest-style `expect(...)` assertion — so the AI does the fuzzy "find and interact" work, but the pass/fail verdict is still a normal, deterministic check.*

---

*(Next section's notes get appended below as more screenshots come in.)*
