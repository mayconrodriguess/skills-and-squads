# Documentation Templates

Copy-pasteable skeletons for the most common docs. Fill in the brackets.

---

## 1. README (root)

```markdown
# [Project Name]

[One-sentence description. What is this and who is it for?]

[![CI](badge-url)](ci-url) [![License](badge-url)](license-url) [![Version](badge-url)](version-url)

---

## Why

[One paragraph: the problem this solves and the audience.]

## Quickstart

Requirements:
- Node 22+ (or Bun 1.1+)
- Docker (optional, for local DB)

```bash
git clone https://github.com/org/repo.git
cd repo
cp .env.example .env
npm install
npm run dev
```

Open http://localhost:3000.

## Features

- [Feature 1]
- [Feature 2]
- [Feature 3]

## Documentation

- [Architecture](./production_artifacts/Solution_Architecture.md)
- [API Reference](./production_artifacts/docs/api/)
- [Contributing](./CONTRIBUTING.md)
- [Changelog](./CHANGELOG.md)

## License

[SPDX identifier, e.g. MIT] -- see [LICENSE](./LICENSE).
```

---

## 2. CHANGELOG (Keep a Changelog)

```markdown
# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning: [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [1.2.0] - 2025-03-14

### Added
- /export endpoint for CSV downloads (#123)

### Changed
- /users now returns `createdAt` as ISO 8601 string. **Breaking for clients parsing epoch ms.** See [migration guide](./production_artifacts/docs/migrations/1.2.0.md).

### Fixed
- Race condition when renaming the same resource twice (#145)

### Security
- Upgraded lodash to 4.17.22 (CVE-2025-XXXX)

[Unreleased]: https://github.com/org/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/org/repo/compare/v1.1.0...v1.2.0
```

---

## 3. CONTRIBUTING

```markdown
# Contributing to [Project Name]

Thanks for your interest! This doc covers how to set up the project, the
conventions we follow, and how to submit changes.

## Development Setup

[Copy from README quickstart, plus any contributor-specific tools]

## Branching

- `main`: always deployable
- Feature branches: `feat/short-description`
- Fix branches: `fix/short-description`

## Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org):

- `feat: add export endpoint`
- `fix: correct timestamp parsing`
- `docs: update quickstart`
- `chore: bump dependencies`
- `refactor: extract validation helper`

Breaking changes: prefix `feat!:` or `fix!:` and add a BREAKING CHANGE footer.

## Pull Requests

- Branch off `main`
- Keep PRs focused -- one concern per PR
- Include tests for new logic
- Pass CI before requesting review
- Update CHANGELOG.md in the Unreleased section

## Running Tests

```bash
npm test              # unit
npm run test:e2e      # end-to-end
npm run lint          # lint + format check
```

## Code Style

- TypeScript strict mode
- Prettier for formatting
- ESLint for linting
- Max line length 100

## Reporting Bugs

Open an issue using the bug template. Include:
- What you expected
- What happened
- Steps to reproduce
- Your environment (OS, Node version)

## Code of Conduct

By participating you agree to our [Code of Conduct](./CODE_OF_CONDUCT.md).
```

---

## 4. Runbook Template

```markdown
# Runbook: [Incident or Operation Name]

**Severity**: [Sev-1 | Sev-2 | Sev-3]
**Audience**: [On-call engineer]
**Last reviewed**: YYYY-MM-DD by [@owner]

## Symptoms

How you know this is happening:
- [Symptom 1 -- alert name or user report]
- [Symptom 2]

## Impact

[Who is affected, what is broken, typical duration]

## Quick Mitigation

The 3-step emergency response. Do these first, investigate after.

1. [Action 1 -- e.g. drain the node, flip the feature flag]
2. [Action 2]
3. Notify [channel] with: "[template message]"

## Diagnosis

Confirm the cause:

- Check [dashboard URL]
- Check [log query]
- Check [metric]

## Remediation

Full fix steps:

1. [Step with command]
2. [Step with command]
3. Verify by [specific check]

## Rollback

If remediation fails:

1. [Rollback step]

## Post-Incident

- Write a retrospective (template: [link])
- File follow-up tickets for prevention
- Update this runbook if anything surprised you
```

---

