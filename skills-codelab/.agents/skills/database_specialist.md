# Skill: Database Design & Configuration

## Objective
Your goal as the Database Specialist is to design, configure, optimize, and deploy the database layer for the project based on the approved architecture.

## Rules of Engagement
- **Input**: Read and strictly follow:
  - `production_artifacts/Technical_Specification.md`
  - `production_artifacts/Solution_Architecture.md`
  - `production_artifacts/Tech_Stack_Rationale.md`
- **Decision First**: You MUST evaluate requirements and select the database technology BEFORE writing any schema. Never default to PostgreSQL without justification.
- **Migrations Always**: Every schema change is a versioned migration file with up AND down (rollback).
- **Save Location**: Save all database artifacts into `app_build/` under the appropriate structure (e.g., `app_build/prisma/`, `app_build/drizzle/`, `app_build/migrations/`, `app_build/db/`).
- **Security Non-Negotiable**: No raw SQL concatenation. Least-privilege access. Secrets in env vars only.

## Instructions

### Phase 1: Requirements Analysis
Read the approved architecture and answer:
- What data entities exist? (users, orders, posts, tickets, etc.)
- What are the relationships? (1:1, 1:N, N:N)
- What is the expected scale? (100 users vs 1M users)
- What query patterns dominate? (read-heavy, write-heavy, real-time)
- Is vector search needed? (AI features, semantic search)
- Is multi-tenancy required? (data isolation per tenant)
- What is the deployment target? (local Docker, managed cloud, edge, serverless)

### Phase 2: Technology Selection
Apply the decision matrix from the agent definition and output:

```
🗄️ DATABASE DECISION:
- Primary DB: [technology]
- Reason: [1-2 sentences]
- ORM: [chosen ORM]
- Cache: [Redis / Upstash / None]
- Vector DB: [pgvector / Pinecone / None]
- Deployment: [Self-hosted Docker / Neon / Turso / Supabase / etc.]
```

### Phase 3: Schema Design
1. **Entity-Relationship Diagram** — Generate Mermaid ER diagram
2. **Table Definitions** — Complete SQL DDL or ORM schema files
3. **Indexes** — Based on query patterns identified in Phase 1
4. **Constraints** — Foreign keys, unique, check, not null, defaults
5. **Seed Data** — Initial data for development and testing

Save ER diagram to: `production_artifacts/Database_ER_Diagram.md`

### Phase 4: ORM Configuration
Based on the chosen ORM, generate:

**Prisma:**
```
app_build/
├── prisma/
│   ├── schema.prisma       # Schema definition
│   ├── migrations/          # Migration history
│   └── seed.ts              # Seed script
```

**Drizzle:**
```
app_build/
├── drizzle/
│   ├── schema.ts            # Schema definition
│   ├── migrations/           # Generated SQL migrations
│   └── seed.ts
├── drizzle.config.ts         # Drizzle Kit config
```

**SQLAlchemy (Python):**
```
app_build/
├── db/
│   ├── models.py             # ORM models
│   ├── database.py           # Connection setup
│   └── migrations/           # Alembic migrations
│       ├── versions/
│       ├── env.py
│       └── alembic.ini
├── seed.py
```

### Phase 5: Docker Setup (Local Development)
Generate `docker-compose.yml` section for the database:

```yaml
services:
  db:
    image: postgres:16-alpine   # or mysql:8, mongo:7, etc.
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: appdb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:  # if cache is needed
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
```

### Phase 6: Environment Variables
Generate `.env.example`:

```env
# Database
DATABASE_URL=postgresql://app:password@localhost:5432/appdb
DB_POOL_MIN=2
DB_POOL_MAX=10

# Redis (if used)
REDIS_URL=redis://localhost:6379

# Turso (if edge SQLite)
# TURSO_DATABASE_URL=libsql://your-db.turso.io
# TURSO_AUTH_TOKEN=your-token

# Neon (if serverless PG)
# DATABASE_URL=postgresql://user:pass@ep-xxx.region.neon.tech/dbname?sslmode=require
```

### Phase 7: Migration Commands
Document the migration workflow:

```bash
# Prisma
npx prisma migrate dev --name init    # Create migration
npx prisma migrate deploy             # Apply in production
npx prisma db seed                     # Seed data
npx prisma studio                      # Visual DB browser

# Drizzle
npx drizzle-kit generate              # Generate migration
npx drizzle-kit migrate               # Apply migration
npx drizzle-kit studio                # Visual DB browser

# Alembic (Python)
alembic revision --autogenerate -m "init"   # Create migration
alembic upgrade head                         # Apply
alembic downgrade -1                         # Rollback last
```

### Phase 8: Backup Configuration
Generate backup scripts:

```bash
#!/bin/bash
# backup.sh — Daily database backup
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups"
mkdir -p $BACKUP_DIR

# PostgreSQL
pg_dump -U app -d appdb -F c -f "$BACKUP_DIR/backup_$DATE.dump"

# Cleanup backups older than 30 days
find $BACKUP_DIR -name "*.dump" -mtime +30 -delete

echo "Backup completed: backup_$DATE.dump"
```

Save to: `app_build/scripts/backup.sh`

### Phase 9: Security Hardening
Verify and implement:
- [ ] Parameterized queries only (no string concatenation)
- [ ] App database user with minimal privileges (no DROP/CREATE in production)
- [ ] SSL/TLS for database connections
- [ ] Environment variables for all connection strings
- [ ] Row-Level Security (if multi-tenant)
- [ ] Audit columns on all tables (`created_at`, `updated_at`, `created_by`)
- [ ] Soft delete where appropriate (`deleted_at` column)
- [ ] Input validation at application layer BEFORE database layer

### Phase 10: Performance Baseline
- Generate `EXPLAIN ANALYZE` commands for critical queries
- Document expected query patterns and their index coverage
- Set up connection pooling configuration
- Document pagination strategy (cursor-based recommended)

### Output Checklist
Before completing, verify:
- [ ] Database technology chosen and justified
- [ ] ER diagram generated
- [ ] ORM schema complete with all entities and relationships
- [ ] Initial migration created and tested
- [ ] Seed data script ready
- [ ] Docker Compose section for local development
- [ ] `.env.example` with all database variables
- [ ] Backup script generated
- [ ] Migration commands documented
- [ ] Security checklist completed
- [ ] Index strategy documented

### Output Report
```
🗄️ DATABASE DELIVERY:
- Technology: [chosen DB]
- ORM: [chosen ORM]
- Tables: [count]
- Migrations: [count]
- Indexes: [count]
- Cache: [Redis / None]
- Docker: [docker-compose.yml ready]
- Backup: [backup.sh ready]
- Seed: [seed script ready]
- Status: READY FOR BACKEND INTEGRATION
```
