# Node.js Patterns Reference

Deep-dive patterns for async, validation, error handling, and production readiness.

---

## 1. Async Patterns

### Pattern Selection Guide

```
Are the operations independent of each other?
  NO  --> Sequential await (each step needs the previous result)
  YES --> Do ALL operations need to succeed?
    YES --> Promise.all() -- fail fast on first rejection
    NO  --> Promise.allSettled() -- collect all results regardless
      Need only the fastest result?
        YES --> Promise.race() -- first to settle wins
```

### Sequential (Dependent Operations)

```typescript
async function createOrder(dto: CreateOrderDTO) {
  const user = await userRepo.findById(dto.userId);       // Need user first
  const inventory = await inventoryService.reserve(dto.items); // Need to reserve
  const order = await orderRepo.create({ user, inventory });   // Then create
  await notificationService.send(user.email, order);           // Then notify
  return order;
}
```

### Promise.all (All Must Succeed)

```typescript
// Good: independent fetches that all must succeed
async function getDashboardData(userId: string) {
  const [profile, orders, notifications] = await Promise.all([
    userService.getProfile(userId),
    orderService.getRecent(userId),
    notificationService.getUnread(userId),
  ]);
  return { profile, orders, notifications };
}
```

### Promise.allSettled (Partial Failure OK)

```typescript
// Good: batch operations where some may fail
async function sendBulkNotifications(userIds: string[]) {
  const results = await Promise.allSettled(
    userIds.map(id => notificationService.send(id))
  );

  const succeeded = results.filter(r => r.status === 'fulfilled').length;
  const failed = results
    .filter((r): r is PromiseRejectedResult => r.status === 'rejected')
    .map(r => r.reason);

  logger.info(`Notifications: ${succeeded} sent, ${failed.length} failed`);
  if (failed.length > 0) logger.warn('Failed notifications', { errors: failed });

  return { succeeded, failed: failed.length };
}
```

### Promise.race (Timeout Pattern)

```typescript
async function fetchWithTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  const timeout = new Promise<never>((_, reject) =>
    setTimeout(() => reject(new Error(`Timeout after ${ms}ms`)), ms)
  );
  return Promise.race([promise, timeout]);
}

// Usage
const data = await fetchWithTimeout(externalApi.getData(), 5000);
```

### Streaming with Async Iterators

```typescript
// Processing large datasets without loading everything into memory
async function processLargeExport(query: QueryParams) {
  const stream = db.query(query).stream();

  for await (const row of stream) {
    await processRow(row); // Backpressure is handled automatically
  }
}
```

### Common Async Mistakes

| Mistake | Problem | Fix |
|---|---|---|
| `await` in a loop | Sequential when parallel is possible | Use `Promise.all()` or `Promise.allSettled()` |
| Unhandled rejection | Process crash (Node 18+) | Always catch or use error middleware |
| Fire and forget | Lost errors, unpredictable timing | Await or explicitly handle with `.catch()` |
| Missing `AbortController` | Can't cancel long operations | Pass signal to fetch/DB calls |
| Blocking the event loop | Frozen server | Offload CPU-heavy work to worker threads |

---

## 2. Validation Patterns

### Zod Recipes

```typescript
import { z } from 'zod';

// ---- Primitive transforms ----
const Email = z.string().email().trim().toLowerCase();
const NonEmptyString = z.string().min(1).trim();
const PositiveInt = z.coerce.number().int().positive();
const UUID = z.string().uuid();

// ---- Object with defaults ----
const PaginationQuery = z.object({
  page: z.coerce.number().int().min(1).default(1),
  pageSize: z.coerce.number().int().min(1).max(100).default(20),
  sort: z.string().optional(),
  order: z.enum(['asc', 'desc']).default('desc'),
});

// ---- Discriminated union ----
const PaymentMethod = z.discriminatedUnion('type', [
  z.object({ type: z.literal('credit_card'), cardNumber: z.string(), cvv: z.string() }),
  z.object({ type: z.literal('pix'), pixKey: z.string() }),
  z.object({ type: z.literal('boleto') }), // no extra fields
]);

// ---- Refinement (custom validation) ----
const DateRange = z.object({
  startDate: z.coerce.date(),
  endDate: z.coerce.date(),
}).refine(
  data => data.endDate > data.startDate,
  { message: 'endDate must be after startDate', path: ['endDate'] }
);

// ---- Transform (derive fields) ----
const CreateUserInput = z.object({
  email: Email,
  name: NonEmptyString,
}).transform(data => ({
  ...data,
  slug: data.name.toLowerCase().replace(/\s+/g, '-'),
}));

// ---- Infer types from schemas ----
type CreateUserDTO = z.infer<typeof CreateUserInput>;
// Result: { email: string; name: string; slug: string }
```

### Valibot (When Bundle Size Matters)

Use Valibot instead of Zod when:
- Frontend validation (tree-shakeable, ~10x smaller)
- Edge functions with strict size limits
- Shared validation schemas between client and server

```typescript
import * as v from 'valibot';

const UserSchema = v.object({
  email: v.pipe(v.string(), v.email(), v.trim(), v.toLowerCase()),
  age: v.pipe(v.number(), v.integer(), v.minValue(0)),
});
```

### Validation Middleware Pattern

