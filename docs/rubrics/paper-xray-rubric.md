# Paper Xray Rubric v0.1

目的：把“这篇稿子哪里不行”从主观抱怨变成结构化诊断。

适用场景：

- 输入已经是一篇成熟稿或准成熟稿；
- 目标不是从零写，而是找出最影响导师满意度的关键问题；
- 输出必须能直接 handoff 给 `revision_agenda` 与 `mentor-polish`。

---

## 1. 总体规则

`paper-xray` 第一版固定检查 8 个维度：

1. `mentor-drift`
2. `ai-smell`
3. `terminology-risk`
4. `claim-precision`
5. `transition-rhythm`
6. `paragraph-architecture`
7. `evidence-language-gap`
8. `truth-risk-lite`

每个维度都必须给出：

- 分数：`1-5`
- 总结
- 至少 1 条可定位 evidence
- 至少 1 条 recommended action

### 分数解释

| 分数 | 含义 |
|---|---|
| 1 | 很差，导师大概率一眼不满意 |
| 2 | 明显有问题，需要优先处理 |
| 3 | 可接受但不稳，仍影响整体质感 |
| 4 | 基本达标，只需少量修整 |
| 5 | 很强，已经接近导师满意状态 |

### 严重度解释

| 严重度 | 含义 | 处理优先级 |
|---|---|---|
| `P0` | 再不修就会伤 scientific meaning 或直接触发导师强烈反感 | 最高 |
| `P1` | 明显拉低稿件质量和导师相似度 | 高 |
| `P2` | 局部可优化项 | 中低 |

---

## 2. 八个核心维度

## 2.1 `mentor-drift`

### 看什么

- 是否明显不像导师会写出来的话；
- 是否偏离导师常用叙述路径；
- 是否缺少导师惯用的力度、收束方式、对比方式。

### 常见症状

- 句子“对”，但不像导师；
- 段落推进太平；
- abstract / conclusion 的 punch 不够；
- 贡献说法松散。

### 评分锚点

- `1`：大面积不像导师，甚至像另一类作者；
- `3`：局部可看，但主干段落仍明显 drift；
- `5`：关键段落明显能看出导师式手法。

### 推荐动作

- 调用 mentor playbook；
- 参考导师 rewrite pattern 重写主题句、结尾句、贡献句。

## 2.2 `ai-smell`

### 看什么

- 模板腔、均质腔、翻译腔、流水账腔；
- 句式重复；
- “看起来很顺但没有狠劲”的语言。

### 常见症状

- 高频模板连接词；
- 一堆安全但空泛的形容；
- 每句都完整但没有重点；
- 段落像“均匀搅拌”后的 AI 文本。

### 推荐动作

- 删空词；
- 提升句子信息密度；
- 把 “safe wording” 改成更明确的 claim language。

## 2.3 `terminology-risk`

### 看什么

- 术语是否符合 GNSS / navigation / deep learning 语境；
- 同一概念是否多套叫法混用；
- 导师偏好的术语是否被替换掉。

### 常见症状

- 同一概念在不同 section 里名字不一样；
- 用了泛 AI 词，没用本领域更精确的说法；
- 引入缩写但后面使用不稳。

### 推荐动作

- 对照 `terminology_preferences`；
- 做 term consistency scan；
- 建立 do-not-replace 清单。

## 2.4 `claim-precision`

### 看什么

- claim 是否过软、过虚、过大、过模糊；
- comparator 是否点名；
- improvement 是否有边界、有条件、有对象。

### 常见症状

- “significantly improves” 但没说对谁、在什么条件下；
- novelty 像口号；
- 贡献句太泛。

### 推荐动作

- 压缩夸张表述；
- 补充条件、范围、对象；
- 把弱 claim 改成可落地的准确 claim。

## 2.5 `transition-rhythm`

### 看什么

- 句间、段间切换是否自然；
- 信息推进是否有节奏；
- 读者是否会在转折处“绊一下”。

### 常见症状

- transition 硬切；
- 逻辑词堆得太多反而不自然；
- 从背景跳方法、从方法跳实验没有桥。

### 推荐动作

- 增加 bridge sentence；
- 重写段首/段尾；
- 调整信息顺序而不是只加连接词。

## 2.6 `paragraph-architecture`

### 看什么

- 每段是否有明确功能；
- 主题句是否顶得住；
- 支撑信息顺序是否合理；
- 段尾是否能自然收束。

### 常见症状

- 一段里混背景、方法、结果、解释；
- 主题句弱；
- 重要信息埋在中间；
- 段落像 notes dump。

### 推荐动作

- 先判定段落功能；
- 再重排句子；
- 必要时拆段或合段。

## 2.7 `evidence-language-gap`

### 看什么

- 实验结果本来不错，但语言没有把价值讲出来；
- 结果和意义之间的桥不够清楚；
- 贡献和实验没有正确绑定。

### 常见症状

- 有提升但没有强调 why it matters；
- 结果存在但没讲 significance；
- 讨论段只是重复 figure。

### 推荐动作

- 把结果翻译成价值；
- 强化 “what this implies”；
- 把 evidence 与 contribution 对齐。

## 2.8 `truth-risk-lite`

### 看什么

- 某些位置一旦润色就容易把 scientific meaning 改坏；
- 公式、实验条件、比较边界、符号定义是否脆弱。

### 常见症状

- 数学/算法描述太容易被压缩坏；
- baseline 对比关系稍改就失真；
- 结论句比证据更大。

### 推荐动作

- 标记 `do_not_break` 约束；
- 需要时 handoff 给 `truth-check-lite`；
- 对高风险句子禁止自由发挥式润色。

---

## 3. 诊断输出要求

每次 `paper-xray` 至少输出：

1. 8 维评分表；
2. `P0/P1/P2` 问题清单；
3. section / paragraph 定位；
4. 推荐修改动作；
5. 不能碰坏的 scientific constraints。

---

## 4. 禁止事项

- 不能只给空泛评价，不给 evidence；
- 不能只说“AI 味重”，不说明重在哪里；
- 不能把 scientific risk 当作普通润色问题；
- 不能用单一分数替代具体问题定位。
