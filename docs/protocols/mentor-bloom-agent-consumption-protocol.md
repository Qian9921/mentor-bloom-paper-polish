# Mentor Bloom Agent Consumption Protocol v0.1

`mentor-bloom` 是对旧的 `$learning` 想法的升级命名。

推荐公开入口：

- `$mentor-bloom`
- 简写：`$bloom`
- 兼容旧叫法：`$learning`（legacy alias）

---

## 1. 这个 workflow 的目标

它不是“重新全量蒸馏导师脑”。

它是：

> 基于新增导师材料，对当前导师脑做一次 agent-first 的增量进化。

---

## 2. 分层原则

- skill：负责触发与治理
- script：负责收集新增材料、生成 evolution packet/brief、管理版本和 changelog
- agent：负责判断新证据是否应该改变导师脑
- verifier：负责决定是否 promotion

---

## 3. 规范产物

至少应有：

- `mentor_evolution_packet.json`
- `mentor_evolution_brief.md`
- `mentor_profile_delta.json`
- `mentor_profile_changelog_entry`

---

## 4. Promotion 原则

新版本导师脑只有在以下条件下才应 promotion：

1. 新证据足够强；
2. 不污染 target draft；
3. 规则变更可解释；
4. 版本可回滚；
5. verifier 审查通过。
