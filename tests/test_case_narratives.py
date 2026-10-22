"""A case's narrative must describe the characteristic its data carries.

adb_c31 shipped with the context paragraph of adb_c30 (cylinder-bore roughness) above solder
void-fraction data and a void-fraction goal (2026-09-18 review). The check is deliberately
coarse: the unit named in the define block, or a word from the title, must appear in the context.
"""
import sys
sys.path[:0] = [".", "harbor/src"]
from dmaic_harbor import v2_tasks as V   # noqa: E402


def test_context_names_the_characteristic():
    bad = []
    for cid, c in V.discover().items():
        blocks, _ = c.generate(c.seeds[0])
        define = blocks.get("define") or {}
        unit = str(define.get("unit") or "")
        if not unit:
            continue   # no unit in the charter to check against (adb_c38's title is abstract)
        words = {w.lower().strip(",.") for w in (c.title or "").split() if len(w) > 4}
        ctx = (c.context or "").lower()
        hit = (unit and unit.split()[0].lower() in ctx) or any(w in ctx for w in words)
        if not hit:
            bad.append((cid, c.title, unit))
    assert not bad, f"context does not mention the characteristic: {bad}"


def test_adb_c31_is_about_voids_not_bores():
    c = V.discover()["adb_c31"]
    assert "void" in c.context.lower() and "bore" not in c.context.lower()
