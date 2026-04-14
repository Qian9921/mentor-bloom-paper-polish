#!/usr/bin/env python3
"""Run the P0 mentor-brain + xray/check pipeline.

Canonical flow:
1. scripts normalize and package mentor materials
2. Codex/agent authors compiled_mentor_profile from the packet
3. downstream xray/check consumes the compiled mentor profile
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def run(cmd: list[str]) -> dict:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    payload = {}
    stdout = result.stdout.strip()
    if stdout:
        last_line = stdout.splitlines()[-1]
        try:
            payload = json.loads(last_line)
        except json.JSONDecodeError:
            payload = {"stdout": stdout}
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mentor-dir", required=True, type=Path)
    parser.add_argument("--draft", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--mentor-id", default="mentor")
    parser.add_argument("--mentor-profile", type=Path, default=None, help="Agent-authored compiled mentor profile. If omitted, pipeline stops after mentor packet generation.")
    parser.add_argument("--bootstrap-mentor-profile", action="store_true", help="Fallback only: use heuristic script compilation when no agent-authored mentor profile is available.")
    parser.add_argument("--xray-report", type=Path, default=None, help="Agent-authored xray report. If omitted, pipeline stops after xray packet generation unless --bootstrap-xray is set.")
    parser.add_argument("--bootstrap-xray", action="store_true", help="Fallback only: use heuristic script xray generation.")
    parser.add_argument("--revision-agenda", type=Path, default=None, help="Agent-authored revision agenda. If omitted, pipeline stops after agenda brief generation unless --bootstrap-revision-agenda is set.")
    parser.add_argument("--bootstrap-revision-agenda", action="store_true", help="Fallback only: use script agenda initialization.")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest = args.output_dir / "mentor_manifest.json"
    mentor_normalized_dir = args.output_dir / "mentor_normalized"
    mentor_packet = args.output_dir / "mentor_distillation_packet.json"
    mentor_brief = args.output_dir / "mentor_distillation_brief.md"
    mentor_profile_output = args.output_dir / "compiled_mentor_profile.json"
    draft_map = args.output_dir / "draft_map.json"
    fact_sheet = args.output_dir / "project_fact_sheet.json"
    term_check = args.output_dir / "term_check.json"
    truth_check = args.output_dir / "truth_check_report.json"
    xray_packet = args.output_dir / "paper_xray_packet.json"
    xray_brief = args.output_dir / "paper_xray_brief.md"
    xray_output = args.output_dir / "xray_report.json"
    agenda_output = args.output_dir / "revision_agenda.json"
    agenda_brief = args.output_dir / "revision_agenda_brief.md"
    packet_dir = args.output_dir / "revision_packet"
    mirror_packet = args.output_dir / "reference_mirror_packet.json"
    mirror_brief = args.output_dir / "reference_mirror_brief.md"
    polish_brief = args.output_dir / "mentor_polish_brief.md"
    polish_workspace_dir = args.output_dir / "mentor_polish_workspace"
    mentor_lexicon = args.output_dir / "mentor_lexicon.json"
    mentor_corpus = args.output_dir / "mentor_corpus_index.json"
    micro_polish_packet = args.output_dir / "micro_polish_packet.json"
    micro_polish_brief = args.output_dir / "micro_polish_brief.md"

    steps = []
    scripts = Path(__file__).resolve().parent

    def call(script: str, extra_args: list[str]) -> dict:
        cmd = ["python3", str(scripts / script), *extra_args]
        payload = run(cmd)
        steps.append({"script": script, "output": payload})
        return payload

    mentor_normalized_dir.mkdir(parents=True, exist_ok=True)
    call("normalize_transcripts.py", ["--input-dir", str(args.mentor_dir), "--output-dir", str(mentor_normalized_dir)])
    call("extract_pdf_text.py", ["--input-dir", str(args.mentor_dir), "--output-dir", str(mentor_normalized_dir)])
    call("build_mentor_manifest.py", ["--input-dir", str(mentor_normalized_dir), "--output", str(manifest), "--mentor-id", args.mentor_id])
    call("build_mentor_distillation_packet.py", ["--manifest", str(manifest), "--output", str(mentor_packet)])
    call("build_mentor_distillation_brief.py", ["--packet", str(mentor_packet), "--output", str(mentor_brief), "--target-profile", str(mentor_profile_output)])

    mentor_profile: Path | None = None
    if args.mentor_profile is not None:
        mentor_profile = args.mentor_profile
        steps.append({"script": "consume_agent_authored_mentor_profile", "output": {"mentor_profile": str(mentor_profile)}})
    elif args.bootstrap_mentor_profile:
        call("compile_mentor_profile.py", ["--manifest", str(manifest), "--output", str(mentor_profile_output), "--mentor-id", args.mentor_id])
        mentor_profile = mentor_profile_output
    else:
        summary = {
            "schema_version": "0.1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "mentor_dir": str(args.mentor_dir),
            "draft": str(args.draft),
            "output_dir": str(args.output_dir),
            "mode": "prepare_only",
            "next_step": "Use mentor_distillation_brief.md with Codex/agent to author compiled_mentor_profile.json, then rerun with --mentor-profile.",
            "steps": steps,
        }
        summary_path = args.output_dir / "pipeline_summary.json"
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"output_dir": str(args.output_dir), "mode": "prepare_only", "summary": str(summary_path)}, ensure_ascii=False))
        return 0

    call("build_draft_map.py", ["--input", str(args.draft), "--output", str(draft_map)])
    call("build_project_fact_sheet.py", ["--draft-map", str(draft_map), "--output", str(fact_sheet)])
    call("run_term_consistency_check.py", ["--input", str(args.draft), "--mentor-profile", str(mentor_profile), "--output", str(term_check)])
    call("truth_check_lite.py", ["--draft-map", str(draft_map), "--project-fact-sheet", str(fact_sheet), "--output", str(truth_check)])
    call("build_paper_xray_packet.py", ["--draft-map", str(draft_map), "--mentor-profile", str(mentor_profile), "--project-fact-sheet", str(fact_sheet), "--term-check", str(term_check), "--truth-check", str(truth_check), "--output", str(xray_packet)])
    call("build_paper_xray_brief.py", ["--packet", str(xray_packet), "--output", str(xray_brief), "--target-xray", str(xray_output)])

    xray: Path | None = None
    if args.xray_report is not None:
        xray = args.xray_report
        steps.append({"script": "consume_agent_authored_xray_report", "output": {"xray_report": str(xray)}})
    elif args.bootstrap_xray:
        call("generate_xray_report.py", ["--draft-map", str(draft_map), "--mentor-profile", str(mentor_profile), "--term-check", str(term_check), "--truth-check", str(truth_check), "--project-fact-sheet", str(fact_sheet), "--output", str(xray_output)])
        xray = xray_output
    else:
        summary = {
            "schema_version": "0.1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "mentor_dir": str(args.mentor_dir),
            "draft": str(args.draft),
            "output_dir": str(args.output_dir),
            "mode": "xray_prepare_only",
            "mentor_profile": str(mentor_profile),
            "next_step": "Use paper_xray_brief.md with Codex/agent to author xray_report.json, then rerun with --xray-report.",
            "steps": steps,
        }
        summary_path = args.output_dir / "pipeline_summary.json"
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"output_dir": str(args.output_dir), "mode": "xray_prepare_only", "summary": str(summary_path)}, ensure_ascii=False))
        return 0

    call("build_revision_agenda_brief.py", ["--xray-report", str(xray), "--mentor-profile", str(mentor_profile), "--project-fact-sheet", str(fact_sheet), "--output", str(agenda_brief), "--target-agenda", str(agenda_output)])

    agenda: Path | None = None
    if args.revision_agenda is not None:
        agenda = args.revision_agenda
        steps.append({"script": "consume_agent_authored_revision_agenda", "output": {"revision_agenda": str(agenda)}})
    elif args.bootstrap_revision_agenda:
        call("init_revision_agenda.py", ["--xray-report", str(xray), "--output", str(agenda_output)])
        agenda = agenda_output
    else:
        summary = {
            "schema_version": "0.1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "mentor_dir": str(args.mentor_dir),
            "draft": str(args.draft),
            "output_dir": str(args.output_dir),
            "mode": "agenda_prepare_only",
            "mentor_profile": str(mentor_profile),
            "xray_report": str(xray),
            "next_step": "Use revision_agenda_brief.md with Codex/agent to author revision_agenda.json, then rerun with --revision-agenda.",
            "steps": steps,
        }
        summary_path = args.output_dir / "pipeline_summary.json"
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"output_dir": str(args.output_dir), "mode": "agenda_prepare_only", "summary": str(summary_path)}, ensure_ascii=False))
        return 0

    call("build_revision_packet.py", ["--draft-map", str(draft_map), "--mentor-profile", str(mentor_profile), "--xray-report", str(xray), "--revision-agenda", str(agenda), "--output-dir", str(packet_dir)])
    call("build_reference_mirror_packet.py", ["--draft-map", str(draft_map), "--xray-report", str(xray), "--revision-agenda", str(agenda), "--mentor-manifest", str(manifest), "--mentor-profile", str(mentor_profile), "--output", str(mirror_packet)])
    call("build_reference_mirror_brief.py", ["--packet", str(mirror_packet), "--output", str(mirror_brief)])
    call("build_mentor_polish_brief.py", ["--mentor-profile", str(mentor_profile), "--xray-report", str(xray), "--revision-agenda", str(agenda), "--project-fact-sheet", str(fact_sheet), "--output", str(polish_brief)])
    call("build_mentor_polish_pass_briefs.py", ["--draft-map", str(draft_map), "--mentor-profile", str(mentor_profile), "--xray-report", str(xray), "--revision-agenda", str(agenda), "--project-fact-sheet", str(fact_sheet), "--reference-mirror-packet", str(mirror_packet), "--output-dir", str(polish_workspace_dir)])
    call("build_mentor_lexicon.py", ["--mentor-profile", str(mentor_profile), "--output", str(mentor_lexicon)])
    call("build_mentor_corpus_index.py", ["--mentor-manifest", str(manifest), "--output", str(mentor_corpus)])
    call("build_micro_polish_packet.py", ["--draft-map", str(draft_map), "--mentor-profile", str(mentor_profile), "--mentor-lexicon", str(mentor_lexicon), "--mentor-corpus-index", str(mentor_corpus), "--xray-report", str(xray), "--output", str(micro_polish_packet)])
    call("build_micro_polish_brief.py", ["--packet", str(micro_polish_packet), "--output", str(micro_polish_brief)])

    summary = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mentor_dir": str(args.mentor_dir),
        "draft": str(args.draft),
        "output_dir": str(args.output_dir),
        "mode": "full_pipeline",
        "mentor_profile": str(mentor_profile),
        "xray_report": str(xray),
        "revision_agenda": str(agenda),
        "steps": steps,
    }
    summary_path = args.output_dir / "pipeline_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": str(args.output_dir), "steps": len(steps), "summary": str(summary_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
