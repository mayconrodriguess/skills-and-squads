---
name: generate-code
description: Generate the implementation for the approved project across frontend, backend, and supporting code. Use whenever the user wants a broad full-stack build in `app_build/` and there is an approved technical specification to follow.
---

# Generate Code

## Objective
Translate approved artifacts into working code without skipping structure, config, or supporting files.

## Project Structure Contract
- `production_artifacts/` contains the approved specification and architecture
- `app_build/` receives the generated implementation
- project `scripts/` stores repeatable generators, setup helpers, and validators
- project `assets/` stores templates, mock data, and supporting static files
- `.agents/skills/` and `.agents/workflows/` are appropriate when the repo needs reusable multi-role execution

## Workflow
1. Read the approved specification before writing code.
2. Decide whether the task should stay full-stack or be split into specialized project-local agents.
3. Generate the required source tree in `app_build/`, including framework config and dependencies.
4. Create helper scripts under project `scripts/` when the same setup or validation will recur.
5. Leave the repo with a runnable structure, not just isolated code fragments.
