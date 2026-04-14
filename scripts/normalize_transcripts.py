#!/usr/bin/env python3
"""Normalize transcript/chat text into cleaner plain text files."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SPEAKER_RE = re.compile(
    r"^\s*(speaker\s*\d+|spk\d+|user|assistant|mentor|prof|advisor|说话人[A-Za-z一二三四五六七八九十0-9]+)\s*[:：]?\s*",
    re.IGNORECASE,
)
TIMESTAMP_RE = re.compile(r"\b\d{1,2}:\d{2}(?::\d{2})?\b")


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = []
    for raw in text.splitlines():
        line = TIMESTAMP_RE.sub("", raw).strip()
        line = SPEAKER_RE.sub("", line)
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            lines.append(line)
    normalized = "\n".join(lines)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized.strip() + ("\n" if normalized.strip() else "")


def collect_text_files(input_dir: Path) -> list[Path]:
    allowed = {".txt", ".md", ".tex"}
    return sorted(path for path in input_dir.rglob("*") if path.is_file() and path.suffix.lower() in allowed)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for src in collect_text_files(args.input_dir):
        rel = src.relative_to(args.input_dir)
        dst = args.output_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        normalized = normalize_text(src.read_text(encoding="utf-8"))
        dst.write_text(normalized, encoding="utf-8")
        results.append({"input": str(src), "output": str(dst), "chars": len(normalized)})

    print(json.dumps({"normalized_files": len(results), "results": results}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
