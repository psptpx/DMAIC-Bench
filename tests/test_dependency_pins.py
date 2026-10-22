"""The dependency set is part of this benchmark's DEFINITION, so it gets tested.

Truth values for the parametric cases are DERIVED at generate() time by scipy/statsmodels
rather than stored, which makes the analysis stack a load-bearing part of the spec instead of
an implementation detail. It is stated in four places that cannot import one another -- the
two image Dockerfiles, this package's pyproject.toml, and the [metadata] block build.py bakes
into every published task.toml -- so the only thing that can keep them equal is a test.

`ANALYSIS_PINS` in harbor/src/dmaic_harbor/spec.py is the single source. The exhaustive
four-site check lives in harbor/tests/test_verify.py (it sits next to spec.py); this file
re-checks the site that belongs to THIS package, so editing pyproject.toml and running only
the bench suite still fails loudly.
"""
import os
import re
import sys

import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
_BENCH_ROOT = os.path.dirname(_HERE)
_HARBOR_SRC = os.path.join(_BENCH_ROOT, "harbor", "src")

if os.path.isdir(_HARBOR_SRC) and _HARBOR_SRC not in sys.path:
    sys.path.insert(0, _HARBOR_SRC)


def _spec():
    """The authoritative pin set, or skip -- harbor may be absent from a slim checkout."""
    if not os.path.isfile(os.path.join(_HARBOR_SRC, "dmaic_harbor", "spec.py")):
        pytest.skip("harbor/src not present; pins are policed by the harbor suite")
    from dmaic_harbor import spec
    return spec


def _deps_block():
    body = open(os.path.join(_BENCH_ROOT, "pyproject.toml"), encoding="utf-8").read()
    return body.split("dependencies = [", 1)[1].split("]", 1)[0]


def _pyproject_pins():
    pairs = re.findall(r'"([A-Za-z0-9_.\-]+)==([\w.]+)"', _deps_block())
    return {k.lower(): v for k, v in pairs}


def test_pyproject_pins_match_the_image_pins():
    """pyproject.toml must not become a second "validated baseline".

    The images install this package with `--no-deps`, so image pins are what actually runs
    wherever a third party executes the published Harbor dataset. When these two disagree,
    anyone who `pip install`s the package and scores outside a container silently gets a
    different environment from the one the paper reports.
    """
    spec = _spec()
    pins = _pyproject_pins()
    for name, version in spec.ANALYSIS_PINS.items():
        assert pins.get(name) == version, (
            f"pyproject.toml pins {name}=={pins.get(name)} but spec.ANALYSIS_PINS says "
            f"{version}; edit spec.ANALYSIS_PINS and update every site")


def test_pyproject_pins_every_analysis_dependency_exactly():
    """No ranges, and no analysis dependency left to the resolver.

    `pandas` is only a transitive of statsmodels but must stay explicitly pinned: statsmodels
    calls `pandas.util._decorators.deprecate_kwarg` with the pre-3.x signature, so an
    unpinned pandas resolves to a version that makes `import statsmodels.tsa` raise
    TypeError. Pinning scipy/statsmodels alone left the environment broken.
    """
    spec = _spec()
    assert not re.search(r'"[A-Za-z0-9_.\-]+[<>~!]=', _deps_block()), "unpinned/ranged dependency"
    assert set(spec.ANALYSIS_PINS) <= set(_pyproject_pins())


# --------------------------------------------------------------------------- SciPy 1.19
#
# SciPy 1.17 began warning that 1.19 removes `critical_values` / `significance_level` /
# `fit_result` from the `stats.anderson` result. Every call site here reads only
# `.statistic`, so no derived truth is at risk -- but the call still had to opt in, and
# `method=` does NOT exist before 1.17, so it cannot simply be passed: the pinned
# environment runs scipy 1.14.1, where passing it raises TypeError.
#
# `truth.verifiers.anderson_statistic` is the one place that knows the difference. These
# tests stop a future edit from reintroducing a bare call.

def test_package_never_calls_stats_anderson_directly():
    """All AD calls route through the compat helper, so a SciPy bump is a one-line change."""
    pkg = os.path.join(_BENCH_ROOT, "dmaic_bench")
    helper = os.path.abspath(os.path.join(pkg, "truth", "verifiers.py"))
    offenders = []
    for root, _dirs, files in os.walk(pkg):
        if "__pycache__" in root:
            continue
        for fn in files:
            if not fn.endswith(".py"):
                continue
            path = os.path.join(root, fn)
            if os.path.abspath(path) == helper:
                continue  # the helper itself
            if re.search(r"\bstats\.anderson\s*\(", open(path, encoding="utf-8").read()):
                offenders.append(os.path.relpath(path, _BENCH_ROOT))
    assert not offenders, (
        f"bare scipy.stats.anderson call(s) in {offenders}; "
        f"use truth.verifiers.anderson_statistic instead")


def test_anderson_statistic_is_bit_identical_and_silent():
    """The forward-compat argument must not move a single bit of the A-squared statistic."""
    import warnings

    import numpy as np
    from scipy import stats

    from dmaic_bench.truth import verifiers

    rng = np.random.default_rng(20260903)
    for n in (8, 12, 25, 40, 101, 500):
        x = rng.normal(10.0, 2.0, n)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            bare = float(stats.anderson(x, dist="norm").statistic)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            helper_value = verifiers.anderson_statistic(x, dist="norm")
        assert bare.hex() == helper_value.hex(), (
            f"A-squared moved at n={n}: {bare!r} -> {helper_value!r}")
        assert not [w for w in caught if issubclass(w.category, FutureWarning)], (
            f"anderson_statistic emitted a FutureWarning at n={n}")
