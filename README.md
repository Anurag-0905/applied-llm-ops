# ⚙️ Enterprise LLM Infrastructure & Agentic Workflows

**Maintainer:** Anurag Sharma  
**Focus:** Applied AI Engineering, LLMOps Economics, and Agentic Routing

## 📌 Executive Overview
This repository contains my technical audits, benchmarks, and prototype deployments of Large Language Models (LLMs) and agentic frameworks. My objective is to bridge the gap between raw data science concepts and operational business strategy by evaluating model deployment costs, latency trade-offs, vector embeddings, and deterministic routing logic for enterprise pipelines.

## 🛠️ Core Competencies & Tech Stack
- **LLM Orchestration & APIs:** Groq, Google Gemini, Ollama (Local open-weight models).
- **Edge Compute & Telemetry:** Evaluating Time to First Token (TTFT), Tokens per Second (TPS), and quantization hardware constraints.
- **Agentic Frameworks:** Intent classification, multi-provider routing, and deterministic tool calling.
- **Tech Stack:** Python, `uv` (dependency management), NumPy, Matplotlib, `tiktoken`.

---

## 📊 Analytical Deep Dives & Benchmarks

### 1. Tokenomics, Pricing Overheads, & Context Constraints
- **Objective:** I audited the hidden costs of LLM API usage and memory limitations.
- **Business Impact:** I identified a severe "Non-English Token Penalty"—regional languages (e.g., Telugu) consume exponentially more tokens than English, heavily inflating our API costs. I proved via 20-turn conversation simulations that developers must actively build sliding memory windows to prevent breaking the 8,192-token context limit in production.
- **File:** `llm/tokens.ipynb`

### 2. Deployment Landscape Matrix & Cost-Benefit Analysis
- **Objective:** I routed LLMs based on hard constraints (data privacy, latency) and operational costs.
- **Business Impact:** I built a weighted selection matrix for three workloads (Public FAQ, PII Document Analysis, Live Agent Assist). I demonstrated that handling Customer PII requires sacrificing cloud API speed for localized, open-weight GPU deployments to maintain data sovereignty, while public FAQs can be routed to highly cost-efficient cloud models instead of overpriced flagship tiers.
- **File:** `llm/model_matrix.ipynb`

### 3. Multi-Provider Routing & Stochastic Variance Control
- **Objective:** I evaluated the risk of stochastic sampling on deterministic business logic.
- **Business Impact:** I conducted a temperature sweep (0.0 to 1.0) on ambiguous support tickets. I proved that any LLM deployed for intent routing or structured data extraction must be strictly locked to `temperature=0.0` to prevent downstream pipeline failures caused by label drift.
- **File:** `llm/providers.ipynb`

### 4. Local Compute Constraints & Quantization Economics
- **Objective:** I benchmarked the feasibility of running open-weight LLMs on consumer hardware.
- **Business Impact:** I quantified the necessity of INT4 precision compression to fit 20B+ parameter models into standard VRAM budgets. I benchmarked local throughput against hosted APIs, concluding that local deployments are optimal for asynchronous data pipelines (like document reading) but introduce too much TTFT latency for live conversational UI.
- **File:** `llm/local_models.ipynb`

### 5. Multimodal ETL & OCR Validation Routing
- **Objective:** I designed a deterministic processing pipeline that ingests raw image scans (e.g., Identity Documents) using Vision models and extracts strictly validated JSON records.
- **Business Impact:** I demonstrated that multimodal image processing exponentially increases API token costs, necessitating batch-processing architectures for high-volume pipelines. I proved that while LLM JSON schemas guarantee syntactic structure, factual accuracy and conditional business rules (e.g., date logic, document types) must be enforced by deterministic code (Pydantic). I established the absolute necessity of Human-in-the-Loop exception routing for failed OCR reads rather than relying on endless, token-burning AI retries.
- **File:** `llm/vision_structured.ipynb`

### 6. Prompt Architecture & Deterministic Constraints
- **Objective:** I audited prompt structures to maximize deterministic reliability while minimizing computational waste.
- **Business Impact:** I demonstrated how separating immutable instructions into the `System` message preserves prefix caching, drastically lowering latency and API costs. I proved that few-shot examples act as a necessary token tax to lock in syntactic formats and protect downstream parsers. I highlighted the risks of reasoning drift in prompts that attempt simultaneous arithmetic and conditional routing, necessitating independent code-based mathematical validation.
- **File:** `prompting/prompt_anatomy.ipynb`