## 5. Migration Guide Template

```markdown
# Migration Guide: [Version X -> Version Y]

## Why

[What changed and why, in 1-2 sentences]

## Breaking Changes

### Change 1: [Name]

Before:
```typescript
// old way
```

After:
```typescript
// new way
```

Why: [reason]

Automated migration: `npx migrate-script` (if available)

## Non-Breaking Improvements

- [Thing X is now faster]
- [Thing Y supports Z]

## Step-by-Step

1. Update dependency to `^Y.0.0`
2. Run `npm install`
3. Apply code changes (see table above)
4. Run `npm test`
5. Deploy

## Troubleshooting

| Symptom | Fix |
|---|---|
| Error `X` | [Answer] |
| Error `Y` | [Answer] |
```

---

## 6. `llms.txt` Template

```markdown
# [Project Name]

> [One-paragraph description -- what this project does, who it's for, the stack]

## Docs

- [Quickstart](/README.md): Run it locally in 10 minutes
- [Architecture](/production_artifacts/Solution_Architecture.md): System design + diagrams
- [Tech Stack](/production_artifacts/Tech_Stack_Rationale.md): Why each tool was chosen
- [API Reference](/production_artifacts/docs/api/): Endpoint documentation
- [Database Schema](/production_artifacts/Database_ER_Diagram.md): ER diagram + entities

## Key Concepts

- [Auth model](/production_artifacts/docs/auth.md)
- [Tenancy](/production_artifacts/docs/tenancy.md)
- [Error handling](/production_artifacts/docs/errors.md)

## Decisions

- [ADR index](/production_artifacts/ADRs/)

## Optional

- [Runbooks](/production_artifacts/docs/runbooks/)
- [Changelog](/CHANGELOG.md)
```

---

## 7. API Endpoint Doc Template

```markdown
## POST /api/v1/orders

Create a new order for the authenticated user.

**Auth**: Bearer token (JWT)
**Rate limit**: 60/minute per user
**Idempotency**: Supported via `Idempotency-Key` header

### Request

```json
{
  "items": [
    { "productId": "prd_123", "quantity": 2 }
  ],
  "shippingAddressId": "adr_456"
}
```

| Field | Type | Required | Notes |
|---|---|---|---|
| items | array | yes | 1-50 items |
| items[].productId | string | yes | Must exist and be in stock |
| items[].quantity | integer | yes | 1-999 |
| shippingAddressId | string | yes | Must belong to the user |

### Response -- 201 Created

```json
{
  "status": "success",
  "data": {
    "id": "ord_789",
    "total": 4250,
    "currency": "BRL",
    "createdAt": "2025-03-14T10:00:00Z"
  }
}
```

### Errors

| Status | Code | Meaning |
|---|---|---|
| 400 | VALIDATION_FAILED | Request body invalid |
| 401 | UNAUTHORIZED | Missing or invalid token |
| 404 | PRODUCT_NOT_FOUND | productId does not exist |
| 409 | OUT_OF_STOCK | Insufficient inventory |
| 422 | ADDRESS_INVALID | Shipping address not usable |
| 429 | RATE_LIMITED | Too many requests |
```

---

## 8. ADR Template (short form)

```markdown
# ADR NNNN: [Short Title]

**Status**: Proposed | Accepted | Deprecated | Superseded by ADR-XXXX
**Date**: YYYY-MM-DD
**Deciders**: [@person1, @person2]

## Context

[What forces are at play? What problem are we solving?]

## Decision

[What did we decide? Be specific and verifiable.]

## Alternatives Considered

- **Option A**: [summary] -- rejected because [reason]
- **Option B**: [summary] -- rejected because [reason]

## Consequences

**Positive**:
- [outcome]

**Negative / Trade-offs**:
- [outcome]

**Follow-up**:
- [action item or re-evaluation trigger]
```

---

## 9. Style Cheat Sheet

| Do | Don't |
|---|---|
| "Run `npm install`" | "You should probably run npm install" |
| "Returns a 404" | "Will return a 404" |
| "Use X for Y" | "X could potentially be used for Y" |
| Code block with realistic data | Code block with `foo`, `bar`, `baz` |
| Link once, inline the rest | "See [link]" then describe it anyway |
