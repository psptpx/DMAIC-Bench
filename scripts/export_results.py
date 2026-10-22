#!/usr/bin/env python3
"""Export the compact per-trial results the paper's tables regenerate from.

    python3 scripts/export_results.py [--out results-<tag>.tar.gz]

For every trial under harbor/jobs/<job>/<trial>/ the archive keeps
  verifier-rescored/reward.json, verifier-rescored/scorecard.json   (the scores used in the paper)
  verifier/reward.json                                             (the in-container score)
  artifacts/trace.json, artifacts/report.md, artifacts/steward-audit.jsonl
  config.json, result.json
and drops the agent's terminal recording and turn record (agent/), which are released
separately with the camera-ready. Job directories are kept by name so
scripts/restraint_analysis.py runs unchanged after `tar xzf` into harbor/.
"""
import argparse, os, tarfile, time
from pathlib import Path

KEEP = ("verifier-rescored/reward.json", "verifier-rescored/scorecard.json", "verifier/reward.json",
        "artifacts/trace.json", "artifacts/report.md", "artifacts/steward-audit.jsonl", "config.json", "result.json")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default=f"results-{time.strftime('%Y%m%d')}.tar.gz"); a = ap.parse_args()
    root = Path("harbor/jobs"); n = 0; size = 0
    with tarfile.open(a.out, "w:gz") as tar:
        for job in sorted(p for p in root.iterdir() if p.is_dir()):
            for meta in ("config.json", "lock.json", "result.json"):
                if (job / meta).exists():
                    tar.add(job / meta, arcname=f"jobs/{job.name}/{meta}")
            for trial in sorted(p for p in job.iterdir() if p.is_dir() and p.name.startswith("dmaic-")):
                for rel in KEEP:
                    f = trial / rel
                    if f.exists():
                        tar.add(f, arcname=f"jobs/{job.name}/{trial.name}/{rel}"); size += f.stat().st_size
                n += 1
    print(f"{a.out}: {n} trials, {size/1e6:.0f} MB uncompressed, {Path(a.out).stat().st_size/1e6:.0f} MB archive")


if __name__ == "__main__":
    main()
