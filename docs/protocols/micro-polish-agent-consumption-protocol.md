# Micro-Polish Agent Consumption Protocol v0.1

目标：让系统具备逐句、逐词级的导师式改稿能力。

---

## 1. 分层原则

- script：准备句子级任务、lexicon、corpus、diff
- agent：执行真正的逐句/逐词判断与替换

script 不得直接批量做 canonical rewrite。

---

## 2. Agent 应回答的问题

agent 在做 micro-polish 时至少应回答：

1. 这句话最不像导师的地方是在词、短语、比较、转折，还是句尾收束？
2. 这里应该调用哪类 mentor lexicon 条目？
3. 这里是否有现成 mentor corpus 片段可以借鉴句法动作？
4. 这次修改是 repair 还是 upgrade？

---

## 3. 输入建议

micro-polish 最好消费：

- mentor lexicon
- mentor corpus index
- sentence-level findings
- local section playbook
- do-not-break constraints

---

## 4. 输出建议

每个 sentence-level task 至少输出：

- original sentence
- revised sentence
- changed words/phrases
- reason for the change
- mentor evidence used
