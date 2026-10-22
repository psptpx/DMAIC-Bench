"""Deterministic dirty-data perturbation (RB robustness variants).

Ported from the perturber of the originating evaluation harness (a separate, unpublished
codebase: `_dirty_rng` / `_apply_dirty` / `dirty_preview`), with the same design
invariants:

  - DETERMINISTIC across processes: the rng is seeded from crc32(f"{case_id}:{seed}"),
    never from str hash() (which is salted per process via PYTHONHASHSEED);
  - the caller's dict is NEVER mutated (deep copy first — legacy providers shared
    module-level literal lists, and native generators may cache too);
  - truths are computed from CLEAN data and are NOT touched here: the perturbations
    (renames, None holes, stringified numbers, distractor keys) must be survivable by
    the system under test without changing the statistical conclusions.

Differences vs the legacy `_apply_dirty` (documented for reviewers):
  - legacy used a hand-written per-case DIRTY_PLAN dict; here the plan is derived
    generically from the block contents (built-in synonym table + structural rules),
    so new cases get dirty variants for free;
  - legacy renamed via deep substring replace (keys AND string values); here only
    top-level KEYS are renamed — string values stay intact so business text is not
    silently rewritten;
  - legacy shuffled the top-level key order; here order is kept (renames/distractor
    already break naive positional parsing, and stable order keeps previews readable).
"""
from __future__ import annotations

import copy
import random
import zlib

# semantic scalar keys: renaming is allowed, but their VALUES must never be nulled
# or stringified — losing an LSL/target silently changes the problem statement.
_PROTECTED_NORMALIZED = {
    "lsl", "usl", "target", "targetvalue",
    "hypothesizedmedian", "hypothesizedmean", "hypothesizedproportion",
    "confidencelevel", "alpha",
}

# built-in key synonym table (exact top-level key -> candidate replacements)
_SYNONYMS = {
    "data": ("values", "measurements"),
    "values": ("data", "readings"),
    "group1": ("groupA",),
    "group2": ("groupB",),
    "groups": ("group_data",),
    "counts": ("defect_counts",),
    "defects": ("defect_counts",),
    "x": ("x_values",),
    "y": ("y_values",),
    "unit": ("uom",),
    "lsl": ("lower_spec", "LSL"),
    "usl": ("upper_spec", "USL"),
    "target": ("target_value",),
    "hypothesizedMedian": ("hypothesized_median",),
    "hypothesizedMean": ("hypothesized_mean",),
    "subgroupSize": ("subgroup_size",),
    "sampleSizes": ("sample_sizes",),
}

# Preserve the published English suffix and distractor order.
_ORIGINAL_SUFFIX = {"en": "_original"}

# Stable candidate order preserves seeded perturbations.
_DISTRACTORS_BY_LOCALE = {
    "en": (
        ("recorder", "J. Zhang"),
        ("remark", "night-shift transcription"),
        ("shift", "day shift B"),
        ("ambient", "23C/45%RH"),
    ),
}


def _rng(case_id: str, seed: int) -> random.Random:
    return random.Random(zlib.crc32(f"{case_id}:{seed}".encode("utf-8")))


def _normalized(key: str) -> str:
    return key.lower().replace("_", "").replace("-", "")


def _is_protected(key) -> bool:
    return isinstance(key, str) and _normalized(key) in _PROTECTED_NORMALIZED


def _has_cjk(s: str) -> bool:
    return any(0x4E00 <= ord(ch) <= 0x9FFF for ch in s)


def block_locale(block) -> str:
    """The official perturbation vocabulary is English."""
    return "en"


