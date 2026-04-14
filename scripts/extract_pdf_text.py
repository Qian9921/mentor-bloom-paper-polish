#!/usr/bin/env python3
"""Extract text from PDFs using the system pdftotext utility."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def collect_pdfs(input_dir: Path) -> list[Path]:
    return sorted(path for path in input_dir.rglob("*.pdf") if path.is_file())


def run_pdftotext(pdf: Path, out_txt: Path) -> dict:
    cmd = ["pdftotext", "-layout", str(pdf), str(out_txt)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "returncode": result.returncode,
        "stderr": result.stderr.strip(),
        "stdout": result.stdout.strip(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    if shutil.which("pdftotext") is None:
        raise SystemExit("pdftotext not found in PATH")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for pdf in collect_pdfs(args.input_dir):
        rel = pdf.relative_to(args.input_dir)
        out_txt = args.output_dir / rel.with_suffix(".txt")
        out_txt.parent.mkdir(parents=True, exist_ok=True)
        info = run_pdftotext(pdf, out_txt)
        results.append(
            {
                "pdf": str(pdf),
                "output": str(out_txt),
                **info,
            }
        )

    print(json.dumps({"pdf_count": len(results), "results": results}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
