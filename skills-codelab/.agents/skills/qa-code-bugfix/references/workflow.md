# QA Code Bugfix Workflow

## Purpose

Use this workflow when the task combines QA engineering, destructive auditing, and a recent-change bugfix requirement. Work from evidence, keep the scope anchored in `app_build/`, and tie at least one concrete defect to the current author's edits from the last week whenever possible.

## Required inputs

- `app_build/`
- `production_artifacts/Technical_Specification.md`
- `production_artifacts/Solution_Architecture.md`
- Git metadata for the current repository

If any required input is missing, stop and report the gap instead of guessing.

## Phase 1: Alignment audit

1. Read `Technical_Specification.md`.
2. Read `Solution_Architecture.md`.
3. Walk the code under `app_build/`.
4. Verify the following before editing:
   - Required features exist.
   - Major user flows are implemented.
   - Architecture layers match the approved design.
   - Framework and library choices do not drift from the approved architecture.
   - Environment/config handling matches the intended deployment model.

Capture discrepancies as concrete findings, not vague concerns.

## Phase 2: Destructive bug hunting

Check each category aggressively:

| Category | What to check |
| --- | --- |
| Dependencies | Missing packages, stale manifests, wrong versions, missing test tooling |
| Imports | Missing modules, dead imports, circular references, wrong paths |
| Syntax | Broken TypeScript, Python syntax failures, invalid JSON or YAML |
| Logic | Wrong conditions, edge-case gaps, off-by-one bugs, broken branching |
| Async | Missing `await`, swallowed promises, races, inconsistent loading states |
| Security | Hardcoded secrets, injection risks, missing validation, XSS exposure |
| Error handling | Missing try/catch, leaky stack traces, unhelpful error states |
| Types | `any` abuse, missing schema validation, weak contracts, inconsistent DTOs |

Prefer evidence from focused commands:

- A targeted test
- A file-level lint/type check
- A direct repro command
- Existing CI or local failure logs

Do not inflate the scope with unrelated legacy defects.

## Phase 3: Recent-change scope

1. Identify the current author from Git config.
2. List commits from the last week for that author.
3. Collect touched files and focus on the overlap with `app_build/`.
4. Confirm the defect is directly caused by those changes.

Use `scripts/detect_recent_scope.py` when it saves time or reduces ambiguity.

If no qualifying bug maps to the author's own edits, say so plainly and stop instead of forcing a fix.

## Phase 4: Test suite creation

Create or extend tests inside `app_build/` only.

Recommended structure:

```text
app_build/
|-- tests/
|   |-- unit/
|   |   |-- services/
|   |   `-- utils/
|   |-- integration/
|   |   |-- api/
|   |   `-- db/
|   `-- e2e/
|       `-- flows/
`-- ...
```

Test priorities:

1. Business logic and service functions
2. Validation and schema handling
3. Critical API paths and persistence behavior
4. Authentication and middleware
5. E2E flows only when the repository actually has a frontend or browser flow

Framework default:

- Node.js: Vitest
- Python: Pytest

Follow the repository's existing tooling if it is already established and coherent.

## Phase 5: Fix implementation

Make the smallest correction that resolves the verified defect.

- Edit only the files needed for the fix.
- Keep the local conventions intact.
- Add dependencies only when the fix or test coverage truly requires them.
- Avoid opportunistic refactors.

You are allowed to overwrite flawed files inside `app_build/`, but keep the changes proportional.

## Phase 6: Verification

Run the narrowest useful validation:

- A targeted test file
- A focused lint or typecheck command
- A direct reproduction command

If full verification cannot run, explain what should run next and why it was blocked.

## Final report

Use this structure:

```text
QA REPORT:
- Files audited: <count>
- Bugs found & fixed: <count>
- Tests created: [unit: X, integration: Y, e2e: Z]
- Security issues: <count>
- Status: READY FOR DEPLOYMENT | NEEDS REVIEW
```

Make the root-cause linkage explicit:

- Which recent commit or file introduced the bug
- Why the failure maps to the current author's changes
- Which validation proved the fix
