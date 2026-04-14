#!/usr/bin/env python3
"""Build a markdown brief for agent-side reference-mirror comparison."""

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
    lines.append("# Reference Mirror Brief")
    lines.append("")
    lines.append("## Mission")
    lines.append("")
    lines.append("Compare weak draft sections against mentor/reference snippets and identify reusable rhetorical moves. Do not rewrite directly in this step; diagnose the difference first.")
    lines.append("")
    for target in packet.get("targets", []):
        lines.append(f"## Section: {target.get('section_id')} | {target.get('heading')}")
        lines.append("")
        lines.append(f"- reason: {target.get('reason')}")
        if target.get("linked_findings"):
            lines.append(f"- linked findings: {', '.join(target['linked_findings'])}")
        lines.append("")
        lines.append("### Mirror Snippets")
        lines.append("")
        for snippet in target.get("mirror_snippets", []):
            lines.append(
                f"- {snippet.get('source_path')}:{snippet.get('line_hint')} | score={snippet.get('score')} | {snippet.get('match_reason')}"
            )
            lines.append(f"  - {snippet.get('text')}")
        lines.append("")
        lines.append("### Questions")
        lines.append("")
        for question in target.get("comparison_questions", []):
            lines.append(f"- {question}")
        lines.append("")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "target_count": len(packet.get('targets', []))}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
