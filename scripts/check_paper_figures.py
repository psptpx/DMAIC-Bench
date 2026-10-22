#!/usr/bin/env python3
"""Validate canonical figure files and their order in the expanded manuscript."""
import argparse
import hashlib
import json
import re
from pathlib import Path


def check(source):
    directory = source / "figures"
    manifest = json.loads((directory / "manifest.json").read_text())
    figures = manifest["figures"]
    assert [f["number"] for f in figures] == list(range(1, len(figures) + 1))
    assert manifest["total_figures"] == len(figures)
    expected = {"README.md", "manifest.json"}
    for figure in figures:
        # Asset IDs remain stable when a new main-text figure shifts appendix numbering.
        asset_number = figure.get("asset_number", figure["number"])
        assert figure["stem"].startswith(f'figure{asset_number:02d}_')
        for extension, relative in figure["files"].items():
            path = source / relative
            expected.add(path.name)
            assert path.is_file(), f"Missing figure: {relative}"
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            assert digest == figure["sha256"][extension], f"Hash mismatch: {relative}"
    actual = {p.name for p in directory.iterdir()}
    assert actual == expected, f"Unexpected/missing assets: {actual ^ expected}"

    def expand(path, chain=()):
        assert path not in chain, f"Cyclic input: {path}"
        text = re.sub(r"(?<!\\)%[^\n]*", "", path.read_text())
        def include(match):
            relative = match.group(1)
            child = source / (relative if relative.endswith('.tex') else relative + '.tex')
            # Optional author metadata is guarded by IfFileExists in the manuscript.
            if not child.exists():
                assert child.name == 'authors.tex', f"Missing input: {child}"
                return ""
            return expand(child, chain + (path,))
        return re.sub(r"\\input\{([^}]+)\}", include, text)

    text = expand(source / manifest["manuscript"])
    included = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{(figures/[^}]+)\}", text)
    ordered = [f["files"]["pdf"] for f in figures]
    assert included == ordered, f"Figure inclusion order differs: {included}"
    for figure in figures:
        assert r"\label{" + figure["label"] + "}" in text, figure["label"]
    print(f"OK: {len(figures)} ordered figures, {3 * len(figures)} verified assets, no unused files.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1] / "paper/iclr")
    check(parser.parse_args().source)
