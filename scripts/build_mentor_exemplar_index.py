#!/usr/bin/env python3
"""Build a positive exemplar index from a mentor corpus index."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


HIGH_VALUE_FUNCTIONS = {
    "contribution_statement",
    "result_statement",
    "figure_or_table_narration",
    "limitation_future_work",
    "discussion_or_conclusion_landing",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def infer_why_good(entry: dict) -> str:
    fn = entry.get("function", "")
    if fn == "contribution_statement":
        return "Clear contribution framing with direct method/value linkage."
    if fn == "result_statement":
        return "Quantified result phrasing that can guide result narration."
    if fn == "figure_or_table_narration":
        return "Useful object-first evidence narration pattern."
    if fn == "limitation_future_work":
        return "Shows boundary + follow-up pairing."
    if fn == "discussion_or_conclusion_landing":
        return "Provides a strong practical landing."
    return "High-value mentor exemplar."


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mentor-corpus-index", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--entry-limit", type=int, default=80)
    args = parser.parse_args()

    corpus = load_json(args.mentor_corpus_index)
    entries = []
    for item in corpus.get("entries", []):
        if item.get("function") not in HIGH_VALUE_FUNCTIONS:
            continue
        entries.append(
            {
                "entry_id": item["entry_id"],
                "source_path": item["source_path"],
                "line_hint": item.get("line_hint", 0),
                "section": item.get("section", "general"),
                "function": item.get("function", "general_sentence"),
                "quality": "high",
                "why_good": infer_why_good(item),
                "text": item["text"],
                "tags": item.get("tags", []),
            }
        )
        if len(entries) >= args.entry_limit:
            break

    payload = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mentor_id": corpus.get("mentor_id", "mentor"),
        "entries": entries,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "entry_count": len(entries)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
