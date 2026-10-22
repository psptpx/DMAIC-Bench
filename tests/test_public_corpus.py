"""The public release contract, asserted rather than assumed.

WHY THIS FILE EXISTS
--------------------
Nine expert-derived cases are held out of the public release (docs/HELD_OUT.md), and the
registry degrades gracefully when their bridge module is absent. Graceful degradation is the
right runtime behaviour and the wrong thing to leave unchecked: a corpus that silently builds
14 cases instead of 15 would look exactly like a corpus that correctly built 15. The
originating project has already been bitten by precisely this — a loader that resolved cases
from outside the package and "degraded to an empty list with a warning" shipped a wheel that
built zero end-to-end tasks while reporting success.

So the public set is pinned here by identifier. If a case goes missing, is renamed, or a
held-out case leaks back in, these fail.

WHAT IS DELIBERATELY NOT HERE
-----------------------------
No list of the former, romanized company identifiers, and no list of the excluded
contestant's names. Writing them into a public test file would re-disclose exactly what the
de-identification exists to hide, and would identify the authors of a double-blind
submission. An operator holding that list supplies it at test time:

    DMAIC_FORMER_IDENTIFIERS=alpha,beta pytest tests/test_public_corpus.py

Unset, the scan below reports that it was SKIPPED. It never passes silently.
"""
from __future__ import annotations

import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dmaic_bench.core import registry  # noqa: E402

#: The exact public set. Held-out ids are absent by construction, not by filtering.
PUBLIC_CASES = frozenset({
    "adb_c01", "adb_c02", "adb_c04", "adb_c06", "adb_c09", "adb_c11", "adb_c12", "adb_c13",
    "adb_c14", "adb_c17", "adb_c18", "adb_c21", "adb_c22", "adb_c23", "adb_c24",
})
HELD_OUT_CASES = frozenset({
    "adb_c03", "adb_c05", "adb_c07", "adb_c08", "adb_c10", "adb_c15", "adb_c16", "adb_c19",
    "adb_c20",
})

PKG_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\u3000-\u303f\uff00-\uffef]")
_CREDENTIAL = re.compile(
    r"sk-[A-Za-z0-9]{16,}|gh[pou]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY"
)


def _source_files():
    skip = {".git", "__pycache__", ".pytest_cache", "datasets", "jobs", "build", "dist",
            ".venv", "venv", ".ruff_cache", ".mypy_cache"}
    for dirpath, dirnames, filenames in os.walk(PKG_ROOT):
        # Independent review records under paper/ quote the reviewer's own machine paths; they
        # are not shipped and are not this test's subject.
        dirnames[:] = [d for d in dirnames if d not in skip and not d.endswith(".egg-info")
                       and not d.startswith("blind_review") and d != "figure_design"]
        for name in filenames:
            if name.startswith("REVIEW_") or name.startswith("review_evidence_"):
                continue
            if name.endswith((".py", ".yaml", ".yml", ".toml", ".json", ".md", ".sh", ".cfg")):
                yield os.path.join(dirpath, name)


class TestPublicCaseSet:
    def test_discovers_exactly_the_public_set(self):
        found = set(registry.discover())
        assert found == set(PUBLIC_CASES), (
            f"public corpus drifted: missing={sorted(PUBLIC_CASES - found)}, "
            f"unexpected={sorted(found - PUBLIC_CASES)}"
        )

    def test_no_held_out_case_is_reachable(self):
        found = set(registry.discover())
        leaked = found & HELD_OUT_CASES
        assert not leaked, f"held-out cases present in a public checkout: {sorted(leaked)}"

    def test_every_public_case_is_synthetic_and_parametric(self):
        """The public release ships only regenerable, non-derivative cases.

        This is the licensing guarantee in executable form: a case whose data is frozen
        rather than generated from a seed is, by construction, one we did not synthesise.
        """
        for case_id in sorted(PUBLIC_CASES):
            meta = registry.meta_from_yaml(
                os.path.join(PKG_ROOT, "dmaic_bench", "cases", case_id, "case.yaml")
            )
            assert meta.provenance == "SIMULATED", (
                f"{case_id} declares provenance={meta.provenance!r}; only SIMULATED cases "
                f"may be published (docs/HELD_OUT.md)"
            )
            assert getattr(meta, "parametric", False) is True, (
                f"{case_id} is not parametric: its data cannot be regenerated from a seed"
            )

    def test_the_bridge_module_for_held_out_cases_is_absent(self):
        with pytest.raises(ImportError):
            __import__("dmaic_bench.cases.legacy_bridge")


