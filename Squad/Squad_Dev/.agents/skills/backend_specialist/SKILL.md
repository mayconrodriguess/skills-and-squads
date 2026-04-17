---
name: backend-specialist
description: >
  Backend architecture, API design, and server-side implementation specialist.
  TRIGGERS: api, rest, graphql, trpc, endpoint, route, controller, service,
  repository, middleware, auth, authentication, authorization, jwt, oauth,
  validation, zod, valibot, error handling, status code, rate limiting,
  hono, fastify, express, nestjs, node, runtime, server, backend, microservice,
  clean code, refactor, layered architecture, dependency injection,
  async, promise, streaming, websocket, cors, helmet, openapi, swagger,
  versioning, envelope pattern, guard clause, srp, dry, kiss, yagni
---

# Backend Specialist

## Objective

Build production-grade server-side systems from approved architecture artifacts.
Every decision -- framework, patterns, error strategy, API style -- must trace
back to `production_artifacts/` documents. When no artifact exists yet, propose
and document the decision before writing code.

---

## 1. Project Structure Contract

All output lands in predictable locations:

| Folder | Purpose |
|---|---|
| `production_artifacts/` | Approved specs, architecture docs, API contracts |
| `app_build/` | All backend source: `src/`, tests, config, `package.json` |
| `app_build/src/` | Layered code: `controllers/`, `services/`, `repositories/`, `middleware/`, `utils/` |
| `scripts/` | Migrations, seeds, smoke tests, code generators |
| `references/` | Deep-dive guides (see Bundled Reference below) |
| `.agents/skills/`, `.agents/workflows/` | Only when backend handoffs will be reused |

### Canonical `app_build/src/` Layout

```
app_build/src/
  index.ts              # Entry point -- bootstraps server
  config/
    env.ts              # Single source for env vars (validated with Zod)
    index.ts
  controllers/          # HTTP layer -- parse request, call service, format response
  services/             # Business logic -- orchestrates repositories + external calls
  repositories/         # Data access -- DB queries, ORM calls
  middleware/           # Auth, logging, error handler, rate limiter, CORS
  routes/               # Route definitions (separated from controllers)
  validators/           # Zod/Valibot schemas for request/response
  errors/               # Custom error classes + centralized handler
  types/                # Shared TypeScript types and interfaces
  utils/                # Pure helper functions
```

---

## 2. Required Inputs

| Document | Required | Purpose |
|---|---|---|
| `production_artifacts/Technical_Specification.md` | YES | Features, constraints, NFRs |
| `production_artifacts/Solution_Architecture.md` | YES | Stack decisions, diagrams |
| `production_artifacts/Tech_Stack_Rationale.md` | When present | Why each tool was chosen |
| `production_artifacts/API_Contract.md` | When present | Endpoint definitions |

If documents conflict, follow the **latest approved artifact** and flag the
conflict in a code comment + PR description.

---

## 3. Framework Selection Decision Tree

Choose based on project needs -- never default to a favorite:

| Criteria | Hono | Fastify | Express | NestJS |
|---|---|---|---|---|
| Edge/serverless-first | Best choice | Good | Avoid | Avoid |
| Raw performance matters | Excellent | Excellent | Adequate | Adequate |
| Minimal API / microservice | Best choice | Good | Good | Overkill |
| Large team / enterprise patterns | Avoid | Good | Avoid | Best choice |
| Existing Express middleware needed | Avoid | Partial compat | Best choice | Built-in |
| Full DI + decorators wanted | No | No | No | Best choice |
| Multi-runtime (Node, Deno, Bun, CF Workers) | Best choice | Node only | Node only | Node only |

### Runtime Considerations

- **Node 22+**: Native TypeScript stripping (`--experimental-strip-types`), no build step for dev
- **Bun**: Fast startup, built-in test runner, SQLite driver -- good for prototyping
- **Deno 2**: Built-in TS, secure by default, npm compat -- consider for greenfield
- Always pin the runtime version in `.nvmrc` or `package.json > engines`

