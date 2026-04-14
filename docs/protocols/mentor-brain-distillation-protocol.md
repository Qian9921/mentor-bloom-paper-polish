# Mentor Brain Distillation Protocol v0.1

目标：把导师材料压缩成一个 **可执行的写作判断协议**，而不是堆成一个材料仓库。

> 规范路径：script 负责准备 packet，Codex / agent 负责真正蒸馏导师脑。

---

## 1. 输入优先级

导师脑优先吃以下材料：

1. 导师本人写的论文；
2. 导师亲手改过的 revision traces；
3. 导师对论文的批注、聊天、语音转录；
4. 少量导师研究线附近的强参考文献。

禁止直接把当前目标稿当作导师样本。

---

## 2. 蒸馏目标

最终必须形成这 5 类东西：

1. `global_rules`
2. `terminology_preferences`
3. `rejection_lexicon`
4. `rewrite_patterns`
5. `section_playbooks`

如果一个产物不能落到这五类之一，大概率说明它还只是“材料”，不是“导师脑”。

---

## 3. 全流程

### Stage A：材料盘点

- 建 manifest；
- 标记 source type；
- 标记 trust tier；
- 对 PDF / transcript 做文本化和标准化。

### Stage B：句级规则提取

重点提取：

- 导师明确说不要什么；
- 导师明确偏好什么；
- 导师反复强调什么；
- 导师如何描述 contribution / limitation / result / value。

### Stage C：局部模式归纳

重点归纳：

- 弱句变强句的模式；
- abstract 与 introduction 的常见组织方式；
- 术语偏好；
- 语气强弱的边界。

### Stage D：编译

把散乱规则编译成一个稳定 profile：

- 必须结构化；
- 必须可被下游脚本和 agent 消费；
- 必须能解释来源。

这一步默认应该由 **Codex / agent** 完成，而不是由 script 直接硬编码写死。

---

## 4. 质量门

导师脑编译完成前，至少回答这 4 个问题：

1. 哪些表达导师明显不喜欢？
2. 哪些 section 导师有稳定偏好？
3. 哪些术语导师会 insist？
4. 下游 agent 是否能直接拿这个 profile 改稿？

任意一个答不上来，说明蒸馏还不够。
