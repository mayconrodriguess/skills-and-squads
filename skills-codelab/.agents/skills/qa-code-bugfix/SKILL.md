---
name: qa-code-bugfix
description: Audit code in app_build against approved production specs, hunt implementation and security defects, scaffold test coverage, and fix a bug introduced by the current author within the last week. Use when Codex must compare app_build to production_artifacts/Technical_Specification.md and production_artifacts/Solution_Architecture.md, add tests inside app_build, or triage and fix failures caused by the author's recent commits.
---

# QA Code Bugfix

## Overview

Audit `app_build/`, tie a concrete defect to the current author's recent edits when possible, implement the smallest viable fix, and verify the result with focused checks and test coverage.

## Start

- Treat `app_build/` as the primary target directory.
- Read `production_artifacts/Technical_Specification.md` and `production_artifacts/Solution_Architecture.md` before making feature or architecture claims.
- Load `references/workflow.md` for the full phase sequence.
- Load `references/audit-checklist.md` when enumerating findings, missing coverage, or release-readiness checks.

## Workflow

### 1) Establish scope

- Use `scripts/detect_recent_scope.py --repo <repo>` to identify the current author and files changed in the last week.
- Default to that recent-change scope when the prompt is empty.
- Stop early if `app_build/` or the required production artifacts are missing.

### 2) Audit alignment

- Compare every relevant area in `app_build/` against the specification and the approved architecture.
- Record missing features, partial implementations, layering violations, framework drift, and configuration mismatches before editing.

### 3) Hunt defects

- Check dependencies, imports, syntax, logic, async handling, security, error handling, and types.
- Prefer the smallest reproducible validation tied to the touched files.
- Keep the root cause tied to the author's recent edits; if failures are unrelated legacy issues, stop and report that no qualifying recent-change bug was found.

### 4) Add or extend tests

- Save tests only under `app_build/` such as `tests/`, `__tests__/`, or `e2e/`.
- Use `scripts/scaffold_test_layout.py <app_build>` if the repository needs a baseline test tree.
- Prefer Vitest for Node.js or Pytest for Python unless the repository already uses an established alternative.

### 5) Fix minimally

- Overwrite flawed files inside `app_build/` when necessary.
- Update manifests only when required for the actual fix or the new tests.
- Avoid unrelated refactors, speculative hardening, or broad cleanup.

### 6) Verify and report

- Run the smallest meaningful validation for the fix.
- Use `scripts/render_qa_report.py` with `assets/qa-report-template.md` to produce the final report if useful.
- Report files audited, bugs fixed, test counts, security issues, and deployment readiness.

### 7) Correção de erros

- Se no meio do teste for verificado por exemplo: a porta 3000 já está ocupada na máquina, Faça a liberação da porta se a aplicação que estiver rodando não for para uso do projeto.
- Caso seja para uso do projeto chamar o Agent @backend-engineer para que ele possa fazer a correção do Codigo.

## Guardrails

- Keep the working area centered on `app_build/`.
- Make the linkage to the current author's last-week changes explicit before calling something a recent-code bugfix.
- Prefer a clear stop with missing inputs or unrelated failures over a weak diagnosis.
- Keep reusable code in `scripts/`, detailed documentation in `references/`, and templates or auxiliary data in `assets/`.
