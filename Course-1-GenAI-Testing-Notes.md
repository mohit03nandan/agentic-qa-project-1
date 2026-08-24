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

*(Next section's notes get appended below as more screenshots come in.)*
