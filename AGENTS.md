# Mentor Bloom Paper Polish - Repository Guidance

Scope: this file governs the entire repository.

## Intent

This repository is a **public-safe framework repo**, not a private project workspace.

Its purpose is to share:

- architecture
- protocols
- schemas
- scripts
- repo-local skill scaffolds
- safe sample files

It should **not** become a dump for:

- private mentor materials
- confidential drafts
- generated artifacts
- local runtime state

## Core execution principles

- **Skills guide; agents judge.**
- **Scripts prepare; they do not replace reasoning.**
- Preserve the repo as a reusable framework for other Codex users.
- Prefer small, explicit, reviewable changes.
- Keep examples safe and generic.

## Content rules

- Do not add private mentor data or real user drafts.
- Do not commit `.omx/`, `artifacts/`, or other local run outputs.
- New public examples must be safe to publish.
- Favor bilingual docs when the content is user-facing and high-value.

## Documentation rules

- Public-facing onboarding should stay concise and practical.
- README should explain:
  - what the repo does
  - how to use the repo-local skills
  - what is intentionally excluded
- When adding a new protocol or schema, link it from the README when it materially affects users.

## Git / release rules

- Keep commits intentional and explanatory.
- If adding new workflow surfaces, ensure the names are stable and memorable.
- Avoid breaking existing skill names without documenting aliases.
