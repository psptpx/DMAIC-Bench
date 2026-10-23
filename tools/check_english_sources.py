"""Reject Han text in current Git-visible text sources, preserving frozen provenance.

Historical frozen source snapshots are immutable exceptions, pinned by SHA-256 rather
than silently translated. Images, PDFs and other binary files need separate inspection.
Ignored local trials and credentials are outside the public source scan.
"""
from __future__ import annotations

import hashlib
import os
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
ARCHIVES = ROOT / 'tests/fixtures/historical_source_hashes.json'
HAN = re.compile(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]')
# Human-facing documentation may be translated. This exact path does not exempt
# task instructions, generators, CLI strings, scoring, or arbitrary Markdown files.
LOCALIZED_DOCUMENTATION = frozenset({'README.zh-CN.md'})


def check():
    frozen = json.loads(ARCHIVES.read_text())
    problems = []
    for name, expected in frozen.items():
        path = ROOT / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            problems.append(f'{name}: historical source snapshot changed')
    try:
        names = subprocess.check_output(
            ['git', 'ls-files', '-co', '--exclude-standard', '-z'], cwd=ROOT).decode().split('\0')
    except (subprocess.CalledProcessError, FileNotFoundError):
        # not a git checkout (for example an unpacked archive): walk the tree instead
        skip = {'.git', '__pycache__', '.pytest_cache', '.ruff_cache', '.mypy_cache', '.venv', 'venv',
                'build', 'dist', 'node_modules'}
        names = []
        for dirpath, dirnames, filenames in os.walk(ROOT):
            dirnames[:] = [d for d in dirnames if d not in skip]
            for f in filenames:
                names.append(str(Path(dirpath, f).relative_to(ROOT)))
    for name in sorted(set(names)):
        path = ROOT / name
        if not name or not path.is_file() or name in frozen:
            continue
        if HAN.search(name):
            problems.append(f'{name}: source filename contains Han text')
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeError:
            if path.suffix in {".py", ".md", ".yaml", ".yml", ".json", ".toml",
                                ".sh", ".j2", ".txt", ".cff", ".tex", ".bib"}:
                problems.append(f"{name}: text source is not valid UTF-8")
            continue
        if name in LOCALIZED_DOCUMENTATION:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if HAN.search(line):
                problems.append(f'{name}:{n}: current source contains Han text')
    return problems


if __name__ == '__main__':
    errors = check()
    print('\n'.join(errors) if errors else 'English sources clean; historical snapshots unchanged')
    raise SystemExit(bool(errors))
