# Mentor Bloom Paper Polish / 导师脑论文润色系统

An agent-first framework for building a mentor-writing brain, diagnosing mature research drafts, and polishing papers toward supervisor-style quality.

一个 **agent-first** 的论文润色框架：先构建导师写作大脑，再诊断成熟稿件，最后把论文往导师风格与教授级写作质量推进。

---

## TL;DR / 一句话说明

- **Build a mentor brain** from papers, comments, transcripts, and revision traces
- **Diagnose a mature draft** with agent-authored xray reports
- **Polish the paper** through pass-based, mentor-style revision workflows

- **构建导师脑**
- **诊断成熟稿**
- **按导师式流程润色论文**

---

## What this repository is / 这个仓库是什么

This repository focuses on three practical abilities:

1. **Mentor Brain distillation**  
   Learn a supervisor's writing preferences, revision habits, terminology, and rhetorical moves from papers, comments, transcripts, and revision traces.

2. **Paper Xray**  
   Diagnose a mature draft for mentor drift, AI flavor, terminology problems, comparison issues, transition weakness, and paragraph-architecture problems.

3. **Mentor Polish**  
   Package the draft into pass-based workspaces so Codex/agents can revise the paper section by section in a mentor-like way.

4. **Micro-Polish with mentor lexicon/corpus**  
   Accumulate mentor-specific professional wording, phrase replacements, and sentence-level exemplars so agents can polish sentence by sentence and even word by word.

这个仓库当前聚焦三个实用能力：

1. **导师脑蒸馏**  
   从导师论文、批注、会议转录、聊天和改稿痕迹中，学习导师的写作偏好、改稿习惯、术语系统和段落动作。

2. **论文 Xray 诊断**  
   对成熟稿做结构化体检，检查导师漂移、AI 味、术语问题、比较不清、转折不稳、段落组织失衡等问题。

3. **导师式润色**  
   把稿件打包成 pass-based workspaces，让 Codex / agents 按导师式流程逐节修改。

4. **逐句/逐词微观润色**  
   积累导师专业写作词汇库和语料库，让 agent 能做 sentence-level 甚至 word-level 的导师式改稿。

---

## Core design principles / 核心设计原则

- **Skills guide, agents judge.**  
  Skills define workflow and guardrails. Scripts prepare artifacts. Codex/agents do the real reasoning, diagnosis, and rewriting.

- **Agent-first canonical path.**  
  Mentor brain, paper xray, revision agenda, and mentor polish all follow an agent-first design. Script-generated outputs are fallback scaffolds only.

- **Mentor-only polish mode is supported.**  
  If your paper's scientific conclusions are already correct, the system can focus purely on supervisor-style writing optimization.

- **Version everything.**  
  Mentor profiles, deltas, changelogs, and artifacts are meant to be inspectable, reviewable, and rollbackable.

- **Sentence-level quality matters.**  
  The framework should eventually support sentence-by-sentence and word-by-word mentor-style polishing through a structured mentor lexicon and corpus.

- **Skill 只指导，agent 才判断。**  
  skill 负责 workflow 和 guardrails；script 负责准备 artifact；真正的判断、诊断、改写由 Codex / agent 完成。

- **主路径必须 agent-first。**  
  导师脑、paper xray、revision agenda、mentor polish 都以 agent-first 为规范路径；script 生成的内容只作为 fallback scaffold。

- **支持 mentor-only polish 模式。**  
  如果论文的科研结论已经正确，系统可以只从导师写作技法和改稿技法角度优化。

- **所有关键对象都应版本化。**  
  导师脑 profile、delta、changelog、artifacts 都应可检查、可评审、可回滚。

- **逐句质量也必须被建模。**  
  框架最终应支持 sentence-level 甚至 word-level 的导师式改稿，这需要结构化的导师词汇库与语料库。

---

## Repository layout / 仓库结构

