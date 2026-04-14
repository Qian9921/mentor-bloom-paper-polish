# Mentor Brain Agent Consumption Protocol v0.1

这是导师脑的 **规范路径**。

重点只有一句话：

> script 只负责整理、标准化、打包；真正的导师脑蒸馏必须由 Codex / agent 消费 packet 后完成。

---

## 1. 为什么不能 script 写死

因为导师脑不是 deterministic mapping。

它涉及：

- 风格判断；
- 规则抽象；
- 术语偏好归纳；
- 弱句到强句的 rewrite pattern 总结；
- section playbook 综合。

这些都不是脚本应该“硬编码决定”的。

脚本能做的是：

- 抽文本；
- 做 manifest；
- 选 snippet；
- 组 packet；
- 导出 brief；
- 保存 artifact。

真正该由 Codex / agent 做的是：

- 证据归纳；
- 规则合并；
- 冲突消解；
- 导师画像编译；
- 下游消费与改稿判断。

---

## 2. 规范两阶段

## Stage A：Script Preparation

脚本负责产出：

- `mentor_material_manifest.json`
- `mentor_distillation_packet.json`
- `mentor_distillation_brief.md`

这一步只解决“材料可读、可消费、可引用”。

## Stage B：Agent Distillation

Codex / agent 读取 packet 与 brief，产出：

- `compiled_mentor_profile.json`
- 可选 `compiled_mentor_profile.md`

这一步才是真正的导师脑蒸馏。

---

## 3. Agent 产出要求

Codex / agent 产出的 `compiled_mentor_profile` 必须：

1. 遵循 schema；
2. 明确给出：
   - `global_rules`
   - `terminology_preferences`
   - `rejection_lexicon`
   - `rewrite_patterns`
   - `section_playbooks`
3. 每条重要规则最好能回指 `evidence_snippets`；
4. 不允许把当前目标论文当导师样本；
5. 不允许无依据臆造导师偏好。

---

## 4. 下游消费关系

下游模块消费顺序：

1. `paper-xray` 消费 `compiled_mentor_profile`
2. `revision_agenda` 消费 `xray_report`
3. `mentor-polish` 同时消费：
   - `compiled_mentor_profile`
   - `xray_report`
   - `revision_agenda`
   - `project_fact_sheet`

所以，导师脑不是一个“脚本内部对象”，而是一个 **agent-authored shared artifact**。
