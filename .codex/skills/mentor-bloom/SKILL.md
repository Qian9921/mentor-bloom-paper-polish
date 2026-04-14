---
name: mentor-bloom
description: Agent-first mentor-brain evolution workflow for absorbing new supervisor materials, proposing profile deltas, and promoting reviewed versions.
---

<Purpose>
Mentor Bloom evolves the mentor brain over time. It does not blindly rebuild the profile. It packages new mentor evidence, asks Codex/agents to propose a profile delta, and promotes a new version only after review.
</Purpose>

<Use_When>
- The user adds new mentor transcripts, comments, or papers
- The mentor profile feels outdated, thin, or incomplete
- The user explicitly asks to re-learn, evolve, strengthen, or refresh the mentor brain
- The user wants a `$learning`-style workflow but with a better name and stronger structure
</Use_When>

<Canonical_Aliases>
- `$mentor-bloom`
- `$bloom`
- Legacy compatibility alias: `$learning`
</Canonical_Aliases>

<Non_Negotiable_Rules>
- Scripts prepare, agents judge
- Never learn from the target draft
- Promotion requires versioning and changelog
- Prefer high-trust mentor-authored or mentor-edited evidence
</Non_Negotiable_Rules>

<Workflow>
1. Build or refresh mentor manifest
2. Build mentor evolution packet + brief
3. Have Codex/agent author `mentor_profile_delta.json`
4. Review the delta
5. If approved, promote a new mentor profile version and append changelog
</Workflow>
