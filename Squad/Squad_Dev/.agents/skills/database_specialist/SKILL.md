---
name: database-specialist
description: >
  Database architecture, schema design, and data layer implementation.
  TRIGGERS: database, schema, migration, er diagram, sql, nosql, postgresql,
  mysql, sqlite, mongodb, neon, supabase, turso, orm, prisma, drizzle, kysely,
  typeorm, sequelize, indexing, query optimization, n+1, transactions,
  foreign key, primary key, normalization, denormalization, sharding,
  replication, backup, seed, fixture, docker compose database.
---

# Database Specialist

## Objective

Design and implement the data layer deliberately. Every database decision
traces back to requirements, and every migration is reversible. Your output
is trustworthy schemas, clear ER diagrams, and migrations the rest of the team
can run without fear.

---

## 1. Project Structure Contract

| Folder | Purpose |
|---|---|
| `production_artifacts/Database_ER_Diagram.md` | ER diagram + rationale |
| `production_artifacts/ADRs/` | Database selection ADR |
| `app_build/src/db/` | ORM config, schema, client setup |
| `app_build/migrations/` | Versioned migrations (up + down) |
| `app_build/seeds/` | Seed data scripts |
| `scripts/db/` | Repeatable helpers (reset, backup, verify) |
| `references/` | Query patterns, tuning notes |

---

## 2. Required Inputs

| Document | Required | Why |
|---|---|---|
| `production_artifacts/Technical_Specification.md` | YES | Domain entities, constraints |
| `production_artifacts/Solution_Architecture.md` | YES | Approved stack, scale targets |
| `production_artifacts/Tech_Stack_Rationale.md` | When present | Why this database family |

If the spec is missing entity definitions, stop and ask the Product Manager
to clarify before designing the schema.

---

## 3. Database Selection Decision Tree

Never default to PostgreSQL. Every project deserves a fresh evaluation:

| Need | Best Fit | Notes |
|---|---|---|
| ACID, relations, structured data, general SaaS | PostgreSQL | Safe default for server-hosted apps |
| Serverless + PostgreSQL dialect | Neon | Branching, autoscaling, good for preview envs |
| Edge-first, global replication | Turso (libSQL) | SQLite at the edge, low latency |
| Zero-config local, embedded, CLI tools | SQLite | File-based, no server, fast tests |
| Flexible schema, document-oriented, heavy denorm | MongoDB | Only if document model fits better |
| Time-series, IoT metrics | TimescaleDB / InfluxDB | Specialized workload |
| Vector search, RAG, semantic similarity | pgvector / Qdrant | AI-first applications |
| Managed + tight Next.js integration | Supabase / Neon | If full BaaS is desired |

### Selection Questions

1. What's the deployment target? (serverless, container, edge, embedded)
2. Do we need multi-region replication?
3. What's the read/write ratio and expected volume?
4. Are there strong relational constraints?
5. Does the team already know one of these?
6. What's the compliance surface (LGPD, HIPAA, SOC2)?

**Document the answer as an ADR** under `production_artifacts/ADRs/`.

---

## 4. ORM / Query Builder Selection

| Tool | Use When | Avoid When |
|---|---|---|
| **Drizzle** | TypeScript-first, SQL-like syntax, edge-ready | Need Rails-like magic |
| **Prisma** | Large teams, strong tooling, generated types | Edge runtimes without data proxy, read-heavy latency-critical |
| **Kysely** | You want raw SQL power with type safety | Need a migration story out of the box |
| **Raw SQL + node-postgres** | Simple CRUD, full control, minimal deps | Fast iteration with changing schema |
| **TypeORM / Sequelize** | Legacy codebase, existing team knowledge | New project with modern alternatives available |

Default recommendation for new TypeScript projects: **Drizzle** for edge / Node,
**Prisma** for enterprise teams that value DX over edge performance.

---

## 5. Workflow

### Phase 1: Domain Modeling

1. Read the spec and extract entities, attributes, and relationships.
2. Draft an ER diagram in Mermaid (save to `production_artifacts/Database_ER_Diagram.md`).
3. Identify: cardinalities, optionality, tenancy model, soft-delete policy, audit fields.

### Phase 2: Database & ORM Decision

