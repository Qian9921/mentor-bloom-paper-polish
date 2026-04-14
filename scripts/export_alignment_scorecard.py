#!/usr/bin/env python3
"""Export a mentor-alignment scorecard by comparing two xray reports."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dimension_map(xray: dict) -> dict[str, dict]:
    return {item["name"]: item for item in xray.get("dimensions", [])}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before-xray", required=True, type=Path)
    parser.add_argument("--after-xray", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    before = load_json(args.before_xray)
    after = load_json(args.after_xray)
    before_map = dimension_map(before)
    after_map = dimension_map(after)
    names = sorted(set(before_map) | set(after_map))
    dimensions = []
    improved = 0
    regressed = 0
    unchanged = 0

    for name in names:
        before_score = float(before_map.get(name, {}).get("score", 0))
        after_score = float(after_map.get(name, {}).get("score", 0))
        delta = after_score - before_score
        if delta > 0:
            improved += 1
        elif delta < 0:
            regressed += 1
        else:
            unchanged += 1
        notes = f"before={before_map.get(name, {}).get('summary', '')} | after={after_map.get(name, {}).get('summary', '')}"
        dimensions.append({"name": name, "before": before_score, "after": after_score, "delta": delta, "notes": notes})

    summary = f"Improved dimensions: {improved}; regressed: {regressed}; unchanged: {unchanged}."
    payload = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "draft_id": after.get("draft_id", before.get("draft_id", "draft")),
        "dimensions": dimensions,
        "summary": summary,
        "remaining_risks": [
            item.get("issue", "")
            for item in after.get("findings", [])
            if item.get("severity") in {"P0", "P1"}
        ][:10],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "improved": improved, "regressed": regressed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
