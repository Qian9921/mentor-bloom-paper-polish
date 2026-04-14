#!/usr/bin/env python3
"""Build a mentor lexicon from a compiled mentor profile and optional delta files."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def add_entry(entries: list[dict], seen: set[tuple[str, str]], term: str, category: str, status: str, replacement_hint: str = "", notes: str = "", source_evidence: list[str] | None = None) -> None:
    key = (term, category)
    if not term or key in seen:
        return
    seen.add(key)
    entries.append(
        {
            "term": term,
            "category": category,
            "status": status,
            "replacement_hint": replacement_hint,
            "notes": notes,
            "source_evidence": source_evidence or [],
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mentor-profile", required=True, type=Path)
    parser.add_argument("--delta", action="append", type=Path, default=[], help="Optional mentor profile delta JSON files")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    profile = load_json(args.mentor_profile)
    entries: list[dict] = []
    seen: set[tuple[str, str]] = set()

    prefs = profile.get("terminology_preferences", {})
    for item in prefs.get("preferred_terms", []):
        add_entry(entries, seen, item.get("term", ""), "preferred_term", "preferred", notes=item.get("notes", ""))
        for alias in item.get("aliases", []):
            add_entry(entries, seen, alias, "generic_phrase_replacement", "avoid", replacement_hint=item.get("term", ""), notes=f"Prefer {item.get('term')}.")

    for item in prefs.get("disallowed_terms", []):
        add_entry(
            entries,
            seen,
            item.get("term", ""),
            "disallowed_term",
            "avoid",
            replacement_hint=item.get("replacement_hint", ""),
            notes=item.get("reason", ""),
        )

    for item in profile.get("rejection_lexicon", []):
        add_entry(entries, seen, item.get("pattern", ""), "generic_phrase_replacement", "avoid", notes=item.get("reason", ""))

    for item in profile.get("global_rules", []):
        rule = item.get("rule", "")
        lower = rule.lower()
        if "comparator" in lower:
            add_entry(entries, seen, "compared with", "comparison_phrase", "preferred", notes=rule)
            add_entry(entries, seen, "relative to", "comparison_phrase", "preferred", notes=rule)
        if "transition" in lower or "bridge" in lower:
            add_entry(entries, seen, "therefore", "transition_phrase", "contextual", notes=rule)
            add_entry(entries, seen, "however", "transition_phrase", "contextual", notes=rule)
        if "figure or table" in lower:
            add_entry(entries, seen, "Figure~", "figure_phrase", "preferred", notes=rule)
            add_entry(entries, seen, "Table~", "figure_phrase", "preferred", notes=rule)
        if "limitation" in lower and "future" in lower:
            add_entry(entries, seen, "future work", "limitation_phrase", "preferred", notes=rule)
        if "conclusion" in lower or "practical" in lower:
            add_entry(entries, seen, "In practical terms", "conclusion_phrase", "preferred", notes=rule)

    for delta_path in args.delta:
        delta = load_json(delta_path)
        changes = delta.get("proposed_changes", {})
        for item in changes.get("add_preferred_terms", []):
            add_entry(entries, seen, item.get("term", ""), "preferred_term", "preferred", notes=item.get("notes", ""), source_evidence=delta.get("evidence_basis", []))
        for item in changes.get("add_disallowed_terms", []):
            add_entry(entries, seen, item.get("term", ""), "disallowed_term", "avoid", replacement_hint=item.get("replacement_hint", ""), notes=item.get("reason", ""), source_evidence=delta.get("evidence_basis", []))
        for item in changes.get("add_rejection_patterns", []):
            add_entry(entries, seen, item.get("pattern", ""), "generic_phrase_replacement", "avoid", notes=item.get("reason", ""), source_evidence=delta.get("evidence_basis", []))

    payload = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mentor_id": profile.get("mentor_id", "mentor"),
        "entries": entries,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "entry_count": len(entries)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
