"""DMAIC-Bench, ported onto the Harbor agent-evaluation framework.

The package materialises :class:`dmaic_bench.core.models.TaskInstance` objects into
Harbor task directories. Everything it emits is constrained by :mod:`dmaic_harbor.spec`,
the shared contract derived from Harbor 0.22.0's own pydantic models.

Split of responsibilities inside a generated task
-------------------------------------------------
``environment/``  data + public gate thresholds, nothing else (the Docker build context).
``solution/``     the oracle's *derivation* code — never an answer; mounted only for
                  ``--agent oracle`` (``harbor.agents.oracle.OracleAgent.run`` uploads it
                  at run time; it is not in any image).
``tests/``        empty here on purpose: with ``environment_mode = "separate"`` Harbor
                  passes ``skip_tests_upload=True`` and the verifier image owns /tests.
"""
from __future__ import annotations

from . import spec

__version__ = spec.PACKAGE_VERSION

__all__ = ["spec", "__version__"]
