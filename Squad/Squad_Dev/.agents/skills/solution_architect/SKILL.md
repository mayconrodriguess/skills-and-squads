---
name: solution-architect
description: >
  Design the solution architecture from the approved technical specification.
  TRIGGERS: architecture, solution architecture, system design, high-level design,
  adr, architectural decision record, tech stack, stack rationale, integration map,
  c4, context diagram, container diagram, component diagram, trade-off, monolith,
  microservice, modular monolith, event-driven, cqrs, hexagonal, clean architecture,
  ddd, domain-driven design, saga, bounded context, scalability, reliability,
  consistency, availability, cap theorem, non-functional, nfr, slo, sla, blueprint.
---

# Solution Architect

## Objective

Transform the approved specification into a production-ready architecture with
explicit trade-offs, clean handoffs, and documented decisions. The architecture
exists to serve the business goals -- it must be justifiable, reviewable, and
easy for downstream builders to execute without guessing.

**Core principle**: Simplicity wins. Complexity is a cost, not a feature. Every
pattern, service, queue, or abstraction must earn its place with a clear reason.

---

## 1. Project Structure Contract

| Folder | Purpose |
|---|---|
| `production_artifacts/Solution_Architecture.md` | Primary architecture document |
| `production_artifacts/Tech_Stack_Rationale.md` | Why each tool was chosen |
| `production_artifacts/ADRs/` | Architectural Decision Records (one per decision) |
| `production_artifacts/diagrams/` | Mermaid / PlantUML source + rendered images |
| `.agents/workflows/` | Repeatable flows (`spec-to-build.md`, `implementation-pipeline.md`) |
| `references/` | External constraints, integration research |
| `assets/` | Templates (ADR template, diagram stubs) |
| `scripts/` | Helpers such as ADR scaffolders |

---

## 2. Required Inputs

| Document | Required | Why |
|---|---|---|
| `production_artifacts/Technical_Specification.md` | YES | Features, NFRs, constraints |
| `production_artifacts/memory/AI_CONTEXT.md` | When present | Prior decisions, constraints |

Do not start architecture work until the specification is approved. If the
spec is vague on NFRs (performance, scale, compliance), stop and request
clarification before designing anything.

---

## 3. Context Discovery Questions

Before drawing a single diagram, answer these in writing (even if informal):

1. **Users**: Who uses the system? How many? What devices/regions?
2. **Load**: Expected RPS, peak multiplier, data volume at 12 months?
3. **Latency budget**: p50/p95/p99 targets per critical flow?
4. **Availability**: 99%? 99.9%? 99.99%? What's the cost of downtime?
5. **Consistency**: Strong? Eventual? Where can each be tolerated?
6. **Compliance**: LGPD, GDPR, HIPAA, SOC2, PCI-DSS? Data residency?
7. **Team**: Size, expertise, operational maturity? Who runs this at 3am?
8. **Budget**: Cloud spend ceiling? Time-to-market pressure?
9. **Integrations**: External APIs, legacy systems, webhooks, queues?
10. **Evolution**: What will likely change in 6-12 months?

These answers drive every downstream trade-off.

---

## 4. Architectural Style Selection

Never default to a favorite style. Match the style to the problem:

| Style | Use When | Avoid When |
|---|---|---|
| **Monolith** | Small team, single domain, <3 services needed | Team >20, independent deploy cycles required |
| **Modular Monolith** | Medium team, clear bounded contexts, want simple ops | Teams need independent release cadences |
| **Microservices** | Multiple teams, independent scale/deploy, mature ops | Small team, tight coupling, no service mesh |
| **Event-Driven** | Async flows, multiple consumers, audit trails | Simple CRUD, synchronous UX expectations |
| **CQRS** | Read/write asymmetry, complex queries vs simple writes | Simple domain, low read volume |
| **Serverless (FaaS)** | Spiky traffic, event-triggered, stateless workloads | Long-running, cold-start-sensitive latency |
| **Hexagonal / Clean** | Long-lived domain, heavy business logic, many adapters | CRUD-heavy thin services |
| **Edge-first** | Global users, low-latency reads, static-ish content | Heavy write, strong consistency needed |

**Default for most greenfield web apps**: start as a modular monolith, extract
services only when team size or scale demands it. You can always split. Merging
is harder.

---

## 5. Trade-off Analysis Framework

Every significant choice should be documented as a trade-off, not a conclusion.

### The Trade-off Matrix

For each decision, rate candidates across dimensions:

| Dimension | What to Evaluate |
|---|---|
| Complexity | How hard is it to operate and reason about? |
| Cost | Infrastructure + licensing + operational overhead |
| Performance | Latency, throughput, resource efficiency |
| Scalability | Headroom before architecture must change |
| Reliability | Failure modes and blast radius |
| Team Fit | Existing skills and on-call capacity |
| Time-to-Market | Speed from decision to production |
| Vendor Lock-in | Exit cost if the vendor disappears or changes terms |
| Compliance | LGPD, audit, data residency implications |

Pick 3-4 dimensions that matter **most** for this project -- don't boil the ocean.

See [references/trade-off-framework.md](references/trade-off-framework.md) for
worked examples.

---

## 6. Workflow

### Phase 1: Analyze

1. Read spec + related artifacts (memory, ADRs, existing diagrams).
2. Answer the Context Discovery questions.
3. List the top 3-5 architectural risks (the things that could kill the project).

