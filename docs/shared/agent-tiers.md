# Agent Tiers

This repository uses a simple three-tier mental model for specialist execution:

## LOW

Use for:
- small lookups
- file mapping
- lightweight packaging

## STANDARD

Use for:
- xray analysis
- mentor-style revision
- approach scoring
- exemplar curation

## THOROUGH

Use for:
- mentor profile synthesis
- mentor profile delta review
- architect-grade framework review
- cross-artifact consistency checks

Rule of thumb:
- if the output changes a persistent mentor artifact, default to **THOROUGH**
- if the output rewrites user-facing paper text, default to **STANDARD**
- if the task only prepares or locates context, default to **LOW**
