# Audit Checklist

## Use this file

Load this reference when you need a compact checklist for auditing `app_build/`, deciding what to test, or building the final QA report.

## Preflight

- Confirm `app_build/` exists.
- Confirm `production_artifacts/Technical_Specification.md` exists.
- Confirm `production_artifacts/Solution_Architecture.md` exists.
- Confirm Git history is available.
- Confirm which stack the repository uses: Node.js, Python, or mixed.

## Spec alignment

- Every required feature from the spec is present.
- Partial implementations are called out explicitly.
- API contracts match the specification.
- Validation rules match the specification.
- Non-functional requirements from the spec are respected when visible in code.

## Architecture alignment

- The code respects the approved layers and boundaries.
- Data access is not leaking into UI or controller code unexpectedly.
- Shared utilities are not bypassing the intended abstractions.
- Framework usage matches the approved architecture.
- Config, secrets, and environment handling align with the deployment design.

## Bug-hunting checklist

- Manifest includes every required runtime dependency.
- Manifest includes every required test dependency.
- Imports resolve cleanly.
- No dead or obviously stale imports remain around the fix area.
- Syntax parses for the touched files.
- Edge cases around null, empty, zero, and invalid input are covered.
- Async flows await or return the correct promises.
- Error handling is specific and user-safe.
- Input validation exists at trust boundaries.
- Hardcoded credentials or tokens are absent.
- User-controlled content is sanitized or encoded where required.
- Types or schemas reflect the real payload shape.

## Test checklist

- Unit tests cover the changed business logic.
- Integration tests cover the contract between layers.
- E2E coverage exists only for real user-facing flows.
- Tests live under `app_build/`.
- New tests fail before the fix when feasible and pass after the fix.

## Verification checklist

- Run the smallest targeted validation that proves the fix.
- Record the exact command or test selection used.
- Note any blocked verification and the reason.
- Avoid claiming full-suite health if only targeted checks ran.

## Ready-for-deployment checklist

- All required features appear implemented.
- The recent-change bug is fixed.
- No unresolved high-severity security issue remains in scope.
- Dependencies required for runtime and tests are present.
- Validation is complete enough for the claimed status.
- The final report states assumptions, blockers, and residual risk clearly.
