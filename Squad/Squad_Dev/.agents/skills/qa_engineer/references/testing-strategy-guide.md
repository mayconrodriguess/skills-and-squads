# Testing Strategy Guide

Deeper practices for building a test suite that scales with the product.

---

## 1. The Testing Pyramid (and Its Variants)

### Classic pyramid

```
Unit (70%) --> Integration (20%) --> E2E (10%)
```

Works for most backend services.

### Trophy (Frontend tilt)

```
Static (types + lint)
Unit
Integration (component)
E2E
```

Popular in the React ecosystem -- integration tests of components catch more
real bugs than isolated unit tests of hooks.

### Honeycomb (Microservices)

```
Unit < Integration (contract) > Implementation details
```

For service-heavy architectures, contract tests between services are often
more valuable than deep unit coverage.

**Rule**: The right shape depends on the architecture. Discuss and choose.

---

## 2. What Each Layer Tests

| Layer | Goal | Speed | Example |
|---|---|---|---|
| **Unit** | A function or class in isolation | ms | Pure functions, domain logic, reducers |
| **Integration** | Two or more units together, possibly touching DB/HTTP | s | Repository + DB, Controller + Service |
| **Contract** | Two services agree on schema | s | Consumer-driven Pact |
| **E2E** | A critical user flow through the real system | 10s-mins | Checkout, signup, payment |
| **Smoke** | System boots and critical endpoints respond | s | After every deploy |
| **Load** | System holds under expected + peak traffic | minutes | Before major launches |

---

## 3. What to Test First (Coverage Priority)

1. **Business rules in the domain** -- where bugs are most expensive
2. **Auth and authorization** -- security-critical
3. **Payment / financial flows** -- money-critical
4. **Data integrity** -- FK constraints, uniqueness, transactions
5. **Boundary validation** -- input sanitization, schema validation
6. **Error paths** -- what should happen when things fail
7. **Happy path** of each public endpoint
8. **Edge cases** -- empty, null, max, min, unicode, timezone

Unmeasured branches become production bugs. Track branch coverage, not just line.

---

## 4. Test Doubles

| Type | Use |
|---|---|
| **Stub** | Returns canned data, no behavior check |
| **Mock** | Verifies calls were made with expected args |
| **Fake** | Working implementation with a shortcut (in-memory DB) |
| **Spy** | Wraps a real function to observe calls |

### When to use a real dependency vs a double

| Use Real | Use Double |
|---|---|
| Pure function | External HTTP API |
| In-process DB (SQLite, Postgres Testcontainers) | Flaky third-party service |
| Domain objects | Payment provider |
| Fast deterministic library | Slow filesystem / network |

**Prefer real dependencies when cheap.** Over-mocking tests the mocks, not the code.

---

## 5. Fixtures & Factories

### Factory pattern beats fixture files

```typescript
// Factory
export const makeUser = (overrides: Partial<User> = {}): User => ({
  id: 'usr_' + randomId(),
  email: 'test@example.com',
  name: 'Test User',
  createdAt: new Date('2025-01-01'),
  ...overrides,
});

// In test
const admin = makeUser({ role: 'admin' });
```

Benefits:
- Each test states only what matters
- Schema changes update one place
- Obvious what's default vs. test-specific

---

## 6. Database Testing

### Strategies

| Strategy | Pros | Cons |
|---|---|---|
| Transaction rollback per test | Fast, isolated | DB must support |
| Truncate per test | Works anywhere | Slower |
| Testcontainers (real Postgres in Docker) | Real behavior | Slower boot |
| In-memory (SQLite shim) | Fastest | Different semantics from Postgres |

**Recommendation**: Testcontainers for integration, transaction rollback for unit.

---

## 7. HTTP / API Testing

### Integration tests

Spin up the real server in-process:

```typescript
import { app } from '../src/server';
import request from 'supertest';

it('creates an order', async () => {
  const res = await request(app)
    .post('/api/v1/orders')
    .set('Authorization', `Bearer ${token}`)
    .send({ items: [{ productId: 'p1', quantity: 2 }] });

  expect(res.status).toBe(201);
  expect(res.body.data.id).toMatch(/^ord_/);
});
```

### Contract tests (Pact)

For services that call each other, Pact lets the consumer declare its
expectations; the provider verifies it doesn't break them.

---

## 8. E2E Testing

### Tools

| Tool | Use |
|---|---|
| **Playwright** | Web, modern, fast, parallel |
| **Cypress** | Web, good DX, can't multi-tab |
| **Detox** | React Native |
| **Maestro** | Native mobile, YAML flows |

### Rules

- Test user-visible outcomes, not implementation
- Use data attributes for selection (`data-testid="submit"`)
- Seed the DB deterministically in `beforeAll`
- Run on CI in parallel shards
- Keep count low -- 10-30 E2Es is plenty; more than that = flaky suite

---

## 9. Avoiding Flakiness

| Cause | Fix |
|---|---|
| Race with async state | `await` correctly, avoid sleeps |
| Shared state | Reset between tests (transactions, beforeEach) |
| Random data (unseeded) | Seeded random, fixed dates |
| Real network | Mock external calls |
| Browser autocomplete | Use fresh browser contexts |
| Timezone | Fix TZ in CI |
| Clock | Freeze with `vi.useFakeTimers()` |

---

## 10. Mutation Testing

Covers the gap coverage metrics miss: **do the assertions actually catch bugs?**

Tools: **Stryker** (JS/TS), **mutmut** (Python), **PIT** (Java).

Mutation score > 60% is a strong signal of meaningful tests.

Run it periodically, not on every commit (slow).

---

## 11. CI Integration

- Run unit + integration on every PR (< 5 min total)
- Run E2E on PR to main + nightly
- Fail the PR on coverage regression (relative, not absolute)
- Upload coverage to Codecov / Coveralls
- Surface failures inline (GitHub Annotations)

---

## 12. When to Delete a Test

Yes, tests can be deleted. Delete if:

- Duplicates another test's assertion
- Tests implementation details (brittleness > value)
- Tests a feature that was removed
- Is permanently flaky with no fix in sight (quarantine first, delete later)

Never delete a test because it's failing. Fix the code or fix the test.

---

## 13. Documentation via Tests

A good test suite is the **living specification**. Name tests in business
language:

```typescript
describe('Checkout', () => {
  describe('when all items are in stock', () => {
    it('creates a paid order');
    it('sends a confirmation email within 2 minutes');
    it('decrements inventory atomically');
  });

  describe('when an item is out of stock', () => {
    it('returns 409 OUT_OF_STOCK');
    it('does not charge the card');
  });
});
```

A new hire can read the describe blocks and understand the domain.
