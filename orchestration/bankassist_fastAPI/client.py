"""
API Client for BankAssist.
Executes standard health checks and streams conversational endpoints over HTTP/SSE.
"""
import json
import sys
import httpx

URL = "http://127.0.0.1:8000"


def stream(session_id: str, message: str) -> None:
    """Execute a streaming POST request to the chat API and print Server-Sent Events."""
    with httpx.stream("POST", f"{URL}/chat/stream", json={"session_id": session_id, "message": message}, timeout=120) as r:
        r.raise_for_status()
        event = None
        for line in r.iter_lines():
            if line.startswith("event: "):
                event = line[len("event: "):]
            elif line.startswith("data: "):
                text = json.loads(line[len("data: "):])["text"]
                if event == "tool":
                    print(f"\n  [tool] {text}")
                elif event == "token":
                    print(text, end="", flush=True)
    print()


def main() -> None:
    """Integration test execution block."""
    try:
        health = httpx.get(f"{URL}/health", timeout=5)
    except httpx.ConnectError:
        sys.exit(f"Connection failed. Ensure the server is listening on {URL}.")
        
    print(f"GET /health -> {health.status_code} {health.text}")
    if health.status_code != 200:
        sys.exit("Health check failed.")

    if len(sys.argv) > 1:
        stream("default_user", " ".join(sys.argv[1:]))
        return

    print("\n=== Test 1: Stateful Conversation Context ===")
    for msg in ("Hi, my name is Priya and I earn 80,000 a month.", "What is my name, and what do I earn?"):
        r = httpx.post(f"{URL}/chat", json={"session_id": "priya", "message": msg}, timeout=120)
        print(f"  User: {msg}\n  Agent: {r.json().get('answer', r.text)} (Status: {r.status_code})")

    print("\n=== Test 2: Session Isolation ===")
    r = httpx.post(f"{URL}/chat", json={"session_id": "ravi", "message": "What is my name?"}, timeout=120)
    print(f"  Agent: {r.json().get('answer', r.text)}")

    print("\n=== Test 3: Payload Validation (Empty Request) ===")
    r = httpx.post(f"{URL}/chat", json={"session_id": "priya", "message": ""}, timeout=30)
    print(f"  Status: {r.status_code} (Expected 422 Unprocessable Entity)")

    print("\n=== Test 4: Tool Execution & SSE Streaming ===")
    stream("priya", "What is the EMI on a 25 lakh home loan at 8.5% for 20 years?")


if __name__ == "__main__":
    main()