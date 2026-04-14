# Agent Swarm Audit Protocol

## Purpose

This protocol exists to keep semantic judgment out of scripts.

Scripts may locate, slice, index, and persist.
They must not decide whether a sentence, opening, transition, or paragraph is mentor-grade.

That judgment belongs to agents.

## Core rule

Use multiple agents to audit the real draft directly, with enough context to understand:

- the sentence
- the full paragraph
- the surrounding paragraph(s)
- the local subsection
- the section role
- the mentor brain

## Required flow

1. **Index only**
   - Script may enumerate sections / paragraphs / line ranges.
   - Script may not assign semantic verdicts.

2. **Independent audits**
   - Spawn multiple agents over disjoint or complementary draft slices.
   - Each agent authors an `agent_swarm_audit_report.json`.

3. **Consensus aggregation**
   - A deterministic merger may combine reports into `agent_swarm_consensus.json`.
   - The merger may deduplicate and count support.
   - The merger may not invent new semantic findings.

4. **Blocking defect extraction**
   - Consensus findings with `must_fix` severity should be copied into a defect ledger.

5. **Agent-only final acceptance**
   - Final pass/fail claims should come from agent review, not from heuristic scripts.

## Recommended staffing

For a long research paper, use a fixed staffing plan instead of improvising per run.

### Default long-paper audit swarm

Use **5 audit agents + 1 consensus agent**:

1. **Intro / Problem Framing Auditor**
   - openings
   - transitions
   - contribution framing

2. **Method Exposition Auditor**
   - subsection openings
   - notation introduction
   - equation bridges
   - reader guidance

3. **Experiment Setup / Baseline Auditor**
   - setup openings
   - baseline logic
   - metric logic
   - configuration placement

4. **Results / Diagnostics Auditor**
   - results openings
   - scene-by-scene narration
   - comparator scope
   - benchmark-report tone

5. **Case Study / Mechanism / Discussion / Conclusion Auditor**
   - case-study openings
   - mechanism explanation
   - practical implication
   - limitation / conclusion landing

6. **Consensus Agent**
   - merges audit reports
   - deduplicates findings
   - assigns blocking severity
   - emits defect-ledger candidates

### Smaller-paper fallback

For a short paper or note, use **3 audit agents + 1 consensus agent**:

- intro/method
- experiments/results
- discussion/conclusion
- consensus

### Hard rule

Do not reduce the swarm to one agent merely because scripts can pre-slice the draft.
Scripts may help locate spans, but the semantic judgment still belongs to the agents.

## When to use

- final opening audits
- sentence-heaviness audits
- transition audits
- paragraph-contract audits
- mentor-alignment signoff

## Anti-pattern to avoid

Do not let a heuristic script become the final judge of:

- whether an opening is clear enough
- whether a sentence is too roundabout
- whether a paragraph reads like the mentor

Those are agent judgments.
