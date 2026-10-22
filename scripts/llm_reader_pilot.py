#!/usr/bin/env python3
"""Pilot: can an LLM read the reports the way the three black belts did?

    source scripts/agent-env.sh <provider>; python3 scripts/llm_reader_pilot.py <model> [--n N]

Feeds each study-2 packet (paper/blind_review_2026-09-19/blind/cases/V???/packet.md) with the
reviewers' protocol questions to an OpenAI-compatible chat endpoint and records the JSON answer
under paper/blind_review_2026-09-19/llm_reader/<model>/V???.json. Agreement with the human
majority is computed by scripts/llm_reader_agreement.py. The 60 units were never used to tune
any rule, so this is a held-out comparison; it is a pilot, not a validated reader.
"""
import argparse, json, os, sys, time, urllib.request
from pathlib import Path

ROOT = Path("paper/blind_review_2026-09-19")
PROTO = (ROOT / "blind" / "PROTOCOL.md").read_text()
SCHEMA = PROTO[PROTO.index("```json"):PROTO.index("```", PROTO.index("```json") + 7) + 3]


def ask(model, packet, blind_id):
    prompt = (PROTO + "\n\n---\n\nYou are one of the three independent reviewers. Read the packet below and answer for its "
              f"focal checkpoint. Reply with ONE JSON object only, in exactly the schema above, with blind_id \"{blind_id}\".\n\n" + packet)
    body = {"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0}
    req = urllib.request.Request(os.environ["OPENAI_BASE_URL"].rstrip("/") + "/chat/completions",
                                 data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"], "Content-Type": "application/json", "User-Agent": "dmaic-bench-reader/1.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        out = json.load(r)
    text = out["choices"][0]["message"]["content"]
    i, j = text.find("{"), text.rfind("}")
    return json.loads(text[i:j + 1]), out.get("usage")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("model"); ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--workers", type=int, default=1); a = ap.parse_args()
    outdir = ROOT / "llm_reader" / a.model; outdir.mkdir(parents=True, exist_ok=True)
    units = sorted(p.name for p in (ROOT / "blind" / "cases").glob("V*"))
    if a.n: units = units[:a.n]

    def one(u):
        dst = outdir / f"{u}.json"
        if dst.exists(): return
        packet = (ROOT / "blind" / "cases" / u / "packet.md").read_text()
        for attempt in range(4):
            try:
                ans, usage = ask(a.model, packet, u)
                ans["_usage"] = usage; dst.write_text(json.dumps(ans, indent=1)); print(u, ans.get("gate_verdict"), ans.get("trajectory_verdict"), flush=True); return
            except Exception as e:
                print(u, "retry", attempt, type(e).__name__, str(e)[:120], flush=True); time.sleep(10 * (attempt + 1))

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        list(ex.map(one, units))


if __name__ == "__main__":
    main()
