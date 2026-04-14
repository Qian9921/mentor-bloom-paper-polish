# MentorPolish v0.2：导师式改稿系统设计

状态：设计稿
目标：让 polish 从“润色动作”升级成“导师式 revision protocol”

---

## 1. 为什么 v0.1 的 polish 还不够

MentorPolish v0.1 已经有：

- xray
- revision agenda
- reference mirror
- polish brief
- pass-based workspace

但它的问题是：

> 更像“改稿准备层”，还不像“真正的导师式改稿系统”。

真正像导师的改稿过程，不是简单地：

- 改句子
- 去 AI 味
- 换几个术语

真正的导师改稿，是一个有顺序的判断流程。

---

## 2. MentorPolish v0.2 的核心目标

MentorPolish v0.2 应该做到：

1. 更规范：每次改稿都按固定协议走；
2. 更像导师：不是 generic academic editing，而是遵循 Yan 的判断结构；
3. 更可验证：每轮改稿都能回答“为什么这样改，改得有没有更像 Yan”；
4. 更会自我提升：真实改稿结果反过来更新导师脑。

---

## 2A. 当前阶段特判：Mentor-Only Polish Mode

就当前任务而言，我建议明确进入一个特化模式：

> **mentor-only polish mode**

这个模式的假设是：

- 当前论文中的 scientific conclusion 暂时视为正确；
- 当前系统不重新裁决算法、数学、实验是否成立；
- 当前主要目标是把稿件改得更像导师。

这意味着当前阶段的 polish 重心应放在：

- 写作组织
- 段落动作
- results narration
- figure/table interpretation
- transition
- terminology
- conclusion landing

而不是把精力主要花在：

- 项目脑再审
- 专家脑技术裁决
- claim/evidence 全量重构

这不是长期总架构，
而是当前最适合你场景的冻结策略。

---

## 3. polish 的六段协议

## 3.1 Diagnose

先判断问题类型，而不是一上来改字。

必须先区分：

- scientific risk
- structure problem
- paragraph problem
- sentence problem
- terminology problem

## 3.2 Prioritize

建议固定优先级：

1. scientific risk
2. structure / paragraph function
3. comparison / evidence alignment
4. terminology
5. local sentence polish

## 3.3 Strategy Select

在真正改之前，要先选策略。

例如当前动作到底是：

- split_dense_paragraph
- add_bridge_transition
- move_summary_after_evidence
- name_the_comparator
- tighten_contribution_sentence
- convert_metric_dump_to_reader_guided_results
- pair_limitation_with_future_work

## 3.4 Execute by Pass

建议固定 5 个 pass：

### Pass 1：Macro Pass

- title
- abstract
- contribution sentence
- result main storyline
- conclusion landing

### Pass 2：Paragraph Pass

- paragraph role
- ordering
- topic sentence
- bridge / transition
- ending sentence

### Pass 3：Sentence Pass

- remove AI flavor
- compress empty wording
- improve precision
- strengthen local punch

### Pass 4：Terminology Pass

- unify technical terms
- replace vague terms with paper-defined terms
- align comparator naming

### Pass 5：Verify Pass

- check whether original finding is solved
- check whether scientific meaning drifted
- check whether style regressed

## 3.5 Style Regression Check

这是 v0.2 要新增的关键。

改完后必须检查：

- 有没有从“更像 Yan”退化成 generic English polishing；
- 有没有把原本有劲的句子改平；
- 有没有把 section 的 local rhythm 改坏；
- 有没有只做表面润色，没有真正解决问题。

## 3.6 Reflection

每轮结束后必须回答：

1. 这轮解决了什么？
2. 哪些问题没解决？
3. 哪些改动最像导师？
4. 哪些地方只是换说法，没有本质提升？

---

## 4. 三个 judge 角色

MentorPolish v0.2 推荐显式引入三个判断器。

## 4.1 Mentor Alignment Judge

问题：

- 这段是否更像 Yan 会写的版本？

## 4.2 Truth Guard Judge

问题：

- 这段是否引入了 claim/evidence 漂移？

## 4.3 Reader Flow Judge

问题：

- 读者是否还需要猜？
- 这段是否更顺着读者理解顺序展开？

