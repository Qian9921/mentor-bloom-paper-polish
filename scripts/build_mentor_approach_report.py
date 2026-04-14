#!/usr/bin/env python3
"""Build a mentor-approach report from an xray report and mentor profile."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


DIMENSION_ORDER = [
    "mentor-drift",
    "ai-smell",
    "terminology-risk",
    "claim-precision",
    "transition-rhythm",
    "paragraph-architecture",
    "evidence-language-gap",
    "truth-risk-lite",
]


def verdict_for_score(score: int) -> str:
    if score >= 85:
        return "close to mentor-grade"
    if score >= 70:
        return "promising but still visibly below mentor-grade"
    if score >= 55:
        return "mid-stage draft; strong work remains"
    return "far from mentor-grade"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xray-report", required=True, type=Path)
    parser.add_argument("--mentor-profile", required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    parser.add_argument("--output-md", type=Path, default=None)
    args = parser.parse_args()

    xray = load_json(args.xray_report)
    mentor = load_json(args.mentor_profile)
    xdims = {item["name"]: item for item in xray.get("dimensions", [])}
    dimensions = []
    total = 0.0
    for name in DIMENSION_ORDER:
        item = xdims.get(name, {"score": 3, "summary": "No summary provided."})
        score = float(item.get("score", 3))
        total += score
        dimensions.append(
            {
                "name": name,
                "score": score,
                "out_of": 5,
                "summary": item.get("summary", ""),
                "target_direction": "push toward 5/5 mentor-grade writing quality",
            }
        )
    overall_score = round(total / (5 * len(DIMENSION_ORDER)) * 100)
    findings = xray.get("findings", [])
    top_gaps = [f"{f.get('section_id','')}: {f.get('issue','')}" for f in findings[:8]]
    strengths = [
        f"{d['name']}: {d['summary']}"
        for d in sorted(dimensions, key=lambda d: d["score"], reverse=True)[:3]
    ]
    report = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "draft_id": xray.get("draft_id", args.xray_report.stem),
        "overall_score": overall_score,
        "verdict": verdict_for_score(overall_score),
        "dimensions": dimensions,
        "top_gaps": top_gaps,
        "strengths": strengths,
        "revision_goal": "Move the draft toward mentor-grade writing by first closing the largest structure/rhythm/terminology gaps and then tightening sentence-level phrasing.",
        "recommended_order": [
            "highest-severity structural gaps",
            "results narration and comparison clarity",
            "terminology tightening",
            "sentence-level micro-polish",
        ],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md_path = args.output_md or args.output_json.with_suffix(".md")
    lines = []
    lines.append("# Mentor Approach Report")
    lines.append("")
    lines.append(f"- overall_score: {overall_score}/100")
    lines.append(f"- verdict: {report['verdict']}")
    lines.append("")
    lines.append("## Strongest areas")
    lines.append("")
    for item in strengths:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Largest gaps")
    lines.append("")
    for item in top_gaps:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Recommended revision order")
    lines.append("")
    for item in report["recommended_order"]:
        lines.append(f"- {item}")
    md_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(json.dumps({"output_json": str(args.output_json), "output_md": str(md_path), "overall_score": overall_score}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
