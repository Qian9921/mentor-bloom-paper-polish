#!/usr/bin/env python3
"""Compile a heuristic mentor profile from manifest-listed text materials.

Fallback/bootstrap only.
Canonical mentor-brain synthesis should be authored by Codex/agent from the
mentor distillation packet and brief.
"""

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
SECTION_DEFAULTS = {
    "abstract": {
        "goal": "State problem, gap, method, evidence, and value compactly.",
        "must_include": ["problem", "method", "evidence", "value"],
        "must_avoid": ["generic novelty slogan"],
        "tone": "tight and evidence-led",
        "structure_hint": "problem -> gap -> method -> evidence -> value"
    },
    "introduction": {
        "goal": "Explain why the problem matters and position the contribution clearly.",
        "must_include": ["context", "gap", "contribution"],
        "must_avoid": ["history dump"],
        "tone": "controlled and persuasive",
        "structure_hint": "context -> limitation -> gap -> contribution"
    },
    "method": {
        "goal": "Explain method components clearly without hype.",
        "must_include": ["setup", "core mechanism", "assumptions"],
        "must_avoid": ["marketing phrasing"],
        "tone": "precise and technical",
        "structure_hint": "setup -> method -> rationale"
    },
    "experiment": {
        "goal": "Connect results to evidence and practical meaning.",
        "must_include": ["setting", "comparison", "result", "implication"],
        "must_avoid": ["table dump without interpretation"],
        "tone": "evidence-led",
        "structure_hint": "setup -> result -> comparison -> implication"
    },
    "conclusion": {
        "goal": "Re-state contribution and takeaway without overclaim.",
        "must_include": ["contribution", "evidence", "takeaway"],
        "must_avoid": ["new unexplained claim"],
        "tone": "tight and controlled",
        "structure_hint": "contribution -> evidence -> takeaway"
    }
}


def normalize_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def read_texts_from_manifest(manifest: dict) -> list[tuple[str, str]]:
    root = Path(manifest["root_dir"])
    texts = []
    for item in manifest.get("items", []):
        rel = item.get("path")
        if not rel:
            continue
        path = root / rel
        if path.suffix.lower() not in TEXT_EXTS or not path.exists():
            continue
        try:
            texts.append((rel, path.read_text(encoding="utf-8")))
        except UnicodeDecodeError:
            continue
    return texts


def extract_rule_lines(texts: list[tuple[str, str]]) -> list[str]:
    rules = []
    for _, text in texts:
        for raw in text.splitlines():
            line = normalize_ws(raw)
            lower = line.lower()
            if not line:
                continue
            if lower.startswith(RULE_PREFIXES):
                rules.append(line)
    return rules


def extract_quoted_terms(line: str) -> list[str]:
    return [normalize_ws(match) for match in re.findall(r"[\"“']([^\"”']+)[\"”']", line)]


def compile_rejection_lexicon(rule_lines: list[str]) -> list[dict]:
    seen = set()
    lexicon = []
    for line in rule_lines:
        lower = line.lower()
        if lower.startswith(("do not", "don't", "avoid", "never", "不要", "避免")):
            patterns = extract_quoted_terms(line)
            if not patterns:
                m = re.search(r"(?:do not|don't|avoid|never)\s+(.+)$", lower)
                if m:
                    patterns = [m.group(1).strip(" .")]
            for pattern in patterns[:3]:
                key = pattern.lower()
                if not pattern or key in seen:
                    continue
                seen.add(key)
                lexicon.append(
                    {
                        "pattern": pattern,
                        "reason": line,
                        "severity": "high" if "do not" in lower or "不要" in lower else "medium",
                    }
                )
    return lexicon


