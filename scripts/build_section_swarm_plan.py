#!/usr/bin/env python3
"""Build a section-level swarm staffing plan from a draft map."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_AUDITORS = [
    "opening_auditor",
    "sentence_word_auditor",
    "transition_flow_auditor",
    "section_contract_auditor",
    "holistic_mentor_alignment_auditor",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def should_skip(section: dict) -> bool:
    heading = section.get("heading", "").strip().lower()
    if not heading or heading == "front matter":
        return True
    return False


def build_payload(draft_map: dict, max_concurrent_agents: int) -> dict:
    sections = []
    for section in draft_map.get("sections", []):
        if should_skip(section):
            continue
        logical_agents = [
            *DEFAULT_AUDITORS,
            "section_consensus_agent",
            "section_reverse_check_agent",
        ]
        waves = [
            {
                "wave_id": "wave-a-auditors",
                "agents": DEFAULT_AUDITORS,
            },
            {
                "wave_id": "wave-b-consensus",
                "agents": ["section_consensus_agent"],
            },
            {
                "wave_id": "wave-c-recheck",
                "agents": ["section_reverse_check_agent"],
            },
        ]
        sections.append(
            {
                "section_id": section["section_id"],
                "heading": section.get("heading", ""),
                "paragraph_count": section.get("paragraph_count", 0),
                "logical_agents": logical_agents,
                "waves": waves,
                "notes": "Each paragraph must be read by at least one audit agent; high-risk sections should be read by all five auditors.",
            }
        )

    return {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "draft_id": draft_map.get("draft_id", "draft"),
        "max_concurrent_agents": max_concurrent_agents,
        "sections": sections,
    }


def write_markdown(payload: dict, output: Path) -> None:
    lines = [
        "# Section Swarm Plan",
        "",
        f"- draft_id: {payload['draft_id']}",
        f"- section_count: {len(payload['sections'])}",
        f"- logical_agents_per_section: 7",
        f"- max_concurrent_agents: {payload['max_concurrent_agents']}",
        "",
    ]
    for section in payload["sections"]:
        lines.append(f"## {section['section_id']} | {section['heading']}")
        lines.append("")
        lines.append(f"- paragraph_count: {section['paragraph_count']}")
        lines.append(f"- logical_agents: {', '.join(section['logical_agents'])}")
        for wave in section["waves"]:
            lines.append(f"- {wave['wave_id']}: {', '.join(wave['agents'])}")
        lines.append(f"- notes: {section['notes']}")
        lines.append("")
    output.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft-map", required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    parser.add_argument("--output-md", type=Path, default=None)
    parser.add_argument("--max-concurrent-agents", type=int, default=6)
    args = parser.parse_args()

    draft_map = load_json(args.draft_map)
    payload = build_payload(draft_map, args.max_concurrent_agents)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path = args.output_md or args.output_json.with_suffix(".md")
    write_markdown(payload, md_path)
    print(
        json.dumps(
            {
                "output_json": str(args.output_json),
                "output_md": str(md_path),
                "section_count": len(payload["sections"]),
                "logical_agents_per_section": 7,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