---

## 4. Workflow

### Phase 1: Analyze

1. Read architecture artifacts and identify: runtime, framework, persistence,
   auth approach, API style, deployment target.
2. Check for an existing `app_build/` -- if it exists, understand its structure
   before modifying.
3. Identify external dependencies and integration points.

### Phase 2: Scaffold

4. Create the layered folder structure under `app_build/src/`.
5. Set up environment validation (`config/env.ts`) using Zod:
   ```typescript
   // Every env var is validated at startup -- fail fast
   const envSchema = z.object({
     PORT: z.coerce.number().default(3000),
     DATABASE_URL: z.string().url(),
     JWT_SECRET: z.string().min(32),
     NODE_ENV: z.enum(['development', 'staging', 'production']).default('development'),
   });
   export const env = envSchema.parse(process.env);
   ```

### Phase 3: Implement

6. **Controllers**: Thin -- parse input, call service, return response. No business logic.
7. **Services**: All business logic lives here. Orchestrate repositories and external APIs.
8. **Repositories**: Data access only. Return domain objects, not raw DB rows.
9. **Validators**: Define request/response schemas at the boundary.
10. **Error handling**: Centralized middleware (see Error Strategy below).
11. **Middleware**: Auth, CORS, rate limiting, request logging.

### Phase 4: Verify

12. Run the readiness checklist (see Bundled Reference).
13. Add or update tests alongside implementation.
14. Place repeatable helpers in `scripts/` (not ad hoc terminal commands).

---

## 5. API Design Patterns

### Style Selection

| Style | When to Use | When to Avoid |
|---|---|---|
| REST | Public APIs, CRUD-heavy, broad client base | Complex nested queries |
| GraphQL | Mobile-first, client-driven queries, multiple frontends | Simple CRUD, small team |
| tRPC | Full-stack TypeScript monorepo, type safety end-to-end | Non-TS clients, public API |

### REST Response Format (Envelope Pattern)

Always wrap responses in a consistent envelope:

```typescript
// Success
{ "status": "success", "data": { ... }, "meta": { "page": 1, "total": 42 } }

// Error
{ "status": "error", "error": { "code": "VALIDATION_FAILED", "message": "...", "details": [...] } }
```

### Versioning Strategy

| Method | Use When |
|---|---|
| URL path (`/api/v1/`) | Public APIs, clear separation needed |
| Header (`Accept-Version: 1`) | Internal APIs, want clean URLs |
| No versioning | Internal tRPC, frequent deploys, no external consumers |

### HTTP Status Codes -- Quick Reference

| Code | Meaning | Use For |
|---|---|---|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST that creates a resource |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation failures |
| 401 | Unauthorized | Missing or invalid auth token |
| 403 | Forbidden | Valid auth but insufficient permissions |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Duplicate resource, version conflict |
| 422 | Unprocessable | Business rule violation |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Error | Unexpected server failure |

---

## 6. Error Handling Strategy

### Custom Error Classes

```typescript
// errors/AppError.ts
export class AppError extends Error {
  constructor(
    public readonly statusCode: number,
    public readonly code: string,
    message: string,
    public readonly details?: unknown,
  ) {
    super(message);
    this.name = 'AppError';
  }
}

export class ValidationError extends AppError {
  constructor(details: unknown) {
    super(400, 'VALIDATION_FAILED', 'Request validation failed', details);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(404, 'NOT_FOUND', `${resource} with id ${id} not found`);
  }
}
```

### Centralized Error Middleware

```typescript
// middleware/errorHandler.ts
function errorHandler(err: Error, req: Request, res: Response, next: NextFunction) {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      status: 'error',
      error: { code: err.code, message: err.message, details: err.details },
    });
  }
  // Unknown errors: log full stack, return generic message
  logger.error('Unhandled error', { error: err, requestId: req.id });
  return res.status(500).json({
    status: 'error',
    error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' },
  });
}
```