def _is_number(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _collect_numeric_arrays(node, path, out):
    """Collect (path, list-ref) for every numeric array of len>=8 whose key isn't protected."""
    if isinstance(node, dict):
        for k, v in node.items():
            if _is_protected(k):
                continue
            _collect_numeric_arrays(v, path + (str(k),), out)
    elif isinstance(node, list):
        if len(node) >= 8 and all(_is_number(v) for v in node):
            out.append((path, node))
        else:
            for i, v in enumerate(node):
                if isinstance(v, (dict, list)):
                    _collect_numeric_arrays(v, path + (f"[{i}]",), out)


def _perturb_block(block, rng):
    """Return (dirty_block, log). Mutation happens on a deep copy only."""
    log = {"renames": {}, "holes": {}, "stringified": None, "distractor": None}
    if not isinstance(block, dict):
        return copy.deepcopy(block), log
    block = copy.deepcopy(block)

    # b. None holes: every numeric array of len>=8 loses 1-2 elements
    arrays = []
    _collect_numeric_arrays(block, (), arrays)
    for path, arr in arrays:
        n = rng.randint(1, 2)
        idxs = sorted(rng.sample(range(len(arr)), n))
        for i in idxs:
            arr[i] = None
        log["holes"][".".join(path)] = idxs

    # d. stringify: pick one numeric array, turn 1 surviving element into its string form
    if arrays:
        path, arr = arrays[rng.randrange(len(arrays))]
        numeric_idx = [i for i, v in enumerate(arr) if _is_number(v)]
        if numeric_idx:
            i = numeric_idx[rng.randrange(len(numeric_idx))]
            arr[i] = str(arr[i])
            log["stringified"] = (".".join(path), i)

    # c. distractor: inject 1 irrelevant key (in the block's own script)
    locale = block_locale(block)
    candidates = [(k, v) for k, v in _DISTRACTORS_BY_LOCALE[locale] if k not in block]
    if arrays:
        n = len(arrays[0][1])
        if "row_id" not in block:
            candidates.append(("row_id", list(range(1, n + 1))))
    if candidates:
        k, v = candidates[rng.randrange(len(candidates))]
        block[k] = v
        log["distractor"] = k

    # a. key synonym renames: 1-2 renameable top-level keys (protected keys MAY be
    # renamed — only their values are sacred).
    #
    # EVERY string key is renameable, regardless of script. The predicate used to be
    # `k in _SYNONYMS or _has_cjk(k)`, which made the rename step fire on a Chinese table's
    # every column but only on the 18 tabulated English names — so an English block drew from a
    # smaller pool, sometimes an empty one, and its dirty variant was strictly LESS perturbed
    # than its Chinese twin. rb.py pairs clean↔dirty and reports the delta, so that difference
    # would have arrived as "the English arm is more robust" rather than as what it is: a
    # weaker perturbation. Language may pick the naming FLAVOUR (`_ORIGINAL_SUFFIX`), never the
    # number of keys touched.
    renameable = [k for k in block if isinstance(k, str) and k != log["distractor"]]
    if renameable:
        n = rng.randint(1, min(2, len(renameable)))
        chosen = rng.sample(renameable, n)
        renames = {}
        for k in chosen:
            if k in _SYNONYMS:
                renames[k] = rng.choice(_SYNONYMS[k])
            else:
                renames[k] = k + _ORIGINAL_SUFFIX["en"]
        block = {renames.get(k, k): v for k, v in block.items()}
        log["renames"] = renames

    return block, log


def _dirty(case_id: str, blocks: dict, seed: int):
    rng = _rng(case_id, seed)
    out, logs = {}, {}
    for stage_id, payload in blocks.items():  # insertion order => deterministic rng stream
        out[stage_id], logs[stage_id] = _perturb_block(payload, rng)
    return out, logs


def dirty_blocks(case_id: str, blocks: dict, seed: int) -> dict:
    """Deterministically perturb ``blocks`` (stage_id -> payload). Original dict untouched."""
    return _dirty(case_id, blocks, seed)[0]


def preview(case_id: str, blocks: dict, seed: int) -> str:
    """Human-readable diff summary of the deterministic perturbation plan."""
    _, logs = _dirty(case_id, blocks, seed)
    lines = [f"=== dirty preview {case_id} seed={seed} (crc32-seeded, deterministic) ==="]
    for stage_id, log in logs.items():
        holes = ", ".join(f"{p}@{idx}" for p, idx in log["holes"].items()) or "-"
        strf = f"{log['stringified'][0]}[{log['stringified'][1]}]" if log["stringified"] else "-"
        lines.append(
            f"[{stage_id}] renames={log['renames'] or '-'} "
            f"nones={holes} stringified={strf} distractor={log['distractor'] or '-'}"
        )
    return "\n".join(lines)
