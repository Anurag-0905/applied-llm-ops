"""Integration test suite for orchestration/bankassist_lc.py.

Executes offline validation of the orchestration pipeline using mock models:
  - chainllm():   Validates ChatOpenAI instantiation from environment variables.
  - chainchain(): Validates LCEL pipeline construction and system prompt integration.
  - calculate_emi: Validates tool schema generation (parse_docstring=True) and execution logic.
  - ask():        Validates the deterministic tool-calling loop, ID mapping, and max_steps termination.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import sys
from pathlib import Path

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import BaseTool

from prompt_utils import CheckResult

PATH = Path("orchestration") / "bankassist_lc.py"
BANKASSIST = Path(__file__).resolve().parent / "bankassist_lc.py"
EMI_Q = "What is the EMI on a 25 lakh home loan at 8.5% for 20 years?"


def load_repo(repo_path):
    path = Path(repo_path) / PATH
    for k, v in {"MODEL": "check-model", "BASE_URL": "http://localhost:9/v1", "API_KEY": "check"}.items():
        os.environ.setdefault(k, v)            # chainllm() only builds the object; nothing is sent
    spec = importlib.util.spec_from_file_location("bankassist_lc", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["bankassist_lc"] = mod
    spec.loader.exec_module(mod)
    return mod


class ScriptedToolModel:
    """Mock model to validate tool invocation and mapping.
    always_call=True forces continuous tool requests to validate the step limit."""

    def __init__(self, always_call=False):
        self.calls, self.always_call, self.seen_ids_ok = 0, always_call, None

    def invoke(self, messages):
        self.calls += 1
        if self.calls > 10:
            raise RuntimeError("Infinite loop detected - step cap not enforced.")
        tool_msgs = [m for m in messages if isinstance(m, ToolMessage)]
        if tool_msgs and not self.always_call:
            asked = {tc["id"] for m in messages if isinstance(m, AIMessage) for tc in (m.tool_calls or [])}
            self.seen_ids_ok = all(t.tool_call_id in asked for t in tool_msgs)
            return AIMessage(content=f"Your EMI would be about Rs {tool_msgs[-1].content} a month.")
        return AIMessage(content="", tool_calls=[{"name": "calculate_emi", "id": f"call_{self.calls}",
                                                  "args": {"principal": 2500000, "annual_rate": 8.5,
                                                           "tenure_months": 240}}])


def _fail_msg(e, n):
    return f"Implementation incomplete - Test {n} failed" if isinstance(e, NotImplementedError) else f"{type(e).__name__}: {e}"


def check_langchain_work(repo_path) -> list:
    repo = Path(repo_path)

    def ck(name, ok, fix="", info=""):
        return CheckResult(name, ok, info if ok else fix)
        
    if not repo.exists():
        return [ck("Workspace directory exists", False, f"{repo} not found. Verify path.")]
    out = [ck("Workspace directory exists", True)]
    
    if not (repo / PATH).exists():
        out.append(ck("orchestration/bankassist_lc.py exists", False,
                      "Module not found - initialize bankassist_lc.py in the workspace directory."))
        return out
    out.append(ck("orchestration/bankassist_lc.py exists", True))
    
    try:
        mod = load_repo(repo)
    except Exception as e:  # noqa: BLE001
        out.append(ck("Module imports successfully", False, f"{type(e).__name__}: {e} - Verify dependencies and syntax."))
        return out
    out.append(ck("Module imports successfully", True))

    # TEST 1
    try:
        llm = mod.llm()
        ok = type(llm).__name__ == "ChatOpenAI" and getattr(llm, "model_name", None) == os.environ["MODEL"]
        out.append(ck("Test 1: llm() initializes ChatOpenAI from environment variables", ok,
                      "Ensure ChatOpenAI uses os.environ for MODEL, BASE_URL, and API_KEY."))
    except Exception as e:  # noqa: BLE001
        out.append(ck("Test 1: llm() initializes ChatOpenAI from environment variables", False, _fail_msg(e, 1)))

    # TEST 2
    try:
        seen = {}

        def fake_model(prompt_value):
            seen["text"] = " ".join(m.content for m in prompt_value.to_messages())
            return AIMessage(content="On Saturdays we are open 10am to 1pm.")
            
        result = mod.chain(RunnableLambda(fake_model)).invoke({"question": "Saturday timings?"})
        ok = isinstance(result, str) and "10am" in result and mod.SYSTEM[:30] in seen.get("text", "") \
            and "Saturday timings?" in seen.get("text", "")
        out.append(ck("Test 2: chain() executes LCEL pipeline with SYSTEM prompt", ok,
                      "Pipeline must route SYSTEM and question to the model and return parsed text."))
    except Exception as e:  # noqa: BLE001
        out.append(ck("Test 2: chain() executes LCEL pipeline with SYSTEM prompt", False, _fail_msg(e, 2)))

    # TEST 3
    try:
        t = mod.calculate_emi
        is_tool = isinstance(t, BaseTool)
        emi = t.invoke({"principal": 2500000, "annual_rate": 8.5, "tenure_months": 240}) if is_tool else None
        out.append(ck("Test 3a: calculate_emi executes correct financial logic",
                      is_tool and emi == 21696, f"Returned {emi!r}; expected integer 21696."))
                      
        props = t.args_schema.model_json_schema().get("properties", {}) if is_tool else {}
        desc = props.get("tenure_months", {}).get("description", "")
        out.append(ck("Test 3b: Tool schema parser extracts argument descriptions", "240" in desc,
                      "tenure_months schema missing expected context. Verify @tool(parse_docstring=True) and Google-style formatting."))
    except Exception as e:  # noqa: BLE001
        out.append(ck("Test 3a: calculate_emi executes correct financial logic", False, _fail_msg(e, 3)))

    # TEST 4
    try:
        model = ScriptedToolModel()
        with contextlib.redirect_stdout(io.StringIO()):     # Suppress execution logs
            answer = mod.ask(model, EMI_Q)
        ok = isinstance(answer, str) and "21696" in answer.replace(",", "") and model.seen_ids_ok
        out.append(ck("Test 4a: ask() loop executes tools and maps tool_call_id", ok,
                      f"Returned {answer!r}. Ensure AIMessage is appended before ToolMessage, and IDs match."))
    except Exception as e:  # noqa: BLE001
        out.append(ck("Test 4a: ask() loop executes tools and maps tool_call_id", False, _fail_msg(e, 4)))
        
    try:
        greedy = ScriptedToolModel(always_call=True)
        with contextlib.redirect_stdout(io.StringIO()):
            mod.ask(greedy, EMI_Q, max_steps=3)
        out.append(ck("Test 4b: ask() loop enforces max_steps termination", greedy.calls == 3,
                      f"Model invoked {greedy.calls} times; loop must terminate at max_steps limit."))
    except Exception as e:  # noqa: BLE001
        out.append(ck("Test 4b: ask() loop enforces max_steps termination", False, _fail_msg(e, 4)))

    # TEST 5
    has_rate = "get_rate" in getattr(mod, "TOOLS", {})
    out.append(ck("Test 5 (Optional): get_rate registered in tool mapping", True,
                  info="Passed" if has_rate else "Skipped"))
                  
    return out