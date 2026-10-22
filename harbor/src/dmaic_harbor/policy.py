"""THE CONTESTANT-ISOLATION POLICY. Build-time only — this module NEVER enters an image.

WHY THIS IS NOT IN ``spec.py``
------------------------------
``spec.py`` is the shared contract between the builder, the in-container steward and the
verifier, so it is staged into BOTH published images (as ``spec.py.txt``, renamed on the way
in — see ``templates/*/Dockerfile``). Anything written in it therefore ships, in every one of
the hundreds of generated task directories.

The exclusion policy is not part of that contract. It is consumed by ``build.py`` and by
``tests/test_public_image_hygiene.py`` on the HOST, before an image exists. Keeping it here
is what lets the policy be written down in full — the reason it exists, which contestant it
covers, and what "excluded" concretely means — without the prose itself becoming the leak it
is meant to prevent. A policy that cannot be written down cannot be audited; a policy written
down inside the payload audits nothing.

Two independent facts make this module safe to be explicit in:

* ``build.py``'s staging lists (``AGENT_MODULES``, ``VERIFIER_MODULES``) name the modules
  that travel, one by one. ``policy`` is not among them, and both Dockerfiles ``COPY`` only
  named paths — neither uses a whole-context copy — so nothing here can reach an image by
  accident.
* ``tests/test_public_image_hygiene.py`` re-derives that claim mechanically on every run and
  pins the set of shippable files that may name the private contestant to exactly one: this
  file, the declaration itself.

THE POLICY
----------
DMAIC-Bench publishes two images (agent + verifier), a Harbor dataset, and the
``dmaic_bench`` wheel that the verifier image installs. One private contestant, run only on the operators' own infrastructure, must appear in none of
them, and not merely in the sense that its code is absent:

  * Its **code** cannot ship. It depends on proprietary software and infrastructure that
    cannot be redistributed, so a reader could not run it either way, and
    a copy inside an image would be dead weight that a reader cannot run and a licence
    problem for us.
  * Its **name** cannot ship either, and this is the half that is easy to get wrong. The
    paper's fairness claim is that the dataset and the images are contestant-neutral: the
    tasks do not know who is being measured. A dataset that names one of its own contestants
    — even only in a docstring, a provenance string, or a CLI subcommand — is evidence
    against that claim, and it is recoverable from any published artifact with ``unzip``.

Its adapters are operator-side code:

  * ``bench/harbor/private/`` holds the Harbor-side agent adapter. The whole directory is
    removed from every Docker build context by ``.dockerignore`` and excluded from the sdist
    and wheel of ``dmaic-harbor`` by ``pyproject.toml``.
  * ``bench/dmaic_bench/adapters/operator/`` and
    ``bench/dmaic_bench/v3/operator_adapter/`` hold the bench-side adapters. They are
    excluded from the built ``dmaic_bench`` wheel by
    ``[tool.setuptools.packages.find].exclude`` in ``bench/pyproject.toml`` — which matters
    because ``build.py --bench-wheel`` stages that wheel into every task's verifier image.

Nothing under ``private/`` may be referenced by a Dockerfile, a ``task.toml``, or the dataset
manifest, and no file that reaches an image may contain any string in
:data:`PUBLIC_IMAGE_FORBIDDEN`.

Operator-side use is unaffected: the adapters keep working from a source checkout, and a
local (uncommitted) job config can run the private contestant against the same dataset.
That is the point — the contestant is excluded from what is PUBLISHED, not from the
experiment.
"""
from __future__ import annotations

import os

#: The operator-only directory inside ``bench/harbor``. Exempt from the scans below because
#: it is the declared home of excluded material, and proven unshippable by the
#: ``.dockerignore`` simulation in the hygiene suite.
PRIVATE_DIR_NAME = "private"

#: Strings that must not appear in ANY byte that reaches a published image, the released
#: dataset, or the built wheel. Widening this tuple widens every check in
#: ``tests/test_public_image_hygiene.py`` — the tests never keep their own copy.
#: Only the STRUCTURAL token is hard-coded. Operator-specific tokens -- the name of an excluded
#: contestant, its vendor, its solver -- are deliberately NOT written here: putting them in a
#: public file is the very disclosure this check exists to prevent, and it would identify the
#: authors of a double-blind submission. An operator supplies them at build time:
#:
#:     DMAIC_FORBIDDEN_TOKENS=acme,acme-solver python3 -m dmaic_harbor.build ...
#:
#: Widening this widens every check in tests/test_public_image_hygiene.py -- the tests never
#: keep their own copy of the list.
_STRUCTURAL_FORBIDDEN = ("private/",)

PUBLIC_IMAGE_FORBIDDEN = _STRUCTURAL_FORBIDDEN + tuple(
    t.strip() for t in os.environ.get("DMAIC_FORBIDDEN_TOKENS", "").split(",") if t.strip()
)


def forbidden_hits(data: bytes) -> list:
    """Which forbidden tokens appear in *data*. Bytes, not text, on purpose.

    A text-based scan has to decide what to do with something that will not decode as UTF-8,
    and the tempting answer — skip it — is exactly wrong: a wheel, an archive or a
    DLP-wrapped source file is precisely where a whole excluded stack can ride along
    unnoticed. Scanning bytes cannot be dodged that way and costs nothing.
    """
    return sorted({token for token in PUBLIC_IMAGE_FORBIDDEN if token.encode() in data})
