"""Method-blind DeepSeek driver (A0 no-tools / A2 tool) for v3: the model is NOT told the method;
it must select from the full menu and DECLARE it per node. Captures declared_methods for Channel-2.
"""
from __future__ import annotations

import json

from dmaic_bench.v2.llm_agent import _expand, _extract_json
from dmaic_bench.v2.tool_agent import _safe_exec
from dmaic_bench.v3.session import MethodBlindSession

_SYS = """You are a Six Sigma Black Belt independently completing a DMAIC project. The environment does not tell you which method to use: select the appropriate method from method_space using each node's data and policy_doc, and declare it. A wrong method (e.g. normal capability for skewed data, Xbar for individual values, or attribute agreement for continuous data) is misuse even if the numbers are correct.{tool}

Output exactly one JSON object per turn:
{{"reasoning":"...","report":{{"<field>":<value>}},"method":"<selected method_id or list>","goto":"<next node>"}}
- The method field declares your method choice and is scored. Report actual computed values; use null for missing values and never fabricate results."""

_TOOL_NOTE = ("You have a Python tool: output {\"tool\":\"python\",\"code\":\"...print(...)\"}  and it will run on "
              "DATA (the current node data), with results returned to you. Use it for actual calculations (e.g. test normality before choosing a capability method).")


def run_methodblind(task, chat_fn, use_tool: bool = False, max_turns: int = 22):
    sess = MethodBlindSession(task)
    brief = sess.briefing()
    entry = brief["entry_node"]
    cur_data = sess.request(entry).get("data") or {}
    hist = {entry: cur_data}
    msgs = [{"role": "system", "content": _SYS.format(tool=_TOOL_NOTE if use_tool else "")},
            {"role": "user", "content":
             "Project briefing (including policy_doc and method_space):\n"
             + json.dumps({k: brief[k] for k in ("project", "policy_doc", "method_space", "nodes",
                                                 "entry_node")}, ensure_ascii=False)
             + f"\nEntry {entry} data: {json.dumps(cur_data, ensure_ascii=False)}\nBegin."}]
    cur = entry
    terminal = [n["key"] for n in brief["nodes"] if n["phase"] == "control"]
    transcript = []
    for _ in range(max_turns):
        r = chat_fn(msgs); c = r["content"]; transcript.append(c)
        msgs.append({"role": "assistant", "content": c})
        try:
            act = _extract_json(c)
        except ValueError:
            msgs.append({"role": "user", "content": "Output only one JSON object."}); continue
        if use_tool and act.get("tool") == "python":
            out = _safe_exec(act.get("code", ""), cur_data, hist)
            msgs.append({"role": "user", "content": f"[python]\n{out}\nContinue."}); continue
        rep = _expand(act.get("report") or {})
        if rep or act.get("method"):
            sess.report(cur, rep, method=act.get("method"))
        goto = act.get("goto")
        if not goto or (goto in terminal and cur in terminal):
            break
        resp = sess.request(goto)
        if resp["kind"] == "data":
            cur = goto; cur_data = resp["data"] or {}; hist[goto] = cur_data
            if goto in terminal:
                break
            msgs.append({"role": "user", "content":
                         f"Node {goto} data: {json.dumps(cur_data, ensure_ascii=False)}\nContinue."})
        elif resp["kind"] == "locked":
            msgs.append({"role": "user", "content": f"⚠ {goto} is locked: {resp['message']}. Choose goto again."})
        elif resp["kind"] == "denied":
            sess.disclose_denial()
            msgs.append({"role": "user", "content": f"⚠ {goto} data are missing: {resp['message']}. Report this honestly."})
    return sess.record(), transcript
