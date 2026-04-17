# Trade-off Analysis Framework

A repeatable method for architectural decisions. Use this to avoid the trap of
"I picked X because I like X."

---

## 1. The Core Idea

Architecture is the art of deferring decisions and owning the ones you can't
defer. Every deferred decision is a trade-off. Make them explicit.

**A trade-off exists whenever a decision helps along one dimension and hurts
along another.** If you can't name a downside, you haven't thought hard enough.

---

## 2. The Five Questions

Apply to every significant decision:

1. **What forces are at play?** Business goals, NFRs, team, budget, compliance.
2. **What are the candidate options?** List at least 3. "Do nothing" is always one.
3. **How does each option rate on the dimensions that matter?**
4. **What breaks first if we pick this?** Capacity, maintainability, cost, team.
5. **Is this decision reversible?** If yes, bias toward speed. If no, slow down.

---

## 3. Dimension Cheat Sheet

Pick 3-5 that matter for **this** decision. Don't rate every dimension every time.

| Dimension | Questions |
|---|---|
| Complexity | How many moving parts? How hard to explain to a new hire? |
| Cost | Cloud + licenses + operational time |
| Performance | Latency, throughput, resource use |
| Scalability | Headroom before we must re-architect |
| Reliability | Failure modes, blast radius, recovery time |
| Team Fit | Existing skills, on-call capacity |
| Time-to-Market | How fast can we ship? |
| Vendor Lock-in | Exit cost? |
| Compliance | Audit, data residency, certifications |
| Evolvability | How easy to change the decision later? |

---

## 4. Worked Example: Choosing a Database

**Context**: SaaS analytics dashboard. Expected 100 tenants, up to 10M rows
per tenant, mostly reads with dashboard queries, team knows PostgreSQL well,
LGPD compliance required, budget is tight.

### Options

| Option | Overview |
|---|---|
| A. PostgreSQL managed (RDS / Supabase) | Familiar, strong consistency |
| B. Neon (serverless PostgreSQL) | PostgreSQL + branching + autoscale |
| C. ClickHouse | Columnar, great for analytics aggregation |
| D. DynamoDB | Fully managed NoSQL, pay per request |

### Matrix

| Dimension (Weight) | A: Postgres RDS | B: Neon | C: ClickHouse | D: DynamoDB |
|---|---|---|---|---|
| Team fit (HIGH) | 5 | 5 | 2 | 2 |
| Cost (HIGH) | 3 | 4 | 3 | 2 |
| Analytics performance (HIGH) | 3 | 3 | 5 | 2 |
| Complexity (MEDIUM) | 4 | 5 | 3 | 4 |
| Compliance (HIGH) | 5 | 5 | 4 | 4 |
| Scale headroom (MEDIUM) | 4 | 5 | 5 | 5 |

Weighted scores favor A or B. ClickHouse wins on analytics but loses on team fit.

### Decision

**Pick B (Neon)**, because:
- Team knows PostgreSQL, zero ramp-up
- Serverless pricing fits tight budget at low scale
- Branching simplifies CI/CD and preview environments
- Can add ClickHouse later for hot analytics if PostgreSQL becomes the bottleneck

### Rejected

- **A (RDS)**: Higher baseline cost, no branching
- **C (ClickHouse)**: Team doesn't know it; analytics isn't yet a bottleneck
- **D (DynamoDB)**: Query model doesn't fit ad-hoc dashboard queries

### Follow-up

- Measure query latency at 6 months; evaluate ClickHouse extraction if p95 > 1s

---

## 5. Worked Example: Sync vs Async Integration

**Context**: Order service needs to notify an inventory service on checkout.
Checkout latency budget is 500ms. Inventory update must happen reliably but
not necessarily immediately.

### Options

- A. Sync HTTP call from Order to Inventory
- B. Async: Order publishes event, Inventory consumes
- C. Hybrid: Sync for critical "reserve stock", async for telemetry

### Key Dimensions

| Dimension | A: Sync | B: Async | C: Hybrid |
|---|---|---|---|
| Latency | Inventory latency bleeds into checkout | Fastest checkout | Acceptable |
| Reliability | Inventory down = checkout down | Decoupled | Partial decoupling |
| Consistency | Immediate | Eventual (seconds) | Mixed |
| Complexity | Low | Medium (queue + idempotency) | Medium-high |

### Decision

**Pick C (Hybrid)**: sync reservation (must succeed or checkout fails), async
for non-critical downstream updates. Adds complexity but meets latency + reliability.

---

## 6. Reversibility as a Decision Factor

From Amazon's two-way / one-way door framing:

- **Two-way door**: easy to reverse. Ship fast, learn, adjust.
  Examples: framework choice inside a service, caching strategy, index design.

- **One-way door**: expensive to reverse. Slow down, research, get consensus.
  Examples: primary database, tenancy model, public API contract, auth scheme.

**Rule**: Spend more time on one-way doors. Don't over-deliberate two-way doors.

---

## 7. Recognizing Bad Trade-off Thinking

| Smell | Fix |
|---|---|
| "Everyone uses X" | Evaluate for your context, not industry fashion |
| "We already know X" | Legitimate, but check X still fits the problem |
| "It'll scale" | Show the math or it doesn't count |
| "We can refactor later" | Only for reversible decisions |
| "It's cheaper on paper" | Include ops time, not just infra cost |
| "Vendor X promises..." | Read the SLA and the exit cost |

---

## 8. Documenting the Decision

Every trade-off analysis ends in an ADR. Without the ADR, the decision evaporates.

Minimum ADR content:
- Forces (why this matters now)
- Options considered
- Chosen option + reasoning
- What was rejected and why
- Expected follow-up / re-evaluation trigger

See [../assets/adr-template.md](../assets/adr-template.md).
