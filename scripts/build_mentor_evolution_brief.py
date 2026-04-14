#!/usr/bin/env python3
"""Build a markdown brief for agent-authored mentor evolution."""

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
    parser.add_argument("--target-delta", required=True, type=Path)
    args = parser.parse_args()

    packet = load_json(args.packet)
    lines = []
    lines.append("# Mentor Bloom Brief")
    lines.append("")
    lines.append("## Mission")
    lines.append("")
    lines.append("Read the new mentor-side evidence and compare it against the current mentor profile. Propose an incremental mentor_profile_delta rather than rewriting the profile blindly.")
    lines.append("")
    lines.append("## Questions To Answer")
    lines.append("")
    for q in packet.get("questions_to_answer", []):
        lines.append(f"- {q}")
    lines.append("")
    lines.append("## New Evidence Snippets")
    lines.append("")
    for item in packet.get("new_evidence_snippets", [])[:24]:
        lines.append(
            f"- {item.get('source_path')}:{item.get('line_hint')} | trust={item.get('trust_tier')} | reason={item.get('reason')} | {item.get('text')}"
        )
    lines.append("")
    lines.append("## Required Output")
    lines.append("")
    lines.append(f"- Write JSON to: `{args.target_delta}`")
    lines.append("- Follow schema: `docs/schemas/mentor_profile_delta.schema.json`")
    lines.append("- Focus on delta: what to add, strengthen, weaken, or retire.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "snippet_count": len(packet.get('new_evidence_snippets', []))}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
