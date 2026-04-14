# Installation / 安装说明

## Goal / 目标

Make the public framework repo easy to use in a Codex workspace without copying private research data into the repository.

在不把私有数据提交到公共仓库的前提下，让这个框架仓库更容易在 Codex 中直接使用。

---

## Option A: Open the repo directly / 方案 A：直接打开仓库

Open the repository as your active Codex workspace:

```bash
git clone https://github.com/Qian9921/mentor-bloom-paper-polish.git
cd mentor-bloom-paper-polish
```

Then use the repo-local skills and commands:

```text
$mentor-bloom
$paper-xray
$mentor-polish
$micro-polish
```

---

## Option B: Copy skill scaffolds to your global Codex home / 方案 B：复制到全局 Codex 目录

If you want the skills globally available:

```bash
mkdir -p ~/.codex/skills/mentor-bloom ~/.codex/skills/paper-xray ~/.codex/skills/mentor-polish ~/.codex/skills/micro-polish
cp .codex/skills/mentor-bloom/SKILL.md ~/.codex/skills/mentor-bloom/
cp .codex/skills/paper-xray/SKILL.md ~/.codex/skills/paper-xray/
cp .codex/skills/mentor-polish/SKILL.md ~/.codex/skills/mentor-polish/
cp .codex/skills/micro-polish/SKILL.md ~/.codex/skills/micro-polish/
```

If you also want the repo-local command docs:

```bash
mkdir -p ~/.codex/commands
cp .codex/commands/*.md ~/.codex/commands/
```

---

## Hooks / Hook 配置

The repository now includes `.codex/hooks.json` plus lightweight hook scripts under `hooks/`.

仓库现在包含：

- `.codex/hooks.json`
- `hooks/session_start_summary.py`
- `hooks/post_bash_json_check.py`

These are lightweight runtime helpers, not a full private production hook system.

它们是轻量级公开 hook 示例，不是私有生产级 hook 全套。
