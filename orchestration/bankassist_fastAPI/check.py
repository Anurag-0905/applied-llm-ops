from __future__ import annotations
"""
Integration Validation Suite for BankAssist API.
Uses FastAPI TestClient and mock LLM streams to validate routing, memory, and SSE logic offline.
"""
import importlib.util
import json
import os
import sys
from pathlib import Path

from langchain_core.messages import AIMessage, AIMessageChunk, HumanMessage, SystemMessage, ToolMessage

from prompt_utils import CheckResult


PATH = Path("orchestration")/ "bankassist_fastAPI" / "app.py"
STARTER = Path(__file__).resolve().parent / "starter.py"
EMI_Q = "What is the EMI on a 25 lakh home loan at 8.5% for 20 years?"


def load_repo(repo_path, path=None):
    """Dynamically import the routing pipeline module for testing."""
    path = Path(path) if path else Path(repo_path) / PATH
    env_vars = {"MODEL": "check-model", "BASE_URL": "http://localhost:9/v1", "API_KEY": "check_key"}
    for k, v in env_vars.items():
        os.environ.setdefault(k, v)
    
    spec = importlib.util.spec_from_file_location("bankassist_app_student", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["bankassist_app_student"] = mod
    spec.loader.exec_module(mod)
    return mod


class FakeStreamingModel:
    """Mocks the LLM stream to evaluate state handling and tool execution paths."""
    def __init__(self):
        self.seen = []

    def stream(self, messages):
        self.seen.append(list(messages))
        if self.seen[-1] and isinstance(self.seen[-1][-1], ToolMessage):
            text = f"Your EMI would be about Rs {messages[-1].content} a month."
        elif "EMI" in str(messages[-1].content):
            yield AIMessageChunk(content="", tool_call_chunks=[{
                "name": "calculate_emi", "id": f"call_{len(self.seen)}", "index": 0,
                "args": json.dumps({"principal": 2500000, "annual_rate": 8.5, "tenure_months": 240})
            }])
            return
        else:
            earlier = [m for m in messages[:-1] if not isinstance(m, SystemMessage)]
            text = f"I can see {len(earlier)} earlier messages."
        for word in text.split(" "):
            yield AIMessageChunk(content=word + " ")

    def invoke(self, messages):
        full = None
        for c in self.stream(messages):
            full = c if full is None else full + c
        return full


def parse_sse(body: str) -> list:
    """Deserialize Server-Sent Events from raw HTTP payloads."""
    events = []
    for block in body.replace("\r\n", "\n").split("\n\n"):
        if not block.strip():
            continue
        fields = dict(line.split(": ", 1) for line in block.split("\n") if ": " in line)
        if "event" not in fields or "data" not in fields:
            raise ValueError(f"Malformed SSE block: {block!r}")
        events.append((fields["event"], json.loads(fields["data"])))
    return events


def _todo(e, n):
    """Format traceback context."""
    return f"{type(e).__name__}: {e}"


def fresh_client(mod):
    """Initialize a fresh test client bound to the mock LLM."""
    from fastapi.testclient import TestClient
    mod.LLM = FakeStreamingModel()
    mod.SESSIONS.clear()
    return TestClient(mod.app), mod.LLM


def check_assist_work(repo_path, path=None) -> list:
    repo = Path(repo_path)
    out = []

    def ck(name, ok, fix="", info=""):
        return CheckResult(name, ok, info if ok else fix)
        
    if path is None:
        if not repo.exists():
            return [ck("Repository structure valid", False, f"Missing path: {repo}")]
        if not (repo / PATH).exists():
            return [ck("Repository structure valid", True), 
                    ck("Application module found", False, "Missing target path")]
    out.append(ck("Application module found", True))
    
    try:
        mod = load_repo(repo, path)
    except Exception as e:
        out.append(ck("Module imports successfully", False, f"{type(e).__name__}: {e}"))
        return out
    out.append(ck("Module imports successfully", True))

    # Health Check Endpoint
    name = "GET /health endpoint response"
    try:
        client, _ = fresh_client(mod)
        r = client.get("/health")
        body = r.json() if r.status_code == 200 else {}
        out.append(ck(name, body.get("status") == "ok" and body.get("model") == os.environ["MODEL"], "Invalid health status"))
    except Exception as e:
        out.append(ck(name, False, _todo(e, 1)))

    # Schema Validation
    name = "Pydantic Schema Validation"
    try:
        from pydantic import ValidationError
        rejected = False
        try:
            mod.ChatRequest(session_id="a", message="")
        except ValidationError:
            rejected = True
        fields = set(mod.ChatResponse.model_fields)
        ok = rejected and {"tool_steps", "turns"} <= fields
        out.append(ck(name, ok, "Schema fields missing or constraints unenforced"))
    except Exception as e:
        out.append(ck(name, False, _todo(e, 2)))

    # Window Logic
    name = "Memory context truncation logic"
    try:
        hist = []
        for i in range(10):
            hist += [HumanMessage(f"q{i}"), AIMessage(f"a{i}")]
        w3 = mod.window(hist, 3)
        ok = (len(w3) == 6 and w3[0].content == "q7" and w3[-1].content == "a9"
              and mod.window([], 3) == [] and len(mod.window(hist[:4], 3)) == 4 and mod.window(hist, 0) == [])
        out.append(ck(name, ok, "Context window slicing failed"))
    except Exception as e:
        out.append(ck(name, False, _todo(e, 3)))

    # Stateful Post
    name = "Session isolation and persistence"
    try:
        client, fake = fresh_client(mod)
        a1 = client.post("/chat", json={"session_id": "alice", "message": "Hi."}).json()
        a2 = client.post("/chat", json={"session_id": "alice", "message": "Who am I?"}).json()
        b1 = client.post("/chat", json={"session_id": "bob", "message": "Hello"}).json()
        ok = ("0 earlier" in a1.get("answer", "") and "2 earlier" in a2.get("answer", "")
              and "0 earlier" in b1.get("answer", "") and a2.get("turns") == 2)
        out.append(ck(name, ok, "State leakage detected or history unsaved"))
    except Exception as e:
        out.append(ck(name, False, _todo(e, 4)))

    # SSE Streaming
    name = "Server-Sent Events payload serialization"
    try:
        s = mod.sse("token", {"text": "two\nlines"})
        ok = s == 'event: token\ndata: {"text": "two\\nlines"}\n\n'
        out.append(ck(name, ok, "SSE formatting non-compliant"))
    except Exception as e:
        out.append(ck(name, False, _todo(e, 5)))

    name = "Streaming response endpoint configuration"
    try:
        client, fake = fresh_client(mod)
        r = client.post("/chat/stream", json={"session_id": "s", "message": EMI_Q})
        events = parse_sse(r.text)
        kinds = [k for k, _ in events]
        ok = (r.headers.get("content-type", "").startswith("text/event-stream") and "tool" in kinds
              and kinds[-1] == "done")
        out.append(ck(name, ok, "Stream events malformed or missing headers"))
    except Exception as e:
        out.append(ck(name, False, _todo(e, 5)))

    # Stretch Delete
    try:
        client, _ = fresh_client(mod)
        client.post("/chat", json={"session_id": "z", "message": "hi"})
        r1 = client.delete("/sessions/z")
        r2 = client.delete("/sessions/z")
        done6 = r1.status_code == 200 and r1.json() == {"deleted": True} and r2.json() == {"deleted": False}
        info = "done" if done6 else "not functional"
    except Exception:
        info = "not implemented"
    out.append(ck("Session memory teardown endpoint", True, info=info))
    
    return out