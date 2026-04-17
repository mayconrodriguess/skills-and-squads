# API Design Guide

Deep-dive reference for REST, GraphQL, and tRPC patterns.

---

## 1. API Style Decision Tree

```
Is the API consumed by external/public clients?
  YES --> REST (widest compatibility, cacheable, well-understood)
    Does the client need flexible querying over deeply nested data?
      YES --> Consider GraphQL alongside REST
      NO  --> REST is sufficient
  NO --> Internal API
    Is the entire stack TypeScript (monorepo)?
      YES --> tRPC (full type safety, zero code generation)
      NO  --> REST or GraphQL depending on query complexity
```

### Comparison Table

| Dimension | REST | GraphQL | tRPC |
|---|---|---|---|
| Type safety | Manual (OpenAPI codegen) | Schema-based (codegen) | Automatic (zero codegen) |
| Overfetching | Common | Solved | Solved |
| Caching | HTTP cache built-in | Complex (needs persisted queries) | App-level only |
| Learning curve | Low | Medium | Low (if you know TS) |
| Tooling maturity | Excellent | Good | Growing |
| File uploads | Native (multipart) | Needs workarounds | Needs workarounds |
| Real-time | WebSocket/SSE separate | Subscriptions built-in | Subscriptions via adapter |
| Public API suitability | Excellent | Good | Poor (TS-only clients) |

---

## 2. REST Patterns

### Resource Naming

| Pattern | Example | Rule |
|---|---|---|
| Collection | `GET /api/v1/users` | Plural nouns |
| Single resource | `GET /api/v1/users/:id` | Singular by ID |
| Nested resource | `GET /api/v1/users/:id/orders` | Max 2 levels deep |
| Action (non-CRUD) | `POST /api/v1/orders/:id/cancel` | Verb only when CRUD doesn't fit |
| Search/filter | `GET /api/v1/users?role=admin&status=active` | Query params for filtering |

### HTTP Methods

| Method | Idempotent | Safe | Request Body | Use For |
|---|---|---|---|---|
| GET | Yes | Yes | No | Read resources |
| POST | No | No | Yes | Create resources, trigger actions |
| PUT | Yes | No | Yes | Full replacement of a resource |
| PATCH | Yes | No | Yes | Partial update |
| DELETE | Yes | No | Optional | Remove a resource |

### Envelope Response Format

```typescript
// Success with data
{
  "status": "success",
  "data": { "id": "abc", "name": "Alice" },
  "meta": { "requestId": "req-123" }
}

// Success with collection
{
  "status": "success",
  "data": [{ "id": "abc" }, { "id": "def" }],
  "meta": {
    "page": 1,
    "pageSize": 20,
    "totalItems": 142,
    "totalPages": 8
  }
}

// Error
{
  "status": "error",
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Request validation failed",
    "details": [
      { "field": "email", "message": "Must be a valid email address" }
    ]
  },
  "meta": { "requestId": "req-124" }
}
```

### Pagination Patterns

| Pattern | Pros | Cons | Use When |
|---|---|---|---|
| Offset (`?page=2&pageSize=20`) | Simple, supports jump-to-page | Slow on large datasets, inconsistent on inserts | Admin panels, small datasets |
| Cursor (`?cursor=abc&limit=20`) | Consistent, performant | No jump-to-page, complex | Feeds, infinite scroll, large datasets |
| Keyset (`?after_id=123&limit=20`) | Fast with index | Tied to sort column | Time-series, log data |

### Filtering, Sorting, Field Selection

```
# Filter
GET /api/v1/products?category=electronics&price_min=100&price_max=500

# Sort (prefix with - for descending)
GET /api/v1/products?sort=-created_at,name

# Field selection (reduce payload)
GET /api/v1/products?fields=id,name,price
```

---

## 3. Authentication Patterns

### Pattern Selection

| Pattern | Use When | Avoid When |
|---|---|---|
| JWT (access + refresh) | SPAs, mobile apps, stateless backends | Need instant token revocation |
| Session cookies | Server-rendered apps, same-domain | Cross-domain, mobile apps |
| API keys | Server-to-server, CLI tools | End-user authentication |
| OAuth 2.0 / OIDC | Third-party login, enterprise SSO | Simple internal tools |

### JWT Best Practices

