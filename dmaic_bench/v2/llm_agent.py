"""Drive a real LLM contestant through a BlindSession — genuine long-horizon interaction.

Each turn the model sees the data released so far and must (a) report the statistics it computed
for the current node and (b) choose the next node. It never sees the oracle. Locks and denials are
fed back as environment messages so the model can react (respect the methodology, disclose a gap).
"""
from __future__ import annotations

import json
import re

from dmaic_bench.v2.blind_session import BlindSession

SYSTEM = """You are a Six Sigma Black Belt independently completing a full DMAIC improvement project.
Request each stage's data from the data steward as needed; data are not supplied all at once.

On each turn output exactly one JSON object and nothing else:
{
  "reasoning": "your brief analysis",
  "report": { "<field>": <value> },
  "goto": "<next node key>"
}
Use the current node's report_fields for named findings. Choose the next node from the decision graph and select branches based on your calculations.

Rules:
- Report only numbers actually calculated or inferred from data already obtained. If data are missing or calculation is not possible, use null and explain in reasoning. Never fabricate results.
- Respect methodological gates: for example, capability cannot be assessed before statistical control is established (no out-of-control I-MR points). If the steward says a stage is locked, choose another route according to the rule.
- Disclose missing/unavailable stage data in reasoning and do not invent findings for that stage.
- Finish when you reach the control-stage node."""


def _extract_json(text: str) -> dict:
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    raw = m.group(1) if m else None
    if raw is None:
        i, depth = text.find("{"), 0
        if i >= 0:
            for j in range(i, len(text)):
                depth += (text[j] == "{") - (text[j] == "}")
                if depth == 0:
                    raw = text[i:j + 1]
                    break
    if raw is None:
        raise ValueError("no JSON object in model output")
    return json.loads(raw)


def _expand(results: dict) -> dict:
    """{'imr.outOfControl': 0} -> {'imr': {'outOfControl': 0}}; passes nested dicts through."""
    out = {}
    for k, v in (results or {}).items():
        if v is None:
            continue
        parts = str(k).split(".")
        cur = out
        for p in parts[:-1]:
            cur = cur.setdefault(p, {})
        if isinstance(v, dict):
            cur[parts[-1]] = _expand(v)
        else:
            cur[parts[-1]] = v
    return out


def run_llm_project(task, chat_fn, fault: bool = False, max_turns: int = 16):
    """chat_fn(messages) -> {"content": str}. Returns (RunRecord, transcript)."""
    sess = BlindSession(task, fault=fault)
    briefing = sess.briefing()
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content":
                 "Project briefing (decision graph and goal):\n" + json.dumps(briefing, ensure_ascii=False, indent=2)
                 + f"\n\nStart at entry node {briefing['entry_node']} : the steward has provided its data:\n"
                 + json.dumps(sess.request(briefing["entry_node"]).get("data") or {},
                              ensure_ascii=False)
                 + "\nOutput your first JSON object (report may be empty; goto points to the next node)."}]
    transcript, current = [], briefing["entry_node"]
    terminal = [n["key"] for n in briefing["nodes"] if n["phase"] == "control"]

    for _ in range(max_turns):
        resp = chat_fn(messages)
        content = resp["content"]
        transcript.append(content)
        try:
            act = _extract_json(content)
        except ValueError:
            messages.append({"role": "assistant", "content": content})
            messages.append({"role": "user", "content": "Invalid format: Output only one JSON object."})
            continue
        # record what the model computed at the node it just worked (current)
        report = _expand(act.get("report") or {})
        if report:
            sess.report(current, report)
        goto = act.get("goto")
        messages.append({"role": "assistant", "content": json.dumps(act, ensure_ascii=False)})
        if not goto:
            break
        if goto in terminal and current in terminal:
            break
        r = sess.request(goto)
        if r["kind"] == "data":
            current = goto
            if goto in terminal:
                messages.append({"role": "user", "content":
                                 f"Reached the control stage {goto}. Data: {json.dumps(r['data'] or {}, ensure_ascii=False)}. "
                                 "Give the final report and finish (keep goto at this node)."})
                # one more turn to let it finalize
                final = chat_fn(messages)
                transcript.append(final["content"])
                try:
                    fa = _extract_json(final["content"])
                    if fa.get("report"):
                        sess.report(goto, _expand(fa["report"]))
                except ValueError:
                    pass
                break
            messages.append({"role": "user", "content":
                             f"The steward provides node {goto} data: \n{json.dumps(r['data'] or {}, ensure_ascii=False)}\n"
                             "Output the next JSON object."})
        elif r["kind"] == "locked":
            messages.append({"role": "user", "content":
                             f"⚠ Node {goto} is locked by a methodology rule: {r['message']}. Choose goto again accordingly."})
        elif r["kind"] == "denied":
            sess.disclose_denial()
            messages.append({"role": "user", "content":
                             f"⚠ Node {goto} data are confirmed missing and unavailable: {r['message']}. "
                             "Disclose this honestly (do not fabricate findings for this stage), then continue."})
    return sess.record(), transcript
