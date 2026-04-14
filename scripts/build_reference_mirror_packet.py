#!/usr/bin/env python3
"""Build a reference-mirror packet for agent consumption."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


TEXT_EXTS = {".txt", ".md", ".tex"}
STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with", "is", "are",
    "this", "that", "we", "our", "it", "be", "as", "by", "from", "at",
    "的", "了", "和", "是", "在", "对", "把", "就", "都", "你", "我", "他", "她", "它"
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def tokenize(text: str) -> set[str]:
    raw = re.findall(r"[A-Za-z][A-Za-z0-9_-]+|[\u4e00-\u9fff]{2,}", text.lower())
    return {tok for tok in raw if tok not in STOPWORDS and len(tok) > 1}


def collect_corpus(manifest: dict) -> list[dict]:
    root = Path(manifest["root_dir"])
    corpus = []
    for item in manifest.get("items", []):
        path = root / item["path"]
        if path.suffix.lower() not in TEXT_EXTS or not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").replace("\r\n", "\n")
        raw_lines = text.splitlines()
        chunks = []
        buffer: list[tuple[int, str]] = []

        def flush() -> None:
            nonlocal buffer
            if not buffer:
                return
            joined = " ".join(part for _, part in buffer)
            joined = re.sub(r"\s+", " ", joined).strip()
            if len(joined) >= 80 and "JOURNAL OF LATEX CLASS FILES" not in joined and "doi.org" not in joined:
                chunks.append((buffer[0][0], joined))
            buffer = []

        for idx, raw in enumerate(raw_lines, start=1):
            line = re.sub(r"\s+", " ", raw).strip()
            if not line:
                flush()
                continue
            if re.fullmatch(r"\d+", line):
                continue
            if len(line) < 2:
                continue
            buffer.append((idx, line))
            if len(" ".join(part for _, part in buffer)) > 450:
                flush()
        flush()

        for idx, line in chunks:
            corpus.append(
                {
                    "source_path": item["path"],
                    "line_hint": idx,
                    "text": line,
                    "tokens": tokenize(line),
                }
            )
    return corpus


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft-map", required=True, type=Path)
    parser.add_argument("--xray-report", required=True, type=Path)
    parser.add_argument("--revision-agenda", required=True, type=Path)
    parser.add_argument("--mentor-manifest", required=True, type=Path)
    parser.add_argument("--mentor-profile", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--top-sections", type=int, default=4)
    parser.add_argument("--snippets-per-section", type=int, default=5)
    args = parser.parse_args()

    draft_map = load_json(args.draft_map)
    xray = load_json(args.xray_report)
    agenda = load_json(args.revision_agenda)
    manifest = load_json(args.mentor_manifest)
    mentor_profile = load_json(args.mentor_profile)
    corpus = collect_corpus(manifest)

    section_lookup = {section["section_id"]: section for section in draft_map.get("sections", [])}
    findings_by_section: dict[str, list[dict]] = defaultdict(list)
    for finding in xray.get("findings", []):
        findings_by_section[finding.get("section_id", "")].append(finding)

    prioritized_sections = []
    seen = set()
    for action in agenda.get("ordered_actions", []):
        sid = action.get("section_id")
        if sid and sid not in seen and sid in section_lookup:
            seen.add(sid)
            prioritized_sections.append(sid)
        if len(prioritized_sections) >= args.top_sections:
            break

    targets = []
    preferred_terms = {
        item["term"] for item in mentor_profile.get("terminology_preferences", {}).get("preferred_terms", [])
    }

    for sid in prioritized_sections:
        section = section_lookup[sid]
        section_text = "\n".join(p.get("text", "") for p in section.get("paragraphs", []))
        query_tokens = tokenize(section.get("heading", "")) | tokenize(section_text)
        query_tokens |= preferred_terms
        scored = []
        for item in corpus:
            overlap = query_tokens & item["tokens"]
            if not overlap:
                continue
            score = len(overlap)
            scored.append(
                {
                    "source_path": item["source_path"],
                    "line_hint": item["line_hint"],
                    "text": item["text"],
                    "match_reason": f"token overlap: {', '.join(sorted(list(overlap))[:8])}",
                    "score": float(score),
                }
            )
        scored.sort(key=lambda item: (-item["score"], item["source_path"], item["line_hint"]))
        findings = findings_by_section.get(sid, [])
        dimensions = sorted({f["dimension"] for f in findings if f.get("dimension")})
        targets.append(
            {
                "section_id": sid,
                "heading": section.get("heading", ""),
                "reason": f"Section is high priority due to findings in {', '.join(dimensions) if dimensions else 'xray report'}.",
                "linked_findings": [f["id"] for f in findings[:8]],
                "mirror_snippets": scored[: args.snippets_per_section],
                "comparison_questions": [
                    "How does the mentor/reference snippet introduce the object before making a claim?",
                    "What rhetorical move is missing in the current section?",
                    "Which terminology choices or transition moves should be borrowed here?",
                    "What should not be copied mechanically because the technical context differs?",
                ],
            }
        )

    payload = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "draft_id": draft_map.get("draft_id", args.draft_map.stem),
        "mentor_manifest": str(args.mentor_manifest),
        "targets": targets,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "target_count": len(targets)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
