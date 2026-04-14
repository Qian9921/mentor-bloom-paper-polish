#!/usr/bin/env python3
"""Build a Codex/agent-facing markdown brief for mentor-brain distillation."""

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
    parser.add_argument("--target-profile", required=True, type=Path)
    args = parser.parse_args()

    packet = load_json(args.packet)
    lines = []
    lines.append("# Mentor Brain Distillation Brief")
    lines.append("")
    lines.append("## Mission")
    lines.append("")
    lines.append("Consume the mentor distillation packet and author a `compiled_mentor_profile.json` that can be used by downstream xray and polish agents.")
    lines.append("")
    lines.append("## Non-negotiable Rules")
    lines.append("")
    lines.append("- Do not learn from the target draft.")
    lines.append("- Do not invent supervisor preferences without evidence.")
    lines.append("- Prefer high-trust mentor-authored or mentor-edited evidence.")
    lines.append("- Output must follow the compiled mentor profile schema.")
    lines.append("")
    lines.append("## Questions You Must Answer")
    lines.append("")
    for question in packet.get("questions_to_answer", []):
        lines.append(f"- {question}")
    lines.append("")
    lines.append("## Candidate Rules")
    lines.append("")
    for item in packet.get("candidate_rules", [])[:20]:
        lines.append(f"- [{item.get('trust_tier')}] {item.get('text')} ({item.get('source_path')})")
    lines.append("")
    lines.append("## Candidate Terms")
    lines.append("")
    for term in packet.get("candidate_terms", []):
        lines.append(f"- {term}")
    lines.append("")
    lines.append("## Evidence Snippets")
    lines.append("")
    for item in packet.get("evidence_snippets", [])[:20]:
        lines.append(
            f"- {item.get('snippet_id')} | {item.get('source_path')} | trust={item.get('trust_tier')} | reason={item.get('reason')} | {item.get('text')}"
        )
    lines.append("")
    lines.append("## Required Output")
    lines.append("")
    lines.append(f"- Write JSON to: `{args.target_profile}`")
    lines.append("- Follow schema: `docs/schemas/compiled_mentor_profile.schema.json`")
    lines.append("- Also include evidence-backed `global_rules`, `terminology_preferences`, `rejection_lexicon`, `rewrite_patterns`, and `section_playbooks`.")
    lines.append("")
    lines.append("## Consumption Reminder")
    lines.append("")
    lines.append("This is the canonical path: scripts prepare the packet, but Codex/agent must perform the actual mentor-brain synthesis.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "snippet_count": len(packet.get('evidence_snippets', []))}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
