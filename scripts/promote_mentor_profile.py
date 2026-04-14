#!/usr/bin/env python3
"""Archive and promote an agent-authored mentor profile version with changelog."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True, type=Path, help="Agent-authored compiled mentor profile JSON")
    parser.add_argument("--version-label", required=True, help="Version label, e.g. v0.2.0-alpha")
    parser.add_argument("--archive-dir", required=True, type=Path)
    parser.add_argument("--changelog", required=True, type=Path)
    parser.add_argument("--delta", type=Path, default=None)
    parser.add_argument("--previous-version", default="")
    parser.add_argument("--summary", required=True)
    parser.add_argument("--current-target", type=Path, default=None, help="Optional path to update as the latest profile copy")
    parser.add_argument("--review-status", default="approved", choices=["draft", "approved", "rejected"])
    args = parser.parse_args()

    profile = load_json(args.profile)
    mentor_id = profile.get("mentor_id", "mentor")
    args.archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = args.archive_dir / f"{mentor_id}_compiled_mentor_profile.{args.version_label}.json"
    shutil.copy2(args.profile, archive_path)

    if args.current_target:
        args.current_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(args.profile, args.current_target)

    args.changelog.parent.mkdir(parents=True, exist_ok=True)
    if args.changelog.exists():
        changelog = load_json(args.changelog)
        if not isinstance(changelog, list):
            raise SystemExit("Changelog file exists but is not a JSON list.")
    else:
        changelog = []

    entry = {
        "schema_version": "0.1.0",
        "promoted_at": datetime.now(timezone.utc).isoformat(),
        "mentor_id": mentor_id,
        "previous_version": args.previous_version,
        "new_version": args.version_label,
        "profile_path": str(archive_path),
        "delta_path": str(args.delta) if args.delta else "",
        "summary": args.summary,
        "review_status": args.review_status,
        "notes": [],
    }
    changelog.append(entry)
    args.changelog.write_text(json.dumps(changelog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"archive_path": str(archive_path), "changelog": str(args.changelog), "entries": len(changelog)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
