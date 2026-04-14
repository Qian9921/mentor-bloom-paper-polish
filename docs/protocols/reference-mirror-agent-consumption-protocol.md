# Reference Mirror Agent Consumption Protocol v0.1

目标：让 Codex / agent 不只是“知道哪里弱”，还能够拿导师或强参考的真实写法来做镜像比对。

---

## 1. 这层为什么重要

很多“AI 味”不是简单语法问题，而是：

- paragraph move 不对；
- figure/table narration 顺序不对；
- 结果段的节奏不对；
- 结论收束方式不对。

这些问题只靠规则清单不够，需要让 agent 看到：

> 同类型内容在导师论文里是怎么写、怎么推进、怎么收的。

---

## 2. 分层原则

- script：负责找可疑 section、抽 mentor snippets、组装 packet
- agent：负责真正做 compare / contrast / abstraction / rewrite guidance

script 不能自己宣称“这个段落应该这样改”，它只能提供镜像材料。

---

## 3. Agent 应回答的问题

消费 `reference_mirror_packet` 后，agent 至少应回答：

1. 当前弱段和导师强段的核心差异是什么？
2. 差异属于：
   - 信息顺序？
   - transition？
   - 术语？
   - 结果强调方式？
   - 收束方式？
3. 当前段落最该借鉴哪一个 move？
4. 哪些 move 能借，哪些不能硬套？

---

## 4. 输出形态建议

Agent 可以输出：

- mirror analysis note
- section-level rewrite note
- paragraph-level rewrite suggestion
- reusable rhetorical move summary

但这些都应建立在真实 mirror snippet 之上。
