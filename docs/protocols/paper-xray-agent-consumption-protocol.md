# Paper Xray Agent Consumption Protocol v0.1

目标：`paper-xray` 的核心诊断必须由 Codex / agent 完成，而不是由脚本代替判断。

---

## 1. 分层原则

- script：准备 draft sections、mentor profile、term findings、truth findings、rubric 维度，并打包成 packet
- agent：对成熟稿做真正诊断、评分、finding 排序、priority 提取

脚本可以做 heuristic pre-check，但不能取代最终 xray 判断。

---

## 2. Agent 必答问题

消费 `paper_xray_packet` 后，agent 至少要回答：

1. 哪些 section 最不像导师？
2. 哪些地方最有 AI 味？
3. 哪些术语、比较、结论最危险？
4. 哪些问题是结构问题，不是句子问题？
5. 哪些 finding 必须先修？

---

## 3. 输出要求

agent 应产出结构化 `xray_report.json`，遵循：

- `docs/schemas/xray_report.schema.json`

至少包含：

- 8 维评分
- findings
- prioritized_actions
- overall summary / overall risk

---

## 4. 禁止事项

- 不得只输出空泛评价
- 不得只给分不举 evidence
- 不得只靠 regex 结果替代段落级诊断
