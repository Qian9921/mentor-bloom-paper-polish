#!/usr/bin/env python3
"""Normalize an explicit must-fix defect ledger and emit JSON + markdown."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", required=True, type=Path, help="Input defect seed JSON")
    parser.add_argument("--output-json", required=True, type=Path, help="Normalized ledger JSON")
    parser.add_argument("--output-md", type=Path, default=None, help="Optional markdown summary")
    args = parser.parse_args()

    seed = load_json(args.seed)
    defects = []
    for idx, item in enumerate(seed.get("defects", []), start=1):
        defects.append(
            {
                "defect_id": item.get("defect_id", f"defect-{idx:03d}"),
                "issue": item["issue"],
                "category": item.get("category", "writing"),
                "source_ref": item["source_ref"],
                "source_excerpt": item.get("source_excerpt", ""),
                "target_file": item.get("target_file", ""),
                "target_locator": item.get("target_locator", ""),
                "status": item.get("status", "open"),
                "blocking": bool(item.get("blocking", True)),
                "evidence": item.get("evidence", []),
                "notes": item.get("notes", ""),
            }
        )

    payload = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "subject_id": seed.get("subject_id", "draft"),
        "source_context": seed.get("source_context", ""),
        "defects": defects,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md_path = args.output_md or args.output_json.with_suffix(".md")
    status_counts: dict[str, int] = {}
    for item in defects:
        status_counts[item["status"]] = status_counts.get(item["status"], 0) + 1

    lines = [
        "# Defect Ledger",
        "",
        f"- subject_id: {payload['subject_id']}",
        f"- total_defects: {len(defects)}",
    ]
    for status in ["open", "fixed", "verified", "rejected"]:
        lines.append(f"- {status}: {status_counts.get(status, 0)}")
    lines.append("")
    for item in defects:
        lines.extend(
            [
                f"## {item['defect_id']} | {item['status']}",
                "",
                f"- issue: {item['issue']}",
                f"- category: {item['category']}",
                f"- source_ref: {item['source_ref']}",
                f"- target: {item['target_file']} :: {item['target_locator']}",
                f"- blocking: {item['blocking']}",
            ]
        )
        if item.get("source_excerpt"):
            lines.append(f"- source_excerpt: {item['source_excerpt']}")
        if item.get("evidence"):
            lines.append("- evidence:")
            for evidence in item["evidence"]:
                lines.append(f"  - {evidence}")
        if item.get("notes"):
            lines.append(f"- notes: {item['notes']}")
        lines.append("")
    md_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(json.dumps({"output_json": str(args.output_json), "output_md": str(md_path), "defect_count": len(defects)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
