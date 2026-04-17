# Schema Patterns & Optimization

Deep-dive reference for database design. The SKILL.md gives the workflow;
this file gives the detailed patterns.

---

## 1. Normalization vs Denormalization

### Normalization (default)

| Form | Rule |
|---|---|
| 1NF | Atomic values, no repeating groups |
| 2NF | 1NF + no partial dependencies on composite keys |
| 3NF | 2NF + no transitive dependencies |
| BCNF | 3NF + every determinant is a candidate key |

**Default**: Start at 3NF. It keeps data consistent and integrity strong.

### When to Denormalize

- Read-heavy workload where joins cost more than storage
- Historical snapshots that should not change when source updates (invoices, audit logs)
- Pre-computed aggregates for dashboards (materialized views are better if supported)
- Caching frequently-joined lookups (with invalidation plan)

**Rule**: Denormalize late. Measure pain first.

---

## 2. Primary Key Strategy

| PK Type | Pros | Cons | Best For |
|---|---|---|---|
| `BigSerial` / `BigInt identity` | Compact, sequential, index-friendly | Leaks record count, predictable | Internal systems |
| UUID v4 (random) | Unguessable, distributable | Bad index locality, bigger | Public IDs |
| UUID v7 (time-sortable) | Unguessable + good index locality | Newer, less tooling | Modern public IDs |
| ULID | Sortable, URL-safe | Slightly less adoption | Distributed systems |
| Natural key (email, slug) | Human-readable | Changes cascade everywhere | Rarely a good idea |

**Default**: `BigSerial` for internal keys, expose UUID v7 for public-facing IDs.

---

## 3. Common Column Patterns

### Audit Fields (add to every table)

```sql
created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
created_by  BIGINT REFERENCES users(id)
updated_by  BIGINT REFERENCES users(id)
```

Use a trigger to keep `updated_at` current:

```sql
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION set_updated_at();
```

### Soft Delete

```sql
deleted_at  TIMESTAMPTZ NULL
```

Add a partial index to exclude deleted rows from most queries:

```sql
CREATE INDEX idx_users_active ON users (email) WHERE deleted_at IS NULL;
```

**Warning**: Soft delete adds complexity to every query. Only use if you need
audit trails or undo. Hard delete + event log is often cleaner.

### Multi-Tenancy

Three models:

| Model | Isolation | Cost | Use When |
|---|---|---|---|
| Database-per-tenant | Strong | High | Regulated, large tenants |
| Schema-per-tenant | Medium | Medium | Tens of tenants, schema drift risk |
| Shared tables + `tenant_id` column | Weak | Low | Many small tenants, default pattern |

For shared tables, **every query must filter by `tenant_id`**. Use Row-Level
Security (PostgreSQL) or a query wrapper to enforce it.

---

## 4. Indexing Deep-Dive

### Selectivity

High-selectivity columns (many unique values) are good index candidates.
Boolean columns are rarely worth indexing alone.

```
selectivity = unique_values / total_rows
  > 0.9  -> great index candidate
  < 0.1  -> probably not worth indexing alone (consider composite)
```

### Composite Index Column Order

Rule: equality filters first, range filters last.

```sql
-- Query: WHERE tenant_id = ? AND status = 'active' AND created_at > ?
CREATE INDEX idx_orders_tenant_status_created
ON orders (tenant_id, status, created_at);
```

### Covering Indexes

Include extra columns so the query plan can skip the table lookup:

```sql
CREATE INDEX idx_users_email_covering
ON users (email) INCLUDE (id, name);
```

### Partial Indexes

```sql
-- Only active users get indexed
CREATE INDEX idx_users_active_email
ON users (email) WHERE deleted_at IS NULL;
```

### When NOT to Index

- Tables with very few rows (<1000)
- Columns rarely used in WHERE/JOIN/ORDER BY
- Write-heavy tables where the index cost outweighs read benefit
- Columns with very low cardinality used alone

---

## 5. N+1 Detection & Fixes

### What It Looks Like

```typescript
const users = await db.user.findMany();
for (const user of users) {
  user.orders = await db.order.findMany({ where: { userId: user.id } }); // N queries
}
```

### Fix 1: JOIN

```typescript
const users = await db.user.findMany({ include: { orders: true } });
```

### Fix 2: Batch Load (dataloader pattern)

```typescript
const users = await db.user.findMany();
const orders = await db.order.findMany({
  where: { userId: { in: users.map(u => u.id) } }
});
// Group orders by userId in memory
```

### Fix 3: Window Function for "Top N per Group"

```sql
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) as rn
  FROM orders
) t WHERE rn <= 5;
```

---

## 6. Pagination

### Offset/Limit (simple but slow for deep pages)

```sql
SELECT * FROM orders ORDER BY created_at DESC LIMIT 20 OFFSET 1000;
-- Scans 1020 rows to return 20
```

### Keyset (cursor) Pagination (recommended)

```sql
-- First page
SELECT * FROM orders ORDER BY created_at DESC, id DESC LIMIT 20;

-- Next page (using last row's cursor)
SELECT * FROM orders
WHERE (created_at, id) < ($last_created_at, $last_id)
ORDER BY created_at DESC, id DESC LIMIT 20;
```

Constant time regardless of page depth.

---

## 7. Transactions & Isolation

### Isolation Levels

| Level | Prevents | Use For |
|---|---|---|
| Read Uncommitted | Nothing | Rarely used |
| Read Committed | Dirty reads | Default for most apps |
| Repeatable Read | + Non-repeatable reads | Reports, analytics |
| Serializable | + Phantom reads | Financial transactions |

### Transaction Rules

- Keep transactions short -- they hold locks
- Don't call external APIs inside a transaction
- Explicit transaction scope in code, not auto-commit surprises
- Handle serialization failures with retry (with backoff)

---

## 8. Connection Pooling

| Environment | Pool Strategy |
|---|---|
| Long-running server | Application-level pool (default 10-20 connections) |
| Serverless (Lambda, Cloud Run) | External pooler: PgBouncer, Neon pooled |
| Edge (Workers, Vercel Edge) | HTTP-based drivers (Neon HTTP, Supabase REST) |

**Rule**: Don't create a new pool per request. Serverless functions should use
an external pooler or HTTP-based driver.

---

## 9. Backup & Recovery

- Full backup daily, retention 30 days minimum
- Point-in-time recovery for critical data (PostgreSQL WAL archiving)
- Test restore quarterly -- an untested backup is no backup
- Store backups in a different region/account than the primary database
- Encrypt backups at rest

---

## 10. Schema Evolution Checklist

Before shipping a schema change:

- [ ] Migration has both `up` and `down`
- [ ] Backward compatible with currently-running application (if zero downtime)
- [ ] Indexes added alongside new query patterns
- [ ] Seed data still runs
- [ ] ER diagram updated in `production_artifacts/`
- [ ] Migration tested against a prod-sized dataset
- [ ] Rollback plan documented
