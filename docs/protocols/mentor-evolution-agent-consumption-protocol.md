# Mentor Evolution Agent Consumption Protocol v0.1

目标：让 `$learning` 或导师脑增量升级走一条严格的 agent-first 路径。

---

## 1. 规范分层

- skill：定义何时启动增量学习
- script：打 manifest、抽新证据、组 evolution packet
- agent：判断新证据是否应升级导师脑
- verifier：决定是否 promotion

---

## 2. 增量学习的核心问题

agent 消费 evolution packet 后，必须回答：

1. 新材料真正提供了什么新增规则？
2. 它是在强化旧规则，还是推翻旧规则？
3. 它的证据是否足够强？
4. 它是否只是一时口头表达，而不是稳定偏好？
5. 是否应升级 profile 版本？

---

## 3. 输出要求

建议 agent 先输出：

- `mentor_profile_delta.json`

再在审查通过后 promotion 为：

- `compiled_mentor_profile.vNext.json`

---

## 4. 禁止事项

- 不得跳过 verifier 直接 promotion
- 不得把 target draft 当学习材料
- 不得因单条低质量 transcript 就重写核心价值观
