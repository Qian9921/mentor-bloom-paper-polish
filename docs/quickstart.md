# Quickstart / 快速开始

## 1. Build a mentor profile / 先构建导师脑

```bash
python3 scripts/build_mentor_manifest.py \
  --input-dir examples \
  --output /tmp/mentor_manifest.json \
  --mentor-id sample

python3 scripts/build_mentor_distillation_packet.py \
  --manifest /tmp/mentor_manifest.json \
  --output /tmp/mentor_packet.json
```

Then have an agent author a compiled mentor profile.

---

## 2. Diagnose a draft / 诊断一篇稿件

```bash
python3 scripts/build_draft_map.py \
  --input examples/sample_mature_draft.md \
  --output /tmp/draft_map.json
```

Then continue with xray packet + brief and let an agent author `xray_report.json`.

---

## 3. Build polishing workspaces / 构建改稿工位

Use the full pipeline or run the individual packet scripts:

```bash
python3 scripts/run_p0_pipeline.py \
  --mentor-dir /path/to/private/mentor/raw \
  --draft /path/to/your_draft.tex \
  --output-dir /tmp/mentor_bloom_run \
  --mentor-id your-mentor \
  --mentor-profile /path/to/compiled_mentor_profile.json \
  --xray-report /path/to/xray_report.json \
  --revision-agenda /path/to/revision_agenda.json
```

This produces:

- mentor approach report
- reference mirror packet
- mentor polish workspace
- mentor lexicon
- mentor corpus
- micro polish packet
