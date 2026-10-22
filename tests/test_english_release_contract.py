"""Compare English default builds to the recorded pre-migration release inputs."""
import importlib.metadata
import json

import pytest

from tools.english_release_contract import FIXTURE, snapshot
from dmaic_harbor.spec import ANALYSIS_PINS


def _pin_mismatches():
    """Installed (package, version) pairs that differ from ANALYSIS_PINS."""
    out = []
    for name, pinned in ANALYSIS_PINS.items():
        try:
            installed = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            installed = 'not installed'
        if installed != pinned:
            out.append(f'{name} {installed} (pinned {pinned})')
    return out


def test_default_english_release_preserves_published_task_contracts():
    # The fingerprint covers derived truth values, which scipy and statsmodels compute at
    # build time, so it is only defined under the pinned analysis environment.
    mismatches = _pin_mismatches()
    if mismatches:
        pytest.skip('analysis environment differs from ANALYSIS_PINS: ' + '; '.join(mismatches)
                    + '. Install the pinned set (pyproject.toml) to run this contract check.')
    expected = json.loads(FIXTURE.read_text())['tasks']
    actual = snapshot()
    assert set(actual) == set(expected), 'published task IDs changed'
    changed = [task_id for task_id in expected if expected[task_id] != actual[task_id]]
    assert not changed, f'agent input or grading contract changed: {changed}'


def test_english_scoring_preserves_pre_migration_fixture_results():
    from tools.english_scoring_contract import check
    assert check(), 'English scoring changed from the recorded pre-migration fixture'


def test_current_sources_are_english_and_historical_snapshots_are_unchanged():
    from tools.check_english_sources import check
    assert check() == []


def test_method_gate_respects_english_word_boundaries():
    from dataclasses import replace
    from dmaic_bench.core import registry, validation
    case = next(iter(registry.discover().values()))
    meta = replace(case.meta, context='The line does not meet its target.', goal='Investigate.')
    assert validation._check_leakage(meta) == []
    assert validation._check_leakage(replace(meta, goal='Run DOE.'))
