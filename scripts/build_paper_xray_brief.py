#!/usr/bin/env python3
"""Build a markdown brief for agent-authored paper xray."""

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
    parser.add_argument("--target-xray", required=True, type=Path)
    args = parser.parse_args()

    packet = load_json(args.packet)
    lines = []
    lines.append("# Paper Xray Brief")
    lines.append("")
    lines.append("## Mission")
    lines.append("")
    lines.append("Read the draft sections, mentor profile preview, term findings, and truth findings. Produce an evidence-backed `xray_report.json` authored by Codex/agent.")
    lines.append("")
    lines.append("## Required Dimensions")
    lines.append("")
    for dim in packet.get("rubric_dimensions", []):
        lines.append(f"- {dim}")
    lines.append("")
    lines.append("## Draft Sections")
    lines.append("")
    for section in packet.get("draft_sections", [])[:12]:
        lines.append(f"- {section.get('section_id')} | {section.get('heading')} | paragraphs={section.get('paragraph_count')}")
    lines.append("")
    lines.append("## Known Pre-Checks")
    lines.append("")
    for item in packet.get("term_findings", [])[:12]:
        lines.append(f"- term finding: {item}")
    for item in packet.get("truth_findings", [])[:12]:
        lines.append(f"- truth finding: {item}")
    lines.append("")
    lines.append("## Mentor Rules Preview")
    lines.append("")
    for item in packet.get("mentor_rules_preview", []):
        lines.append(f"- {item.get('rule')}")
    lines.append("")
    lines.append("## Do-Not-Break Constraints")
    lines.append("")
    for item in packet.get("do_not_break_constraints", []):
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Required Output")
    lines.append("")
    lines.append(f"- Write JSON to: `{args.target_xray}`")
    lines.append("- Follow schema: `docs/schemas/xray_report.schema.json`")
    lines.append("- Every important finding should cite local evidence from the draft.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "dimension_count": len(packet.get('rubric_dimensions', []))}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