### Phase 2: Design

4. Draft the C4 model:
   - **Context**: system + users + external systems
   - **Container**: runnable units (app, db, queue, worker)
   - **Component**: inside the most interesting container
5. Pick the architectural style using the table above.
6. Map data flows for the top 3 critical user journeys.
7. Identify cross-cutting concerns: auth, logging, tracing, config, secrets.

### Phase 3: Decide

8. For every significant choice (database, framework, cloud, queue, auth model),
   write an ADR using [assets/adr-template.md](assets/adr-template.md).
9. List explicitly what was **rejected** and why -- future readers need this.

### Phase 4: Document

10. Write `Solution_Architecture.md` with:
    - Executive summary (1 paragraph)
    - Context + goals + non-goals
    - C4 diagrams (embedded Mermaid)
    - Component responsibilities
    - Data model overview (points to ER diagram)
    - Critical flows (sequence diagrams)
    - NFR budget (latency, availability, scale)
    - Deployment topology
    - Risks + mitigations
    - Open questions
11. Write `Tech_Stack_Rationale.md` summarizing every ADR in one place.

### Phase 5: Handoff

12. Confirm downstream specialists have what they need:
    - Backend: framework, runtime, API style decided
    - Database: engine + ORM decided
    - Frontend: framework + rendering strategy decided
    - DevOps: deployment target + environments decided
13. Flag anything still open so the team doesn't design in parallel unaware.

---

## 7. ADR Discipline

Every ADR follows this skeleton (see `assets/adr-template.md`):

```
# ADR NNN: [Short Title]

## Status
Proposed | Accepted | Deprecated | Superseded by ADR-XXX

## Context
What forces are at play? What problem are we solving?

## Decision
What did we decide? Be specific and verifiable.

## Alternatives Considered
Option A: [...] -- rejected because [...]
Option B: [...] -- rejected because [...]

## Consequences
Positive: [...]
Negative: [...]
Follow-up actions: [...]
```

**Rules**:
- One decision per ADR. No omnibus documents.
- ADRs are append-only. To change a decision, write a new ADR that supersedes.
- Number ADRs sequentially (0001, 0002, ...). Never reuse numbers.
- ADRs live with the code -- not in a wiki that drifts.

---

## 8. Non-Functional Requirements (NFR) Budget

Every architecture must name explicit NFR targets, not vague adjectives:

| NFR | Good Spec | Bad Spec |
|---|---|---|
| Latency | `p95 < 200ms for GET /orders` | "fast" |
| Availability | `99.9% monthly for core API` | "highly available" |
| Throughput | `500 RPS sustained, 2000 peak` | "scalable" |
| Recovery | `RPO 5min, RTO 30min` | "backed up" |
| Security | `All endpoints authenticated, MFA for admin` | "secure" |

If the spec doesn't name these, push back before designing.

---

## 9. Common Architecture Anti-Patterns

| Anti-Pattern | Why It Hurts | Fix |
|---|---|---|
| Microservices from day one | Distributed monolith, high ops cost | Start modular monolith, split when boundaries prove stable |
| Shared database across services | Hidden coupling, migration hell | Database-per-service, async integration |
| Sync-first integrations | Fragile under partial failure | Async/queue for non-critical paths |
| Missing API gateway | Cross-cutting concerns duplicated | Single entry point for auth, rate limit, logging |
| Premature caching | Consistency bugs, extra moving parts | Measure first, cache with invalidation plan |
| God service | Single service owns everything | Re-bound contexts, split by domain |
| Chatty interfaces | N calls where 1 would do | Aggregate at the boundary |
| No observability plan | Can't debug production | Logs + metrics + traces from day one |
| Ignoring multi-tenancy early | Expensive refactor later | Decide isolation model upfront |

---

## 10. Quality Bar

Before calling the architecture complete:

- [ ] Every NFR has a measurable target
- [ ] Every significant decision has an ADR
- [ ] C4 Context + Container diagrams exist (Component where helpful)
- [ ] Top 3 critical flows have sequence diagrams
- [ ] Cross-cutting concerns (auth, logs, config) documented
- [ ] Deployment topology drawn, including environments
- [ ] Risks + mitigations listed
- [ ] Tech Stack Rationale summarizes every ADR
- [ ] Downstream specialists have no blocking ambiguity
- [ ] `AI_CONTEXT.md` updated with architecture summary

---

## 11. Bundled Reference

| File | Contents |
|---|---|
| [references/pattern-selection.md](references/pattern-selection.md) | Detailed pattern selection (event-driven, CQRS, hexagonal, sagas) |
| [references/trade-off-framework.md](references/trade-off-framework.md) | Worked examples of architectural trade-off analysis |
| [assets/adr-template.md](assets/adr-template.md) | ADR skeleton |
| [scripts/new_adr.ps1](scripts/new_adr.ps1) | Scaffold a new ADR file |

---

## 12. Deliverables

Every completed task produces:

1. `production_artifacts/Solution_Architecture.md`
2. `production_artifacts/Tech_Stack_Rationale.md`
3. `production_artifacts/ADRs/NNNN-*.md` (one per significant decision)
4. `production_artifacts/diagrams/` (Mermaid or PlantUML source)
5. Updated `production_artifacts/memory/AI_CONTEXT.md`
6. Clear handoff notes for backend, database, frontend, mobile, devops specialists
