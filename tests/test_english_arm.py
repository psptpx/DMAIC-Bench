"""Canonical English release: routing, hygiene, stable IDs and numerical truths."""
from __future__ import annotations

import os
import re
import sys

import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
_BENCH = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_BENCH, "harbor", "src"))

from dmaic_bench.core import i18n                      # noqa: E402
from dmaic_bench.core import registry                  # noqa: E402
from dmaic_bench.tasks import builder                  # noqa: E402
from dmaic_harbor import build as harbor_build         # noqa: E402
from dmaic_harbor import steward_service               # noqa: E402

sys.path.insert(0, os.path.join(_BENCH, "tools"))
import truth_digest                                        # noqa: E402


#: The corpus's numeric ground floor, over ``tools/truth_digest.py``'s stated recipe: every
#: ``(method_id, field, expected, tol)`` for every case at seeds 1-3, sorted, SHA-256, 16 hex.
#:
#: It is pinned here rather than described in prose because the localisation touched the
#: builder, the registry, the legacy bridge and 24 case directories, and the invariant that
#: matters — none of that moved a number — is not visible in any diff. Regenerate with
#: ``python3 tools/truth_digest.py`` and change this constant ONLY together with a truth that
#: was deliberately re-derived.
#: Two corpora, two digests (docs/HELD_OUT.md). Change either ONLY together with a truth that
#: a reference implementation reproduces.
TRUTH_DIGEST_FULL = "\1"            # all 24 cases
TRUTH_DIGEST_PUBLIC = "da2cfe846ee660d5"   # the 15 synthetic cases, 249 tuples


def _expected_digest():
    from dmaic_bench.v2.expert_migration import _legacy_bridge_available
    return TRUTH_DIGEST_FULL if _legacy_bridge_available() else TRUTH_DIGEST_PUBLIC


TRUTH_DIGEST = _expected_digest()


@pytest.fixture(scope="module")
def cases():
    return registry.discover()


@pytest.fixture(scope="module")
def canonical_cases(cases):
    """Every canonical case must participate in the English release checks."""
    return sorted(cases)


# --------------------------------------------------------------------------- the factor exists







def test_language_reaches_the_task_instance_and_the_steward_config(cases, canonical_cases):
    for case_id in canonical_cases[:3]:
        for task in builder.build_tasks(cases[case_id], seeds=(1,), variants=("clean",),
                                        tiers=("T1", "T3")):
            assert task.language == "en"
            assert harbor_build.build_steward_config(task)["language"] == task.language


def test_the_honesty_probe_denies_in_the_arms_own_language(cases, canonical_cases):
    seen = {}
    for case_id in canonical_cases:
        for task in builder.build_tasks(cases[case_id], seeds=(1,), variants=("clean",),
                                        tiers=("T3",), with_faults=True):
            if task.fault is None:
                continue
            seen[task.language] = task.fault.denial_message
            assert not i18n.has_cjk(task.fault.denial_message), (
                f"{task.task_id}: the refusal the agent reads is in the wrong language — a "
                "probe that denies in the other language tells the agent which arm it is in")
    assert set(seen) == {"en"}, seen


def test_the_builders_own_strings_are_localised(cases, canonical_cases):
    """The T1 goal and the T2 prior-facts block are written BY THE BUILDER, not by a case."""
    for case_id in canonical_cases:
        for task in builder.build_tasks(cases[case_id], seeds=(1,), variants=("clean",),
                                        tiers=("T1", "T2")):
            if task.language != "en":
                continue
            assert not i18n.has_cjk(task.goal), f"{task.task_id}: goal is not localised"
            assert not i18n.has_cjk(task.prior_facts), \
                f"{task.task_id}: prior_facts is not localised"


# --------------------------------------------------------------------------- the factor is clean

def test_every_english_topic_is_routable(cases, canonical_cases):
    problems = {}
    for case_id in canonical_cases:
        meta = i18n.localize_meta(cases[case_id].meta, "en")
        found = steward_service.topic_problems(
            [{"stage_id": s.stage_id, "topics": s.topics} for s in meta.stages])
        if found:
            problems[case_id] = found
    assert problems == {}, problems


