"""The base-image script must DERIVE its pins from the verifier Dockerfile, never copy them.

Two consecutive G3 runs lost all 312 trials to the network, and neither failure was a
benchmark defect: every buildx builder on the host uses the `docker-container` driver, which
cannot see the local image store, so builds resolve an already-present base image over the
registry; and the host's egress proxy is not inherited by a build container, so `pip install`
gets ECONNREFUSED while the host reaches PyPI fine.

`scripts/build-verifier-base.sh` removes both by building the base once. The hazard it
introduces is a SECOND copy of the pinned scientific stack: if the script's list drifts from
the verifier Dockerfile's, the per-task `pip install` stops short-circuiting and silently
goes back to needing the network — which is the failure this was supposed to end, returning
as an intermittent one.
"""
from __future__ import annotations

import re
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = _ROOT / "scripts" / "build-verifier-base.sh"
DOCKERFILE = _ROOT / "harbor" / "templates" / "verifier" / "Dockerfile"

#: `name==version` as the Dockerfile writes it.
_PIN = re.compile(r"^\s+([A-Za-z0-9_.-]+==[0-9][^\s\\]*)", re.M)


def test_the_script_exists_and_is_executable():
    assert SCRIPT.is_file()
    assert SCRIPT.stat().st_mode & 0o111, "the script is not executable"


def test_the_script_hardcodes_no_version_pin():
    """The whole point: one list, in the Dockerfile, extracted by the script."""
    pins = _PIN.findall(SCRIPT.read_text(encoding="utf-8"))
    assert pins == [], (
        f"the base-image script carries its own copy of {pins}; it must extract the pins from "
        f"{DOCKERFILE.relative_to(_ROOT)} so the two cannot drift")


def test_the_extraction_range_still_matches_the_dockerfile():
    """The script slices the pip layer with a sed address pair. If the Dockerfile's pip layer
    is reworded, that slice silently yields nothing and the base image ships with no
    scientific stack at all — which fails as a missing import inside a verifier, far from
    here. Pin both ends of the range."""
    text = DOCKERFILE.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")
    start = "RUN pip install --no-cache-dir --retries 5 --timeout 180 \\"
    assert start in text, "the pip layer's first line changed; the script's sed range is stale"
    assert start.rstrip(" \\") in script, "the script no longer looks for that first line"
    pins = _PIN.findall(text)
    assert len(pins) >= 15, f"only {len(pins)} pins found in the verifier Dockerfile"
    assert pins[-1].startswith("attrs=="), (
        f"the pip layer's last pin is now {pins[-1]!r}; the script's sed range ends at "
        "'attrs==' and would truncate the list")


def test_the_proxy_never_becomes_an_env_in_the_image():
    """A baked proxy would follow the verifier into a trial that runs with no network."""
    script = SCRIPT.read_text(encoding="utf-8")
    assert "ARG PIP_PROXY" in script
    assert not re.search(r"^\s*echo\s+\"?ENV\s+.*PROXY", script, re.M | re.I), (
        "the generated Dockerfile sets a proxy ENV; it must stay a build ARG")
