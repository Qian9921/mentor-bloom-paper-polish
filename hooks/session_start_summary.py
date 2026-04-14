#!/usr/bin/env python3
"""Lightweight session-start summary for the public framework repo."""

from pathlib import Path

root = Path(__file__).resolve().parents[1]
skills = sorted(p.parent.name for p in (root / ".codex" / "skills").glob("*/SKILL.md"))
print(f"Mentor Bloom repo loaded | skills={', '.join(skills)}")
