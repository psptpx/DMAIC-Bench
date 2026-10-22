"""Validate frozen independent human expert reviews and produce descriptive agreement tables.

Uses only reviewer outputs and the supplied blinded inputs. Never reads coordinator
material, original system identities, reference answers, or benchmark scores.
"""
from pathlib import Path
from collections import Counter
from itertools import combinations
import csv
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent
RIDS = ["R1", "R2", "R3"]
IDS = [f"V{i:03d}" for i in range(1, 61)]
ENUMS = {
    "gate_verdict": {"STOP", "GO", "UNDETERMINED"},
    "report_asserts_forbidden_conclusion": {"YES", "NO", "NOT_APPLICABLE"},
    "report_recommends_forbidden_action": {"YES", "NO", "NOT_APPLICABLE"},
    "report_withholds_warranted_conclusion": {"YES", "NO", "NOT_APPLICABLE"},
    "report_completeness": {"COMPLETE", "STOPPED_APPROPRIATELY", "UNREACHED", "EVASIVE", "EMPTY"},
    "extra_computation": {"NONE", "RESTRICTED_DESCRIPTIVE", "VALID_ALTERNATIVE", "UNACCEPTABLE", "MIXED"},
    "trajectory_verdict": {"ACCEPTABLE", "UNACCEPTABLE", "MIXED", "INSUFFICIENT"},
}
LISTS = ["forbidden_at_checkpoint", "permitted_at_checkpoint", "forbidden_quotes", "allowed_alternatives", "evidence"]
STRINGS = ["extra_computation_detail", "rationale", "numerical_check", "evidence_problem"]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(text):
    # Formatting/whitespace only: no removal of words or substantive punctuation.
    return re.sub(r"\s+", " ", re.sub(r"[*_`#]", "", text)).strip()


def majority(values):
    label, count = Counter(values).most_common(1)[0]
    return label if count >= 2 else "NO_MAJORITY"


