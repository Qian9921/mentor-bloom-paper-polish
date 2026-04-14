# Micro-Polish Result Agent Consumption Protocol v0.1

目标：让 agent 真正消费 `micro_polish_packet` 并输出可被脚本安全应用的句级改稿结果。

---

## 1. 分层原则

- script：准备 packet，应用 agent 结果，输出 diff
- agent：逐句判断并写出 `micro_polish_result.json`

script 不得自行决定 canonical sentence rewrite。

---

## 2. Agent 输出要求

agent 应输出：

- `micro_polish_result.json`

遵循：

- `docs/schemas/micro_polish_result.schema.json`

每条 revision 至少包含：

- task_id
- section_id
- original_sentence
- revised_sentence
- reason

---

## 3. 应用原则

应用脚本只做：

- exact replacement safety check
- deterministic apply
- diff export

如果：

- 原句不存在
- 原句出现多次且无法唯一定位
- 替换会造成明显应用歧义

应用脚本应报错，而不是擅自猜测。
