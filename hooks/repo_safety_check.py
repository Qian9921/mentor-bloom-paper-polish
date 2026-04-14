#!/usr/bin/env python3
"""Enforce that the public repo stays free of private/runtime content."""

from __future__ import annotations

import sys
from pathlib import Path


FORBIDDEN_DIRS = [
    ".omx",
    "artifacts",
]
FORBIDDEN_PREFIXES = [
    "data/mentor/raw",
    "data/mentor/normalized",
    "data/mentor/compiled/versions",
    "data/paper_inputs",
]


def main() -> int:
    root = Path.cwd()
    violations: list[str] = []
    for rel in FORBIDDEN_DIRS:
        if (root / rel).exists():
            violations.append(rel)
    for rel in FORBIDDEN_PREFIXES:
        if (root / rel).exists():
            violations.append(rel)
    if violations:
        print(
            "Public repo safety check failed; forbidden local/private paths present: "
            + ", ".join(sorted(violations)),
            file=sys.stderr,
        )
        return 1
    print("Mentor Bloom repo safety check ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