```typescript
// middleware/validate.ts
import { ZodSchema, ZodError } from 'zod';

export function validate(schema: ZodSchema, source: 'body' | 'query' | 'params' = 'body') {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req[source]);
    if (!result.success) {
      throw new ValidationError(formatZodErrors(result.error));
    }
    req[source] = result.data; // Replace with parsed + transformed data
    next();
  };
}

function formatZodErrors(error: ZodError) {
  return error.issues.map(issue => ({
    field: issue.path.join('.'),
    message: issue.message,
    code: issue.code,
  }));
}

// Usage in routes
router.post('/users', validate(createUserSchema), userController.create);
router.get('/users', validate(paginationSchema, 'query'), userController.list);
```

---

## 3. Error Handling Deep-Dive

### Error Class Hierarchy

```typescript
// Base application error
export class AppError extends Error {
  public readonly isOperational: boolean;

  constructor(
    public readonly statusCode: number,
    public readonly code: string,
    message: string,
    public readonly details?: unknown,
    isOperational = true,
  ) {
    super(message);
    this.name = this.constructor.name;
    this.isOperational = isOperational;
    Error.captureStackTrace(this, this.constructor);
  }
}

// Specific errors
export class BadRequestError extends AppError {
  constructor(message = 'Bad request', details?: unknown) {
    super(400, 'BAD_REQUEST', message, details);
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Authentication required') {
    super(401, 'UNAUTHORIZED', message);
  }
}

export class ForbiddenError extends AppError {
  constructor(message = 'Insufficient permissions') {
    super(403, 'FORBIDDEN', message);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, id?: string) {
    super(404, 'NOT_FOUND', id ? `${resource} '${id}' not found` : `${resource} not found`);
  }
}

export class ConflictError extends AppError {
  constructor(message: string) {
    super(409, 'CONFLICT', message);
  }
}

export class ValidationError extends AppError {
  constructor(details: unknown) {
    super(422, 'VALIDATION_FAILED', 'Validation failed', details);
  }
}

export class RateLimitError extends AppError {
  constructor(retryAfterSeconds?: number) {
    super(429, 'RATE_LIMITED', 'Too many requests', { retryAfter: retryAfterSeconds });
  }
}
```

### Operational vs Programming Errors

| Type | Examples | Action |
|---|---|---|
| Operational | Invalid input, auth failure, timeout, DB constraint | Return appropriate HTTP error |
| Programming | TypeError, null reference, missing import | Log + return 500 + alert |

```typescript
// In the error handler middleware
if (err instanceof AppError && err.isOperational) {
  // Expected error -- return structured response
  return res.status(err.statusCode).json({ ... });
}

// Programming error -- this is a bug
logger.fatal('Programming error detected', { error: err });
// In production, you may want to restart the process
process.exitCode = 1;
```

### Async Error Wrapper

```typescript
// Wraps async route handlers to catch unhandled promise rejections
export function asyncHandler(fn: (req: Request, res: Response, next: NextFunction) => Promise<void>) {
  return (req: Request, res: Response, next: NextFunction) => {
    fn(req, res, next).catch(next);
  };
}

// Usage -- no try/catch needed in every controller
router.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await userService.getById(req.params.id);
  if (!user) throw new NotFoundError('User', req.params.id);
  res.json({ status: 'success', data: user });
}));
```

---

## 4. Logging Best Practices

### Structured Logging

```typescript
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: process.env.NODE_ENV === 'development'
    ? { target: 'pino-pretty' }
    : undefined, // JSON in production
  redact: ['req.headers.authorization', 'req.body.password', 'req.body.token'],
});
```

### Log Levels

| Level | When | Example |
|---|---|---|
| `fatal` | Process must exit | Unrecoverable DB connection failure |
| `error` | Operation failed, needs attention | Payment processing failed |
| `warn` | Unexpected but handled | Deprecated API version used |
| `info` | Normal operation milestones | Server started, user created |
| `debug` | Diagnostic detail | SQL query, cache hit/miss |
| `trace` | Very verbose | Full request/response bodies |

---

## 5. Graceful Shutdown

```typescript
async function gracefulShutdown(signal: string) {
  logger.info(`Received ${signal}. Starting graceful shutdown...`);

  // 1. Stop accepting new requests
  server.close();

  // 2. Wait for in-flight requests (with timeout)
  const shutdownTimeout = setTimeout(() => {
    logger.error('Forced shutdown after timeout');
    process.exit(1);
  }, 30_000);

  try {
    // 3. Close database connections
    await db.destroy();
    // 4. Close other resources (Redis, queues, etc.)
    await cache.disconnect();

    clearTimeout(shutdownTimeout);
    logger.info('Graceful shutdown complete');
    process.exit(0);
  } catch (err) {
    logger.error('Error during shutdown', { error: err });
    process.exit(1);
  }
}

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));
```

---

## 6. Health Check Endpoint

```typescript
router.get('/health', async (req, res) => {
  const checks = await Promise.allSettled([
    db.raw('SELECT 1'),           // Database
    cache.ping(),                  // Redis/cache
  ]);

  const healthy = checks.every(c => c.status === 'fulfilled');

  res.status(healthy ? 200 : 503).json({
    status: healthy ? 'healthy' : 'degraded',
    timestamp: new Date().toISOString(),
    checks: {
      database: checks[0].status === 'fulfilled' ? 'up' : 'down',
      cache: checks[1].status === 'fulfilled' ? 'up' : 'down',
    },
  });
});
```
