# Defect Ledger Protocol

## Purpose

The defect ledger is the hard-gate layer for explicit mentor- or user-called problems.

It exists to prevent the following failure mode:

- the mentor brain has learned the rule
- the user or mentor has explicitly pointed out the defect
- the draft is still declared clean before that exact defect is cleared

## Core rule

If a mentor transcript, mentor feedback item, or direct user message explicitly points out a concrete writing defect, that defect must be entered into the ledger and treated as a blocking item until it is verified as fixed.

## Required behavior

1. Create one ledger entry per explicit defect.
2. Record:
   - source reference
   - issue description
   - target file / locator
   - current status
   - verification evidence
3. Do not declare the draft clean while any blocking defect remains `open`.
4. Human-explicit defects outrank heuristic scorer findings.

## Status meaning

- `open`: defect known and unresolved
- `fixed`: an edit has been made, but verification is still pending
- `verified`: the defect has been re-checked and cleared
- `rejected`: the defect was intentionally not applied, with rationale

## Recommended flow

1. Capture mentor/user explicit defects in a seed JSON
2. Build the normalized ledger artifact
3. Revise the draft
4. Update each ledger entry with evidence
5. Verify that all blocking defects are `verified`
6. Only then allow final-clean claims
