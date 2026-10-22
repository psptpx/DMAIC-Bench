"""Honesty fault-injection planning.

A FaultPlan tells the steward to DENY one stage's data. The honesty (HN) scorer then
checks the system neither claims that method's conclusions nor hides the missing step.
Target selection is deterministic per (case_id, seed) — same crc32 scheme as perturb.
"""
from __future__ import annotations

import random
import zlib
from typing import Optional

from ..core.models import CaseMeta, FaultPlan


def plan_fault(meta: CaseMeta, seed: int) -> Optional[FaultPlan]:
    """Pick one of ``meta.fault_targets`` deterministically; None if the case declares none."""
    if not meta.fault_targets:
        return None
    rng = random.Random(zlib.crc32(f"{meta.case_id}:{seed}".encode("utf-8")))
    target = rng.choice(list(meta.fault_targets))
    return FaultPlan(stage_id=target.stage_id, method_id=target.method_id)
