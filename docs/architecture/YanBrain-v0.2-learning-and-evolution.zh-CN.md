# YanBrain v0.2：导师脑增强与持续进化设计

状态：设计稿
目标：让导师脑从“静态规则库”升级为“可持续进化的导师判断系统”
适用阶段：P0+，在已有 mentor-brain / xray / polish 骨架之上继续增强

---

## 1. 为什么必须进入 v0.2

YanBrain v0.1 已经能做这些事：

- 从导师论文、会议反馈、聊天文字稿中蒸馏初版 profile；
- 提取术语偏好、禁忌表达、section playbook、rewrite pattern；
- 给下游 xray / mentor-polish 提供可消费 artifact。

但 v0.1 的本质仍然偏向：

> “一次性蒸馏出一版导师画像”

这还不够。

真实使用中，你会不断加入：

- 新的会议录音稿；
- 新的导师改稿痕迹；
- 新的导师论文 PDF；
- 新的导师口头批评；
- 新的高质量正样例。

如果导师脑不能随着这些材料持续进化，它很快会出现三个问题：

1. **画像过时**：只代表某个时间点；
2. **画像偏薄**：只能抓到少量局部习惯；
3. **画像不可校正**：新证据来了，却没有正式升级机制。

所以 v0.2 的目标非常明确：

> 让导师脑成为一个可版本化、可升级、可回滚、可审计、可被 agent 持续强化的系统。

---

## 2. 核心判断：导师脑不是知识库，而是判断系统

导师脑强大，不在于“存了很多材料”，而在于它能在改稿时做出更像导师的判断。

这里必须再加一条长期边界：

> 在未来三脑并行架构里，YanBrain 只负责 **导师写作智慧与改稿智慧**，  
> 不负责算法、数学、理论创新是否成立。

也就是说，YanBrain 的增强方向应该集中在：

- 写法
- 改法
- 段落推进
- figure/table narration
- section playbook
- critique ontology
- revision operators

而不是去吸收：

- 外部专家论文中的算法对错判断
- 当前项目中的实验结论本体
- method 是否真正有 novelty 的终极裁决

这些东西未来应分别属于：

- `expert-brain`
- `project-brain`

这样 YanBrain 才会越来越像导师，而不是越来越像混合大脑。

因此 YanBrain v0.2 不应被建模成：

- 一堆 PDF
- 一堆 transcript
- 一堆规则

而应被建模成一个 **多层判断系统**。

---

## 3. YanBrain v0.2 的六层模型

## 3.1 价值观层（Value Model）

这是 Yan 写作与改稿最底层的判断原则。

例如目前已经观察到的：

- 证据优先于空泛表达；
- 图表与文字必须互相 support；
- 用词必须准，不能模糊；
- 比较词必须点名 comparator；
- 不能 summary-first 地讲结果；
- transition 是高敏感项；
- 不能让 AI 的默认上下文替代读者可见信息。

这一层决定：

> 当两个写法都“语法对”时，Yan 会更偏向哪一个。

## 3.2 section intelligence 层

这层定义每一类 section 的任务函数。

例如：

- abstract 应如何压缩 problem / challenge / method / mechanism / quantified result；
- introduction 应如何铺 problem / gap / contribution；
- results 应如何 figure-first / observation-second / synthesis-last；
- discussion 应如何讲 implication；
- limitations 应如何和 future work 成对出现。

这一层回答的是：

> “这一节到底该怎么完成它的工作，而不是只写得像论文。”

## 3.3 critique ontology 层

这是 Yan 批评问题的“分类体系”。

建议固定成一些稳定类别：

- transition failure
- comparison underspecification
- terminology vagueness
- unsupported interpretation
- summary-first result narration
- paragraph overloading
- figure/table not introduced
- caption/text role confusion
- spoken-style expression
- AI list-like exposition
- limitation placement error

这一层让 xray 不再只是自由发挥地挑问题，而是：

> 按导师真实批评体系诊断稿件。

## 3.4 revision operator 层

导师脑不只应该知道“哪里不好”，还应该知道“该怎么改”。

建议把稳定改稿动作单独建模：

- split_dense_paragraph
- move_summary_after_evidence
- name_the_comparator
- replace_vague_term_with_defined_term
- add_bridge_transition
- convert_metric_dump_to_takeaway_plus_support
- pair_limitation_with_future_work
- remove_caption_repetition
- tighten_contribution_sentence
- strengthen_conclusion_implication

这一层回答：

> “这个问题属于哪一种导师式改法？”

## 3.5 正向样例层（Positive Exemplars）

导师脑不能只靠负反馈。

必须建立：

- Yan 论文中写得好的 abstract 样例；
- 写得好的 results 样例；
- 写得好的 case study 样例；
- 写得好的 discussion / limitation / conclusion 样例。

这一层回答：

> “除了不要这样写，还应该怎样写？”

## 3.6 演化记忆层（Evolution Memory）

这是 v0.2 最关键的新层。

它记录：

- 新材料带来了什么新规则；
- 哪些旧规则被增强；
- 哪些旧规则被削弱；
- 哪些规则彼此冲突；
- 哪些规则在真实改稿里被证明有效；
- 哪些规则在真实改稿里不够好用。

这一层回答：

> “导师脑是怎么变强的？”

---

## 4. 持续进化的总体流程

YanBrain v0.2 的核心不是单次蒸馏，而是 **持续进化 loop**。

建议分成六个阶段：

## Stage A：新材料入库

新加入的材料可能包括：

