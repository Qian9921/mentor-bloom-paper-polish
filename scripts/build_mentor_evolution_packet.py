#!/usr/bin/env python3
"""Build an agent-consumable mentor evolution packet from new materials and the current profile."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


TEXT_EXTS = {".txt", ".md", ".tex"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def snippet_lines(text: str) -> list[tuple[int, str]]:
    scored = []
    for idx, raw in enumerate(text.splitlines(), start=1):
        line = re.sub(r"\s+", " ", raw).strip()
        if len(line) < 20:
            continue
        if re.fullmatch(r"\d+", line):
            continue
        lower = line.lower()
        score = 0
        if idx <= 60:
            score += 3
        if "abstract" in lower or "introduction" in lower or "conclusion" in lower:
            score += 4
        if any(token in lower for token in ["propose", "proposed", "results", "reduce", "improve", "efficient", "credibility", "uncertainty", "integrity", "logistic", "huber"]):
            score += 2
        if any(token in lower for token in ["do not", "avoid", "prefer", "must", "不要", "避免", "应该"]):
            score += 3
        scored.append((score, idx, line))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [(idx, line) for _, idx, line in scored]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--current-profile", required=True, type=Path)
    parser.add_argument("--current-manifest", required=True, type=Path)
    parser.add_argument("--previous-manifest", type=Path, default=None)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--snippet-limit", type=int, default=24)
    args = parser.parse_args()

    current_profile = load_json(args.current_profile)
    current_manifest = load_json(args.current_manifest)
    previous_manifest = load_json(args.previous_manifest) if args.previous_manifest else {"items": []}

    previous_hashes = {item.get("sha256") for item in previous_manifest.get("items", [])}
    root = Path(current_manifest["root_dir"])
    candidate_items = [
        item for item in current_manifest.get("items", [])
        if item.get("sha256") not in previous_hashes
    ]
    if not candidate_items:
        candidate_items = current_manifest.get("items", [])

    per_file_buckets = []
    for item in candidate_items:
        path = root / item["path"]
        if path.suffix.lower() not in TEXT_EXTS or not path.exists():
            continue
        bucket = []
        for line_no, text in snippet_lines(read_text(path)):
            reason = "new-material-evidence"
            lower = text.lower()
            if any(token in lower for token in ["do not", "avoid", "prefer", "must", "不要", "避免", "应该"]):
                reason = "rule-candidate"
            elif any(token in lower for token in ["figure", "table", "结果", "结论", "transition", "baseline", "metric", "evidence", "support"]):
                reason = "critique-candidate"
            bucket.append(
                {
                    "source_path": item["path"],
                    "source_type": item.get("source_type", "unknown"),
                    "trust_tier": item.get("trust_tier", "low"),
                    "line_hint": line_no,
                    "text": text,
                    "reason": reason,
                }
            )
        if bucket:
            per_file_buckets.append(bucket)

    snippets = []
    index = 0
    while len(snippets) < args.snippet_limit:
        progressed = False
        for bucket in per_file_buckets:
            if index < len(bucket):
                snippets.append(bucket[index])
                progressed = True
                if len(snippets) >= args.snippet_limit:
                    break
        if not progressed:
            break
        index += 1

    payload = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mentor_id": current_profile.get("mentor_id", "mentor"),
        "current_profile": str(args.current_profile),
        "new_material_manifest": str(args.current_manifest),
        "new_evidence_snippets": snippets,
        "questions_to_answer": [
            "What genuinely new mentor preferences are supported by the new materials?",
            "Which old rules should be strengthened, weakened, or retired?",
            "What conflicts appear between the new evidence and the current mentor profile?",
            "What should be promoted into the next mentor profile version?"
        ],
        "promotion_contract": {
            "delta_target": "docs/schemas/mentor_profile_delta.schema.json",
            "profile_target": "docs/schemas/compiled_mentor_profile.schema.json",
            "must_preserve_history": True
        }
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "snippet_count": len(snippets), "candidate_materials": len(candidate_items)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