### 7. Reasoning Economics & Latent Compute
- **Objective:** I audited the cost-to-benefit ratio of advanced LLM reasoning techniques (Chain of Thought, Step-Back, Majority Voting).
- **Business Impact:** I proved that forcing explicit Chain of Thought on native-reasoning models incurs a massive "Latent Compute Tax" with zero accuracy gain, whereas local open-weight models strictly require it to function. I demonstrated that 5x Majority Voting is a waste of compute on deterministic tasks. I established scratchpad architectures as mandatory privacy firewalls for processing regulated financial data without exposing PII.
- **File:** `prompting/reasoning.ipynb`

### 8. Structured Prompting & Data Isolation
- **Objective:** I engineered a secure, version-controlled prompt architecture to prevent data leakage and prompt injection.
- **Business Impact:** I mitigated "lexical hijacking" by encapsulating untrusted user payloads within strict XML boundaries and injecting them dynamically via Jinja2 templates. I decoupled system prompts from Python execution code into dedicated `.md` files to support Git CI/CD versioning and auditable prompt configurations, achieving 100% held-out accuracy on enterprise routing tasks.
- **File:** `prompting/structured.ipynb`

### 9. Automated Evaluation & LLM-as-a-Judge
- **Objective:** I engineered an automated evaluation pipeline to programmatically grade prompt architectures against a deterministic rubric.
- **Business Impact:** I replaced binary string-match accuracy with strict JSON-schema LLM judges to evaluate reasoning, rule adherence, and hallucination rates independently. I implemented deterministic order-shuffling to neutralize position bias during A/B testing and proved that "All four criteria" boolean pass rates decay faster than single-metric accuracy, necessitating granular observability.
- **File:** `prompting/evaluation.ipynb`

### 10. Defensive Prompting & Adversarial Injection
- **Objective:** I audited the vulnerability of structured pipelines to deliberate prompt injection vectors (override, exfiltration, smuggling, prefix injection).
- **Business Impact:** I proved that XML tags alone fail to stop deliberate context confusion. I engineered a hardened architecture using explicit instruction hierarchies and programmatic scratchpad discarding to neutralize adversarial payloads. I reduced injection success rates to near-zero without degrading clean-ticket business accuracy, serializing the audit to an immutable CI/CD markdown report.
- **File:** `prompting/defensive_prompting.ipynb`

### 11. Chat State Architecture & Memory Windows
- **Objective:** I audited conversational state management for LLM pipelines to solve context exhaustion and compounding API costs.
- **Business Impact:** I demonstrated that LLM APIs are inherently stateless, and blindly passing raw conversation history scales token costs linearly. I engineered and benchmarked two enterprise memory architectures—Sliding Windows (truncation) and Summarization Compression (secondary LLM reduction)—to balance token expenditure against factual recall, proving that long-running agents require explicit token budgeting strategies.
- **File:** `prompting/chat_memory.ipynb`

### 12. Deterministic Tool Execution & Agentic Routing
- **Objective:** I engineered a secure function-calling orchestration layer to bridge stochastic LLM text generation with rigid external APIs and mathematical computations.
- **Business Impact:** I eliminated native computation hallucinations by restricting the model to JSON schema outputs mapped to Python execution functions. To prevent over-calling and argument hallucination, I implemented strict code-level type validation, autonomous self-correction loops, and an upstream intent router that completely blocks function schemas from reaching the model during conversational FAQ interactions.
- **File:** `prompting/function_calling.ipynb`

---

## ⚙️ Execution & Reproduction

This workspace relies on `uv` for lightning-fast dependency synchronization. 

```bash
# Clone the repository
git clone [https://github.com/Anurag-0905/applied-llm-ops.git](https://github.com/Anurag-0905/applied-llm-ops.git)
cd applied-llm-ops

# Sync dependencies
uv sync

# Set up environment variables for API routing
cp .env.example .env
# Edit .env with your specific GROQ_API_KEY and GEMINI_API_KEY

# Launch the Jupyter Lab environment
uv run jupyter lab