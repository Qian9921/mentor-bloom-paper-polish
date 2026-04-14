#!/usr/bin/env python3
"""Check terminology consistency against a compiled mentor profile."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def load_text(path: Path) -> str:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if "sections" in data:
            return "\n\n".join(
                paragraph["text"]
                for section in data["sections"]
                for paragraph in section.get("paragraphs", [])
            )
    return path.read_text(encoding="utf-8")


def count_occurrences(text: str, phrase: str) -> list[int]:
    pattern = re.compile(rf"(?<!\w){re.escape(phrase)}(?!\w)", re.IGNORECASE)
    return [m.start() for m in pattern.finditer(text)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Draft text file or draft_map JSON")
    parser.add_argument("--mentor-profile", required=True, type=Path, help="Compiled mentor profile JSON")
    parser.add_argument("--output", required=True, type=Path, help="Output JSON path")
    args = parser.parse_args()

    text = load_text(args.input)
    profile = json.loads(args.mentor_profile.read_text(encoding="utf-8"))
    prefs = profile.get("terminology_preferences", {})
    findings = []
    family_summary = defaultdict(list)

    for entry in prefs.get("preferred_terms", []):
        preferred = entry.get("term", "").strip()
        if not preferred:
            continue
        aliases = [alias for alias in entry.get("aliases", []) if alias and alias != preferred]
        preferred_hits = count_occurrences(text, preferred)
        alias_hits = {alias: count_occurrences(text, alias) for alias in aliases}
        used_aliases = {alias: hits for alias, hits in alias_hits.items() if hits}
        family_summary[preferred].append({"preferred_hits": len(preferred_hits), "alias_hits": {k: len(v) for k, v in used_aliases.items()}})
        if used_aliases:
            findings.append(
                {
                    "type": "preferred_term_inconsistency",
                    "preferred_term": preferred,
                    "preferred_hits": len(preferred_hits),
                    "alias_hits": {k: len(v) for k, v in used_aliases.items()},
                    "notes": entry.get("notes", ""),
                }
            )

    for entry in prefs.get("disallowed_terms", []):
        term = entry.get("term", "").strip()
        if not term:
            continue
        hits = count_occurrences(text, term)
        if hits:
            findings.append(
                {
                    "type": "disallowed_term",
                    "term": term,
                    "hits": len(hits),
                    "replacement_hint": entry.get("replacement_hint", ""),
                    "reason": entry.get("reason", ""),
                }
            )

    payload = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input": str(args.input),
        "mentor_profile": str(args.mentor_profile),
        "finding_count": len(findings),
        "findings": findings,
        "term_families": family_summary,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "finding_count": len(findings)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
