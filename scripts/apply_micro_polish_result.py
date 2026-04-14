#!/usr/bin/env python3
"""Apply an agent-authored micro-polish result deterministically."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Source draft file")
    parser.add_argument("--result", required=True, type=Path, help="Agent-authored micro_polish_result.json")
    parser.add_argument("--output", required=True, type=Path, help="Output polished draft")
    parser.add_argument("--allow-multiple", action="store_true", help="Allow replacements when the original sentence occurs multiple times")
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8")
    result = load_json(args.result)
    applied = 0
    for item in result.get("revisions", []):
        original = item["original_sentence"]
        revised = item["revised_sentence"]
        count = text.count(original)
        if count == 0:
            raise SystemExit(f"Original sentence not found for task {item['task_id']}: {original}")
        if count > 1 and not args.allow_multiple:
            raise SystemExit(
                f"Original sentence occurs {count} times for task {item['task_id']}; "
                "use a more specific revision result or pass --allow-multiple."
            )
        text = text.replace(original, revised, 1 if count >= 1 and not args.allow_multiple else count)
        applied += 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    print(json.dumps({"output": str(args.output), "applied_revisions": applied}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
