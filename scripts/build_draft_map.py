#!/usr/bin/env python3
"""Build a structured section/paragraph map from a draft."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


WORD_RE = re.compile(r"\b\w+\b", re.UNICODE)


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def detect_heading(line: str, suffix: str) -> tuple[int, str] | None:
    stripped = line.strip()
    if not stripped:
        return None

    md = re.match(r"^(#{1,6})\s+(.*?)\s*$", stripped)
    if md:
        return len(md.group(1)), md.group(2).strip()

    tex = re.match(r"^\\(chapter|section|subsection|subsubsection)\*?\{(.+?)\}\s*$", stripped)
    if tex:
        level_map = {"chapter": 1, "section": 1, "subsection": 2, "subsubsection": 3}
        return level_map[tex.group(1)], tex.group(2).strip()

    numbered = re.match(r"^(\d+(?:\.\d+)*)\s+(.+)$", stripped)
    if numbered:
        return numbered.group(1).count(".") + 1, numbered.group(2).strip()

    if suffix == ".txt" and stripped == stripped.upper() and len(stripped) <= 120 and len(stripped.split()) <= 12:
        return 1, stripped.title()

    return None


def build_paragraphs(lines: list[str], start_line: int, section_idx: int) -> list[dict]:
    paragraphs = []
    buffer: list[tuple[int, str]] = []

    def flush() -> None:
        nonlocal buffer
        if not buffer:
            return
        para_text = "\n".join(text for _, text in buffer).strip()
        if para_text:
            line_start = buffer[0][0]
            line_end = buffer[-1][0]
            para_id = f"p-{section_idx:03d}-{len(paragraphs)+1:03d}"
            paragraphs.append(
                {
                    "paragraph_id": para_id,
                    "line_start": line_start,
                    "line_end": line_end,
                    "word_count": len(WORD_RE.findall(para_text)),
                    "char_count": len(para_text),
                    "text": para_text,
                }
            )
        buffer = []

    for offset, raw in enumerate(lines, start=start_line):
        if not raw.strip():
            flush()
            continue
        buffer.append((offset, raw.rstrip("\n")))
    flush()
    return paragraphs


def build_sections(lines: list[str], suffix: str) -> list[dict]:
    headings: list[tuple[int, int, str]] = []
    for idx, line in enumerate(lines, start=1):
        found = detect_heading(line, suffix)
        if found:
            level, title = found
            headings.append((idx, level, title))

    if not headings:
        paragraphs = build_paragraphs(lines, 1, 1)
        return [
            {
                "section_id": "section-001-front-matter",
                "heading": "Front Matter",
                "level": 0,
                "line_start": 1,
                "line_end": len(lines),
                "paragraph_count": len(paragraphs),
                "paragraphs": paragraphs,
            }
        ]

    sections = []
    boundaries = headings + [(len(lines) + 1, 0, "__END__")]

    if headings[0][0] > 1:
        paragraphs = build_paragraphs(lines[: headings[0][0] - 1], 1, 1)
        sections.append(
            {
                "section_id": "section-001-front-matter",
                "heading": "Front Matter",
                "level": 0,
                "line_start": 1,
                "line_end": headings[0][0] - 1,
                "paragraph_count": len(paragraphs),
                "paragraphs": paragraphs,
            }
        )

    base_index = len(sections) + 1
    for local_idx, current in enumerate(headings):
        line_no, level, title = current
        next_line_no = boundaries[local_idx + 1][0]
        content = lines[line_no: next_line_no - 1]
        section_idx = base_index + local_idx
        paragraphs = build_paragraphs(content, line_no + 1, section_idx)
        sections.append(
            {
                "section_id": f"section-{section_idx:03d}-{slugify(title)}",
                "heading": title,
                "level": level,
                "line_start": line_no,
                "line_end": next_line_no - 1,
                "paragraph_count": len(paragraphs),
                "paragraphs": paragraphs,
            }
        )
    return sections


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, type=Path, help="Draft file (.md/.txt/.tex)")
    p.add_argument("--output", required=True, type=Path, help="Output JSON path")
    p.add_argument("--draft-id", default=None, help="Override draft id")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    text = args.input.read_text(encoding="utf-8")
    lines = text.splitlines()
    sections = build_sections(lines, args.input.suffix.lower())
    payload = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "draft_id": args.draft_id or args.input.stem,
        "source_file": str(args.input),
        "source_format": args.input.suffix.lower() or "text",
        "section_count": len(sections),
        "sections": sections,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "section_count": len(sections)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