```text
.
├─ docs/
│  ├─ architecture/   # High-level design docs
│  ├─ protocols/      # Agent/script/skill execution rules
│  ├─ rubrics/        # Diagnostic rubrics
│  └─ schemas/        # JSON schema contracts
├─ scripts/           # Deterministic tooling only
├─ hooks/             # Hook design notes / placeholders
├─ examples/          # Safe sample inputs for public/demo use
└─ .codex/skills/     # Repo-local Codex skill scaffolds
```

说明：

- `docs/architecture/`：总体设计与阶段性架构文档  
- `docs/protocols/`：agent/script/skill 分层协议  
- `docs/rubrics/`：诊断规则  
- `docs/schemas/`：artifact 合同  
- `scripts/`：确定性工位，不替代 agent 思考  
- `examples/`：公开可用的示例输入  
- `.codex/skills/`：repo-local skill 入口

---

## Quick start / 快速开始

### 1) Clone the repo / 克隆仓库

```bash
git clone https://github.com/Qian9921/mentor-bloom-paper-polish.git
cd mentor-bloom-paper-polish
```

### 1.5) Requirements / 运行依赖

Minimal assumptions:

- Python 3.10+
- `pdftotext` available in `PATH` if you want PDF extraction
- Codex CLI or a Codex-compatible agent environment if you want the full agent-first workflow

最低依赖：

- Python 3.10+
- 若要抽 PDF 文本，需要系统里有 `pdftotext`
- 若要走完整 agent-first 路径，需要 Codex CLI 或兼容环境

### 2) Prepare your mentor materials / 准备导师材料

Place your supervisor materials under a private folder, for example:

```text
data/mentor/raw/
  ├─ papers/
  ├─ transcripts/
  ├─ comments/
  └─ revision_traces/
```

建议：

- 导师论文
- 会议录音转文字稿
- 聊天记录
- 批注
- 导师亲改痕迹

### 3) Prepare your draft / 准备你的论文稿件

Put your draft under something like:

```text
data/paper_inputs/
  └─ your_paper.tex / your_paper.md / your_paper.txt
```

If possible, also prepare a **clean prose-only export** for better polishing quality.

如果可以，尽量同时准备：

- 原始 `.tex`
- 一份干净的 prose-only 文本版本

后者通常更利于 xray 和 polish。

---

## How to use the skills / 如何使用这些 skills

### Recommended skill names / 推荐 skill 名称

- `$mentor-bloom` / `$bloom`  
  Evolve the mentor brain using new materials

- `$paper-xray`  
  Diagnose a mature paper draft

- `$mentor-polish`  
  Build pass-based polishing workspaces and revise toward supervisor style

- `$micro-polish`  
  Run sentence-level and word-level mentor-style polishing with mentor lexicon/corpus support

说明：

- `$mentor-bloom` / `$bloom`：让导师脑持续进化  
- `$paper-xray`：对成熟稿做结构化体检  
- `$mentor-polish`：按导师式流程打包并润色
- `$micro-polish`：做逐句/逐词的导师式微观润色

### Legacy alias / 兼容旧名

- `$learning` → use `$mentor-bloom` instead

### How other users can actually invoke these skills / 其他用户如何真正使用这些 skill

If you open this repository in Codex, the repo-local skill scaffolds under `.codex/skills/` are the intended entry points.

Typical usage:

```text
$mentor-bloom
$paper-xray
$mentor-polish
$micro-polish
```

如果你在 Codex 中打开这个仓库，`.codex/skills/` 下的 repo-local skill 就是推荐入口。

典型调用方式：

```text
$mentor-bloom
$paper-xray
$mentor-polish
$micro-polish
```

If your environment does **not** automatically expose repo-local skills, you still have two practical options:

1. keep the repo open as the active workspace and use the docs/protocols/scripts manually
2. copy the relevant skill scaffold into your own Codex skills directory

如果你的环境**不会自动暴露** repo-local skills，也有两个简单办法：

1. 直接在这个仓库里按 docs/protocols/scripts 手动走流程
2. 把对应的 skill scaffold 复制到你自己的 Codex skills 目录

