#!/usr/bin/env python3
"""Best-effort JSON validation for recently touched workspace files."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    root = Path.cwd()
    checked = 0
    for path in root.rglob("*.json"):
        # keep it lightweight for repo-local use
        if ".git" in path.parts:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
            checked += 1
        except Exception as exc:
            print(f"JSON validation failed: {path}: {exc}", file=sys.stderr)
            return 1
    print(f"Mentor Bloom JSON check ok | files={checked}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
