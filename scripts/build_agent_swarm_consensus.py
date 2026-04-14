#!/usr/bin/env python3
"""Merge multiple agent-authored audit reports into a consensus artifact."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


SEVERITY_ORDER = {"must_fix": 3, "strong": 2, "soft": 1}
VERDICT_ORDER = {"fail": 3, "borderline": 2, "pass_but_tighten": 1, "pass": 0}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", action="append", required=True, type=Path, help="Agent-authored audit report JSON")
    parser.add_argument("--output-json", required=True, type=Path)
    parser.add_argument("--output-md", type=Path, default=None)
    args = parser.parse_args()

    reports = [load_json(path) for path in args.report]
    if not reports:
        raise SystemExit("No reports provided")

    draft_id = reports[0].get("draft_id", "draft")
    section_buckets: dict[str, dict] = {}
    finding_buckets: dict[tuple[str, str], dict] = {}

    for path, report in zip(args.report, reports):
        auditor = report.get("auditor", path.stem)
        for item in report.get("section_verdicts", []):
            key = item["section_id"]
            bucket = section_buckets.setdefault(
                key,
                {"section_id": key, "verdict": item["verdict"], "supporting_reports": []},
            )
            if VERDICT_ORDER[item["verdict"]] > VERDICT_ORDER[bucket["verdict"]]:
                bucket["verdict"] = item["verdict"]
            bucket["supporting_reports"].append(auditor)

        for item in report.get("findings", []):
            key = (item["target_locator"], item["issue"])
            bucket = finding_buckets.setdefault(
                key,
                {
                    "target_locator": item["target_locator"],
                    "issue_type": item["issue_type"],
                    "severity": item["severity"],
                    "issue": item["issue"],
                    "rewrite_direction": item["rewrite_direction"],
                    "supporting_auditors": [],
                },
            )
            if SEVERITY_ORDER[item["severity"]] > SEVERITY_ORDER[bucket["severity"]]:
                bucket["severity"] = item["severity"]
            if auditor not in bucket["supporting_auditors"]:
                bucket["supporting_auditors"].append(auditor)

    section_verdicts = sorted(section_buckets.values(), key=lambda item: item["section_id"])
    findings = sorted(
        finding_buckets.values(),
        key=lambda item: (-SEVERITY_ORDER[item["severity"]], item["target_locator"], item["issue"]),
    )
    blocking_count = sum(1 for item in findings if item["severity"] == "must_fix")

    payload = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "draft_id": draft_id,
        "source_reports": [str(path) for path in args.report],
        "section_verdicts": section_verdicts,
        "consensus_findings": findings,
        "blocking_count": blocking_count,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md_path = args.output_md or args.output_json.with_suffix(".md")
    lines = [
        "# Agent Swarm Consensus",
        "",
        f"- draft_id: {draft_id}",
        f"- source_reports: {len(args.report)}",
        f"- blocking_count: {blocking_count}",
        "",
        "## Section verdicts",
        "",
    ]
    for item in section_verdicts:
        lines.append(f"- {item['section_id']}: {item['verdict']} ({', '.join(item['supporting_reports'])})")
    lines += ["", "## Consensus findings", ""]
    for item in findings:
        lines.append(f"### {item['target_locator']} | {item['severity']}")
        lines.append(f"- issue_type: {item['issue_type']}")
        lines.append(f"- issue: {item['issue']}")
        lines.append(f"- rewrite_direction: {item['rewrite_direction']}")
        lines.append(f"- supporting_auditors: {', '.join(item['supporting_auditors'])}")
        lines.append("")
    md_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(json.dumps({"output_json": str(args.output_json), "output_md": str(md_path), "blocking_count": blocking_count}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
