# Revision Agenda Agent Consumption Protocol v0.1

目标：把 `xray_report` 转成真正有执行顺序的修改 agenda。

---

## 1. 分层原则

- script：准备 xray report、mentor rules、project constraints、目标 schema
- agent/planner：做真正的优先级判断与行动排序

---

## 2. Agenda 的核心问题

agent 在生成 agenda 时必须明确：

1. 哪些问题先修，不然后面改了也会返工？
2. 哪些属于 macro 问题，哪些属于 paragraph 问题，哪些只是 sentence 问题？
3. 哪些地方先不要动，因为 scientific risk 太高？
4. 每个 action 的 success criteria 是什么？

---

## 3. 输出要求

输出结构化 `revision_agenda.json`，遵循：

- `docs/schemas/revision_agenda.schema.json`

---

## 4. 禁止事项

- 不得按发现顺序机械排序
- 不得把所有问题都当 sentence polish
- 不得忽略 do-not-break constraints