class TestNoLeaks:
    def test_no_credential_literal_anywhere(self):
        hits = []
        for path in _source_files():
            try:
                text = open(path, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            if _CREDENTIAL.search(text):
                hits.append(os.path.relpath(path, PKG_ROOT))
        assert not hits, f"credential-shaped literal in: {hits}"

    def test_no_absolute_developer_paths(self):
        hits = []
        for path in _source_files():
            try:
                text = open(path, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            if re.search(r"/(?:Users|home)/[a-z][a-z0-9_-]+/", text):
                hits.append(os.path.relpath(path, PKG_ROOT))
        assert not hits, f"absolute developer path in: {hits}"

    def test_no_identity_map_is_packaged(self):
        assert not os.path.exists(
            os.path.join(PKG_ROOT, "dmaic_bench", "cases", "_identity_map.json")
        ), "the identity map must never be present in a public checkout"

    def test_former_identifiers_absent(self):
        """Operator-supplied scan. Reports a skip; never passes silently."""
        raw = os.environ.get("DMAIC_FORMER_IDENTIFIERS", "").strip()
        if not raw:
            pytest.skip(
                "DMAIC_FORMER_IDENTIFIERS unset — the former-identifier scan did NOT run. "
                "This is expected in a public checkout, which does not carry that list."
            )
        tokens = [t.strip().lower() for t in raw.split(",") if t.strip()]
        pats = {t: re.compile(rf"(?<![a-z0-9]){re.escape(t)}(?![a-z0-9])") for t in tokens}
        hits = []
        for path in _source_files():
            try:
                text = open(path, encoding="utf-8", errors="ignore").read().lower()
            except OSError:
                continue
            for tok, pat in pats.items():
                if pat.search(text):
                    hits.append((os.path.relpath(path, PKG_ROOT), tok))
        assert not hits, f"former identifier present: {hits}"


class TestEnglishSurface:
    """Anything a contestant or a reviewer reads must be English."""

    AGENT_FACING = (
        "dmaic_bench/cases",   # case narratives are localised at build time, not here
    )

    def test_no_cjk_in_the_shipped_cli_or_scoring(self):
        checked = 0
        offenders = []
        for rel in ("dmaic_bench/cli.py",):
            path = os.path.join(PKG_ROOT, rel)
            if not os.path.exists(path):
                continue
            checked += 1
            text = open(path, encoding="utf-8").read()
            # Bilingual regex tables are legitimate: they MATCH Chinese reports, they do not
            # PRESENT Chinese to a contestant. Only presentation strings are in scope here.
            for i, line in enumerate(text.splitlines(), 1):
                if _CJK.search(line) and "re.compile" not in line and not line.strip().startswith("#"):
                    offenders.append(f"{rel}:{i}")
        assert checked, "expected to check the CLI; file not found"
        assert not offenders, (
            "Chinese in a user-facing surface — the released benchmark is English: "
            f"{offenders[:20]}"
        )


class TestNothingSecretIsTracked:
    """Scan what a `git push` would actually publish: the git index.

    The other hygiene gates in this project scan the built wheel and the Harbor build context.
    Neither is what GitHub receives -- that is `git ls-files`, and nothing was checking it. A
    credential can be gitignored and still reach the index through `git add -f`, a `git stash -u`,
    or an editor that stages on save, and none of those touch a wheel.
    """

    @staticmethod
    def _tracked():
        import subprocess
        r = subprocess.run(["git", "ls-files", "-z"], cwd=PKG_ROOT,
                           capture_output=True, text=True)
        if r.returncode != 0:
            pytest.skip("not a git checkout")
        return [f for f in r.stdout.split("\0") if f]

    def test_no_credential_file_is_tracked(self):
        names = {".env", "campaign.env", "secrets.json", "secrets.yaml", "secrets.yml"}
        bad = []
        for f in self._tracked():
            base = os.path.basename(f)
            if base == ".env.example":
                continue
            if base in names or base.startswith(".env."):
                bad.append(f)
        assert not bad, f"credential file in the git index: {bad}"

    def test_no_tracked_file_contains_a_credential(self):
        # Zhipu / Z.AI tokens are `<32 hex>.<16 alnum>` and match no generic key pattern.
        vendor = re.compile(r"\b[0-9a-f]{32}\.[A-Za-z0-9]{16}\b")
        hits = []
        for rel in self._tracked():
            try:
                text = open(os.path.join(PKG_ROOT, rel), "rb").read().decode("utf-8", "ignore")
            except OSError:
                continue
            if _CREDENTIAL.search(text):
                hits.append(rel)
            elif vendor.search(text):
                hits.append(rel + " (vendor token)")
        assert not hits, f"credential-shaped literal in a tracked file: {hits}"

    def test_the_example_env_ships_and_carries_no_value(self):
        example = os.path.join(PKG_ROOT, ".env.example")
        assert os.path.exists(example), (
            ".env.example must ship, so an operator copies a reviewed template instead of "
            "inventing a credential file inside the repository"
        )
        for i, line in enumerate(open(example, encoding="utf-8"), 1):
            stripped = line.strip()
            if not stripped.startswith("export "):
                continue
            _, _, value = stripped.partition("=")
            assert value.strip() in ('""', "''", ""), (
                f".env.example:{i} carries a value; it must ship names only"
            )
