#!/usr/bin/env python3
"""Build a markdown brief for agent-authored revision agenda generation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xray-report", required=True, type=Path)
    parser.add_argument("--mentor-profile", required=True, type=Path)
    parser.add_argument("--project-fact-sheet", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--target-agenda", required=True, type=Path)
    args = parser.parse_args()

    xray = load_json(args.xray_report)
    mentor = load_json(args.mentor_profile)
    fact = load_json(args.project_fact_sheet)

    lines = []
    lines.append("# Revision Agenda Brief")
    lines.append("")
    lines.append("## Mission")
    lines.append("")
    lines.append("Turn the xray findings into an ordered revision agenda authored by Codex/agent. Prioritize truth protection first, then supervisor-visible weaknesses, then local polish.")
    lines.append("")
    lines.append("## Highest-Priority Findings")
    lines.append("")
    for item in xray.get("findings", [])[:20]:
        lines.append(
            f"- [{item.get('severity')}] {item.get('dimension')} | section={item.get('section_id')} | issue={item.get('issue')} | action={item.get('recommended_action')}"
        )
    lines.append("")
    lines.append("## Mentor Rules Preview")
    lines.append("")
    for item in mentor.get("global_rules", [])[:10]:
        lines.append(f"- {item.get('rule')}")
    lines.append("")
    lines.append("## Do-Not-Break Constraints")
    lines.append("")
    for item in fact.get("do_not_break_constraints", []):
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Required Output")
    lines.append("")
    lines.append(f"- Write JSON to: `{args.target_agenda}`")
    lines.append("- Follow schema: `docs/schemas/revision_agenda.schema.json`")
    lines.append("- Do not sort mechanically by file order; sort by revision leverage and scientific safety.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "finding_count": len(xray.get('findings', []))}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
