"""
BankAssist LLM Pipeline: Universal Routing & Fallback.

Production-grade implementation using LiteLLM for unified API calling,
automatic failover, and token-based telemetry. Defaults to a local
Ollama instance with a cloud fallback via Groq.
"""
import logging
import os
import time

import litellm
from dotenv import find_dotenv, load_dotenv
from litellm import Router, completion, cost_per_token

# Configure Environment & Logging
os.environ.setdefault("LITELLM_LOCAL_MODEL_COST_MAP", "True")
load_dotenv(find_dotenv(usecwd=True), override=True)

litellm.suppress_debug_info = True
logging.getLogger("LiteLLM Router").setLevel(logging.CRITICAL)

SYSTEM = (
    "You are BankAssist, Northwind Bank's assistant. Branches are open 10am-4pm Monday to Friday "
    "and 10am-1pm on Saturday. Home loan rates: 8.5% floating, 9.0% fixed. Answer in 2-3 sentences."
)

# Core Model Configuration
_on_ollama = "11434" in os.getenv("BASE_URL", "")
PRIMARY = os.getenv("LLM_PRIMARY") or (("ollama_chat/" if _on_ollama else "groq/") + os.getenv("MODEL", "openai/gpt-oss-20b"))
FALLBACK = os.getenv("LLM_FALLBACK") or "groq/openai/gpt-oss-120b"


def params(model: str) -> dict:
    """Resolve connection parameters dynamically based on the provider prefix."""
    if model.startswith("ollama"):
        return {"model": model, "api_base": os.getenv("OLLAMA_BASE", "http://localhost:11434")}
    
    # Securely map to Groq or generic fallback
    return {"model": model, "api_key": os.getenv("GROQ_API_KEY") or os.getenv("API_KEY", "")}


def messages_for(question: str) -> list:
    """Format the standard message payload for Chat APIs."""
    return [{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}]


def answered_by(response) -> str:
    """Extract the exact model that generated the response."""
    return response._hidden_params.get("litellm_model_name") or response.model


def fallbacks_used(response) -> int:
    """Determine how many failover attempts were executed."""
    return int((response._hidden_params.get("additional_headers") or {}).get("x-litellm-attempted-fallbacks", 0) or 0)


def ask_once(model: str, question: str):
    """Execute a single API call without failover logic."""
    return completion(
        **params(model), 
        messages=messages_for(question), 
        temperature=0, 
        max_tokens=1500
    )


def compare(question: str) -> list:
    """Compare responses concurrently across the primary and fallback models."""
    out = []
    for model in (PRIMARY, FALLBACK):
        response = ask_once(model, question)
        out.append((model, response.choices[0].message.content))
    return out


def make_router(primary: str = PRIMARY, fallback: str = FALLBACK) -> Router:
    """Initialize a resilient LiteLLM router with automatic fallback protocols."""
    return Router(
        model_list=[
            {"model_name": "bankassist", "litellm_params": params(primary)},
            {"model_name": "bankassist-backup", "litellm_params": params(fallback)},
        ],
        fallbacks=[{"bankassist": ["bankassist-backup"]}],
        num_retries=1,
        timeout=30,
    )


def cost_line(response, model: str, seconds: float) -> str:
    """Calculate and format telemetry metadata."""
    p, c = response.usage.prompt_tokens, response.usage.completion_tokens
    try:
        cost_in, cost_out = cost_per_token(model=model, prompt_tokens=p, completion_tokens=c)
        cost = cost_in + cost_out
    except Exception:
        cost = 0.0  # Local models incur $0.00 infrastructure cost
    return f"{model} | {p + c} tokens | ${cost:.6f} | {seconds:.2f}s"


def ask_logged(router: Router, question: str) -> str:
    """Execute a routed API call with full cost and latency telemetry."""
    t = time.perf_counter()
    
    response = router.completion(
        model="bankassist", 
        messages=messages_for(question)
    )
    
    elapsed = time.perf_counter() - t
    actual_model = answered_by(response)
    
    print(cost_line(response, actual_model, elapsed))
    
    if fallbacks_used(response) > 0:
        print(f"⚠️ Failover Triggered: Request answered by {actual_model}")
        
    return response.choices[0].message.content


def main():
    """Integration execution block."""
    q = "What is the home loan floating rate, and when are branches open on Saturday?"
    
    print("=== Pipeline Configuration ===")
    print(f"PRIMARY  = {PRIMARY}")
    print(f"FALLBACK = {FALLBACK}\n")

    print("=== Execution Demo: Model Comparison ===")
    for model, text in compare(q):
        print(f"{model}:\n  {text}")
    print()

    print("=== Execution Demo: Standard Router ===")
    router = make_router()
    answer = ask_logged(router, q)
    print(f"\nResponse:\n{answer}\n")
    
    print("=== Execution Demo: Forced Failover ===")
    broken_router = make_router(primary="groq/model-that-does-not-exist")
    fallback_answer = ask_logged(broken_router, q)
    print(f"\nResponse:\n{fallback_answer}")


if __name__ == "__main__":
    main()