def test_no_english_label_or_topic_names_a_method(cases, canonical_cases):
    """V3, on the surface the plan measured 128 zh violations of: `steward.json` is
    agent-visible and the steward echoes `label (topics)` in unroutable and status replies."""
    leaks = {}
    for case_id in canonical_cases:
        meta = i18n.localize_meta(cases[case_id].meta, "en")
        found = harbor_build.steward_label_leaks(
            [{"stage_id": s.stage_id, "label": s.label, "topics": list(s.topics)}
             for s in meta.stages])
        if found:
            leaks[case_id] = found
    assert leaks == {}, leaks


def test_no_english_context_or_goal_names_a_method(cases, canonical_cases):
    leaks = {}
    for case_id in canonical_cases:
        meta = i18n.localize_meta(cases[case_id].meta, "en")
        hits = harbor_build.method_terms_in(meta.context + "\n" + meta.goal)
        if hits:
            leaks[case_id] = hits
    assert leaks == {}, leaks


def test_english_blocks_carry_no_source_language_string(cases, canonical_cases):
    """The glossary's completeness gate. A missed term ships a Chinese column name to an
    English-arm agent, and nothing else in the stack would notice."""
    residue = {}
    for case_id in canonical_cases:
        blocks = i18n.localize_case(cases[case_id], "en").generate(1).blocks
        found = i18n.residual_source_strings(blocks)
        if found:
            residue[case_id] = sorted({t for _, t in found})[:5]
    assert residue == {}, residue


def test_english_case_text_carries_no_source_language_string(cases, canonical_cases):
    for case_id in canonical_cases:
        meta = i18n.localize_meta(cases[case_id].meta, "en")
        assert not i18n.has_cjk(meta.context), case_id
        assert not i18n.has_cjk(meta.goal), case_id
        for s in meta.stages:
            assert not i18n.has_cjk(s.label), f"{case_id}/{s.stage_id}"
            assert not any(i18n.has_cjk(t) for t in s.topics), f"{case_id}/{s.stage_id}"


#: How an appraiser/operator identifier is allowed to read in the English arm: a ROLE (or a
#: piece of equipment, since two cases run their repeatability study on machines rather than
#: people) followed by a code. "Appraiser A", "Inspector B", "Vision unit 2" pass;
#: "Dai Shijuan" does not, and that is the whole point — a romanised personal name is invisible
#: to every CJK-keyed hygiene guard in the suite.
_ROLE_CODE = __import__("re").compile(r"^[A-Z][A-Za-z]*(?: [a-z]+)* (?:[A-Z]|[0-9]+)$")

#: The subset that must be a HUMAN role, used on the glossary entries for real personal names.
_HUMAN_ROLE_CODE = __import__("re").compile(r"^(Appraiser|Inspector|Operator) [A-Z0-9]+$")




def test_no_english_block_carries_a_person_shaped_identifier(cases):
    """Checked on the ARTEFACT, not on the table: the guard has to hold for whatever the
    glossary happens to contain, including entries added later.

    Human identifiers reach a block in two shapes — as a value under an appraiser/operator
    field (``appraiserId``), and as a COLUMN KEY (``Inspector A``, one column per appraiser).
    Both are checked.
    """
    import re as _re
    field = _re.compile(r"appraiser|operator|inspector", _re.I)
    values = []

    def walk(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if field.search(str(k)) and isinstance(v, str):
                    values.append(str(v))
                if field.search(str(k)) and isinstance(v, list) and \
                        all(isinstance(x, str) for x in v):
                    values.extend(v)
                if i18n.has_cjk(str(k)) is False and field.search(str(k)) and \
                        isinstance(v, (int, float)):
                    pass
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)

    for case_id, case in sorted(cases.items()):
        blocks = case.generate(1).blocks
        before = len(values)
        walk(blocks)
        for value in set(values[before:]):
            assert _ROLE_CODE.match(value), \
                f"{case_id}: identifier {value!r} is not an opaque role code"
    if not values:
        # The cases carrying named appraisers (attribute-agreement and gage studies with
        # per-operator columns) are all held out, so a public checkout has no subject here.
        # Skip loudly; never pass vacuously.
        pytest.skip(
            "no appraiser/operator identifier in the public corpus -- the cases carrying them "
            "are held out (docs/HELD_OUT.md); this runs for an operator with the full corpus"
        )


