#!/usr/bin/env python3
"""Initialize a revision agenda from an xray report."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


SEVERITY_ORDER = {"P0": 0, "P1": 1, "P2": 2}
DIMENSION_TO_ACTION = {
    "truth-risk-lite": "protect_truth",
    "claim-precision": "tighten_claim",
    "ai-smell": "replace_ai_style",
    "transition-rhythm": "repair_transition",
    "paragraph-architecture": "repair_paragraph_structure",
    "terminology-risk": "fix_terminology",
    "mentor-drift": "rewrite",
    "evidence-language-gap": "tighten_claim",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xray-report", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    xray = json.loads(args.xray_report.read_text(encoding="utf-8"))
    findings = sorted(
        xray.get("findings", []),
        key=lambda item: (SEVERITY_ORDER.get(item.get("severity", "P2"), 9), item.get("section_id", ""), item.get("id", "")),
    )
    actions = []
    for priority, finding in enumerate(findings, start=1):
        action_type = DIMENSION_TO_ACTION.get(finding.get("dimension", ""), "rewrite")
        actions.append(
            {
                "priority": priority,
                "section_id": finding.get("section_id"),
                "paragraph_id": finding.get("paragraph_id"),
                "action_type": action_type,
                "rationale": finding.get("issue", ""),
                "linked_findings": [finding.get("id")],
                "constraints": finding.get("do_not_break", []),
                "success_criteria": [
                    "Finding is explicitly addressed.",
                    "Revision remains faithful to project facts.",
                ],
            }
        )

    payload = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "draft_id": xray.get("draft_id", args.xray_report.stem),
        "strategy_summary": "Prioritize truth protection first, then supervisor-visible weaknesses, then style cleanup.",
        "ordered_actions": actions,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "action_count": len(actions)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