def main():
    errors, warnings, reviews, frozen = [], [], {}, {}
    manifest = json.loads((BASE / "input_manifest.json").read_text())
    for rid in RIDS:
        inp = BASE / rid / "blind"
        expected_files = manifest["reviewer_input_files"][rid]
        actual_files = {str(p.relative_to(inp)) for p in inp.rglob("*") if p.is_file()}
        if actual_files != set(expected_files):
            errors.append(f"{rid}: input file set changed")
        for rel, expected_hash in expected_files.items():
            if not (inp / rel).exists() or digest(inp / rel) != expected_hash:
                errors.append(f"{rid}: input hash mismatch: {rel}")
        path = BASE / rid / "output" / f"review_{rid}.json"
        synthesis = path.with_name(f"synthesis_{rid}.md")
        if not path.exists() or not synthesis.exists():
            errors.append(f"{rid}: final JSON or synthesis absent")
            continue
        data = json.loads(path.read_text())
        for key in ["reviewer_id", "reviewer_type", "perspective", "blinding_compliance", "review_method", "sources", "reviews"]:
            if key not in data:
                errors.append(f"{rid}: missing top-level {key}")
        if data.get("reviewer_id") != rid:
            errors.append(f"{rid}: wrong reviewer_id")
        if data.get("reviewer_type") != "Human":
            errors.append(f"{rid}: incorrect human reviewer_type")
        entries = data.get("reviews", [])
        if len(entries) != 60 or Counter(r.get("blind_id") for r in entries) != Counter(IDS):
            errors.append(f"{rid}: case coverage is not exactly V001–V060 once each")
        order = json.loads((inp / f"order_{rid}.json").read_text())
        if [r.get("blind_id") for r in entries] != order:
            warnings.append(f"{rid}: JSON array is not in assigned reading order; check reading log/disclosure")
        by_id = {r["blind_id"]: r for r in entries}
        reviews[rid] = by_id
        for case, row in by_id.items():
            for key, values in ENUMS.items():
                if row.get(key) not in values:
                    errors.append(f"{rid}/{case}: invalid or absent {key}: {row.get(key)!r}")
            for key in LISTS:
                if not isinstance(row.get(key), list) or not all(isinstance(x, str) for x in row[key]):
                    errors.append(f"{rid}/{case}: invalid list {key}")
            for key in STRINGS:
                if not isinstance(row.get(key), str) or not row[key].strip():
                    errors.append(f"{rid}/{case}: absent or empty {key}")
            if type(row.get("confidence")) is not int or not 1 <= row["confidence"] <= 5:
                errors.append(f"{rid}/{case}: confidence must be integer 1–5")
            yes = any(row.get(k) == "YES" for k in ["report_asserts_forbidden_conclusion", "report_recommends_forbidden_action"])
            if yes != bool(row.get("forbidden_quotes")):
                errors.append(f"{rid}/{case}: YES fields and forbidden_quotes disagree")
            report = (inp / "cases" / case / "report.md").read_text()
            for quote in row.get("forbidden_quotes", []):
                if quote not in report and normalized(quote) not in normalized(report):
                    warnings.append(f"{rid}/{case}: quote requires manual verification: {quote}")
        frozen[rid] = {
            "review_json": str(path.relative_to(BASE)), "review_sha256": digest(path),
            "synthesis_md": str(synthesis.relative_to(BASE)), "synthesis_sha256": digest(synthesis),
        }
    validation = {"errors": errors, "warnings": warnings, "input_hashes_verified": not any("input" in e for e in errors)}
    (BASE / "validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n")
    if errors:
        print(json.dumps(validation, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    agreement = {}
    for key in ENUMS:
        counts = {rid: dict(Counter(reviews[rid][case][key] for case in IDS)) for rid in RIDS}
        unanimous = [case for case in IDS if len({reviews[rid][case][key] for rid in RIDS}) == 1]
        pairwise = {}
        for a, b in combinations(RIDS, 2):
            n = sum(reviews[a][case][key] == reviews[b][case][key] for case in IDS)
            pairwise[f"{a}_{b}"] = {"agree": n, "total": 60, "fraction": n / 60}
        agreement[key] = {
            "per_reviewer_counts": counts,
            "unanimous_count": len(unanimous), "total": 60,
            "unanimous_fraction": len(unanimous) / 60,
            "pairwise": pairwise,
            "majority_counts": dict(Counter(majority([reviews[rid][case][key] for rid in RIDS]) for case in IDS)),
            "disagreement_ids": [case for case in IDS if case not in unanimous],
        }

    rows = []
    for case in IDS:
        packet = (BASE / "R1" / "blind" / "cases" / case / "packet.md").read_text()
        focal = next(line.removeprefix("Focal assessment: ") for line in packet.splitlines() if line.startswith("Focal assessment:"))
        row = {"blind_id": case, "focal_assessment": focal}
        for key in ENUMS:
            votes = [reviews[rid][case][key] for rid in RIDS]
            for rid, value in zip(RIDS, votes):
                row[f"{rid}_{key}"] = value
            row[f"majority_{key}"] = majority(votes)
            row[f"unanimous_{key}"] = len(set(votes)) == 1
        rows.append(row)
    with (BASE / "case_comparison.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (BASE / "case_comparison.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    (BASE / "agreement_summary.json").write_text(json.dumps(agreement, ensure_ascii=False, indent=2) + "\n")
    focal_breakdown = {}
    for row in rows:
        group = focal_breakdown.setdefault(row["focal_assessment"], {
            "cases": [], "majority_gate_counts": Counter(),
            "majority_trajectory_counts": Counter(), "gate_disagreements": [],
            "trajectory_disagreements": [],
        })
        group["cases"].append(row["blind_id"])
        group["majority_gate_counts"][row["majority_gate_verdict"]] += 1
        group["majority_trajectory_counts"][row["majority_trajectory_verdict"]] += 1
        if not row["unanimous_gate_verdict"]:
            group["gate_disagreements"].append(row["blind_id"])
        if not row["unanimous_trajectory_verdict"]:
            group["trajectory_disagreements"].append(row["blind_id"])
    (BASE / "focal_breakdown.json").write_text(json.dumps(focal_breakdown, ensure_ascii=False, indent=2) + "\n")
    md = [
        "# Case-by-case independent human expert reviews", "",
        "These are independent human expert Master Black Belt judgments. "
        "Original first-round votes are retained. Majority labels summarize votes and are not adjudicated truth.", "",
        "## Index", "",
        "| Case | R1 gate / conduct | R2 gate / conduct | R3 gate / conduct |", 
        "|---|---|---|---|",
    ]
    for case in IDS:
        cells = [f"{reviews[rid][case]['gate_verdict']} / {reviews[rid][case]['trajectory_verdict']}" for rid in RIDS]
        md.append(f"| [{case}](#{case.lower()}) | " + " | ".join(cells) + " |")
    for row in rows:
        case = row["blind_id"]
        md.extend(["", f"## {case}", "", row["focal_assessment"], "",
                   f"Majority gate: **{row['majority_gate_verdict']}**. Majority conduct: **{row['majority_trajectory_verdict']}**.", ""])
        for rid in RIDS:
            r = reviews[rid][case]
            md.extend([f"### {rid}", "",
                f"**Gate: {r['gate_verdict']}; conduct: {r['trajectory_verdict']}; confidence: {r['confidence']}/5.**", "",
                r["rationale"], "",
                f"Report asserts forbidden conclusion: {r['report_asserts_forbidden_conclusion']}; "
                f"recommends forbidden action: {r['report_recommends_forbidden_action']}; "
                f"withholds warranted conclusion: {r['report_withholds_warranted_conclusion']}; "
                f"completeness: {r['report_completeness']}.", "",
            ])
            for key, label in [
                ("forbidden_at_checkpoint", "Forbidden at checkpoint"),
                ("permitted_at_checkpoint", "Permitted at checkpoint"),
                ("forbidden_quotes", "Report quotations supporting YES judgments"),
                ("allowed_alternatives", "Allowed alternatives"),
                ("evidence", "Evidence"),
            ]:
                md.extend([f"**{label}**", ""])
                md.extend([f"- {item}" for item in r[key]] or ["None."])
                md.append("")
            md.extend([
                f"**Extra computation: {r['extra_computation']}.** {r['extra_computation_detail']}", "",
                f"**Numerical check:** {r['numerical_check']}", "",
                f"**Evidence problem:** {r['evidence_problem']}", "",
            ])
    (BASE / "case_reviews.md").write_text("\n".join(md) + "\n")
    (BASE / "frozen_reviews.json").write_text(json.dumps(frozen, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"validation": validation, "agreement": {k: agreement[k] for k in ["gate_verdict", "trajectory_verdict"]}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
