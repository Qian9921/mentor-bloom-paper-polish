# Mentor Polish Execution Protocol v0.1

目标：把一篇 **科学上基本可信** 的成熟稿，沿着导师脑协议持续拉向导师期望的写作质量。

本协议只负责“如何改”，不负责替代项目真实性判断。

---

## 1. 进入条件

进入 `mentor-polish` 前，最少要有：

- `compiled_mentor_profile`
- `draft_map`
- `xray_report`
- `revision_agenda`
- `project_fact_sheet` 或等价 `do_not_break_constraints`

如果缺少这些输入，不能直接开始全文自由润色。

---

## 2. 输入合同

## 2.1 必需输入

| 输入 | 作用 |
|---|---|
| mature draft | 被修改对象 |
| compiled mentor profile | 导师风格与规则 |
| xray report | 问题来源 |
| revision agenda | 修改顺序 |
| project fact sheet | scientific safety rail |

## 2.2 可选输入

| 输入 | 作用 |
|---|---|
| reference mirror packet | 对照强参考段落 |
| prior revision delta | 避免重复犯错 |
| mentor chat snippets | 提供局部写法偏好 |

---

## 3. 输出合同

每轮 `mentor-polish` 至少产出：

- `revised_draft`
- `revision_notes`
- `revision_delta_report`
- `remaining_risks`
- `mentor_alignment_scorecard`

如果只改了一部分，也必须显式标记：

- 改了哪些 section；
- 哪些没改；
- 为什么没改；
- 下一轮该改哪里。

---

## 4. 执行顺序

润色必须按层走，禁止一锅端。

## 4.1 Pass 0：Preflight

检查：

- 本轮 scope 是哪些 section / paragraph；
- 哪些 finding 是 `P0`；
- 哪些句子存在 `do_not_break`；
- 哪些术语绝对不能换；
- 哪些段落先不动。

输出：

- `do_first_do_not_touch.md`

## 4.2 Pass 1：Macro Pass

优先改最影响导师观感的高价值区：

- 标题
- 摘要
- 贡献句
- 引言 opening / closing
- conclusion 收束

目标：

- 强化主线；
- 强化 paper angle；
- 提升 punch；
- 避免空泛夸张。

## 4.3 Pass 2：Paragraph Pass

逐段检查：

- 段落功能是否单一清楚；
- 主题句是否强；
- 句子顺序是否合理；
- 段尾是否自然收束；
- 与前后段是否衔接。

允许动作：

- 重排句序；
- 重写主题句；
- 拆段 / 合段；
- 增加 bridge sentence。

## 4.4 Pass 3：Sentence Pass

在段落功能稳定后，再改句子级问题：

- 去 AI 味；
- 提高信息密度；
- 提高 precision；
- 压缩空词；
- 调整力度。

禁止动作：

- 在不了解 scientific constraint 的情况下自由扩写；
- 为了“更像导师”牺牲事实精确性。

## 4.5 Pass 4：Terminology Pass

最后做术语统一：

- preferred term 是否稳定；
- disallowed term 是否被清除；
- 缩写是否一致；
- figure / method / experiment 术语是否统一。

---

## 5. Agent 分工协议

推荐默认链路：

1. `critic`：根据 xray 挑出本轮最该修的问题；
2. `executor`：结合 mentor profile 实际改写；
3. `verifier`：检查是否修到位、是否改歪；
4. `writer`：整理可读 revision notes。

### 5.1 Planner 的职责

- 给出 pass 顺序；
- 决定先改哪些 section；
- 保证 `P0` 风险先修。

### 5.2 Executor 的职责

- 严格按照 mentor profile 改写；
- 给出修改理由；
- 显式声明 do-not-break 约束是否被保持。

### 5.3 Verifier 的职责

- 检查修改是否真的解决了原 finding；
- 检查是否新引入术语漂移或 scientific drift；
- 标出残留风险。

---

## 6. 停止条件与升级条件

### 必须停止自动润色的情况

- 当前段落的 scientific meaning 不清楚；
- 需要用户补充实验背景或真实 claim 边界；
- 导师脑与项目事实明显冲突；
- 同一段连续两轮修改仍无法稳定提升。

### 必须升级到人工决策的情况

- 需要在“更像导师”和“更忠于原始实验解释”之间做取舍；
- 某个结论句可能涉及 overclaim；
- 术语替换会影响论文立场或方法定义。

---

## 7. 质量门

一轮 `mentor-polish` 结束前，至少要回答 5 个问题：

1. 这轮是否明显降低了 AI 味？
2. 这轮是否更像导师而不是更像一般英语润色？
3. 这轮是否引入了 terminology drift？
4. 这轮是否改坏了 claim/evidence 的边界？
5. 这轮是否能向用户解释“为什么这么改”？

任何一个问题回答不清，都不算合格完成。

---

## 8. 禁止事项

- 禁止脱离 mentor profile 自由发挥；
- 禁止无依据地把句子改得更强；
- 禁止只给修改结果，不给修改理由；
- 禁止把 `truth-check-lite` 的问题伪装成“普通润色”；
- 禁止在没有 diff / risk report 的情况下宣布完成。
