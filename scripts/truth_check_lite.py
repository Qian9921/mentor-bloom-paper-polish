#!/usr/bin/env python3
"""Run a lightweight scientific-risk check on a draft map."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


RISK_PATTERNS = [
    ("overclaim-first", re.compile(r"\b(first|best|state[- ]of[- ]the[- ]art)\b", re.IGNORECASE), "P0", "Verify that novelty/comparison claims are explicitly supported."),
    ("overclaim-improvement", re.compile(r"\b(significantly improves?|greatly enhances?|outperforms?|superior performance|better performance)\b", re.IGNORECASE), "P1", "Add comparator, metric, and condition boundaries."),
    ("inflated-novelty", re.compile(r"\b(very novel|highly effective|robust results)\b", re.IGNORECASE), "P1", "Replace hype with bounded technical description."),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft-map", required=True, type=Path)
    parser.add_argument("--project-fact-sheet", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    draft_map = json.loads(args.draft_map.read_text(encoding="utf-8"))
    fact_sheet = json.loads(args.project_fact_sheet.read_text(encoding="utf-8")) if args.project_fact_sheet else {}
    findings = []
    for section in draft_map.get("sections", []):
        section_id = section["section_id"]
        for paragraph in section.get("paragraphs", []):
            text = paragraph.get("text", "")
            for risk_name, pattern, severity, action in RISK_PATTERNS:
                for match in pattern.finditer(text):
                    findings.append(
                        {
                            "id": f"{risk_name}-{section_id}-{paragraph['paragraph_id']}-{match.start()}",
                            "severity": severity,
                            "risk_type": risk_name,
                            "section_id": section_id,
                            "paragraph_id": paragraph["paragraph_id"],
                            "evidence": match.group(0),
                            "recommended_action": action,
                        }
                    )

    if fact_sheet.get("do_not_break_constraints"):
        for idx, constraint in enumerate(fact_sheet["do_not_break_constraints"], start=1):
            findings.append(
                {
                    "id": f"constraint-{idx:03d}",
                    "severity": "P2",
                    "risk_type": "do-not-break-constraint",
                    "section_id": "",
                    "paragraph_id": "",
                    "evidence": constraint,
                    "recommended_action": "Carry this constraint into mentor-polish and revision verification.",
                }
            )

    overall = "low"
    if any(item["severity"] == "P0" for item in findings):
        overall = "high"
    elif any(item["severity"] == "P1" for item in findings):
        overall = "medium"

    payload = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "draft_id": draft_map.get("draft_id", args.draft_map.stem),
        "overall_risk_level": overall,
        "findings": findings,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "finding_count": len(findings), "overall_risk_level": overall}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
