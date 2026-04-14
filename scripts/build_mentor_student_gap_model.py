#!/usr/bin/env python3
"""Build a mentor-student gap model from one or more xray reports."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


GAP_MAP = {
    "mentor-drift": ("mentor_drift", "rewrite"),
    "ai-smell": ("ai_smell", "tighten_sentence"),
    "terminology-risk": ("terminology_vagueness", "replace_vague_word_with_domain_term"),
    "claim-precision": ("comparison_or_scope_weakness", "name_the_comparator"),
    "transition-rhythm": ("transition_weakness", "add_bridge_transition"),
    "paragraph-architecture": ("paragraph_overload", "split_dense_paragraph"),
    "evidence-language-gap": ("weak_result_implication", "metric-only-to-value-plus-boundary"),
    "truth-risk-lite": ("boundary_control_risk", "protect_truth"),
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def severity_for_count(count: int) -> str:
    if count >= 6:
        return "high"
    if count >= 3:
        return "medium"
    return "low"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xray-report", action="append", required=True, type=Path)
    parser.add_argument("--mentor-id", required=True)
    parser.add_argument("--user-id", default="user")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    buckets = defaultdict(list)
    for path in args.xray_report:
        report = load_json(path)
        for finding in report.get("findings", []):
            gap_type, operator = GAP_MAP.get(finding.get("dimension", ""), ("general_gap", "rewrite"))
            buckets[(gap_type, operator)].append(finding.get("issue", ""))

    gap_types = []
    for (gap_type, operator), issues in buckets.items():
        gap_types.append(
            {
                "gap_type": gap_type,
                "severity": severity_for_count(len(issues)),
                "description": issues[0] if issues else "",
                "evidence_count": len(issues),
                "example_findings": issues[:5],
                "recommended_operator": operator,
            }
        )
    gap_types.sort(key=lambda item: (-item["evidence_count"], item["gap_type"]))

    payload = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mentor_id": args.mentor_id,
        "user_id": args.user_id,
        "gap_types": gap_types,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "gap_type_count": len(gap_types)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
