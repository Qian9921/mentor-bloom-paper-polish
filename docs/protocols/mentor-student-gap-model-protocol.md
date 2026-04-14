# Mentor Student Gap Model Protocol v0.1

目标：从真实 xray / revising 经验中抽出“用户最常偏离导师标准的地方”，形成可被后续 skill 直接利用的 gap model。

---

## 1. 为什么需要这层

通用导师脑告诉系统：

- 导师喜欢什么
- 导师讨厌什么

但它不直接回答：

> 当前这个用户最常在哪些地方偏离导师？

gap model 就是专门解决这个问题。

---

## 2. 分层原则

- script：从 xray report 或 revision history 中汇总 recurring gap types
- agent：在后续 diagnosis / polish 时优先关注这些高频偏差

---

## 3. 典型 gap type

- summary-first results narration
- comparator missing
- terminology vagueness
- transition weakness
- paragraph overload
- unsupported interpretation
- weak practical landing

---

## 4. 用法

`paper-xray` 和 `mentor-polish` 都可以把 gap model 作为优先级加权器：

- 高频 gap → 优先诊断
- 高频 gap → 优先改
