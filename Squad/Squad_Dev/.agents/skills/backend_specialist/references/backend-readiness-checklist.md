# Backend Readiness Checklist

Run through every item before marking a backend task as complete.

## Architecture Alignment

- [ ] Runtime matches approved spec (Node version pinned in `.nvmrc` or `engines`)
- [ ] Framework matches approved spec (no surprise swaps)
- [ ] Folder structure follows the layered convention (`controllers/`, `services/`, `repositories/`)
- [ ] Entry point boots cleanly (`npm run dev` works without manual steps)

## Configuration & Environment

- [ ] All env vars are validated at startup with Zod/Valibot (fail fast)
- [ ] No secrets hardcoded in source files
- [ ] `.env.example` exists with all required variables (no values)
- [ ] `NODE_ENV` is respected (dev vs staging vs production behavior)

## Input Validation

- [ ] Every external input (body, query, params, headers) is validated
- [ ] Validation happens at the controller/route boundary, not deep in services
- [ ] Validation errors return 400 with field-level detail
- [ ] Data is transformed during validation (trim, lowercase emails, coerce types)

## Error Handling

- [ ] Centralized error handler middleware exists
- [ ] All responses use the envelope format (`{ status, data/error }`)
- [ ] Custom error classes for common cases (NotFound, Validation, Unauthorized)
- [ ] Unknown errors return 500 with generic message (no stack trace in production)
- [ ] All errors are logged server-side with request context

## Authentication & Authorization

- [ ] Auth follows the approved model (JWT, session, OAuth, API key)
- [ ] Protected routes use auth middleware
- [ ] Authorization checks exist (role/permission-based where needed)
- [ ] Token expiry and refresh are handled
- [ ] Failed auth returns 401 (missing) or 403 (insufficient)

## Database Access

- [ ] All queries use parameterized statements or ORM
- [ ] No raw string concatenation in SQL
- [ ] Connection pooling is configured
- [ ] Transactions are used for multi-step writes
- [ ] N+1 query patterns are avoided (see database specialist)

## Security

- [ ] CORS configured with explicit origin whitelist
- [ ] Security headers set (`helmet` or equivalent)
- [ ] Rate limiting on auth and expensive endpoints
- [ ] `npm audit` passes with no critical/high vulnerabilities
- [ ] No `*` versions in `package.json`
- [ ] Logging never includes secrets, tokens, or PII

## Code Quality

- [ ] Functions are under ~20 lines with 0-2 parameters
- [ ] Guard clauses used instead of deep nesting
- [ ] No magic numbers/strings -- constants are named
- [ ] Business logic is in services, not controllers
- [ ] Shared logic is extracted to utils (DRY after 3+ duplications)

## Testing

- [ ] Critical path tests exist (happy path + main error cases)
- [ ] Tests can run without external services (mocked or in-memory DB)
- [ ] Test commands are documented in `package.json` scripts

## Documentation

- [ ] API endpoints are documented (OpenAPI spec, Postman collection, or inline)
- [ ] README or spec describes how to run, test, and deploy
- [ ] Architecture decisions are captured in `production_artifacts/`

## Deployment Readiness

- [ ] Health check endpoint exists (`GET /health`)
- [ ] Graceful shutdown handles in-flight requests
- [ ] Logging is structured (JSON) for production
- [ ] Build step produces clean output (no dev dependencies in production)
