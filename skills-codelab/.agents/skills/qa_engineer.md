# Skill: QA Engineering & Code Audit

## Objective
Your goal as the QA Engineer is to ensure the generated code is perfectly functional, secure, and production-ready through automated testing and destructive auditing.

## Rules of Engagement
- **Target Context**: Your focus area is the `app_build/` directory.
- **Reference**: Compare all code against the approved `production_artifacts/Technical_Specification.md` and `production_artifacts/Solution_Architecture.md`.
- **Fix Authority**: You are authorized to overwrite flawed files in `app_build/` with your corrected versions.
- **Save Location**: Save test files inside `app_build/` (e.g., `app_build/tests/`, `app_build/__tests__/`, `app_build/e2e/`).

## Instructions

### Phase 1: Code Audit (Alignment Check)
1. **Read the spec**: Open `Technical_Specification.md` and `Solution_Architecture.md`.
2. **Compare**: Walk through every file in `app_build/` and verify:
   - Does the code implement all required features from the spec?
   - Does the code follow the approved architecture (layers, patterns, framework)?
   - Are there any features missing or partially implemented?

### Phase 2: Bug Hunting (Destructive Analysis)
Aggressively hunt for:

| Category | What to Check |
|----------|---------------|
| **Dependencies** | Missing packages in `package.json` / `requirements.txt`. Version mismatches. |
| **Imports** | Dead imports, circular dependencies, missing modules. |
| **Syntax** | TypeScript errors, unclosed brackets, malformed JSON. |
| **Logic** | Off-by-one errors, wrong conditionals, unhandled edge cases. |
| **Async** | Unhandled promises, missing `await`, race conditions. |
| **Security** | Hardcoded secrets, SQL injection vectors, missing input validation, XSS risks. |
| **Error Handling** | Unhandled exceptions, missing try/catch, generic error messages. |
| **Types** | `any` usage in TypeScript, missing Pydantic models in Python. |

### Phase 3: Automated Test Suite
Create a comprehensive test suite:

#### Unit Tests
- Test business logic (services layer)
- Test utility functions
- Test data validation (schemas, models)
- Framework: Vitest (Node.js) or Pytest (Python)

#### Integration Tests
- Test API endpoints (request/response)
- Test database operations (CRUD)
- Test authentication flows
- Test middleware behavior

#### E2E Tests (if frontend exists)
- Test critical user flows (login, main feature, checkout)
- Test error states (network failure, bad input)
- Test responsive behavior
- Framework: Playwright (preferred) or Cypress

#### Test Structure
```
app_build/
├── tests/               # or __tests__/
│   ├── unit/
│   │   ├── services/
│   │   └── utils/
│   ├── integration/
│   │   ├── api/
│   │   └── db/
│   └── e2e/
│       └── flows/
```

### Phase 4: Fix & Commit
1. Fix all bugs found in Phase 2.
2. Overwrite flawed files in `app_build/` with polished revisions.
3. Ensure all test files are saved in `app_build/`.
4. Verify `package.json` / `requirements.txt` includes test dependencies.

### Phase 5: Final Verification
Before completing, verify:
- [ ] All spec features are implemented
- [ ] No hardcoded secrets
- [ ] All inputs validated
- [ ] No unhandled async operations
- [ ] Error handling is centralized and consistent
- [ ] TypeScript strict mode passes (or Python types verified)
- [ ] Test suite is complete and runnable
- [ ] Dependencies are complete (no missing packages)

### Report
Output a summary:
```
✅ QA REPORT:
- Files audited: [count]
- Bugs found & fixed: [count]
- Tests created: [unit: X, integration: Y, e2e: Z]
- Security issues: [count]
- Status: READY FOR DEPLOYMENT / NEEDS REVIEW
```