这三个 judge 不一定都要是独立 agent，但逻辑上必须存在。

---

## 5. polish 不应只做“纠错”，还应做“强化”

导师式改稿不只是：

- 把错的改对

还包括：

- 把弱的改强
- 把散的改紧
- 把糊的改准
- 把平的改有推进感

因此 MentorPolish v0.2 应明确区分两类动作：

## 5.1 Repair Actions

- fix transition
- fix term
- fix comparator
- fix unsupported statement

## 5.2 Upgrade Actions

- strengthen contribution
- sharpen conclusion
- improve result narration
- improve paragraph rhythm
- improve implication articulation

---

## 6. Reference Mirror 在 polish 中的位置

reference-mirror 不应是可有可无的辅助项。

它在 v0.2 中应承担一个明确角色：

> 帮 agent 理解“Yan 在同类问题上通常怎么写”。

尤其适用于：

- abstract 重写
- result paragraph 重写
- figure/table narration
- case study explanation
- discussion / limitation pairing

---

## 7. 规范输入与输出

## 7.1 输入

MentorPolish v0.2 的规范输入至少应包含：

- compiled mentor profile
- xray report
- revision agenda
- project fact sheet
- reference mirror packet
- pass brief
- section task

## 7.2 输出

每次 pass 至少应输出：

- revised text
- revision rationale
- preserved constraints
- unresolved issues
- verify notes

---

## 8. 质量门

一轮 polish 完成前，至少要回答 6 个问题：

1. 这轮改动解决的是结构问题还是表面问题？
2. 这轮是否真的更像 Yan？
3. 这轮是否更好地服务读者理解？
4. 这轮是否引入 terminology drift？
5. 这轮是否改坏 scientific meaning？
6. 这轮是否留下了清晰的改稿理由？

任何一条答不清，都不算高质量完成。

---

## 9. 与 YanBrain v0.2 的闭环

MentorPolish v0.2 不应该只消费导师脑，它还应反哺导师脑。

每次真实改稿后，应记录：

- 哪些 rule 真有用；
- 哪些 rewrite operator 反复有效；
- 哪些 judgement 最接近导师；
- 哪些 mirror snippet 最常帮助改稿；
- 哪些 old rule 不够好用。

这些信息回流到 YanBrain v0.2 的 evolution memory。

---

## 10. 最终结论

MentorPolish v0.2 的升级方向不是：

> “让 AI 更会润色。”

而是：

> “让 Codex 按导师真实的改稿顺序和判断逻辑去改稿。”

也就是说：

- 先判断
- 再定策略
- 再按 pass 执行
- 再检查风格回归
- 再把经验反哺导师脑

只有这样，polish 才会越来越规范、越来越稳、越来越像导师。

---

## 10A. 如何减少“反复修”并提升一轮成稿率

你前面问的一个关键问题是：

> 为什么导师脑都在了，还不能一次性做好？

MentorPolish v0.2 的后续升级，应该直接围绕“减少迭代次数”来设计。

我建议从四个方向补：

### 1. 更厚的正向样例库

不仅知道导师讨厌什么，
还要让系统看到：

- Yan 如何写 abstract
- 如何开 result paragraph
- 如何做 figure/table interpretation
- 如何写 discussion / limitation / conclusion

### 2. 更强的 revision operator 库

不是让 agent 自由发挥“润色”，
而是让它明确选择：

- split
- reorder
- bridge
- name comparator
- tighten claim
- convert metric-dump to synthesis-first
- strengthen implication landing

### 3. 改稿前先做 strategy simulation

也就是：

- 先诊断
- 再选策略
- 再预演改法
- 最后才写回正文

这样能明显减少“写了又返工”的情况。

### 4. 输入层更干净

像 raw `.tex` 带前置 bib / 模板噪声的输入，会降低一轮成稿率。

如果能先提供：

- prose-only export
- cleaned manuscript text
- section-isolated workspace

系统会更容易一轮做对。

所以，如果我们的目标是未来尽量“一轮成稿”，
真正要强化的是：

> 导师脑厚度 + 改稿动作库 + strategy layer + 干净输入

而不是单纯继续堆更多 heuristic script。
