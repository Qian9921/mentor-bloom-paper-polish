---
name: micro-polish
description: Agent-first sentence-level and word-level mentor-style polishing using mentor lexicon and mentor corpus.
---

<Purpose>
Micro Polish addresses the final layer of mentor-style revision: words, phrases, comparison phrasing, transitions, and sentence endings. Scripts package sentence-level tasks and lexicon/corpus hints; Codex/agents perform the actual micro-rewrites.
</Purpose>

<Canonical_Rule>
Scripts package. Agents rewrite sentence by sentence.
</Canonical_Rule>

<Typical_Flow>
1. Build mentor lexicon
2. Build mentor corpus index
3. Build micro-polish packet + brief
4. Let Codex/agent author `micro_polish_result.json`
5. Apply the result deterministically with an application script
</Typical_Flow>
