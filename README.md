# ⚙️ Enterprise LLM Infrastructure & Agentic Workflows

**Maintainer:** Anurag Sharma  
**Focus:** Applied AI Engineering, LLMOps Economics, and Agentic Routing

## 📌 Executive Overview

This repository contains my technical audits, benchmarks, and prototype deployments of Large Language Models (LLMs) and agentic frameworks. My objective is to bridge the gap between raw data science concepts and operational business strategy by evaluating model deployment costs, latency trade-offs, vector embeddings, and deterministic routing logic for enterprise pipelines.

## 🛠️ Core Competencies & Tech Stack

- **LLM Orchestration & APIs:** Groq, Google Gemini, Ollama (Local open-weight models), LangChain, LiteLLM.
- **Edge Compute & Telemetry:** Evaluating Time to First Token (TTFT), Tokens per Second (TPS), and quantization hardware constraints.
- **Agentic Frameworks:** Intent classification, multi-provider routing, LCEL pipelines, and deterministic tool calling.
- **Backend Architecture:** FastAPI, Uvicorn, Pydantic, Server-Sent Events (SSE).
- **Retrieval & Vector Math:** Dense Embeddings (`BAAI/bge-small-en-v1.5`, `all-MiniLM-L6-v2`), Cosine Similarity, MRR Benchmarking.
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
- **File:** `orchestration/chat_memory.ipynb`

### 12. Deterministic Tool Execution & Agentic Routing

- **Objective:** I engineered a secure function-calling orchestration layer to bridge stochastic LLM text generation with rigid external APIs and mathematical computations.
- **Business Impact:** I eliminated native computation hallucinations by restricting the model to JSON schema outputs mapped to Python execution functions. To prevent over-calling and argument hallucination, I implemented strict code-level type validation, autonomous self-correction loops, and an upstream intent router that completely blocks function schemas from reaching the model during conversational FAQ interactions.
- **File:** `orchestration/function_calling.ipynb`

### 13. Framework Abstraction & LangChain Orchestration

- **Objective:** I transitioned raw REST API tool execution into a scalable LangChain pipeline.
- **Business Impact:** I eliminated hand-written JSON schema maintenance by leveraging Python type hints for automated OpenAI-compliant schema generation. I implemented LangChain Expression Language (LCEL) to decouple system contracts from runtime execution, standardizing multi-provider routing (Ollama/Groq) behind a unified message interface while strictly bounding the agentic loop to prevent infinite execution costs.
- **File:** `orchestration/langchain_build.ipynb`

### 14. API Gateway & Cost Economics (LiteLLM)

- **Objective:** I engineered a resilient LLM gateway to abstract provider-specific SDKs, enabling seamless switching between Groq, Ollama, and OpenAI architectures.
- **Business Impact:** I implemented automated fallback routing to prevent hard outages and rate-limit drops from degrading the customer experience. I built real-time token cost accounting pipelines to map compute expenditure directly to individual model interactions, ensuring strict budget observability.
- **File:** `orchestration/litellm_gateway.ipynb`

### 15. API Orchestration & Streaming (FastAPI)

- **Objective:** I engineered a production-grade FastAPI server to deploy agentic workflows behind a stateless HTTP interface.
- **Business Impact:** I reduced perceived latency via Server-Sent Events (SSE) streaming. I implemented strict Pydantic payload validation to reject malformed requests (HTTP 422) before consuming token budgets, and designed scalable in-memory sliding windows to manage concurrent conversational states across isolated sessions.
- **File:** `orchestration/fastapi_server.ipynb` & `orchestration/bankassist_fastAPI/app.py`

### 16. Semantic Search & Dense Embeddings (Retrieval Architecture)

- **Objective:** I engineered the retrieval layer (the "R" in RAG) using offline dense vector embeddings to map unstructured enterprise knowledge by semantic meaning, benchmarking it against sparse keyword search.
- **Business Impact:** I proved that legacy keyword (BM25) search fails entirely on synonymous queries (MRR: 0.50), rendering it unfit for intent routing. By transitioning to a 384-dimensional dense vector space (`bge-small-en-v1.5`) and executing cosine similarity sweeps, I achieved a perfect `hit@3` score (10/10) with an MRR of 0.95. I also quantified the necessity of strict cosine thresholds (e.g., 0.63) to block irrelevant out-of-scope retrievals from reaching the LLM, preventing downstream hallucinations.
- **File:** `vectordbs/embeddings.ipynb` & `vectordbs/search.py`

### 17. Vector Databases & ANN Indexing (ChromaDB)

- **Objective:** I engineered a persistent, disk-backed vector database using ChromaDB to replace in-memory, brute-force semantic search.
- **Business Impact:** I demonstrated that flat exact search degrades linearly (O(N)), making it unscalable for enterprise-level catalogues of 50 million+ vectors. I implemented HNSW (Hierarchical Navigable Small World) approximate nearest neighbor indexes to achieve sub-linear latency. I proved the critical necessity of hard metadata filtering at the database layer (not post-retrieval) to guarantee strict tenant isolation, and empirically evaluated the trade-off between computational latency and `recall@k` accuracy by tuning `ef_search` and `M` parameters.
- **File:** `vectordbs/store.py` & `vectordbs/vector_db.ipynb`

### 18. Production Vector Stores & Multi-Tenancy (Qdrant & pgvector)

- **Objective:** I migrated the retrieval layer from an embedded library (ChromaDB) to production client-server databases (Qdrant and PostgreSQL with `pgvector`) to support multi-user concurrency, persistence, and horizontal scaling.
- **Business Impact:** I executed a zero-re-embed migration and proved 100% retrieval parity (`overlap@k = 1.0`) across ChromaDB, Qdrant, and `pgvector`. I audited cross-tenant data leakage in shared collections and enforced mandatory query-level payload filtering to isolate customer records. I also modeled memory economics at scale, demonstrating that `int8` and `binary` quantization compress 100M-vector RAM footprints from 153.6 GB down to 38.4 GB and 4.8 GB, respectively.
- **File:** `vectordbs/vector_stores.ipynb` & `vectordbs/migrate.py`

### 19. Hybrid Search, RRF Fusion & Cross-Encoder Reranking

- **Objective:** I engineered a two-stage hybrid retrieval architecture combining sparse BM25 keyword search with dense vector embeddings, Reciprocal Rank Fusion (RRF), and cross-encoder reranking (`Xenova/ms-marco-MiniLM-L-6-v2`).
- **Business Impact:** I proved that single-method retrieval fails on real customer traffic—dense vectors missed exact product codes (`SKU-EL-004`, 7/9 exact), while BM25 failed on paraphrased queries (11/13 semantic). Implementing two-stage hybrid retrieval with cross-encoder reranking achieved 100% `hit@3` (22/22) and lifted MRR to 0.95. I also calibrated a logit-based relevance gate to block out-of-scope queries before LLM generation and deployed server-side hybrid prefetching in Qdrant.
- **File:** `vectordbs/hybrid_rerank.ipynb` & `vectordbs/hybrid.py`

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
