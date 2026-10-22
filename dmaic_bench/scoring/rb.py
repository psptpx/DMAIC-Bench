"""RB — Robustness: performance drop between clean and dirty variants of the same task.

Cards pair on (case_id, tier, seed, variant-stripped task name) so the ONLY thing that differs
inside a pair is the data perturbation. The pair score is harmonic(MS recall, NF ratio) —
robustness is about still finding and computing the right things, not about honesty (which is
gated globally by TGS).
"""
from __future__ import annotations

import re

from .tgs import harmonic

_VARIANT_TOKEN = re.compile(r"[-_.](clean|dirty)(?=[-_.]|$)")


def pair_key(card: dict) -> tuple:
    base = _VARIANT_TOKEN.sub("", card["task_id"])
    return (card["case_id"], card["tier"], card["seed"], base)


def _pair_score(card: dict) -> float:
    return harmonic(card["ms"]["recall"], card["nf"]["summary"]["ratio"])


def robustness_delta(clean_cards: list, dirty_cards: list) -> dict:
    clean_by = {pair_key(c): c for c in clean_cards}
    dirty_by = {pair_key(c): c for c in dirty_cards}
    per_pair = []
    for key in sorted(clean_by.keys() & dirty_by.keys()):
        cs, ds = _pair_score(clean_by[key]), _pair_score(dirty_by[key])
        per_pair.append({"key": list(key), "clean": cs, "dirty": ds, "delta": cs - ds})
    n = len(per_pair)
    mean_clean = sum(p["clean"] for p in per_pair) / n if n else 0.0
    mean_dirty = sum(p["dirty"] for p in per_pair) / n if n else 0.0
    return {
        "pairs": n,
        "mean_clean": mean_clean,
        "mean_dirty": mean_dirty,
        "delta": mean_clean - mean_dirty,
        "per_pair": per_pair,
    }
