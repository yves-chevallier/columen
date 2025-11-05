#!/usr/bin/env python3
"""Offline regression test for the columnspread demo document.

Usage:
    python3 scripts/check_columnspread.py

The script recompiles ``test.tex`` repeatedly so the aux-driven column allocation
logic converges, then inspects ``test.aux`` to confirm the computed column
counts for each list match the expected demonstration values. It also verifies
that the preset CSV registered for ``defaults=exam`` expands to the expected
environment list.
"""

from __future__ import annotations

import pathlib
import re
import subprocess
import sys
from typing import Iterable


ROOT = pathlib.Path(__file__).resolve().parent.parent
TEX_FILE = ROOT / "test.tex"
EXPECTED_COLUMNS = [5, 3, 5, 3, 5, 3, 5]
EXAM_PRESET_ENVIRONMENTS = [
    "itemize",
    "enumerate",
    "description",
    "choices",
    "checkboxes",
    "oneparchoices",
    "oneparcheckboxes",
    "parts",
    "subparts",
]


def run_pdflatex(source: pathlib.Path = TEX_FILE) -> None:
    """Compile the TeX source three times so aux data stabilises."""
    for _ in range(3):
        subprocess.run(
            ["pdflatex", "-interaction=batchmode", source.name],
            cwd=ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def read_columns(aux_path: pathlib.Path) -> list[int]:
    """Parse the aux file and collect the column counts per list."""
    data = aux_path.read_text(encoding="utf8")
    pattern = re.compile(r"\\WI@definecols\{auto-(\d+)\}\{(\d+)\}")
    columns: dict[int, int] = {}
    for match in pattern.finditer(data):
        idx = int(match.group(1))
        columns[idx] = int(match.group(2))
    return [columns[i] for i in sorted(columns)]


def parse_preset_csv(name: str) -> list[str]:
    """Extract the CSV registered via \\@namedef{columnspread@preset@<name>}."""
    tex_source = TEX_FILE.read_text(encoding="utf8")
    pattern = re.compile(
        rf"\\@namedef\{{columnspread@preset@{re.escape(name)}\}}\{{([^}}]*)\}}"
    )
    match = pattern.search(tex_source)
    if not match:
        raise RuntimeError(f"Preset '{name}' not found in {TEX_FILE}")
    csv = match.group(1)
    return [item.strip() for item in csv.split(",") if item.strip()]


def assert_columns(expected: Iterable[int], observed: Iterable[int], label: str) -> None:
    expected_list = list(expected)
    observed_list = list(observed)
    if observed_list != expected_list:
        lines = [
            f"{label} mismatch:",
            f"  expected: {expected_list}",
            f"  observed: {observed_list}",
        ]
        raise AssertionError("\n".join(lines))


def main() -> int:
    if not TEX_FILE.exists():
        print(f"Missing {TEX_FILE}", file=sys.stderr)
        return 2

    # Ensure the exam preset CSV matches the documented environments.
    preset_envs = parse_preset_csv("exam")
    if preset_envs != EXAM_PRESET_ENVIRONMENTS:
        print("defaults=exam environment list mismatch:", file=sys.stderr)
        print(f"  expected: {EXAM_PRESET_ENVIRONMENTS}", file=sys.stderr)
        print(f"  observed: {preset_envs}", file=sys.stderr)
        return 1

    run_pdflatex()
    observed_columns = read_columns(ROOT / "test.aux")
    try:
        assert_columns(EXPECTED_COLUMNS, observed_columns, "Column count")
    except AssertionError as err:
        print(str(err), file=sys.stderr)
        return 1

    # When defaults=exam is applied, the expectations should remain the same.
    try:
        assert_columns(EXPECTED_COLUMNS, observed_columns, "defaults=exam column count")
    except AssertionError as err:
        print(str(err), file=sys.stderr)
        return 1

    print("Column counts and presets match expected demo values.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
