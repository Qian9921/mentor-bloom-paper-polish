#!/usr/bin/env python3
"""Export a markdown brief for Codex/agent mentor-polish execution."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mentor-profile", required=True, type=Path)
    parser.add_argument("--xray-report", required=True, type=Path)
    parser.add_argument("--revision-agenda", required=True, type=Path)
    parser.add_argument("--project-fact-sheet", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    mentor = load_json(args.mentor_profile)
    xray = load_json(args.xray_report)
    agenda = load_json(args.revision_agenda)
    fact = load_json(args.project_fact_sheet)

    lines = []
    lines.append("# Mentor Polish Brief")
    lines.append("")
    lines.append("## Goal")
    lines.append("")
    lines.append("Use the mentor profile and revision agenda to revise the draft toward supervisor-level quality without breaking project facts.")
    lines.append("")
    lines.append("## Global Rules")
    lines.append("")
    for rule in mentor.get("global_rules", []):
        lines.append(f"- {rule.get('rule')}")
    lines.append("")
    lines.append("## Preferred Terms")
    lines.append("")
    for item in mentor.get("terminology_preferences", {}).get("preferred_terms", []):
        aliases = item.get("aliases", [])
        alias_suffix = f" | aliases: {', '.join(aliases)}" if aliases else ""
        lines.append(f"- {item.get('term')}{alias_suffix}")
    lines.append("")
    lines.append("## Disallowed Terms")
    lines.append("")
    for item in mentor.get("terminology_preferences", {}).get("disallowed_terms", []):
        hint = item.get("replacement_hint") or "(replace with a more precise term)"
        lines.append(f"- {item.get('term')} -> {hint}")
    lines.append("")
    lines.append("## Do-Not-Break Constraints")
    lines.append("")
    for item in fact.get("do_not_break_constraints", []):
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Highest-Priority Findings")
    lines.append("")
    for finding in xray.get("findings", [])[:12]:
        lines.append(
            f"- [{finding.get('severity')}] {finding.get('dimension')} | section={finding.get('section_id')} | issue={finding.get('issue')} | evidence={finding.get('evidence')}"
        )
    lines.append("")
    lines.append("## Ordered Actions")
    lines.append("")
    for action in agenda.get("ordered_actions", []):
        constraints = action.get("constraints", [])
        lines.append(f"### Priority {action.get('priority')}")
        lines.append(f"- section: {action.get('section_id')}")
        lines.append(f"- action_type: {action.get('action_type')}")
        lines.append(f"- rationale: {action.get('rationale')}")
        if constraints:
            lines.append(f"- constraints: {', '.join(constraints)}")
        if action.get("success_criteria"):
            lines.append("- success criteria:")
            for criterion in action["success_criteria"]:
                lines.append(f"  - {criterion}")
        lines.append("")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "action_count": len(agenda.get("ordered_actions", []))}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
