#!/usr/bin/env python3
"""Build pass-based mentor-polish briefs and section tasks for agent consumption."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path | None) -> dict:
    if path is None or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


PASS_CONFIGS = [
    ("01_macro_pass.md", "macro-pass", "Focus on title/abstract/contribution/conclusion level structure and punch."),
    ("02_paragraph_pass.md", "paragraph-pass", "Fix paragraph roles, sequencing, topic sentences, transitions, and section flow."),
    ("03_sentence_pass.md", "sentence-pass", "Remove AI flavor, compress weak wording, and sharpen sentence-level precision."),
    ("04_terminology_pass.md", "terminology-pass", "Normalize terminology, abbreviations, and exact technical wording."),
    ("05_verify_pass.md", "verify-pass", "Check whether rewritten text resolved findings without breaking project facts."),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft-map", required=True, type=Path)
    parser.add_argument("--mentor-profile", required=True, type=Path)
    parser.add_argument("--xray-report", required=True, type=Path)
    parser.add_argument("--revision-agenda", required=True, type=Path)
    parser.add_argument("--project-fact-sheet", required=True, type=Path)
    parser.add_argument("--reference-mirror-packet", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    draft_map = load_json(args.draft_map)
    mentor_profile = load_json(args.mentor_profile)
    xray = load_json(args.xray_report)
    agenda = load_json(args.revision_agenda)
    fact = load_json(args.project_fact_sheet)
    mirror = load_json(args.reference_mirror_packet)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    pass_brief_names = []
    findings_by_section: dict[str, list[dict]] = defaultdict(list)
    for finding in xray.get("findings", []):
        findings_by_section[finding.get("section_id", "")].append(finding)

    actions_by_section: dict[str, list[dict]] = defaultdict(list)
    for action in agenda.get("ordered_actions", []):
        actions_by_section[action.get("section_id", "")].append(action)

    mirror_by_section = {item["section_id"]: item for item in mirror.get("targets", [])}

    for filename, pass_name, goal in PASS_CONFIGS:
        path = args.output_dir / filename
        pass_brief_names.append(filename)
        lines = []
        lines.append(f"# {pass_name}")
        lines.append("")
        lines.append(f"- goal: {goal}")
        lines.append(f"- draft_id: {draft_map.get('draft_id')}")
        lines.append("")
        lines.append("## Non-negotiable constraints")
        lines.append("")
        for item in fact.get("do_not_break_constraints", []):
            lines.append(f"- {item}")
        lines.append("")
        lines.append("## Global mentor rules")
        lines.append("")
        for rule in mentor_profile.get("global_rules", [])[:12]:
            lines.append(f"- {rule.get('rule')}")
        lines.append("")
        path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")

    section_tasks = []
    for section in draft_map.get("sections", []):
        sid = section["section_id"]
        if sid not in actions_by_section:
            continue
        task_path = args.output_dir / f"{sid}.md"
        lines = []
        lines.append(f"# Section Task: {sid} | {section.get('heading')}")
        lines.append("")
        lines.append("## Current Paragraphs")
        lines.append("")
        for paragraph in section.get("paragraphs", []):
            lines.append(f"### {paragraph.get('paragraph_id')}")
            lines.append(paragraph.get("text", ""))
            lines.append("")
        lines.append("## Findings")
        lines.append("")
        for finding in findings_by_section.get(sid, []):
            lines.append(
                f"- [{finding.get('severity')}] {finding.get('dimension')} | issue={finding.get('issue')} | evidence={finding.get('evidence')}"
            )
        lines.append("")
        lines.append("## Ordered Actions")
        lines.append("")
        for action in actions_by_section.get(sid, []):
            lines.append(
                f"- priority {action.get('priority')} | {action.get('action_type')} | {action.get('rationale')}"
            )
        lines.append("")
        lines.append("## Section Playbook")
        lines.append("")
        key = (section.get("heading") or "").lower()
        playbook = mentor_profile.get("section_playbooks", {}).get(key, {})
        if playbook:
            lines.append(f"- goal: {playbook.get('goal')}")
            lines.append(f"- structure: {playbook.get('structure_hint')}")
            lines.append(f"- must_include: {', '.join(playbook.get('must_include', []))}")
            lines.append(f"- must_avoid: {', '.join(playbook.get('must_avoid', []))}")
        else:
            lines.append("- no exact section playbook; follow global rules and findings.")
        lines.append("")
        lines.append("## Reference Mirror Hints")
        lines.append("")
        mirror_target = mirror_by_section.get(sid)
        if mirror_target:
            for snippet in mirror_target.get("mirror_snippets", []):
                lines.append(
                    f"- {snippet.get('source_path')}:{snippet.get('line_hint')} | {snippet.get('match_reason')} | {snippet.get('text')}"
                )
        else:
            lines.append("- no mirror hints packaged for this section.")
        lines.append("")
        lines.append("## Do-Not-Break Constraints")
        lines.append("")
        for item in fact.get("do_not_break_constraints", []):
            lines.append(f"- {item}")
        task_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
        section_tasks.append(
            {
                "section_id": sid,
                "heading": section.get("heading", ""),
                "task_file": task_path.name,
                "passes": ["macro-pass", "paragraph-pass", "sentence-pass", "terminology-pass", "verify-pass"],
            }
        )

    manifest = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "draft_id": draft_map.get("draft_id", args.draft_map.stem),
        "pass_briefs": pass_brief_names,
        "section_tasks": section_tasks,
    }
    manifest_path = args.output_dir / "workspace_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": str(args.output_dir), "section_task_count": len(section_tasks)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
