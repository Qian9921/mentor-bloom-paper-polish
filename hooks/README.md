# Hooks v0.1

本目录预留给 P0 阶段的自动触发层。

建议第一批 hook：

- `session-bootstrap`
- `artifact-persist`
- `revision-verify`
- `notify-long-run`
- `state-checkpoint`

约束：

1. hook 只触发，不推理；
2. hook 只调用 script 或状态保存；
3. hook 失败不能静默吞掉；
4. hook 行为必须可重跑、可审计。
