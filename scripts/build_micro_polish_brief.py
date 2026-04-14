#!/usr/bin/env python3
"""Build a markdown brief for agent-authored micro-polish."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    packet = load_json(args.packet)
    lines = []
    lines.append("# Micro-Polish Brief")
    lines.append("")
    lines.append("## Mission")
    lines.append("")
    lines.append("Perform sentence-level and word-level mentor-style polishing. Use the mentor lexicon and mentor corpus as evidence-backed guides. Do not change scientific meaning.")
    lines.append("")
    for task in packet.get("tasks", []):
        lines.append(f"## {task.get('task_id')} | {task.get('section_id')} | {task.get('task_type')}")
        lines.append("")
        lines.append(f"- sentence: {task.get('sentence_text')}")
        if task.get("issues"):
            lines.append(f"- issues: {' | '.join([x for x in task['issues'] if x])}")
        if task.get("recommended_lexicon_entries"):
            lines.append(f"- lexicon hints: {', '.join(task['recommended_lexicon_entries'])}")
        if task.get("recommended_corpus_entries"):
            lines.append(f"- corpus hints: {', '.join(task['recommended_corpus_entries'])}")
        if task.get("constraints"):
            lines.append(f"- constraints: {', '.join(task['constraints'])}")
        lines.append("")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "task_count": len(packet.get('tasks', []))}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
