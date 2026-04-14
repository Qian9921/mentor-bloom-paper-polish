#!/usr/bin/env python3
"""Build an agent-consumable mentor distillation packet from a mentor manifest."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


TEXT_EXTS = {".txt", ".md", ".tex"}
RULE_PREFIXES = (
    "do not ",
    "don't ",
    "avoid ",
    "prefer ",
    "use ",
    "should ",
    "must ",
    "never ",
    "不要",
    "避免",
    "优先",
    "应该",
    "必须",
)
DOMAIN_CANDIDATES = [
    "integrated navigation",
    "integrated positioning",
    "positioning accuracy",
    "localization accuracy",
    "gnss observations",
    "urban navigation",
    "inertial measurements",
    "signal blockage",
    "multipath effects",
]
KEY_FEEDBACK_HINTS = (
    "ai",
    "转折",
    "baseline",
    "metric",
    "比较",
    "总结",
    "点名",
    "用词",
    "模糊",
    "清楚",
    "support",
    "evidence",
    "figure",
    "table",
    "结果",
    "结论",
)


def normalize_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def is_noise_line(line: str) -> bool:
    stripped = normalize_ws(line)
    if not stripped:
        return True
    if re.fullmatch(r"\d+", stripped):
        return True
    if re.fullmatch(r"说话人[A-Za-z一二三四五六七八九十0-9]+", stripped):
        return True
    if len(stripped) < 4:
        return True
    return False


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--snippet-limit", type=int, default=24)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    root = Path(manifest["root_dir"])
    evidence_snippets = []
    candidate_rules = []
    domain_hits: Counter[str] = Counter()

    for item in manifest.get("items", []):
        rel = item.get("path", "")
        path = root / rel
        if path.suffix.lower() not in TEXT_EXTS or not path.exists():
            continue
        text = read_text(path)
        if not text:
            continue
        lines = text.splitlines()
        for idx, raw in enumerate(lines, start=1):
            line = normalize_ws(raw)
            if is_noise_line(line):
                continue
            lower = line.lower()
            if len(evidence_snippets) < args.snippet_limit and idx <= 5:
                evidence_snippets.append(
                    {
                        "snippet_id": f"snippet-{len(evidence_snippets)+1:03d}",
                        "source_path": rel,
                        "source_type": item.get("source_type", "unknown"),
                        "trust_tier": item.get("trust_tier", "low"),
                        "line_hint": idx,
                        "text": line,
                        "reason": "opening-context"
                    }
                )
            if lower.startswith(RULE_PREFIXES):
                candidate_rules.append(
                    {
                        "text": line,
                        "source_path": rel,
                        "trust_tier": item.get("trust_tier", "low")
                    }
                )
                if len(evidence_snippets) < args.snippet_limit:
                    evidence_snippets.append(
                        {
                            "snippet_id": f"snippet-{len(evidence_snippets)+1:03d}",
                            "source_path": rel,
                            "source_type": item.get("source_type", "unknown"),
                            "trust_tier": item.get("trust_tier", "low"),
                            "line_hint": idx,
                            "text": line,
                            "reason": "explicit-rule"
                        }
                    )
            if any(hint in lower for hint in KEY_FEEDBACK_HINTS):
                if len(evidence_snippets) < args.snippet_limit:
                    evidence_snippets.append(
                        {
                            "snippet_id": f"snippet-{len(evidence_snippets)+1:03d}",
                            "source_path": rel,
                            "source_type": item.get("source_type", "unknown"),
                            "trust_tier": item.get("trust_tier", "low"),
                            "line_hint": idx,
                            "text": line,
                            "reason": "feedback-hint"
                        }
                    )
            if any(term in lower for term in DOMAIN_CANDIDATES):
                for term in DOMAIN_CANDIDATES:
                    if term in lower:
                        domain_hits[term] += 1
                if len(evidence_snippets) < args.snippet_limit:
                    evidence_snippets.append(
                        {
                            "snippet_id": f"snippet-{len(evidence_snippets)+1:03d}",
                            "source_path": rel,
                            "source_type": item.get("source_type", "unknown"),
                            "trust_tier": item.get("trust_tier", "low"),
                            "line_hint": idx,
                            "text": line,
                            "reason": "domain-term"
                        }
                    )

    candidate_terms = [term for term, _ in domain_hits.most_common()]

    payload = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mentor_id": manifest.get("mentor_id", "mentor"),
        "source_manifest": str(args.manifest),
        "source_summary": manifest.get("summary", {}),
        "evidence_snippets": evidence_snippets,
        "candidate_rules": candidate_rules,
        "candidate_terms": candidate_terms,
        "questions_to_answer": [
            "What does the supervisor repeatedly reject?",
            "What terminology does the supervisor prefer or insist on?",
            "How does the supervisor sharpen contribution and result language?",
            "What section-specific playbooks can be inferred?",
            "Which rewrite patterns are safe and reusable downstream?"
        ],
        "output_contract": {
            "target_schema": "docs/schemas/compiled_mentor_profile.schema.json",
            "required_sections": [
                "global_rules",
                "terminology_preferences",
                "rejection_lexicon",
                "rewrite_patterns",
                "section_playbooks"
            ],
            "must_cite_evidence": True
        }
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "snippet_count": len(evidence_snippets), "candidate_rule_count": len(candidate_rules)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