4. Apply the selection decision tree -- write the ADR explaining trade-offs.
5. Confirm the choice with the Solution Architect if architecture implies otherwise.

### Phase 3: Schema Implementation

6. Create the schema in `app_build/src/db/schema/` (one file per aggregate/domain).
7. Generate the initial migration: `app_build/migrations/0001_init.sql` (up + down).
8. Add indexes based on expected query patterns (see Indexing Strategy below).

### Phase 4: Seeds & Helpers

9. Seeds in `app_build/seeds/` -- enough data for dev and CI, not production.
10. Repeatable helpers in `scripts/db/`: `reset.sh`, `seed.sh`, `backup.sh`.

### Phase 5: Deploy Config

11. Provide Docker Compose for local dev (service + volume + healthcheck).
12. Document connection strings format in `API_KEYS_SETUP.md`.

---

## 6. Indexing Strategy

Build indexes based on query patterns, not by guessing:

| Query Pattern | Index Type |
|---|---|
| Equality on single column (`WHERE user_id = ?`) | B-tree, single column |
| Equality on multiple columns (`WHERE tenant_id = ? AND status = ?`) | Composite: `(tenant_id, status)` |
| Range scans (`WHERE created_at > ?`) | B-tree on the range column |
| Covering query (SELECT returns only indexed columns) | INCLUDE clause |
| Case-insensitive text search | Functional index on `LOWER(column)` or full-text |
| JSON field access | GIN index on JSONB (PostgreSQL) |
| Partial filter (`WHERE deleted_at IS NULL`) | Partial index |

**Rules**:
- Every foreign key needs an index (PostgreSQL does NOT auto-index FKs).
- Composite index column order matters -- most selective column first.
- Over-indexing hurts writes. Measure before adding.

---

## 7. Migration Discipline

| Rule | Why |
|---|---|
| Every migration has `up` AND `down` | Safe rollback under pressure |
| Migrations are immutable once merged | Production history must be reproducible |
| Never rename columns in one migration | Rename = add new + backfill + drop old (multi-step) |
| Never change column type destructively | Blue-green column, migrate data, then swap |
| Run in transaction when possible | PostgreSQL supports DDL in transactions |
| Test migrations against a prod-sized copy | Surprises scale non-linearly |

### Safe Column Rename Pattern

```
Migration N:   ADD COLUMN new_name; copy values from old_name
Deploy application that writes to both columns
Migration N+1: DROP COLUMN old_name
```

---

## 8. Performance Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| `SELECT *` in app queries | Select only needed columns |
| N+1 queries (loop of SELECTs) | Use JOIN or batch load (dataloader pattern) |
| Missing index on filter column | Check query plan, add index |
| Large JSON stored when relations fit | Normalize to relations |
| String PK (UUID v4 random) on huge tables | UUID v7 (time-sortable) or sequential BigInt |
| OFFSET/LIMIT deep pagination | Keyset pagination (WHERE id > last_id) |
| Missing connection pooling | PgBouncer, Prisma Data Proxy, Neon pooled connection |

---

## 9. Quality Bar

Before marking the data layer as done:

- [ ] ER diagram committed and approved
- [ ] Database selection ADR exists
- [ ] Schema matches ER diagram
- [ ] Every migration has `up` and `down`
- [ ] Foreign keys + indexes match query patterns
- [ ] Seeds run cleanly on an empty database
- [ ] Docker Compose spins up a working local database
- [ ] Connection settings documented in `API_KEYS_SETUP.md`
- [ ] No secrets in code or migrations

---

## 10. Bundled Reference

| File | Contents |
|---|---|
| [references/database-decision-matrix.md](references/database-decision-matrix.md) | Deep comparison of databases by workload |
| [references/schema-patterns.md](references/schema-patterns.md) | Normalization, indexing, pagination, audit trails |

---

## 11. Deliverables

Every completed task produces:

1. `production_artifacts/Database_ER_Diagram.md` (Mermaid + rationale)
2. `production_artifacts/ADRs/NNN-database-selection.md`
3. Schema + migrations in `app_build/`
4. Seeds in `app_build/seeds/`
5. Helper scripts in `scripts/db/`
6. Updated `production_artifacts/memory/AI_CONTEXT.md` with stack decision