- Access token: short-lived (15 min)
- Refresh token: longer-lived (7-30 days), stored in httpOnly cookie
- Include only essential claims (sub, role) -- not sensitive data
- Validate `iss`, `aud`, `exp` on every request
- Use asymmetric keys (RS256/ES256) for multi-service architectures

### Auth Middleware Pattern

```typescript
// middleware/auth.ts
export function requireAuth(roles?: string[]) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const token = extractBearerToken(req);
    if (!token) throw new UnauthorizedError('Missing auth token');

    const payload = await verifyToken(token);
    if (roles && !roles.includes(payload.role)) {
      throw new ForbiddenError('Insufficient permissions');
    }

    req.user = payload;
    next();
  };
}

// Usage in routes
router.get('/admin/users', requireAuth(['admin']), adminController.listUsers);
router.get('/profile', requireAuth(), userController.getProfile);
```

---

## 4. Rate Limiting

### Strategy

| Endpoint Type | Limit | Window | Action on Exceed |
|---|---|---|---|
| Login / auth | 5 requests | 15 min | 429 + exponential backoff hint |
| Password reset | 3 requests | 1 hour | 429 + silent (don't reveal user exists) |
| API general | 100 requests | 1 min | 429 + `Retry-After` header |
| Expensive operations | 10 requests | 1 min | 429 + queue suggestion |
| Webhooks (incoming) | 1000 requests | 1 min | 429 + log for review |

### Implementation

```typescript
// Using a sliding window with Redis (or in-memory for small apps)
import rateLimit from 'express-rate-limit';

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 5,
  standardHeaders: true,       // Return rate limit info in headers
  legacyHeaders: false,
  message: { status: 'error', error: { code: 'RATE_LIMITED', message: 'Too many attempts' } },
});

app.use('/api/v1/auth', authLimiter);
```

---

## 5. API Versioning

### Strategy Selection

| Strategy | Implementation | Use When |
|---|---|---|
| URL path | `/api/v1/users`, `/api/v2/users` | Public API, clear breakpoints |
| Header | `Accept-Version: 1` or `API-Version: 2024-01-01` | Internal, clean URLs |
| Query param | `?version=1` | Quick prototyping (not recommended for production) |
| No versioning | Single version, frequent deploys | tRPC, internal with aligned deploy cycles |

### Breaking vs Non-Breaking Changes

| Non-Breaking (no version bump) | Breaking (requires new version) |
|---|---|
| Adding new fields to response | Removing or renaming fields |
| Adding new optional query params | Changing field types |
| Adding new endpoints | Changing URL structure |
| Adding new enum values | Removing enum values |
| Deprecation notices | Changing auth mechanism |

---

## 6. API Documentation (OpenAPI)

### Minimum Requirements

- Every endpoint has a summary and description
- Request/response schemas are defined (auto-generated from Zod when possible)
- Error responses are documented
- Authentication requirements are specified per endpoint
- Examples are provided for complex payloads

### Zod-to-OpenAPI Pattern

```typescript
import { createDocument } from 'zod-openapi';

// Define schemas once, use for validation AND documentation
const UserSchema = z.object({
  id: z.string().uuid().openapi({ description: 'Unique user identifier' }),
  email: z.string().email(),
  role: z.enum(['user', 'admin']),
  createdAt: z.string().datetime(),
});
```

### Documentation Hosting

- **Scalar** or **Swagger UI** at `/docs` in development
- **Redocly** for polished public documentation
- Auto-generate client SDKs from the OpenAPI spec when needed

---

## 7. GraphQL Considerations

When GraphQL is chosen:

| Practice | Detail |
|---|---|
| Schema-first vs code-first | Use code-first with TypeGraphQL or Pothos for type safety |
| Query depth limiting | Set max depth (usually 5-7) to prevent abuse |
| Query complexity analysis | Assign cost to fields, reject expensive queries |
| DataLoader | Mandatory for N+1 prevention in resolvers |
| Persisted queries | Use in production to prevent arbitrary query execution |
| Error handling | Use union types for expected errors, extensions for unexpected |

---

## 8. tRPC Considerations

When tRPC is chosen:

| Practice | Detail |
|---|---|
| Router organization | One router per domain (`userRouter`, `orderRouter`) |
| Middleware | Use tRPC middleware for auth, logging, rate limiting |
| Input validation | Built-in Zod integration -- use it everywhere |
| Error handling | Use `TRPCError` with appropriate codes |
| Subscriptions | Use WebSocket adapter for real-time needs |
| Testing | Test procedures directly without HTTP layer |
