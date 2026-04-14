#!/usr/bin/env python3
"""Build an agent-consumable paper-xray packet."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


DIMENSIONS = [
    "mentor-drift",
    "ai-smell",
    "terminology-risk",
    "claim-precision",
    "transition-rhythm",
    "paragraph-architecture",
    "evidence-language-gap",
    "truth-risk-lite",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft-map", required=True, type=Path)
    parser.add_argument("--mentor-profile", required=True, type=Path)
    parser.add_argument("--project-fact-sheet", required=True, type=Path)
    parser.add_argument("--term-check", required=True, type=Path)
    parser.add_argument("--truth-check", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    draft_map = load_json(args.draft_map)
    mentor = load_json(args.mentor_profile)
    fact = load_json(args.project_fact_sheet)
    term = load_json(args.term_check)
    truth = load_json(args.truth_check)

    payload = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "draft_id": draft_map.get("draft_id", args.draft_map.stem),
        "mentor_profile": str(args.mentor_profile),
        "project_fact_sheet": str(args.project_fact_sheet),
        "draft_sections": draft_map.get("sections", []),
        "term_findings": term.get("findings", []),
        "truth_findings": truth.get("findings", []),
        "rubric_dimensions": DIMENSIONS,
        "output_contract": {
            "target_schema": "docs/schemas/xray_report.schema.json",
            "required_fields": [
                "overall_summary",
                "overall_risk_level",
                "dimensions",
                "findings",
                "prioritized_actions"
            ]
        },
        "mentor_rules_preview": mentor.get("global_rules", [])[:12],
        "do_not_break_constraints": fact.get("do_not_break_constraints", []),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "section_count": len(payload["draft_sections"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