---

## Canonical workflows / 规范工作流

### A. Mentor brain evolution / 导师脑进化

1. Add new mentor materials
2. Build mentor manifest
3. Build mentor evolution packet + brief
4. Have Codex/agent author `mentor_profile_delta.json`
5. Review and promote a new mentor profile version

### B. Paper xray / 论文诊断

1. Build draft map
2. Build project fact sheet
3. Build xray packet + brief
4. Have Codex/agent author `xray_report.json`

### C. Mentor polish / 导师式润色

1. Build revision agenda brief
2. Have Codex/agent author `revision_agenda.json`
3. Build reference mirror packet + brief
4. Build mentor polish briefs + pass-based workspace
5. Let Codex/agent revise section by section

### D. Micro polish / 逐句微观润色

1. Build mentor lexicon
2. Build mentor corpus index
3. Build micro-polish packet + brief
4. Let Codex/agent revise sentence-level tasks

### Minimal public demo flow / 最小公开演示流程

You can use the example files in `examples/` to understand the workflow shape without any private data:

```bash
python3 scripts/build_mentor_manifest.py \
  --input-dir examples \
  --output /tmp/mentor_manifest.json \
  --mentor-id sample
```

然后结合：

- `scripts/README.md`
- `docs/protocols/`
- `docs/schemas/`

就能理解完整 agent-first 工作流应该怎么接起来。

---

## Important usage rule / 最重要的使用规则

> **Scripts do not replace thinking.**

Scripts can:

- normalize files
- export packets
- build manifests
- generate diffs
- manage versions

But scripts should **not** be treated as the canonical decision-maker for:

- mentor-brain synthesis
- final xray diagnosis
- final revision agenda
- actual mentor-style rewriting

这些必须由 Codex / agents 完成。

---

## Public-safe content / 公共仓库中保留的内容

This repository is intentionally kept clean for public use:

- included:
  - docs
  - scripts
  - hooks notes
  - safe examples

- excluded:
  - private mentor raw data
  - generated run artifacts
  - local state
  - confidential paper drafts

这个仓库默认只放：

- 文档
- 脚本
- hook 说明
- 示例文件

不会默认放：

- 私有导师材料
- 运行中间产物
- `.omx/`
- 私密论文草稿

This separation is intentional. The framework repo should remain safe to clone, browse, and reuse publicly.

这种分离是刻意的：这个仓库应该保持“公开可 clone、可浏览、可复用”的状态。

---

## Current status / 当前状态

This repo already contains:

- P0 architecture docs
- YanBrain v0.2 design
- MentorPolish v0.2 design
- mentor-only polish mode
- agent-first schema/protocol/tooling
- mentor-bloom evolution scaffolding

当前已包含：

- P0 架构设计
- YanBrain v0.2 设计
- MentorPolish v0.2 设计
- mentor-only polish mode
- agent-first schema / protocol / tooling
- mentor-bloom 持续进化脚手架

And now also includes:

- repo-level `AGENTS.md`
- `LICENSE`
- bilingual onboarding README

并且现在还包含：

- 仓库级 `AGENTS.md`
- `LICENSE`
- 中英双语 README

---

## Suggested next phase / 下一阶段建议

The most valuable next steps are:

1. Add more repo-local skill surfaces (`paper-xray`, `mentor-polish`)
2. Add an agent-authored `mentor_profile_delta` review/promote loop
3. Add a cleaner prose export path for `.tex` papers
4. Build a held-out benchmark for “mentor-likeness”

后续最值得做的是：

1. 增加更完整的 repo-local skill 入口
2. 完成 `mentor_profile_delta` 的 review/promote 闭环
3. 给 `.tex` 论文提供更干净的 prose export
4. 建立“像不像导师”的 held-out benchmark

---

## License / 许可

This repository is released under the MIT License. See `LICENSE`.

本仓库采用 MIT License，见 `LICENSE`。
