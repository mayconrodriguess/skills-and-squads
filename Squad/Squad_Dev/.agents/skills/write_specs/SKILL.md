---
name: write-specs
description: >
  Turn raw product ideas into an actionable technical specification in
  `production_artifacts/Technical_Specification.md`.
  TRIGGERS: spec, specification, technical spec, product spec, prd, brief,
  requirements, user stories, acceptance criteria, moscow, scope, in scope,
  out of scope, nfr, non-functional, success criteria, kpi, metric, okr,
  gherkin, given when then, feature file, edge case, assumption, constraint,
  milestone, phase plan, mvp definition.
---

# Write Specs

## Objective

Convert loose requirements into a concrete technical specification and stop for
approval before downstream work begins. A good spec makes architecture simpler,
reduces rework, and gives the whole Squad a single source of truth.

**Core principle**: A spec is a contract with the future. It exists to be
referenced during design, build, review, and release.

---

## 1. Project Structure Contract

When the workspace is empty, scaffold before writing:

- `.agents/`
- `.agents/skills/`
- `.agents/workflows/`
- `app_build/`
- `production_artifacts/`
- `production_artifacts/memory/`
- `scripts/`
- `references/`
- `assets/`

Use the bundled scaffold script for this step.

---

## 2. Workflow

### Phase 1: Clarification Interview

1. Identify who the user(s) are, what problem they have, and what "success" looks like.
2. Run the Clarification Interview (Section 3) and capture answers verbatim.
3. Surface contradictions, missing info, and risky assumptions.

### Phase 2: Scaffold

4. If the repo is empty, run `scripts/init_project_structure.ps1`.
5. Copy the spec template from `assets/technical_spec_template.md`.

### Phase 3: Draft

6. Fill the spec using the sections in Section 4.
7. Use MoSCoW prioritization (Section 5) for all requirements.
8. Express acceptance criteria as Gherkin (Given/When/Then) for any non-trivial behavior.
9. Name explicit NFR targets (latency, availability, scale, compliance).
10. List assumptions, risks, open questions.

### Phase 4: Review

11. Read the spec in one pass as if you've never seen the project.
12. Check: could the next specialist execute without asking you?
13. Link to any supporting research or competitors in `references/`.

### Phase 5: Handoff

14. Stop and ask for approval. Do NOT proceed to architecture before sign-off.
15. Once approved, write a one-paragraph summary to `production_artifacts/memory/AI_CONTEXT.md`.

---

## 3. Clarification Interview

Ask these before writing a single requirement. If answers are missing, stop and ask.

### Problem & Users

1. What problem are we solving? In one sentence.
2. Who experiences this problem? (persona, role, context)
3. How do they solve it today? What's broken about that?
4. What does success look like in 3 months? In 12 months?

### Scope & Boundaries

5. What's explicitly **in scope** for this release?
6. What's explicitly **out of scope**? (this matters as much as in-scope)
7. What's the deadline or launch window?
8. What's the budget ceiling (cloud, tooling, people)?

### Constraints

