# Truth Check Lite Protocol v0.1

目标：在不重建完整项目脑的前提下，尽量防止润色把 scientific meaning 改坏。

---

## 1. 关注范围

`truth-check-lite` 重点看这些风险：

- overclaim；
- comparator 缺失；
- 条件边界丢失；
- 结果比证据更大；
- 术语替换导致方法定义漂移；
- 把“观察到的现象”写成“理论上已证明”。

---

## 2. 典型高风险表达

- first / best / state-of-the-art
- significantly improves / greatly enhances
- very novel / highly effective
- outperforms existing methods
- robust results / superior performance

如果这些话出现，但没有边界、条件、对象、对比或证据，就应该触发风险。

---

## 3. 输出要求

每轮至少输出：

- 风险级别；
- 风险条目；
- 每条风险的 evidence；
- 推荐动作。

---

## 4. 与 mentor-polish 的关系

- `mentor-polish` 负责“写得像导师”；
- `truth-check-lite` 负责“别把事实写坏”。

两者不可互相替代。
