---
name: audit-code
description: Perform a focused code audit inside `app_build/` against approved project artifacts. Use whenever the user asks for a quick implementation review, bug sweep, dependency check, or targeted remediation pass without asking for a full QA program.
---

# Audit Code

## Objective
Run a fast, high-signal audit of the current implementation, fix clear defects, and leave the workspace in a more reliable state.

## Project Structure Contract
Before touching code, verify the workspace and create only what is needed:

- `production_artifacts/` for source-of-truth documents
- `app_build/` for the implementation under review
- `scripts/` for any repeatable validator or fixer you create
- `references/` for short audit notes when the findings need to persist
- `.agents/`, `.agents/skills/`, `.agents/workflows/` only if the repo needs a reusable audit workflow

## Required Inputs
- `production_artifacts/Technical_Specification.md`
- `production_artifacts/Solution_Architecture.md` when it exists
- the current code under `app_build/`

If the required artifacts are missing, say exactly what is missing before auditing.

## Workflow
1. Read the specification and architecture constraints.
2. Inspect the current implementation with a bias for runtime failures, missing dependencies, broken imports, config drift, and obvious logic bugs.
3. Fix concrete defects directly in `app_build/`.
4. Create or update a small helper under project `scripts/` only when the same check would likely be reused.
5. Summarize the findings, fixes, and any residual risk.

## Output
- code fixes inside `app_build/`
- optional helper scripts in project `scripts/`
- a concise audit report in the response
