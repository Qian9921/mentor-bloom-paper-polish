# P0 Artifact Schemas

本目录定义 P0 阶段最核心的 artifact 合同。

当前覆盖：

- `mentor_material_manifest.schema.json`：导师材料清单
- `mentor_distillation_packet.schema.json`：给 Codex / agent 消费的导师脑蒸馏包
- `mentor_evolution_packet.schema.json`：给 Codex / agent 消费的导师脑增量进化包
- `mentor_profile_delta.schema.json`：导师脑增量升级提案
- `mentor_profile_changelog_entry.schema.json`：导师脑版本晋升记录
- `mentor_lexicon.schema.json`：导师专业写作词汇库
- `mentor_corpus_index.schema.json`：导师句级/段级语料索引
- `micro_polish_packet.schema.json`：逐句/逐词改稿任务包
- `compiled_mentor_profile.schema.json`：导师脑编译产物
- `project_fact_sheet.schema.json`：轻量项目事实表
- `paper_xray_packet.schema.json`：给 Codex / agent 消费的诊断包
- `xray_report.schema.json`：成熟稿诊断报告
- `truth_check_report.schema.json`：科学风险轻检查报告
- `revision_agenda.schema.json`：修改计划
- `reference_mirror_packet.schema.json`：导师/参考镜像比对包
- `mentor_polish_workspace.schema.json`：pass-based mentor-polish 工作区清单
- `mentor_alignment_scorecard.schema.json`：修改后对齐评分

设计原则：

1. schema 先冻结关键字段，再逐步扩展；
2. 上游 script 负责稳定产出；
3. agent 可以补内容，但不能破坏合同；
4. 所有 P0 run 都应至少落下 manifest / xray / agenda / delta / scorecard 之一。