9. Compliance requirements? (LGPD, GDPR, HIPAA, SOC2, PCI)
10. Performance SLOs? (latency, throughput, uptime)
11. Platforms? (web, iOS, Android, desktop, CLI, API)
12. Integrations with existing systems or third-party APIs?
13. Team size and skillset?
14. Hard tech constraints? (must use X, can't use Y)

### Risk & Assumptions

15. What are we assuming that could be wrong?
16. What's the biggest risk to the project?
17. What happens if we ship late? If we don't ship at all?

Record answers in `production_artifacts/references/interview-notes.md` so
downstream readers see the reasoning.

---

## 4. Specification Structure

Required sections in every spec:

1. **Executive Summary** -- 1 paragraph, the elevator pitch
2. **Problem Statement** -- who, what, why now
3. **Goals & Non-Goals** -- explicit scope boundaries
4. **Users & Personas** -- who uses this, their jobs-to-be-done
5. **User Stories** -- "As a [role], I want [capability], so that [outcome]"
6. **Functional Requirements** -- MoSCoW prioritized, with acceptance criteria
7. **Non-Functional Requirements** -- measurable NFRs (see Section 6)
8. **Assumptions & Constraints** -- explicit list
9. **Dependencies** -- external systems, APIs, teams
10. **Risks & Mitigations** -- what could fail
11. **Success Metrics** -- how we know we shipped the right thing
12. **Rollout Plan** -- phased launch, feature flags, rollback
13. **Open Questions** -- things still unresolved
14. **Glossary** -- domain terms (if non-trivial)

Each section has a required format. See `assets/technical_spec_template.md`.

---

## 5. MoSCoW Prioritization

Every requirement gets one of four labels:

| Label | Meaning | Example |
|---|---|---|
| **Must** | Launch blocker. No Must, no release. | "User can log in with email + password" |
| **Should** | Important but launch can slip it one sprint. | "Password strength meter" |
| **Could** | Nice to have. Ship if time allows. | "Social login with Google" |
| **Won't** (this time) | Out of scope. Explicitly excluded. | "Two-factor auth -- v2" |

**Rule**: If everything is Must, nothing is. Expect a ~40/30/20/10 split.

---

## 6. Non-Functional Requirements (NFR)

Vague NFRs are invisible. Name the target:

| NFR | Good Spec | Bad Spec |
|---|---|---|
| Latency | `p95 < 200ms for POST /orders` | "fast" |
| Availability | `99.9% monthly for public API` | "highly available" |
| Throughput | `500 RPS sustained, 2000 peak` | "scalable" |
| Data retention | `User data retained 24 months after deletion` | "secure" |
| Recovery | `RPO 5min, RTO 30min` | "backed up" |
| Accessibility | `WCAG 2.2 AA compliance` | "accessible" |
| i18n | `pt-BR + en-US at launch; pluggable for more` | "supports languages" |
| Privacy | `LGPD-compliant; opt-in telemetry only` | "respects privacy" |

If the stakeholder can't commit to a number, ask "What's bad enough to delay
launch? What's good enough to ship?" That's your NFR envelope.

---

## 7. Acceptance Criteria (Gherkin)

Write non-trivial behavior as Given/When/Then so tests can later mirror it:

```gherkin
Feature: Order checkout
  As a logged-in customer
  I want to place an order
  So that I receive the items I selected

  Scenario: Successful checkout with valid card
    Given I have 3 items in my cart
    And my saved card is valid
    When I confirm the order
    Then the order is created with status "paid"
    And I receive a confirmation email within 2 minutes

  Scenario: Checkout fails when item is out of stock
    Given I have an out-of-stock item in my cart
    When I confirm the order
    Then the checkout returns 409 OUT_OF_STOCK
    And no charge is made against my card
```

**Rule**: Every "Must" requirement has at least one Gherkin scenario.

---

## 8. User Story Pattern

```
As a [role]
I want [capability]
So that [outcome / benefit]

Acceptance criteria:
- [ ] [Gherkin scenario 1]
- [ ] [Gherkin scenario 2]
- [ ] [Edge case handled]
```

Avoid:
- Stories about tech ("As a developer, I want to use Redis"). Tech is a means, not an end.
- Stories without a "so that" clause. If you can't state the outcome, the value isn't clear.

---

## 9. Common Spec Smells

| Smell | Fix |
|---|---|
| Lists features without problems | Lead each feature with the user problem it solves |
| Everything is Must | Apply MoSCoW honestly |
| No measurable NFRs | Attach numbers: latency, uptime, scale |
| No out-of-scope section | Readers assume everything is in-scope |
| Missing edge cases | Add a "Failure Modes" subsection per critical flow |
| Long but vague | Trim prose, add acceptance criteria |
| Decides the tech stack | Defer to the Solution Architect |
| No success metric | Add 1-3 metrics that prove value delivery |

---

## 10. Quality Bar

Before handing off:

- [ ] Executive summary is 1 paragraph a stakeholder can understand
- [ ] In-scope and out-of-scope are both explicit
- [ ] Every requirement has a MoSCoW label
- [ ] Every Must has at least one Gherkin scenario
- [ ] NFRs have measurable numbers
- [ ] Risks listed with mitigations
- [ ] Success metrics defined (and measurable)
- [ ] Open questions listed -- nothing hidden
- [ ] Interview notes saved to `production_artifacts/references/`
- [ ] Ready for architect handoff, with no tech decisions forced

---

## 11. Bundled Resources

- [assets/technical_spec_template.md](assets/technical_spec_template.md) -- baseline outline
- [scripts/init_project_structure.ps1](scripts/init_project_structure.ps1) -- scaffold the repo contract

---

## 12. Deliverables

Every completed task produces:

1. `production_artifacts/Technical_Specification.md`
2. `production_artifacts/references/interview-notes.md` (if new project)
3. Updated `production_artifacts/memory/AI_CONTEXT.md` with spec summary
4. Explicit STOP and approval request before downstream work starts
