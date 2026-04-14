# Section Swarm Execution Protocol

## Purpose

For long papers, a single audit swarm over the whole draft is still too coarse.
This protocol raises the unit of work to the **section** and assigns a dedicated
mini-swarm to each section.

## Core staffing rule

For each section, allocate at least:

- **5 section auditors**
- **1 section consensus agent**
- **1 section reverse-check agent**

That is **7 logical agents per section**.

## Auditor roles inside one section

1. **Opening Auditor**
   - paragraph openings
   - subsection openings
   - local topic clarity

2. **Sentence / Word Auditor**
   - heavy or roundabout sentences
   - vague wording
   - mentor-lexicon drift

3. **Transition / Flow Auditor**
   - paragraph-to-paragraph flow
   - subsection handoff
   - why-next clarity

4. **Section-Contract Auditor**
   - whether the section is doing the right rhetorical job
   - whether paragraph order matches the section contract

5. **Holistic Mentor-Alignment Auditor**
   - overall mentor feel
   - whether the section still sounds machine-like or student-like

6. **Section Consensus Agent**
   - merges the 5 audit reports
   - emits section-level blocking findings

7. **Section Reverse-Check Agent**
   - re-reads the revised section after edits
   - verifies that the section actually passes

## Paragraph coverage rule

Every paragraph in the section must be read by at least one audit agent.
For high-risk sections, prefer having all 5 auditors read the full section.

## Concurrency rule

If the runtime cannot host all logical agents concurrently, execute them in waves.

### Recommended waves per section

- **Wave A**: the 5 section auditors
- **Wave B**: section consensus agent
- **Wave C**: section reverse-check agent

This preserves the logical staffing model even when the runtime concurrency cap is low.

## Hard rule

Do not reduce the logical staffing model just because the tool/runtime can only host a smaller number of concurrent agents.

The solution is **waves**, not **under-staffing**.
