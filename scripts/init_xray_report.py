#!/usr/bin/env python3
"""Initialize a structured xray report skeleton from a draft map."""

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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft-map", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    draft_map = json.loads(args.draft_map.read_text(encoding="utf-8"))
    sections = draft_map.get("sections", [])
    findings = []
    for section in sections:
        findings.append(
            {
                "id": f"todo-{section['section_id']}",
                "dimension": "mentor-drift",
                "severity": "P2",
                "section_id": section["section_id"],
                "paragraph_id": None,
                "issue": "TODO: fill after diagnosis",
                "evidence": f"Section heading: {section.get('heading')}",
                "recommended_action": "Diagnose this section against the rubric.",
                "do_not_break": [],
            }
        )

    payload = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "draft_id": draft_map.get("draft_id", args.draft_map.stem),
        "overall_summary": "TODO: fill after paper-xray review.",
        "overall_risk_level": "medium",
        "dimensions": [{"name": name, "score": 3, "summary": "TODO"} for name in DIMENSIONS],
        "findings": findings,
        "prioritized_actions": [],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "finding_count": len(findings)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
