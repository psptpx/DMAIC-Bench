"""A2 — a general tool-using DMAIC agent: model + planning + memory + a real Python tool.

The decisive contrast with A0 (no-tools) is the compute tool: the SAME base model, given a sandbox
that runs its numpy/scipy code on the released data, can compute the gating statistics exactly and
therefore pass the methodology gates — so A2 is expected to jump far above A0's 0.00. That is the
whole point of "the contestant is an agent architecture, not a bare model".

Protocol (blind session): each turn the model outputs ONE JSON object, either
  {"tool":"python","code":"...print(...)..."}     # runs on DATA (current node) + HISTORY (all data)
or
  {"report":{"<dotted field>":value,...},"goto":"<next node>"}   # conclude the node and advance
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile

from dmaic_bench.v2.blind_session import BlindSession
from dmaic_bench.v2.llm_agent import _expand, _extract_json

SYSTEM = """You are a Six Sigma Black Belt independently leading a complete DMAIC improvement project. You have a Python calculation tool (numpy/scipy available); use it for actual calculations rather than mental arithmetic. Request data from the steward as needed; data are not supplied all at once.

You may start with a brief stage plan. After that, output only one JSON object per turn.

To calculate using the current node data:
{"tool":"python","code":"import numpy as np; x=np.array(DATA['process_run']['data']); print(...)"}
- DATA is the current node data dictionary; HISTORY contains all data obtained so far.
- Print the values you need; stdout will be returned to you.
- File, network, and system calls are prohibited.

To report the current node findings and advance:
{"report":{"<field>":<value>}, "goto":"<next node key>"}
- Use dotted names from the node's report_fields (e.g. imr.outOfControl / normality.pValue / cap.ppk).
- Report actual tool-calculated values. Disclose missing data; never fabricate results.
- Choose branches using your calculations and DMAIC methodology (e.g. investigate special causes instead of assessing capability when the process is out of control).
"""

_DENY = re.compile(r"\b(os\.|subprocess|sys\.|open\s*\(|eval\s*\(|exec\s*\(|__import__|socket|shutil|"
                   r"pathlib|requests|urllib|pickle|input\s*\()")


def _safe_exec(code: str, data: dict, history: dict, timeout: int = 20) -> str:
    if _DENY.search(code or ""):
        return "ERROR: Prohibited call (os/subprocess/open/eval/network etc.). Use numpy/scipy for pure computation only."
    preamble = ("import json,numpy as np\n"
                "try:\n import scipy.stats as st\nexcept Exception: st=None\n"
                f"DATA=json.loads({json.dumps(json.dumps(data or {}))})\n"
                f"HISTORY=json.loads({json.dumps(json.dumps(history or {}))})\n")
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(preamble + code)
        path = f.name
    try:
        r = subprocess.run([sys.executable, path], capture_output=True, text=True,
                           timeout=timeout)
        out = (r.stdout or "")[-3000:]
        if r.returncode != 0:
            out += "\n[stderr]\n" + (r.stderr or "")[-1500:]
        return out.strip() or "(no output — remember to print your results)"
    except subprocess.TimeoutExpired:
        return "ERROR: Execution timed out"
    finally:
        os.unlink(path)


def run_tool_agent_project(task, chat_fn, fault: bool = False, max_turns: int = 26):
    sess = BlindSession(task, fault=fault)
    brief = sess.briefing()
    history = {}
    entry_data = sess.request(brief["entry_node"]).get("data") or {}
    history[brief["entry_node"]] = entry_data
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content":
                 "Project briefing:\n" + json.dumps(brief, ensure_ascii=False, indent=2)
                 + f"\nEntry node {brief['entry_node']} data: {json.dumps(entry_data, ensure_ascii=False)}"
                 + "\nYou may give a stage plan first, then begin (calculate with Python or advance using report+goto)."}]
    transcript, current, cur_data = [], brief["entry_node"], entry_data
    terminal = [n["key"] for n in brief["nodes"] if n["phase"] == "control"]

    for _ in range(max_turns):
        resp = chat_fn(messages)
        content = resp["content"]
        transcript.append(content)
        messages.append({"role": "assistant", "content": content})
        try:
            act = _extract_json(content)
        except ValueError:
            messages.append({"role": "user", "content": "Output only one JSON object."})
            continue

        if act.get("tool") == "python":
            out = _safe_exec(act.get("code", ""), cur_data, history)
            messages.append({"role": "user", "content": f"[Python output]\n{out}\nContinue (tool or report+goto)."})
            continue

        report = _expand(act.get("report") or {})
        if report:
            sess.report(current, report)
        goto = act.get("goto")
        if not goto or (goto in terminal and current in terminal):
            break
        r = sess.request(goto)
        if r["kind"] == "data":
            current, cur_data = goto, (r["data"] or {})
            history[goto] = cur_data
            if goto in terminal:
                messages.append({"role": "user", "content":
                                 f"Reached the control stage {goto}, data: {json.dumps(cur_data, ensure_ascii=False)}. "
                                 "Give the final report and finish."})
                fin = chat_fn(messages); transcript.append(fin["content"])
                try:
                    fa = _extract_json(fin["content"])
                    if fa.get("report"):
                        sess.report(goto, _expand(fa["report"]))
                except ValueError:
                    pass
                break
            messages.append({"role": "user", "content":
                             f"Node {goto} data: {json.dumps(cur_data, ensure_ascii=False)}\nContinue."})
        elif r["kind"] == "locked":
            messages.append({"role": "user", "content":
                             f"⚠ Node {goto} is locked by a methodological gate: {r['message']}. Choose goto again."})
        elif r["kind"] == "denied":
            sess.disclose_denial()
            messages.append({"role": "user", "content":
                             f"⚠ Node {goto} data are missing/unavailable: {r['message']}. Disclose this honestly; do not fabricate results."})
    return sess.record(), transcript