def test_no_arm_carries_a_romanised_organisation_identity(cases):
    """The A10 guard, over the WHOLE corpus rather than the three-task slice
    ``harbor/tests/test_build.py`` builds.

    Two real findings this caught while the arm was being authored, both invisible to every
    CJK-keyed guard in the suite:

    * a stamped base index mark (an index mark stamped on a base) rendered as "base arrow datum", and
      ``arrow`` is one of the romanised customer ids that used to BE a case id;
    * a narrow copper track description rendered as "narrow copper track", and the wheel-hygiene scan is a
      naked byte scan, so "narrow" contains "arrow" too.

    Matching here is likewise naked containment, deliberately: it is the same rule the
    published-artifact guard applies, and an English arm that only passes a laxer rule than
    the artifact guard is an English arm that fails at release time.
    """
    import json as _json
    path = os.path.join(_BENCH, "dmaic_bench", "cases", "_identity_map.json")
    if not os.path.exists(path):
        pytest.skip("no identity map (a released tree) — nothing to check against")
    secrets = set()

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if (isinstance(v, str)
                        and k in ("title", "internal_title", "former_case_id",
                                  "legacy_source_id", "source")
                        and len(v.strip()) >= 3 and v.strip().isascii()):
                    secrets.add(v.strip().lower())
                else:
                    walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    with open(path, encoding="utf-8") as fh:
        walk(_json.load(fh))
    assert secrets, "the identity map yielded no romanised identity to check against"

    offenders = []
    for case_id, case in sorted(cases.items()):
        for lang in i18n.languages_for(case.meta):
            local = i18n.localize_case(case, lang)
            blob = "\n".join([
                local.meta.title, local.meta.context, local.meta.goal,
                _json.dumps(local.generate(1).blocks, ensure_ascii=False),
                "\n".join(s.label + " " + " ".join(s.topics) + " " + (s.summary_fact or "")
                           for s in local.meta.stages),
            ]).lower()
            for secret in secrets:
                if secret in blob:
                    offenders.append((case_id, lang, secret))
    # The zh arm's `title` is the INTERNAL one in a developer tree by design (the bridge
    # re-applies it and `build.assert_public_identity` refuses to emit a corpus carrying it),
    # so only Latin identities are in scope here and they must not appear at all.
    assert offenders == [], offenders


# --------------------------------------------------------------------------- nothing else moved

def _truth_key(t):
    return (str(t.stage_id), t.method_id, t.field, t.expected, t.tol, t.soft)






def test_corpus_truth_digest_is_unchanged():
    assert truth_digest.digest() == TRUTH_DIGEST, (
        "a truth value, field, tolerance or method id moved. The English arm is a rendering "
        "of the SAME cases; if this is deliberate, re-derive the truth and update the pin in "
        "the same commit.")








# --------------------------------------------------------------------------- the localiser





# --------------------------------------------------------------------------- metric-cue reach

#: A cue alternative counts as an ENGLISH HOOK only if it carries a run of at least this many
#: consecutive ASCII letters. Two is deliberately not enough: `CL`, `AD` and `Pp` are matched
#: case-insensitively by `hn.cue_lines`, so they fire inside "include", "made" and "supply" and
#: select lines that have nothing to do with the metric.
ENGLISH_HOOK_MIN_LETTERS = 3


def _top_level_alternatives(pattern: str) -> list:
    """Split a regex on its TOP-LEVEL ``|`` only.

    A naive ``pattern.split("|")`` tears ``cent(re|er) line`` and ``[=?<?]`` apart and then
    reports the halves as separate alternatives, which is how a cue with no English hook can
    look like it has one.
    """
    out, buf, depth, in_class, i = [], [], 0, False, 0
    while i < len(pattern):
        ch = pattern[i]
        if ch == "\\":                      # escape: the pair is opaque
            buf.append(pattern[i:i + 2])
            i += 2
            continue
        if in_class:
            buf.append(ch)
            in_class = ch != "]"
        elif ch == "[":
            in_class = True
            buf.append(ch)
        elif ch == "(":
            depth += 1
            buf.append(ch)
        elif ch == ")":
            depth -= 1
            buf.append(ch)
        elif ch == "|" and depth == 0:
            out.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
        i += 1
    out.append("".join(buf))
    return out


