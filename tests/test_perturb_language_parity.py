"""English dirty-data strength must not depend on the spelling of field names."""
import pytest

from dmaic_bench.tasks import perturb

_READINGS = [10.2, 10.4, 9.8, 10.1, 10.6, 9.9, 10.3, 10.0, 10.5, 9.7, 10.2, 10.1]
_TEMPS = [58.1, 57.4, 59.0, 58.6, 57.9, 58.2, 58.8, 57.6, 59.1, 58.0, 58.4, 57.8]

ALTERNATE_BLOCK = {
    "coating reading": list(_READINGS),
    "bath temperature": list(_TEMPS),
    "lower limit": 9.5,
    "work station": "line 3",
}

EN_BLOCK = {
    "coating_thickness": list(_READINGS),
    "bath_temperature": list(_TEMPS),
    "lower_limit": 9.5,
    "station": "line 3",
}


def _strength(original, dirty):
    """Structural measurement of how much a block was perturbed."""
    def leaves(node):
        if isinstance(node, dict):
            for v in node.values():
                yield from leaves(v)
        elif isinstance(node, list):
            for v in node:
                yield from leaves(v)
        else:
            yield node

    return {
        "renames": len(set(original) - set(dirty)),
        "holes": sum(1 for v in leaves(dirty) if v is None),
        "stringified": sum(1 for v in leaves(dirty)
                           if isinstance(v, str) and v.replace(".", "", 1).isdigit()),
        "new_keys": len(set(dirty) - set(original)),
    }


@pytest.mark.parametrize("seed", [1, 2, 3, 7, 11])
def test_perturbation_strength_is_field_spelling_independent(seed):
    alternate = perturb.dirty_blocks("adb_cXX", {"S": ALTERNATE_BLOCK}, seed=seed)["S"]
    en = perturb.dirty_blocks("adb_cXX", {"S": EN_BLOCK}, seed=seed)["S"]
    assert _strength(ALTERNATE_BLOCK, alternate) == _strength(EN_BLOCK, en), (
        "the same block perturbed in two field spellings received different amounts of damage; "
        "RB would read that as a robustness difference")


@pytest.mark.parametrize("seed", [1, 2, 3, 7, 11])
def test_english_keys_are_renameable_at_all(seed):
    """The specific regression: none of these English keys is in the synonym table.

    Under the old `k in _SYNONYMS or _has_cjk(k)` predicate the renameable pool for this block
    was EMPTY, so the rename step never fired and the English dirty variant lost a whole class
    of perturbation.
    """
    en = perturb.dirty_blocks("adb_cXX", {"S": EN_BLOCK}, seed=seed)["S"]
    assert set(EN_BLOCK) - set(en), "no English key was renamed"




def test_scalar_spec_limit_value_survives_in_both_field_spellings():
    """Renaming a spec limit's KEY is allowed; its value must come through untouched."""
    for block in (ALTERNATE_BLOCK, EN_BLOCK):
        dirty = perturb.dirty_blocks("adb_cXX", {"S": block}, seed=3)["S"]
        assert 9.5 in dirty.values()


def test_distractors_and_suffix_are_english():
    from dmaic_bench.core.i18n import residual_source_strings
    dirty = perturb.dirty_blocks("adb_cXX", {"S": EN_BLOCK}, seed=5)["S"]
    assert not residual_source_strings(dirty)
    assert any(k.endswith("_original") for k in dirty)
