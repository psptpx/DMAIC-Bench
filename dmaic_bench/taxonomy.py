"""Loader/validator for the canonical method taxonomy (taxonomy.yaml)."""
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))
TAXONOMY_PATH = os.path.join(_HERE, "taxonomy.yaml")


@dataclass(frozen=True)
class CanonicalOutput:
    name: str
    tol_class: str


@dataclass(frozen=True)
class Method:
    method_id: str
    spec_keys: tuple
    aliases: tuple
    family: str
    data_type: str
    prerequisites: tuple
    canonical_outputs: tuple  # tuple[CanonicalOutput]


class Taxonomy:
    def __init__(self, methods: list[Method], tol_defaults: dict):
        self.methods = {m.method_id: m for m in methods}
        self.tol_defaults = tol_defaults
        self._by_spec_key = {}
        for m in methods:
            for k in m.spec_keys:
                if k in self._by_spec_key:
                    raise ValueError(f"spec key {k} mapped by two methods")
                self._by_spec_key[k] = m.method_id

    def __contains__(self, method_id: str) -> bool:
        return method_id in self.methods

    def get(self, method_id: str) -> Method:
        return self.methods[method_id]

    def method_for_spec_key(self, spec_key: str) -> str | None:
        return self._by_spec_key.get(spec_key)

    def families(self) -> set:
        return {m.family for m in self.methods.values()}

    def resolve_alias(self, name: str) -> str | None:
        """Best-effort mapping of a free-form method name to a method_id."""
        n = name.strip().lower()
        if n in self.methods:
            return n
        for m in self.methods.values():
            if n == m.method_id.lower() or n in (a.lower() for a in m.aliases):
                return m.method_id
        return None


@lru_cache(maxsize=1)
def load(path: str = TAXONOMY_PATH) -> Taxonomy:
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    methods = []
    for e in raw["methods"]:
        app = e.get("applicability", {})
        methods.append(Method(
            method_id=e["method_id"],
            spec_keys=tuple(e.get("spec_keys", [])),
            aliases=tuple(e.get("aliases", [])),
            family=e["family"],
            data_type=app.get("data_type", "any"),
            prerequisites=tuple(app.get("prerequisites", [])),
            canonical_outputs=tuple(
                CanonicalOutput(o["name"], o["tol_class"]) for o in e.get("canonical_outputs", [])
            ),
        ))
    ids = [m.method_id for m in methods]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate method_id in taxonomy")
    return Taxonomy(methods, raw.get("tol_defaults", {}))
