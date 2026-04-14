#!/usr/bin/env python3
"""Generate a before/after revision delta report."""

from __future__ import annotations

import argparse
import difflib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def count_words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text, flags=re.UNICODE))


def count_paragraphs(text: str) -> int:
    return len([chunk for chunk in re.split(r"\n\s*\n", text) if chunk.strip()])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", required=True, type=Path)
    parser.add_argument("--after", required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    parser.add_argument("--output-diff", type=Path)
    args = parser.parse_args()

    before_text = args.before.read_text(encoding="utf-8")
    after_text = args.after.read_text(encoding="utf-8")
    before_lines = before_text.splitlines()
    after_lines = after_text.splitlines()
    matcher = difflib.SequenceMatcher(a=before_lines, b=after_lines)

    opcode_counts = {"replace": 0, "delete": 0, "insert": 0, "equal": 0}
    changed_line_count = 0
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        opcode_counts[tag] += 1
        if tag != "equal":
            changed_line_count += max(i2 - i1, j2 - j1)

    summary = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "before": str(args.before),
        "after": str(args.after),
        "stats": {
            "before_lines": len(before_lines),
            "after_lines": len(after_lines),
            "before_words": count_words(before_text),
            "after_words": count_words(after_text),
            "before_paragraphs": count_paragraphs(before_text),
            "after_paragraphs": count_paragraphs(after_text),
            "changed_line_count": changed_line_count,
            "opcode_counts": opcode_counts,
        },
    }

    diff_text = "\n".join(
        difflib.unified_diff(
            before_lines,
            after_lines,
            fromfile=str(args.before),
            tofile=str(args.after),
            lineterm="",
        )
    )
    diff_path = args.output_diff or args.output_json.with_suffix(".diff")
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    diff_path.write_text(diff_text + ("\n" if diff_text else ""), encoding="utf-8")
    print(json.dumps({"output_json": str(args.output_json), "output_diff": str(diff_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
