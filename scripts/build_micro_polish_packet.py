#!/usr/bin/env python3
"""Build a micro-polish packet for sentence-level agent rewriting."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [part.strip() for part in parts if part.strip()]


def is_latex_heavy(text: str) -> bool:
    latex_markers = ["\\begin{", "\\end{", "\\label{", "\\caption{", "\\includegraphics", "\\toprule", "\\midrule", "\\bottomrule"]
    return any(marker in text for marker in latex_markers)


def best_sentence(sentences: list[str]) -> str:
    scored = []
    for sentence in sentences:
        penalty = sentence.count("\\") * 5
        if is_latex_heavy(sentence):
            penalty += 50
        score = len(sentence) - penalty
        scored.append((score, sentence))
    scored.sort(key=lambda item: item[0], reverse=True)
    return scored[0][1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft-map", required=True, type=Path)
    parser.add_argument("--mentor-profile", required=True, type=Path)
    parser.add_argument("--mentor-lexicon", required=True, type=Path)
    parser.add_argument("--mentor-corpus-index", required=True, type=Path)
    parser.add_argument("--xray-report", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--task-limit", type=int, default=50)
    args = parser.parse_args()

    draft_map = load_json(args.draft_map)
    lexicon = load_json(args.mentor_lexicon)
    corpus = load_json(args.mentor_corpus_index)
    xray = load_json(args.xray_report)

    preferred_terms = [item["term"] for item in lexicon.get("entries", []) if item.get("status") == "preferred"]
    corpus_entries = corpus.get("entries", [])
    findings = xray.get("findings", [])

    paragraph_lookup = {}
    for section in draft_map.get("sections", []):
        for paragraph in section.get("paragraphs", []):
            paragraph_lookup[(section["section_id"], paragraph["paragraph_id"])] = paragraph["text"]

    tasks = []
    for finding in findings:
        sid = finding.get("section_id")
        pid = finding.get("paragraph_id")
        para_text = paragraph_lookup.get((sid, pid))
        if not para_text:
            continue
        if is_latex_heavy(para_text):
            continue
        sentences = split_sentences(para_text)
        if not sentences:
            continue
        sentence = best_sentence(sentences)
        task_type = "tighten_sentence"
        issue_text = " ".join([finding.get("issue", ""), finding.get("recommended_action", "")]).lower()
        if "transition" in issue_text:
            task_type = "transition_fix"
        elif "comparator" in issue_text or "compare" in issue_text:
            task_type = "comparator_fix"
        elif "term" in issue_text or "word" in issue_text:
            task_type = "word_replacement"
        elif "phrase" in issue_text:
            task_type = "phrase_replacement"
        elif "ending" in issue_text or "landing" in issue_text:
            task_type = "ending_landing"

        recommended_lexicon = [term for term in preferred_terms if term.lower() in para_text.lower() or term.lower() in issue_text][:5]
        recommended_corpus = [entry["entry_id"] for entry in corpus_entries if entry.get("section") in {("general" if not sid else sid.split('-', 2)[-1]), "general"}][:3]
        tasks.append(
            {
                "task_id": f"micro-task-{len(tasks)+1:03d}",
                "section_id": sid or "",
                "paragraph_id": pid or "",
                "sentence_index": sentences.index(sentence),
                "sentence_text": sentence,
                "task_type": task_type,
                "issues": [finding.get("issue", ""), finding.get("recommended_action", "")],
                "recommended_lexicon_entries": recommended_lexicon,
                "recommended_corpus_entries": recommended_corpus,
                "constraints": finding.get("do_not_break", []),
            }
        )
        if len(tasks) >= args.task_limit:
            break

    payload = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "draft_id": draft_map.get("draft_id", args.draft_map.stem),
        "mentor_profile": str(args.mentor_profile),
        "mentor_lexicon": str(args.mentor_lexicon),
        "mentor_corpus_index": str(args.mentor_corpus_index),
        "tasks": tasks,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "task_count": len(tasks)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