def _longest_latin_word(alternative: str) -> int:
    """Longest run of consecutive ASCII letters in one alternative, regex syntax removed.

    ``\\s``/``\\b`` become separators rather than the letters s and b, so ``P\\s*[=?]`` scores
    1 (the bare operator it is) instead of 2.
    """
    text = re.sub(r"\\[sSbBdDwWAZ]", "  ", alternative)   # class/anchor escapes -> separator
    text = re.sub(r"\\(.)", r"\1", text)                  # any other escape -> its literal
    text = re.sub(r"[\[\](){}?*+^$.]", " ", text)         # metacharacters -> separator
    runs = re.findall(r"[A-Za-z]+", text)
    return max((len(r) for r in runs), default=0)


def _english_hooks(cue: str) -> list:
    return [a for a in _top_level_alternatives(cue)
            if _longest_latin_word(a) >= ENGLISH_HOOK_MIN_LETTERS]


def _en_cue_entries(cases):
    """``(case_id, method_id, field, metric_cue)`` for every cue the ENGLISH arm scores on."""
    out = []
    for case_id in sorted(cases):
        case = cases[case_id]
        if "en" not in i18n.languages_for(case.meta):
            continue
        for truth in i18n.localize_case(case, "en").generate(1).truths:
            if truth.metric_cue:
                out.append((case_id, truth.method_id, truth.field, truth.metric_cue))
    return out


def test_every_metric_cue_carries_an_english_hook(cases):
    """Every scored metric must be reachable from an English report."""
    offenders = [(c, m, f, cue) for c, m, f, cue in _en_cue_entries(cases)
                 if not _english_hooks(cue)]
    assert not offenders, (
        "these metric_cue patterns cannot match an English report, so their metric is exempt "
        "from the fabrication check in the English arm. Add meaningful English alternatives:\n"
        + "\n".join(f"  {c} {m}.{f}: {cue!r}" for c, m, f, cue in offenders))


def test_a_bare_operator_is_not_an_english_hook():
    """The gate above is only worth having if a bare ``P =`` fails it.

    Every p-value cue in the corpus carries a comparison operator, and an operator matches the
    line of EVERY method that states a p-value -- it identifies statistics, not this metric. If
    it counted as a hook, the gate would pass on a corpus where nothing was fixed.
    """
    for bare in (r"P\s*[=＝<＜]", r"t\s*[=＝]", r"F\s*[=＝]",
                 r"\bZ\s*[=＝]", r"χ", r"%"):
        assert not _english_hooks(bare), f"{bare!r} must not count as an English hook"
    for real in (r"furnace", r"cent(?:re|er)\s*line", r"[Aa]nderson", r"R-?squared",
                 r"out[- ]of[- ]control"):
        assert _english_hooks(real), f"{real!r} must count as an English hook"


def test_the_alternation_splitter_respects_groups_and_classes():
    """``cent(re|er) line`` is ONE alternative; splitting on every ``|`` invents two."""
    assert _top_level_alternatives(r"cent(re|er) line|pooled") == [r"cent(re|er) line", "pooled"]
    assert _top_level_alternatives("P\\s*[=＝<＜]|significant") == [
        "P\\s*[=＝<＜]", "significant"]
    assert _top_level_alternatives(r"a\|b|c") == [r"a\|b", "c"]




def test_canonical_sources_and_default_build(cases):
    from pathlib import Path
    assert i18n.DEFAULT_LANGUAGE == "en"
    assert i18n.LANGUAGES == ("en",)
    assert not list((Path(_BENCH) / "dmaic_bench/cases").glob("*/locale.*.yaml"))
    for case in cases.values():
        assert case.meta.language == "en"
        assert not case.meta.translations
        default = builder.build_tasks(case, with_faults=True)
        explicit = builder.build_tasks(case, with_faults=True, languages=("en",))
        assert default == explicit
        assert default
        assert all(t.task_id.endswith(("-en", "-en-fault")) for t in default)
        assert i18n.localize_case(case, "en") is case


def test_unsupported_language_is_rejected(cases):
    case = next(iter(cases.values()))
    for languages in (("zh",), ("en", "zh")):
        with pytest.raises(ValueError, match="English only"):
            builder.build_tasks(case, languages=languages)
    with pytest.raises(ValueError, match="English only"):
        i18n.localize_case(case, "zh")
