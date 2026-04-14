#!/usr/bin/env python3
"""Build a mentor corpus index from a mentor manifest."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


TEXT_EXTS = {".txt", ".md", ".tex"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def infer_section(text: str) -> str:
    lower = text.lower()
    if "abstract" in lower:
        return "abstract"
    if "introduction" in lower:
        return "introduction"
    if "conclusion" in lower:
        return "conclusion"
    if "discussion" in lower:
        return "discussion"
    if "figure" in lower or "table" in lower:
        return "results"
    return "general"


def infer_function(text: str) -> tuple[str, str]:
    lower = text.lower()
    if any(token in lower for token in ["we propose", "this paper proposes", "in this work"]):
        return "contribution_statement", "introduce_method"
    if any(token in lower for token in ["results show", "compared with", "relative to"]):
        return "result_statement", "scoped_comparison"
    if any(token in lower for token in ["figure~", "table~", "fig.", "tab."]):
        return "figure_or_table_narration", "object_then_observation"
    if any(token in lower for token in ["limitation", "future work"]):
        return "limitation_future_work", "boundary_then_followup"
    if any(token in lower for token in ["in practical terms", "this matters", "therefore"]):
        return "discussion_or_conclusion_landing", "implication_landing"
    return "general_sentence", "general_exposition"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mentor-manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--entry-limit", type=int, default=200)
    args = parser.parse_args()

    manifest = load_json(args.mentor_manifest)
    root = Path(manifest["root_dir"])
    entries = []
    counter = 0

    for item in manifest.get("items", []):
        path = root / item.get("path", "")
        if path.suffix.lower() not in TEXT_EXTS or not path.exists():
            continue
        for line_no, raw in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
            text = re.sub(r"\s+", " ", raw).strip()
            if len(text) < 40:
                continue
            section = infer_section(text)
            function, move = infer_function(text)
            counter += 1
            entries.append(
                {
                    "entry_id": f"mentor-corpus-{counter:04d}",
                    "source_path": item["path"],
                    "line_hint": line_no,
                    "section": section,
                    "function": function,
                    "rhetorical_move": move,
                    "text": text,
                    "tags": [section, function, move],
                }
            )
            if len(entries) >= args.entry_limit:
                break
        if len(entries) >= args.entry_limit:
            break

    payload = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mentor_id": manifest.get("mentor_id", "mentor"),
        "entries": entries,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "entry_count": len(entries)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