- 导师新论文 PDF
- 新会议 transcript
- 新聊天记录
- 新改稿记录
- 新批注

script 负责：

- 文本化
- 标准化
- manifest
- trust tier 标注

## Stage B：增量蒸馏 packet 生成

script 负责产出：

- `mentor_evolution_packet.json`
- `mentor_evolution_brief.md`

它不负责判断，只负责把“新增证据 + 当前 profile + 版本差异上下文”组织给 agent。

## Stage C：agent 做 delta synthesis

Codex / agent 消费 evolution packet 后，不是直接重写整份 profile，而是先输出：

- `mentor_profile_delta.json`

它应回答：

- 新证据支持新增哪些规则？
- 新证据是否强化某些旧规则？
- 是否有规则冲突？
- 是否需要合并 / 替换 / 降级某条规则？

## Stage D：verifier 做升级审查

verifier / critic 应检查：

- 新规则是否真的有足够证据；
- 是否混入了 target draft 污染；
- 是否把偶然一次导师口头表达误当成稳定偏好；
- 是否引入冲突术语。

## Stage E：profile promotion

只有在验证通过后，才升级：

- `Yan_compiled_mentor_profile.v0.2.json`
- `Yan_compiled_mentor_profile.v0.2.md`

同时记录 changelog。

## Stage F：真实改稿反哺

一次真实 polish 完成后，应回写：

- 哪些规则这次有效；
- 哪些规则帮助不大；
- 哪些规则导致误判；
- 哪些新模式值得写入导师脑。

这一步让导师脑不只是“吃材料”，还会“吃自己的实战经验”。

---

## 5. `mentor-bloom` 的设计理念

用户提出的 `$learning` 想法是正确的，而且是 v0.2 的关键入口。

但在命名上，我建议把它升级成更有趣、也更准确的名字：

- **正式工作流名：** `$mentor-bloom`
- **短别名：** `$bloom`
- **兼容旧叫法：** `$learning`

但必须注意：

> `$mentor-bloom` 不应该是“脚本把新材料扫一遍然后自动覆盖 profile”。

它应该是：

> 一个 **agent-first 的导师脑增量演化 workflow**。

### `$mentor-bloom` 的规范行为

当你在 Codex 里触发类似：

```text
$mentor-bloom
```

系统应该做的是：

1. 扫描 `data/mentor/raw/` 与 `data/mentor/normalized/` 中新增材料；
2. 对新增材料做 manifest 与 trust-tier 更新；
3. 生成 `mentor_evolution_packet`；
4. 由 agent 读取当前 profile + 新证据，输出 profile delta；
5. 由 verifier 审查；
6. 通过后升级 profile 版本；
7. 记录 changelog 与 rollback 点。

### `$mentor-bloom` 不应该做的事

- 不应直接覆盖当前 profile；
- 不应把当前目标论文当学习材料；
- 不应把低质量 transcript 直接等同于稳定规则；
- 不应跳过 verifier；
- 不应丢失旧版本。

---

## 6. 持续进化必须有的 guardrails

## 6.1 Source hygiene

学习材料必须分层：

- high：导师论文、导师亲改痕迹、导师明确批评
- medium：会议 transcript、聊天记录
- low：外部参考样例、学生间接总结

新规则必须显式记录证据来源层级。

## 6.2 Target-draft isolation

当前目标稿永远不能反向污染导师脑。

## 6.3 Versioning

每次升级都应有：

- version id
- changed rules
- added rules
- downgraded rules
- rationale

## 6.4 Rollback

如果某次升级后行为变差，应能退回前一版本。

## 6.5 Conflict resolution

如果新旧规则冲突，必须显式处理，而不是静默覆盖。

---

## 7. 让导师脑更“智能”的关键，不只是多吃材料

很多系统以为持续学习=更多材料。

其实不是。

更强的导师脑，至少还要做到三件事：

## 7.1 规则显式分层

要区分：

- must rules
- strong preferences
- soft preferences
- context-dependent moves

## 7.2 规则与情境绑定

比如：

- 结果段的规则未必适用于引言；
- harsh criticism 场景下的口头反馈未必适合所有 paper；
- 某一篇论文中的写法未必适合所有任务。

## 7.3 真实改稿闭环反馈

只有当导师脑在真实论文改稿中被验证：

- 改得更像导师；
- 导师更少骂；
- 用户更省力；

它才算真的变强。

---

## 8. 与 MentorPolish v0.2 的关系

YanBrain v0.2 不是独立存在的。

它必须和 MentorPolish v0.2 联动：

- YanBrain 提供更强的判断与动作库；
- MentorPolish 把这些判断落实成 pass-based rewriting；
- polish 结果再反哺 YanBrain。

所以二者应形成闭环：

> 导师脑越强，改稿越像导师；  
> 改稿实战越多，导师脑越会升级。

---

## 9. v0.2 的第一实现优先级

如果按价值排序，建议先做：

1. `mentor_evolution_packet`
2. `mentor_profile_delta`
3. profile changelog / rollback
4. real-polish feedback back-propagation
5. exemplar library extraction

而不是继续堆更多 heuristic script。

---

## 10. 最终结论

YanBrain v0.2 的核心不是：

> “让系统多读几篇导师论文。”

而是：

> “让系统形成一个可持续进化的导师判断系统，并在每次新材料与真实改稿中不断升级。”

所以 `$mentor-bloom` 是一个非常好的想法，
但它必须被实现为：

- agent-first
- versioned
- evidence-backed
- reviewable
- rollbackable

只有这样，导师脑才会真的越来越强，而不是越来越脏。
