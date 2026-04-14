#!/usr/bin/env python3
"""Assemble a revision packet for mentor-polish runs."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path | None) -> dict:
    if path is None:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(text: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else " " for ch in text).strip()


def resolve_playbook(section_heading: str, profile: dict) -> dict:
    playbooks = profile.get("section_playbooks", {})
    if not isinstance(playbooks, dict):
        return {}
    heading = normalize(section_heading)
    if heading in playbooks:
        return playbooks[heading]
    for key, value in playbooks.items():
        if key in heading or heading in key:
            return value
    return {}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft-map", required=True, type=Path)
    parser.add_argument("--mentor-profile", required=True, type=Path)
    parser.add_argument("--xray-report", type=Path)
    parser.add_argument("--revision-agenda", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    draft_map = load_json(args.draft_map)
    mentor_profile = load_json(args.mentor_profile)
    xray = load_json(args.xray_report)
    agenda = load_json(args.revision_agenda)

    findings_by_section: dict[str, list[dict]] = {}
    for finding in xray.get("findings", []):
        section_id = finding.get("section_id", "unscoped")
        findings_by_section.setdefault(section_id, []).append(finding)

    actions_by_section: dict[str, list[dict]] = {}
    for action in agenda.get("ordered_actions", []):
        section_id = action.get("section_id", "unscoped")
        actions_by_section.setdefault(section_id, []).append(action)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    section_files = []
    for section in draft_map.get("sections", []):
        section_id = section["section_id"]
        packet = {
            "section_id": section_id,
            "heading": section.get("heading"),
            "level": section.get("level"),
            "mentor_global_rules": mentor_profile.get("global_rules", []),
            "mentor_terminology_preferences": mentor_profile.get("terminology_preferences", {}),
            "mentor_section_playbook": resolve_playbook(section.get("heading", ""), mentor_profile),
            "xray_findings": findings_by_section.get(section_id, []),
            "agenda_actions": actions_by_section.get(section_id, []),
            "paragraphs": section.get("paragraphs", []),
        }
        section_path = args.output_dir / f"{section_id}.json"
        section_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        section_files.append(section_path.name)

    manifest = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "draft_map": str(args.draft_map),
        "mentor_profile": str(args.mentor_profile),
        "xray_report": str(args.xray_report) if args.xray_report else None,
        "revision_agenda": str(args.revision_agenda) if args.revision_agenda else None,
        "section_packet_count": len(section_files),
        "section_packets": section_files,
    }
    manifest_path = args.output_dir / "packet_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": str(args.output_dir), "section_packet_count": len(section_files)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