def compile_terminology_preferences(rule_lines: list[str], texts: list[tuple[str, str]]) -> dict:
    preferred_terms = []
    disallowed_terms = []
    seen_pref = set()
    seen_disallowed = set()

    prefer_patterns = [
        re.compile(r"prefer\s+(.+?)\s+over\s+(.+?)(?:[.;]|$)", re.IGNORECASE),
        re.compile(r"use\s+(.+?)\s+instead of\s+(.+?)(?:[.;]|$)", re.IGNORECASE),
    ]
    for line in rule_lines:
        for pattern in prefer_patterns:
            m = pattern.search(line)
            if m:
                preferred = normalize_ws(m.group(1))
                disallowed = normalize_ws(m.group(2))
                if preferred.lower() not in seen_pref:
                    preferred_terms.append({"term": preferred, "aliases": [disallowed], "notes": line})
                    seen_pref.add(preferred.lower())
                if disallowed.lower() not in seen_disallowed:
                    disallowed_terms.append({"term": disallowed, "replacement_hint": preferred, "reason": line})
                    seen_disallowed.add(disallowed.lower())

        lower = line.lower()
        if "do not say" in lower or "不要说" in line or "不要用" in line:
            quoted = extract_quoted_terms(line)
            for term in quoted:
                if term.lower() not in seen_disallowed:
                    disallowed_terms.append({"term": term, "replacement_hint": "", "reason": line})
                    seen_disallowed.add(term.lower())

    corpus = "\n".join(text for _, text in texts).lower()
    candidates = [
        "integrated navigation",
        "positioning accuracy",
        "gnss observations",
        "urban navigation",
        "inertial measurements",
    ]
    for term in candidates:
        if term in corpus and term.lower() not in seen_pref:
            preferred_terms.append({"term": term, "aliases": [], "notes": "Corpus-supported domain term."})
            seen_pref.add(term.lower())

    return {
        "preferred_terms": preferred_terms,
        "disallowed_terms": disallowed_terms,
    }


def compile_global_rules(rule_lines: list[str]) -> list[dict]:
    seen = set()
    rules = []
    for line in rule_lines:
        normalized = normalize_ws(line)
        key = normalized.lower()
        if key in seen:
            continue
        seen.add(key)
        priority = "must" if key.startswith(("must", "do not", "don't", "never", "不要", "必须")) else "strong"
        rules.append({"rule": normalized, "rationale": "Extracted from mentor-side guidance.", "priority": priority})
    return rules


def compile_rewrite_patterns(rule_lines: list[str]) -> list[dict]:
    patterns = []
    if any("sharper" in line.lower() or "更狠" in line for line in rule_lines):
        patterns.append(
            {
                "name": "soft-to-sharp-contribution",
                "before_pattern": "soft contribution sentence",
                "after_pattern": "specific contribution with boundary and value",
                "use_when": "A contribution sentence feels weak or generic.",
                "avoid_when": "The evidence is not strong enough for a sharper claim."
            }
        )
    if any("matters" in line.lower() or "意义" in line for line in rule_lines):
        patterns.append(
            {
                "name": "result-to-meaning",
                "before_pattern": "metric improvement without implication",
                "after_pattern": "metric improvement tied to why it matters",
                "use_when": "Results need explicit practical meaning.",
                "avoid_when": "The paper has not established the implication."
            }
        )
    if not patterns:
        patterns.append(
            {
                "name": "generic-to-evidence-led",
                "before_pattern": "generic sentence",
                "after_pattern": "evidence-led sentence with bounded claim",
                "use_when": "The draft sounds generic or AI-like.",
                "avoid_when": "The sentence contains unresolved scientific risk."
            }
        )
    return patterns


def compile_style_axes(texts: list[tuple[str, str]], rule_lines: list[str]) -> list[dict]:
    corpus = "\n".join(text for _, text in texts).lower()
    total_words = Counter(re.findall(r"[a-zA-Z]+", corpus))
    return [
        {
            "axis": "evidence_density",
            "preference": "high" if total_words["result"] + total_words["evidence"] + total_words["improve"] > 0 else "medium",
            "notes": "Supervisor guidance tends to stay evidence-led."
        },
        {
            "axis": "hype_tolerance",
            "preference": "low" if any("do not" in line.lower() or "不要" in line for line in rule_lines) else "medium",
            "notes": "Derived from anti-hype guidance."
        }
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--mentor-id", default=None)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    texts = read_texts_from_manifest(manifest)
    rule_lines = extract_rule_lines(texts)

    payload = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mentor_id": args.mentor_id or manifest.get("mentor_id", "mentor"),
        "source_manifest": str(args.manifest),
        "style_axes": compile_style_axes(texts, rule_lines),
        "global_rules": compile_global_rules(rule_lines),
        "terminology_preferences": compile_terminology_preferences(rule_lines, texts),
        "rejection_lexicon": compile_rejection_lexicon(rule_lines),
        "rewrite_patterns": compile_rewrite_patterns(rule_lines),
        "section_playbooks": SECTION_DEFAULTS,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "global_rules": len(payload["global_rules"]), "rejection_lexicon": len(payload["rejection_lexicon"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
