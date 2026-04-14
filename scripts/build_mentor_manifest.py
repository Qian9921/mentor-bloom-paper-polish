#!/usr/bin/env python3
"""Build a normalized mentor-material manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def sha256sum(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def is_hidden(path: Path) -> bool:
    return any(part.startswith(".") for part in path.parts)


def infer_material_type(path: Path) -> str:
    text = str(path).lower()
    suffix = path.suffix.lower()
    if any(token in text for token in ["讨论", "开会", "meeting", "transcript", "录音"]):
        return "transcript"
    if any(token in text for token in ["问题", "建议", "批注", "反馈", "comment", "feedback", "review"]):
        return "comment"
    if "revision" in text or "rewrite" in text or "tracked" in text:
        return "revision_trace"
    if "chat" in text or "wechat" in text or "message" in text:
        return "chat"
    if "transcript" in text or "meeting" in text or "audio" in text:
        return "transcript"
    if "comment" in text or "feedback" in text or "review" in text:
        return "comment"
    if "reference" in text or "literature" in text:
        return "reference"
    if "slide" in text or suffix in {".ppt", ".pptx", ".key"}:
        return "slide"
    if suffix in {".pdf", ".doc", ".docx"}:
        return "paper"
    if suffix in {".tex", ".md", ".txt", ".rtf"}:
        return "notes" if "note" in text else "paper"
    return "other"


def infer_source_type(path: Path, material_type: str) -> str:
    text = str(path).lower()
    if any(token in text for token in ["mentor", "advisor", "supervisor", "prof", "yan"]):
        if material_type in {"paper", "reference"}:
            return "mentor_authored"
        if material_type in {"revision_trace", "comment"}:
            return "mentor_edited"
        return "mentor_spoken"
    if material_type == "reference":
        return "external_reference"
    if "student" in text or "draft" in text:
        return "student_authored"
    return "unknown"


def infer_trust_tier(material_type: str, source_type: str) -> str:
    if source_type in {"mentor_authored", "mentor_edited"}:
        return "high"
    if material_type in {"transcript", "comment", "chat"} and source_type == "mentor_spoken":
        return "high"
    if source_type == "external_reference":
        return "medium"
    if material_type in {"paper", "notes"}:
        return "medium"
    return "low"


def guess_language(path: Path) -> str:
    text = str(path).lower()
    if ".zh" in text or "zh-cn" in text or "中文" in text:
        return "zh"
    return "en"


def title_guess(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ").strip()


def collect_files(root: Path, include_hidden: bool) -> list[Path]:
    files = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if not include_hidden and is_hidden(path.relative_to(root)):
            continue
        files.append(path)
    return files


def build_manifest(root: Path, output: Path, mentor_id: str, lab_domain: str, include_hidden: bool) -> dict:
    items = []
    by_material_type: Counter[str] = Counter()
    by_trust_tier: Counter[str] = Counter()
    total_bytes = 0

    for idx, path in enumerate(collect_files(root, include_hidden), start=1):
        stat = path.stat()
        material_type = infer_material_type(path)
        source_type = infer_source_type(path, material_type)
        trust_tier = infer_trust_tier(material_type, source_type)
        mime_type, _ = mimetypes.guess_type(path.name)
        item = {
            "id": f"mentor-material-{idx:04d}",
            "path": str(path.relative_to(root)),
            "filename": path.name,
            "extension": path.suffix.lower(),
            "sha256": sha256sum(path),
            "bytes": stat.st_size,
            "material_type": material_type,
            "source_type": source_type,
            "trust_tier": trust_tier,
            "language": guess_language(path),
            "mime_type": mime_type or "application/octet-stream",
            "mtime": iso(stat.st_mtime),
            "title_guess": title_guess(path),
        }
        items.append(item)
        by_material_type[material_type] += 1
        by_trust_tier[trust_tier] += 1
        total_bytes += stat.st_size

    manifest = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mentor_id": mentor_id,
        "root_dir": str(root.resolve()),
        "lab_domain": lab_domain,
        "summary": {
            "file_count": len(items),
            "total_bytes": total_bytes,
            "by_material_type": dict(sorted(by_material_type.items())),
            "by_trust_tier": dict(sorted(by_trust_tier.items())),
        },
        "items": items,
    }
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input-dir", required=True, type=Path, help="Root directory of mentor materials")
    p.add_argument("--output", required=True, type=Path, help="Output JSON path")
    p.add_argument("--mentor-id", default="mentor", help="Logical mentor identifier")
    p.add_argument("--lab-domain", default="GNSS/navigation", help="Domain tag stored in the manifest")
    p.add_argument("--include-hidden", action="store_true", help="Include hidden files")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if not args.input_dir.exists():
        raise SystemExit(f"Input directory does not exist: {args.input_dir}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest(
        root=args.input_dir,
        output=args.output,
        mentor_id=args.mentor_id,
        lab_domain=args.lab_domain,
        include_hidden=args.include_hidden,
    )
    print(
        json.dumps(
            {
                "output": str(args.output),
                "file_count": manifest["summary"]["file_count"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
