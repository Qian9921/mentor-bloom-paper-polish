#!/usr/bin/env python3
"""Generate a heuristic xray report from draft, mentor profile, term check, and truth-check findings."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


AI_PATTERNS = [
    ("it is worth noting that", "Template phrase sounds machine-like."),
    ("very novel", "Inflated novelty phrasing."),
    ("better performance", "Generic performance language without specificity."),
    ("robust results", "Weak generic evaluation phrase."),
]
CLAIM_PATTERNS = [
    ("improves", "Specify compared-to-what and under what conditions."),
    ("better performance", "Name the comparator and metric."),
    ("novel", "State the contribution concretely rather than via hype."),
]
TRANSITION_STARTERS = ("in this work", "experimental results show", "many existing methods")


def load_json(path: Path | None) -> dict:
    if path is None or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def section_text(section: dict) -> str:
    return "\n".join(paragraph.get("text", "") for paragraph in section.get("paragraphs", []))


def add_finding(findings: list[dict], dimension: str, severity: str, section_id: str, paragraph_id: str | None, issue: str, evidence: str, action: str, do_not_break: list[str] | None = None) -> None:
    findings.append(
        {
            "id": f"{dimension}-{section_id}-{paragraph_id or 'section'}-{len(findings)+1:03d}",
            "dimension": dimension,
            "severity": severity,
            "section_id": section_id,
            "paragraph_id": paragraph_id,
            "issue": issue,
            "evidence": evidence,
            "recommended_action": action,
            "do_not_break": do_not_break or [],
        }
    )


def compute_dimension_scores(findings: list[dict]) -> dict[str, int]:
    scores = {name: 5 for name in [
        "mentor-drift",
        "ai-smell",
        "terminology-risk",
        "claim-precision",
        "transition-rhythm",
        "paragraph-architecture",
        "evidence-language-gap",
        "truth-risk-lite",
    ]}
    penalty = {"P0": 2, "P1": 1, "P2": 1}
    for item in findings:
        scores[item["dimension"]] = max(1, scores[item["dimension"]] - penalty.get(item["severity"], 1))
    return scores


def severity_rank(sev: str) -> int:
    return {"P0": 0, "P1": 1, "P2": 2}.get(sev, 9)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft-map", required=True, type=Path)
    parser.add_argument("--mentor-profile", required=True, type=Path)
    parser.add_argument("--term-check", type=Path)
    parser.add_argument("--truth-check", type=Path)
    parser.add_argument("--project-fact-sheet", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    draft_map = load_json(args.draft_map)
    mentor_profile = load_json(args.mentor_profile)
    term_check = load_json(args.term_check)
    truth_check = load_json(args.truth_check)
    fact_sheet = load_json(args.project_fact_sheet)
    findings: list[dict] = []

    rejection_patterns = [
        (item.get("pattern", "").lower(), item.get("reason", "Mentor rejected pattern."), item.get("severity", "medium"))
        for item in mentor_profile.get("rejection_lexicon", [])
        if item.get("pattern")
    ]
    constraints = fact_sheet.get("do_not_break_constraints", [])

    for section in draft_map.get("sections", []):
        text = section_text(section)
        section_id = section["section_id"]
        paragraphs = section.get("paragraphs", [])

        for paragraph in paragraphs:
            para_text = paragraph.get("text", "")
            para_id = paragraph["paragraph_id"]
            lower = para_text.lower()

            for pattern, reason in AI_PATTERNS:
                if pattern in lower:
                    add_finding(findings, "ai-smell", "P1", section_id, para_id, reason, pattern, "Rewrite this phrasing into a more evidence-led sentence.")
                    add_finding(findings, "mentor-drift", "P1", section_id, para_id, "This phrasing is unlikely to match supervisor style.", pattern, "Rewrite using mentor rewrite patterns.", constraints)

            for pattern, action in CLAIM_PATTERNS:
                if pattern in lower:
                    add_finding(findings, "claim-precision", "P1", section_id, para_id, "Claim language is too generic or under-specified.", pattern, action, constraints)

            for pattern, reason, severity in rejection_patterns:
                if pattern and pattern in lower:
                    sev = "P1" if severity == "high" else "P2"
                    add_finding(findings, "mentor-drift", sev, section_id, para_id, "Matched mentor rejection pattern.", pattern, reason, constraints)

            if any(lower.startswith(starter) for starter in TRANSITION_STARTERS) and para_id != paragraphs[0]["paragraph_id"]:
                add_finding(findings, "transition-rhythm", "P2", section_id, para_id, "Paragraph opening feels abrupt or mechanically restarted.", para_text[:80], "Add a bridge sentence or reframe the opening.")

            sentence_count = len(re.split(r"(?<=[.!?])\s+", para_text.strip()))
            categories = 0
            if any(token in lower for token in ("challenging", "degrade", "problem", "limitation")):
                categories += 1
            if any(token in lower for token in ("propose", "framework", "method", "combine")):
                categories += 1
            if any(token in lower for token in ("result", "improve", "baseline", "performance")):
                categories += 1
            if sentence_count >= 3 and categories >= 3:
                add_finding(findings, "paragraph-architecture", "P2", section_id, para_id, "Paragraph mixes too many functions at once.", f"{sentence_count} sentences with problem/method/result cues mixed.", "Split or reorder the paragraph around a single function.")

            if ("result" in lower or "performance" in lower or "improve" in lower) and not re.search(r"\d", para_text):
                add_finding(findings, "evidence-language-gap", "P1", section_id, para_id, "Results are described without concrete evidence cues.", para_text[:100], "Bind the result sentence to a comparator, metric, or condition.")

    for item in term_check.get("findings", []):
        issue = "Terminology inconsistency detected."
        evidence = item.get("term") or item.get("preferred_term") or str(item)
        action = item.get("replacement_hint") or "Normalize terminology to mentor-preferred terms."
        add_finding(
            findings,
            "terminology-risk",
            "P1" if item.get("type") == "disallowed_term" else "P2",
            "",
            None,
            issue,
            evidence,
            action,
            constraints,
        )

    for item in truth_check.get("findings", []):
        add_finding(
            findings,
            "truth-risk-lite",
            item.get("severity", "P2"),
            item.get("section_id", ""),
            item.get("paragraph_id"),
            f"Scientific-risk-lite finding: {item.get('risk_type', 'risk')}",
            item.get("evidence", ""),
            item.get("recommended_action", ""),
            constraints,
        )

    dimension_scores = compute_dimension_scores(findings)
    dimension_summary = defaultdict(list)
    for item in findings:
        dimension_summary[item["dimension"]].append(item["issue"])

    dimensions = []
    for name in [
        "mentor-drift",
        "ai-smell",
        "terminology-risk",
        "claim-precision",
        "transition-rhythm",
        "paragraph-architecture",
        "evidence-language-gap",
        "truth-risk-lite",
    ]:
        summary = "; ".join(dimension_summary.get(name, [])[:2]) or "No major finding detected by heuristic pass."
        dimensions.append({"name": name, "score": dimension_scores[name], "summary": summary})

    findings.sort(key=lambda item: (severity_rank(item["severity"]), item.get("section_id", ""), item["id"]))
    prioritized_actions = []
    for idx, item in enumerate(findings[:12], start=1):
        prioritized_actions.append(
            {
                "priority": idx,
                "title": f"{item['dimension']} -> {item['issue']}",
                "rationale": item["recommended_action"],
                "linked_findings": [item["id"]],
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
        "overall_summary": f"Heuristic xray generated {len(findings)} findings across 8 dimensions.",
        "overall_risk_level": overall,
        "dimensions": dimensions,
        "findings": findings,
        "prioritized_actions": prioritized_actions,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "finding_count": len(findings), "overall_risk_level": overall}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
