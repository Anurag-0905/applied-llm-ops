import json
import os

import uvicorn
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv(find_dotenv(usecwd=True), override=True)

SYSTEM = """You are BankAssist, Northwind Bank's assistant for retail customers. Answer in 2-3 friendly sentences.
Facts you may quote (never invent a number that is not here):
- Branches: 10am-4pm Monday to Friday, 10am-1pm Saturday, closed Sunday.
- Home loan rates: 8.5% floating, 9.0% fixed. Personal loan rate: 10.5% fixed.
- No prepayment penalty on floating-rate loans. Minimum credit score for a new loan: 700.
Remember what the customer told you earlier in this conversation (name, income, amounts) and use it.
Use a tool only for an exact EMI or today's rate. If a tool says INVALID, ask the customer for the missing detail."""

MAX_STEPS = 3
CAP_MESSAGE = "Sorry, I couldn't finish that one. Could you ask it in a simpler way?"


def make_llm():
    """Initialize the ChatOpenAI language model."""
    return ChatOpenAI(model=os.environ["MODEL"], base_url=os.environ.get("BASE_URL"),
                      api_key=os.environ["API_KEY"], temperature=0, max_tokens=1500)


@tool(parse_docstring=True)
def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> int:
    """Exact monthly EMI for a loan. Use ONLY when the customer asks for an EMI amount.

    Args:
        principal: loan amount in rupees, e.g. 25 lakh = 2500000
        annual_rate: interest rate in percent per year, e.g. 8.5
        tenure_months: total months, e.g. 20 years = 240
    """
    r = annual_rate / 12 / 100
    return round(principal * r * (1 + r) ** tenure_months / ((1 + r) ** tenure_months - 1))


@tool(parse_docstring=True)
def get_rate(product: str, rate_type: str) -> float:
    """Today's interest rate in percent per year. Use when the customer asks for a rate or needs one for an EMI.

    Args:
        product: "home_loan" or "personal_loan"
        rate_type: "floating" or "fixed" (personal loans are fixed only)
    """
    card = {("home_loan", "floating"): 8.5, ("home_loan", "fixed"): 9.0, ("personal_loan", "fixed"): 10.5}
    return card[(product, rate_type)]


TOOLS = {"calculate_emi": calculate_emi, "get_rate": get_rate}

LLM = None


def get_llm():
    """Retrieve or initialize the globally cached LLM instance with bound tools."""
    global LLM
    if LLM is None:
        LLM = make_llm().bind_tools(list(TOOLS.values()))
    return LLM


def run_tool(call) -> ToolMessage:
    """Safely execute a tool call and return the result as a ToolMessage."""
    if call["name"] not in TOOLS:
        return ToolMessage(f"INVALID: there is no tool called {call['name']}.", tool_call_id=call["id"])
    try:
        return TOOLS[call["name"]].invoke(call)
    except Exception as e:
        return ToolMessage(f"INVALID: {type(e).__name__}: {e}", tool_call_id=call["id"])


def stream_turn(llm_with_tools, messages, max_steps=MAX_STEPS):
    """Execute the agent loop with streaming support."""
    messages = list(messages)
    said = []
    for _ in range(max_steps):
        full = None
        for chunk in llm_with_tools.stream(messages):
            full = chunk if full is None else full + chunk
            if isinstance(chunk.content, str) and chunk.content:
                said.append(chunk.content)
                yield "token", chunk.content
        if full is None or not full.tool_calls:
            yield "done", "".join(said)
            return
        messages.append(full)
        for call in full.tool_calls:
            result = run_tool(call)
            yield "tool", f"{call['name']}({call['args']}) -> {result.content}"
            messages.append(result)
    said.append(CAP_MESSAGE)
    yield "token", CAP_MESSAGE
    yield "done", "".join(said)


def run_turn(llm_with_tools, messages):
    """Execute the agent loop synchronously."""
    steps, answer = [], ""
    for kind, text in stream_turn(llm_with_tools, messages):
        if kind == "tool":
            steps.append(text)
        elif kind == "done":
            answer = text
    return answer, steps


app = FastAPI(title="BankAssist", version="0.22")


@app.get("/health")
def health():
    """Health check endpoint to verify API and model status."""
    return {"status": "ok", "model": os.environ["MODEL"]}


class ChatRequest(BaseModel):
    session_id: str
    message: str = Field(min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    tool_steps: list[str]
    turns: int


KEEP_TURNS = 4
SESSIONS: dict[str, list] = {}


def window(history: list, keep_turns: int = KEEP_TURNS) -> list:
    """Extract the most recent context window from the session history."""
    return history[-2 * keep_turns:] if keep_turns > 0 else []


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """Process a synchronous chat request."""
    history = SESSIONS.setdefault(req.session_id, [])
    messages = [SystemMessage(SYSTEM), *window(history), HumanMessage(req.message)]
    answer, steps = run_turn(get_llm(), messages)
    history += [HumanMessage(req.message), AIMessage(answer)]
    return ChatResponse(session_id=req.session_id, answer=answer, tool_steps=steps, turns=len(history) // 2)


def sse(event: str, data: dict) -> str:
    """Format data as a Server-Sent Event."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


@app.post("/chat/stream")
def chat_stream(req: ChatRequest):
    """Process an asynchronous chat request returning a stream."""
    history = SESSIONS.setdefault(req.session_id, [])
    messages = [SystemMessage(SYSTEM), *window(history), HumanMessage(req.message)]

    def events():
        for kind, text in stream_turn(get_llm(), messages):
            if kind == "done":
                history.extend([HumanMessage(req.message), AIMessage(text)])
            yield sse(kind, {"text": text})

    return StreamingResponse(events(), media_type="text/event-stream")


@app.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    """Purge a conversation session from memory."""
    if session_id in SESSIONS:
        SESSIONS.pop(session_id)
        return {"deleted": True}
    return {"deleted": False}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)