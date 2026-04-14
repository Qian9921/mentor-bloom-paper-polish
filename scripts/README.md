# P0 Scripts

当前可运行脚本：

- `extract_pdf_text.py`
- `normalize_transcripts.py`
- `build_mentor_manifest.py`
- `build_mentor_distillation_packet.py`
- `build_mentor_distillation_brief.py`
- `build_mentor_evolution_packet.py`
- `build_mentor_evolution_brief.py`
- `compile_mentor_profile.py`（仅 bootstrap / fallback，不是 canonical path）
- `build_mentor_lexicon.py`
- `build_mentor_corpus_index.py`
- `build_mentor_exemplar_index.py`
- `build_mentor_student_gap_model.py`
- `build_draft_map.py`
- `build_project_fact_sheet.py`
- `build_paper_xray_packet.py`
- `build_paper_xray_brief.py`
- `truth_check_lite.py`
- `generate_xray_report.py`
- `build_revision_agenda_brief.py`
- `init_revision_agenda.py`
- `build_revision_packet.py`
- `build_reference_mirror_packet.py`
- `build_reference_mirror_brief.py`
- `build_mentor_polish_brief.py`
- `build_mentor_polish_pass_briefs.py`
- `build_micro_polish_packet.py`
- `build_micro_polish_brief.py`
- `export_alignment_scorecard.py`
- `run_term_consistency_check.py`
- `diff_revision.py`
- `promote_mentor_profile.py`
- `run_p0_pipeline.py`

推荐最短闭环：

```bash
python3 scripts/run_p0_pipeline.py \
  --mentor-dir data/mentor/raw \
  --draft data/paper_inputs/sample_mature_draft.md \
  --output-dir artifacts/polish_runs/pipeline_run_agent_prepare \
  --mentor-id martin-mentor
```

这会默认停在 **mentor-brain 准备阶段**，并产出：

- `mentor_manifest.json`
- `mentor_distillation_packet.json`
- `mentor_distillation_brief.md`

然后应由 Codex / agent 消费 brief，产出真正的：

- `compiled_mentor_profile.json`

如果你已经有 agent-authored mentor profile，再继续到 xray 准备阶段：

```bash
python3 scripts/run_p0_pipeline.py \
  --mentor-dir data/mentor/raw \
  --draft data/paper_inputs/sample_mature_draft.md \
  --output-dir artifacts/polish_runs/pipeline_xray_prepare \
  --mentor-id martin-mentor \
  --mentor-profile path/to/compiled_mentor_profile.json
```

这会默认停在 **paper-xray 准备阶段**，并产出：

- `paper_xray_packet.json`
- `paper_xray_brief.md`

然后应由 Codex / agent 产出：

- `xray_report.json`

如果你已经有 agent-authored xray report，再继续到 agenda 准备阶段：

```bash
python3 scripts/run_p0_pipeline.py \
  --mentor-dir data/mentor/raw \
  --draft data/paper_inputs/sample_mature_draft.md \
  --output-dir artifacts/polish_runs/pipeline_agenda_prepare \
  --mentor-id martin-mentor \
  --mentor-profile path/to/compiled_mentor_profile.json \
  --xray-report path/to/xray_report.json
```

这会默认停在 **revision-agenda 准备阶段**，并产出：

- `revision_agenda_brief.md`

然后应由 Codex / agent 产出：

- `revision_agenda.json`

如果你已经有 agent-authored revision agenda，再继续到 full packaging：

```bash
python3 scripts/run_p0_pipeline.py \
  --mentor-dir data/mentor/raw \
  --draft data/paper_inputs/sample_mature_draft.md \
  --output-dir artifacts/polish_runs/pipeline_full_agent_first \
  --mentor-id martin-mentor \
  --mentor-profile path/to/compiled_mentor_profile.json \
  --xray-report path/to/xray_report.json \
  --revision-agenda path/to/revision_agenda.json
```

这会进一步产出：

- `reference_mirror_packet.json`
- `reference_mirror_brief.md`
- `mentor_polish_workspace/`
- `mentor_lexicon.json`
- `mentor_corpus_index.json`
- `mentor_exemplar_index.json`
- `mentor_student_gap_model.json`
- `micro_polish_packet.json`
- `micro_polish_brief.md`

说明：

- 导师脑持续进化 workflow 推荐名：`$mentor-bloom`（简写 `$bloom`，兼容旧叫法 `$learning`）；
- 导师脑的 canonical path 是 **agent-first**，不是 script-first；
- `paper-xray` 的 canonical path 现在也是 **agent-first**；
- `revision-agenda` 的 canonical path 现在也是 **agent-first**；
- 这些脚本先提供 **稳定工位**，不替代 Codex/agent 的判断；
- `compile_mentor_profile.py`、`generate_xray_report.py`、`truth_check_lite.py` 目前是 **heuristic MVP**；
- `init_xray_report.py` 仍保留为 scaffold fallback；
- 真正的高质量导师脑蒸馏与最终改写，仍应由 Codex 在这些 artifact 合同之上执行；
- `reference-mirror` 现在也走 agent-first：script 只打包 mirror snippets，agent 再做对照分析；
- `mentor-polish` 当前新增了 pass-based workspace briefs，script 只产出任务包，agent 再按 pass 真正改写；
- `micro-polish` 当前也走 agent-first：script 只打包 sentence-level tasks 与 lexicon/corpus 线索，agent 再逐句改；
- `build_mentor_polish_brief.py` 可把 pipeline 产物整理成 agent 可直接消费的改稿 brief；
- `export_alignment_scorecard.py` 用于 before/after xray 对比评估。
