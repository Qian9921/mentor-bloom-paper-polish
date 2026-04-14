#!/usr/bin/env python3
"""Build a lightweight project fact sheet from a draft map."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


KEYWORD_PATTERNS = {
    "problem_signals": ["challenging", "degrade", "multipath", "blockage", "difficulty", "problem"],
    "method_signals": ["propose", "framework", "method", "combine", "gnss", "inertial", "neural", "network"],
    "evidence_signals": ["experiment", "results", "improve", "better", "accuracy", "baseline"],
}


def section_text(section: dict) -> str:
    return "\n".join(paragraph.get("text", "") for paragraph in section.get("paragraphs", []))


def unique_matches(text: str, patterns: list[str]) -> list[str]:
    lower = text.lower()
    return [pattern for pattern in patterns if pattern in lower]


def extract_contribution_candidates(sections: list[dict]) -> list[str]:
    results = []
    for section in sections:
        heading = (section.get("heading") or "").lower()
        if heading in {"abstract", "introduction"}:
            for paragraph in section.get("paragraphs", []):
                for sentence in re.split(r"(?<=[.!?])\s+", paragraph.get("text", "")):
                    if any(token in sentence.lower() for token in ("propose", "present", "framework", "method")):
                        results.append(sentence.strip())
    return results[:10]


def extract_terminology_candidates(text: str) -> list[str]:
    candidates = set()
    for phrase in ["GNSS", "inertial measurements", "urban navigation", "integrated positioning", "integrated navigation", "localization accuracy", "positioning accuracy"]:
        if phrase.lower() in text.lower():
            candidates.add(phrase)
    return sorted(candidates)


def build_constraints(text: str) -> list[str]:
    constraints = []
    lower = text.lower()
    if "gnss" in lower and "inertial" in lower:
        constraints.append("Do not remove the GNSS + inertial multimodal method description.")
    if "baseline" in lower or "better performance" in lower:
        constraints.append("Do not strengthen comparison claims without explicit comparator support.")
    if "accuracy" in lower:
        constraints.append("Preserve metric meaning when rewriting accuracy-related sentences.")
    return constraints


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft-map", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    draft_map = json.loads(args.draft_map.read_text(encoding="utf-8"))
    sections = draft_map.get("sections", [])
    full_text = "\n\n".join(section_text(section) for section in sections)

    payload = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "draft_id": draft_map.get("draft_id", args.draft_map.stem),
        "problem_signals": unique_matches(full_text, KEYWORD_PATTERNS["problem_signals"]),
        "method_signals": unique_matches(full_text, KEYWORD_PATTERNS["method_signals"]),
        "evidence_signals": unique_matches(full_text, KEYWORD_PATTERNS["evidence_signals"]),
        "contribution_candidates": extract_contribution_candidates(sections),
        "terminology_candidates": extract_terminology_candidates(full_text),
        "do_not_break_constraints": build_constraints(full_text),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "constraints": len(payload["do_not_break_constraints"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
