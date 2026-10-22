"""Deterministic data steward — hands out one stage's data per request.

The steward is the bench's "process owner": contestants must ASK for data by topic
(one batch per turn). Routing is pure string matching — no LLM, fully reproducible:

  1. lowercase the request text; among UNRELEASED stages, a stage matches if any of
     its topics occurs as a substring; the earliest-declared matching stage wins;
  2. no topic hit but the text signals continuation (next/more/continue)
     -> next unreleased stage in declaration order;
  3. the matched stage is the fault-plan stage -> "denied" with the plan's denial
     message (the stage is consumed: it will never be released later);
  4. nothing unreleased remains -> "exhausted";
  5. otherwise -> "unavailable", listing the remaining stage labels.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Optional

from ..core.models import TaskInstance

_CONTINUATION = re.compile(r"next|more|continue")


@dataclass
class StewardResponse:
    kind: str                    # "data" | "denied" | "unavailable" | "exhausted"
    stage_id: Optional[str]
    label: Optional[str]
    message: str                 # ready to send to the agent verbatim


class DataSteward:
    def __init__(self, task: TaskInstance):
        self._task = task
        self._stages = list(task.stages)          # declaration order
        self._pending = [s.stage_id for s in self._stages]  # unreleased, in order
        self._log = []
        self._turn = 0

    # ------------------------------------------------------------------ public API

    def request(self, text: str) -> StewardResponse:
        self._turn += 1
        resp = self._route(text or "")
        self._log.append({"turn": self._turn, "request_text": text,
                          "kind": resp.kind, "stage_id": resp.stage_id})
        return resp

    def remaining(self) -> list:
        """Unreleased stage_ids (a denied fault stage is consumed, hence absent)."""
        return list(self._pending)

    def audit_log(self) -> list:
        return [dict(e) for e in self._log]

    # ------------------------------------------------------------------ routing

    def _route(self, text: str) -> StewardResponse:
        if not self._pending:
            return StewardResponse("exhausted", None, None,
                                   "All data has been provided; no batches remain.")
        lowered = text.lower()
        stage = None
        for s in self._stages:  # declaration order => earliest match wins
            if s.stage_id in self._pending and any(t.lower() in lowered for t in s.topics):
                stage = s
                break
        if stage is None and _CONTINUATION.search(lowered):
            stage = self._stage_by_id(self._pending[0])
        if stage is None:
            labels = ", ".join(self._stage_by_id(sid).label for sid in self._pending)
            return StewardResponse("unavailable", None, None,
                                   f"That data is unavailable. Available data topics: {labels}")

        self._pending.remove(stage.stage_id)
        fault = self._task.fault
        if fault is not None and stage.stage_id == fault.stage_id:
            return StewardResponse("denied", stage.stage_id, stage.label,
                                   fault.denial_message)
        payload = self._task.data.blocks.get(stage.stage_id, {})
        message = f"[{stage.label}]\n{json.dumps(payload, ensure_ascii=False)}"
        return StewardResponse("data", stage.stage_id, stage.label, message)

    def _stage_by_id(self, stage_id: str):
        return next(s for s in self._stages if s.stage_id == stage_id)
