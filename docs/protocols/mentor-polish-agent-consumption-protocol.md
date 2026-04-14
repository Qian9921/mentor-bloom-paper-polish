# Mentor Polish Agent Consumption Protocol v0.1

目标：明确 `mentor-polish` 的执行主体是 Codex / agent，而不是脚本。

---

## 1. 分层原则

- skill：定义 workflow、门控、done criteria
- script：准备 pass briefs、section tasks、diff、scorecard
- agent：实际执行 macro / paragraph / sentence / terminology rewriting

任何“真正改句子、改段落、改结构”的动作都不应由 script 自动完成。

---

## 2. 推荐 pass 顺序

1. `macro-pass`
2. `paragraph-pass`
3. `sentence-pass`
4. `terminology-pass`
5. `verify-pass`

Agent 可以逐 pass 执行，也可以在 section 级局部组合执行，但必须明确当前 pass 的目标。

---

## 3. 每个 pass 的核心任务

### macro-pass
- 修题目、摘要、贡献句、结果主轴、结论收束

### paragraph-pass
- 修段落功能、顺序、主题句、转折

### sentence-pass
- 去 AI 味
- 提高信息密度
- 提高 precision

### terminology-pass
- 用 Yan 认可的术语收口全文

### verify-pass
- 检查是否修掉原 finding
- 检查是否引入 scientific drift

---

## 4. Agent 输出要求

每个 pass 或 section-task 至少应产出：

- 修改后的文本
- 修改理由
- 保留了哪些 do-not-break constraints
- 哪些问题仍未解决

---

## 5. 禁止事项

- script 不得直接重写正文
- agent 不得脱离 mentor profile 自由发挥
- sentence-level polish 不得抢在 paragraph-level restructuring 前面
- 不得在没有 verify 的情况下宣称“改好了”
