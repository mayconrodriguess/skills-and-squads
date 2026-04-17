# Architectural Pattern Selection

Deep-dive guide for selecting architectural patterns. The SKILL.md gives the
high-level decision tree; this file explains the nuance.

---

## 1. Monolith vs Modular Monolith vs Microservices

### Monolith

**One deployable unit. Single codebase. Single database.**

Pros:
- Simplest to develop, test, deploy
- ACID transactions across the whole domain
- Low ops burden -- one thing to monitor
- Refactoring across boundaries is cheap

Cons:
- Whole app redeploys for any change
- Scaling is coarse (scale everything or nothing)
- Tech stack is uniform across modules

**Best for**: early-stage products, teams < 10, single domain.

### Modular Monolith

**One deployable unit but internal module boundaries are enforced** (via
package structure, visibility rules, or separate compilation units).

Pros:
- Keeps monolith simplicity
- Prepares ground for future extraction
- Module contracts force discipline

Cons:
- Needs tooling/linting to enforce boundaries
- Still scales as one unit

**Best for**: growing teams, clear bounded contexts, expecting to scale but not
wanting to pay the distributed tax yet.

### Microservices

**Multiple deployable units, each with its own data and team.**

Pros:
- Independent scale, deploy, tech choice
- Failure isolation (ideally)
- Aligns with team autonomy

Cons:
- Distributed system complexity (network, consistency, tracing)
- Requires mature CI/CD, observability, service discovery
- Cross-service transactions are hard (see Sagas)

**Best for**: multiple teams with independent roadmaps, proven bounded contexts,
mature platform team.

### Decision Rule

> Start with a modular monolith. Extract a service when:
> - A module has a clearly different scaling profile
> - A separate team will own it
> - Its release cadence genuinely differs from the rest

---

## 2. Event-Driven Architecture

### When It Fits

- Multiple consumers need the same event
- Producer shouldn't know about consumers
- Async processing is acceptable (user doesn't wait)
- Audit/replay is valuable

### Patterns

| Pattern | Use |
|---|---|
| **Pub/Sub** | Many independent consumers, fan-out |
| **Event Sourcing** | Immutable audit trail, time-travel, rebuild state |
| **Choreography** | Services react to events independently |
| **Orchestration** | A central coordinator drives the flow (see Sagas) |

### Trade-offs

- Eventual consistency becomes the norm
- Debugging is harder -- must have tracing
- Idempotent consumers are mandatory
- Schema evolution must be backward compatible

### When NOT to Use

- Simple CRUD where sync API is fine
- Strong-consistency UX (user expects immediate reflection)
- Small team without observability maturity

---

## 3. CQRS (Command Query Responsibility Segregation)

**Separate models for reading and writing.**

### Use When

- Read and write workloads are very different (heavy reads, few writes)
- Complex queries needed that don't fit the write model
- You need multiple read models for different views

### Warnings

- Doubles the model surface area
- Often paired with event sourcing -- consistency window between write and read
- Overkill for basic CRUD

---

## 4. Hexagonal / Ports & Adapters (Clean Architecture)

**Domain logic sits in the center. External systems (DB, HTTP, queue) are
adapters plugged into ports.**

### Use When

- Long-lived domain with complex business rules
- Multiple input adapters (REST, gRPC, CLI, queue)
- Want to swap infrastructure without touching domain
- Testability is paramount

### Avoid When

- Thin CRUD services with little domain logic
- Small team that won't maintain the discipline

---

## 5. Saga Pattern (Distributed Transactions)

**A sequence of local transactions where each compensates the previous on
failure.**

### Types

| Type | How |
|---|---|
| **Choreography** | Each service listens to events and publishes next event |
| **Orchestration** | A saga coordinator tells each service what to do |

### Rules

- Every step needs a **compensating action** (undo)
- Compensations must be idempotent
- Monitor for stuck sagas
- Orchestration scales better with many steps; choreography with few

---

## 6. API Gateway Pattern

**Single entry point that handles cross-cutting concerns.**

Use for:
- Auth / token validation
- Rate limiting
- Request routing
- Response aggregation (BFF pattern)
- Logging / metrics / tracing injection

Avoid making it:
- A god service with business logic
- A single point of failure without HA

---

## 7. Backend-for-Frontend (BFF)

**One API gateway per client type (web, mobile, partner).**

Use when:
- Clients have genuinely different data needs
- Different teams own web vs mobile
- Reducing over-fetching matters

Avoid when:
- Clients are similar -- a single GraphQL / REST API suffices

---

## 8. Strangler Fig (Legacy Migration)

**Gradually route traffic from legacy to new system until legacy can be
retired.**

Steps:
1. Put a facade in front of the legacy system
2. Build new functionality behind the facade
3. Redirect one endpoint at a time to the new system
4. Delete the legacy when no traffic remains

Do **not** big-bang rewrite. Never works.

---

## 9. Edge-First Architecture

**Compute + data close to users globally.**

Use when:
- Global user base, latency-sensitive
- Mostly reads with occasional writes
- Content can tolerate eventual consistency

Stacks:
- Cloudflare Workers + D1 / KV / R2
- Vercel Edge + Neon / Turso
- Deno Deploy + Deno KV

Warnings:
- Write-heavy workloads suffer
- Connection pooling to traditional DBs needs care (use HTTP drivers)

---

## 10. Pattern Selection Cheat Sheet

| Problem | Pattern |
|---|---|
| "Service A needs data from B often" | Reconsider boundaries, or event carry state |
| "One slow endpoint blocks others" | Bulkhead, async processing |
| "Cascading failures" | Circuit breaker, timeout, retry with backoff |
| "Consistent state across services" | Saga + compensations |
| "Many clients, different needs" | BFF or GraphQL |
| "Replay history" | Event sourcing |
| "Hot read path" | Cache, read replica, CQRS |
| "Legacy won't die" | Strangler fig |
| "Global latency" | Edge compute + regional data |