### Rules

- NEVER expose stack traces or internal details in production responses.
- ALWAYS log the full error server-side with request context.
- Validation errors include field-level detail; business errors include a human-readable message.
- Use `try/catch` in controllers; let the centralized handler catch everything else.

---

## 7. Async Patterns

| Pattern | Use When | Risk |
|---|---|---|
| `await` sequential | Operations depend on each other | Slow if independent |
| `Promise.all()` | All must succeed, all independent | One failure rejects all |
| `Promise.allSettled()` | Need all results even if some fail | Must check each status |
| `Promise.race()` | First response wins (timeout, fallback) | Losers keep running |
| `for await...of` | Streaming data, backpressure needed | Memory if not consumed |

**Rule**: Default to `Promise.allSettled()` for batch operations. Use `Promise.all()` only when
a single failure should abort everything.

---

## 8. Validation at Boundaries

- Validate ALL external input: request body, query params, path params, headers.
- Use Zod (default) or Valibot (when bundle size matters).
- Validate at the controller/route level -- services trust their input.
- Transform data during validation (trim strings, coerce numbers).

```typescript
// validators/user.ts
export const createUserSchema = z.object({
  email: z.string().email().trim().toLowerCase(),
  name: z.string().min(2).max(100).trim(),
  role: z.enum(['user', 'admin']).default('user'),
});
```

---

## 9. Security Checklist

| Area | Requirement |
|---|---|
| Secrets | Environment variables only. Never in code, never in git |
| Auth | JWT with short expiry + refresh tokens, or session-based |
| Input | Validate and sanitize all external input |
| SQL | Parameterized queries or ORM -- never string concatenation |
| CORS | Explicit origin whitelist, no `*` in production |
| Headers | Use `helmet` or equivalent for security headers |
| Rate limiting | Apply to auth endpoints and expensive operations |
| Dependencies | `npm audit` clean, no `*` versions in package.json |
| Logging | Never log secrets, tokens, passwords, or PII |

---

## 10. Clean Code Rules

These are non-negotiable in every file:

| Rule | Detail |
|---|---|
| SRP | One reason to change per function/class/module |
| DRY | Extract when duplicated 3+ times (not before) |
| KISS | Simplest solution that meets requirements |
| YAGNI | Don't build features nobody asked for |
| Functions | Max ~20 lines, 0-2 parameters preferred, 3 max |
| Naming | Verb for functions (`getUserById`), noun for variables (`userList`) |
| Guard clauses | Return early for invalid states -- flat > nested |
| No magic values | Extract to named constants |
| Before editing | Check who depends on the code you are changing |

---

## 11. Quality Bar

Before marking any backend task as done:

- [ ] Runtime and framework match the approved architecture
- [ ] Layered architecture: controllers are thin, business logic is in services
- [ ] All external input is validated at the boundary
- [ ] Errors are centralized and return the envelope format
- [ ] Auth and authorization follow the approved model
- [ ] Database access uses parameterized queries or ORM
- [ ] Environment variables are validated at startup
- [ ] No secrets in code or git
- [ ] Security headers and CORS are configured
- [ ] Tests exist for critical paths
- [ ] API documentation (OpenAPI or equivalent) exists for public endpoints
- [ ] Runnable dev path: `npm install && npm run dev` works

---

## 12. Bundled Reference

Deep-dive guides live in `references/` -- consult them for detailed patterns:

| File | Contents |
|---|---|
| [references/backend-readiness-checklist.md](references/backend-readiness-checklist.md) | Pre-completion verification checklist |
| [references/api-design-guide.md](references/api-design-guide.md) | REST, GraphQL, tRPC patterns, auth, rate limiting, OpenAPI |
| [references/nodejs-patterns.md](references/nodejs-patterns.md) | Async patterns, validation recipes, error handling deep-dive |
