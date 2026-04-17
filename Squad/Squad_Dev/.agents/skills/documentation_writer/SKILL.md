---
name: documentation-writer
description: >
  Produce or refresh project documentation from approved artifacts.
  TRIGGERS: documentation, docs, readme, changelog, api docs, openapi, swagger,
  user guide, developer guide, onboarding, contribution guide, adr index,
  deployment guide, runbook, troubleshooting, migration guide, release notes,
  tutorial, how-to, reference, llms.txt, docstring, jsdoc, tsdoc, mkdocs,
  docusaurus, vitepress, astro starlight.
---

# Documentation Writer

## Objective

Turn approved architecture and implementation context into documentation that
helps the next person move quickly. Good docs reduce support burden, onboarding
time, and the number of "why did we build it this way?" conversations.

**Core principle**: Write for the reader, not the writer. Know your audience
before you write a single line.

---

## 1. Project Structure Contract

| Folder | Purpose |
|---|---|
| `production_artifacts/` | Source-of-truth docs (specs, architecture, ADRs) |
| `production_artifacts/docs/` | Generated/curated docs for humans |
| `production_artifacts/docs/api/` | API reference (OpenAPI + rendered) |
| `production_artifacts/docs/runbooks/` | Operational procedures |
| `README.md` (root) | Project entry point, quickstart |
| `CHANGELOG.md` (root) | Versioned change history |
| `CONTRIBUTING.md` (root) | How to contribute |
| `llms.txt` (root) | AI-readable project summary |
| `assets/` | Templates (README, ADR, changelog) |
| `references/` | Style guides, doc research |

---

## 2. Required Inputs

| Document | Required | Why |
|---|---|---|
| `production_artifacts/Technical_Specification.md` | YES | What the system does |
| `production_artifacts/Solution_Architecture.md` | YES | How it's built |
| `production_artifacts/Tech_Stack_Rationale.md` | When present | Why each tool |
| `production_artifacts/ADRs/` | When present | Decision history |
| OpenAPI spec / API Contract | When API exists | Endpoint reference |

If source artifacts are missing or contradictory, **stop and flag**. Don't paper
over inconsistencies -- they will bite the reader.

---

## 3. Audience-First Decision Matrix

Before writing, name the primary audience. Every doc has one.

| Audience | Needs | Writing Style |
|---|---|---|
| New developer onboarding | How to run it locally in 10 minutes | Step-by-step, copy-pasteable |
| Experienced contributor | Design rationale, where to change what | Conceptual + references |
| API consumer (external) | Endpoints, auth, error codes, examples | Reference + quickstart |
| Operator / SRE | How to deploy, monitor, recover | Runbook, checklist-style |
| Future maintainer | Why decisions were made | ADRs, architecture notes |
| AI agent / LLM | Machine-readable summary | Structured, `llms.txt` |
| Business stakeholder | What it does, what's shipped | Plain language, no jargon |

**Rule**: One document, one audience. Mixed audiences produce mediocre docs.

---

## 4. Document Types & Templates

| Type | Location | Template |
|---|---|---|
| README (root) | `/README.md` | [assets/readme-template.md](assets/readme-template.md) |
| Architecture overview | `production_artifacts/Solution_Architecture.md` | -- |
| ADR | `production_artifacts/ADRs/NNNN-*.md` | solution_architect/assets/adr-template.md |
| API Reference | `production_artifacts/docs/api/` | OpenAPI → rendered |
| Changelog | `/CHANGELOG.md` | [references/doc-templates.md](references/doc-templates.md) (Keep a Changelog) |
| Contribution guide | `/CONTRIBUTING.md` | [references/doc-templates.md](references/doc-templates.md) |
| Runbook | `production_artifacts/docs/runbooks/*.md` | [references/doc-templates.md](references/doc-templates.md) |
| Migration guide | `production_artifacts/docs/migrations/*.md` | [references/doc-templates.md](references/doc-templates.md) |
| llms.txt | `/llms.txt` | [references/doc-templates.md](references/doc-templates.md) |

---

## 5. Workflow

### Phase 1: Discover

1. Read all approved artifacts.
2. List documents that exist and their freshness.
3. Identify gaps: what exists in code but not in docs?
4. Confirm the audience for each doc you plan to write or refresh.

### Phase 2: Outline

5. For each doc, draft a section outline before writing prose.
6. Pick the template that matches the audience.
7. Choose concrete examples to anchor abstract concepts.

### Phase 3: Write

8. Lead with the outcome: what will the reader be able to do after reading?
9. Keep paragraphs short (3-5 lines max).
10. Use tables for options/comparisons, lists for steps.
11. Show code, don't just describe it. Every code block is runnable or clearly marked as pseudo.
12. Link to deeper material rather than inlining everything.

### Phase 4: Verify

13. Run every command in the docs exactly as written.
14. Ask: would a stranger succeed with only this doc and the repo?
15. Check links, cross-references, and code snippets compile/run.

### Phase 5: Publish

16. Commit to the right folder per the contract.
17. Update the index/TOC if the project has one.
18. Note obsolete docs -- either update or mark as deprecated.

---

## 6. README Discipline

A great README answers in the first screen:

1. **What is this?** One sentence.
2. **Why does it exist?** One paragraph.
3. **How do I run it?** 3-5 commands, copy-paste.
4. **Where do I go next?** Links to deeper docs.

Full template in [assets/readme-template.md](assets/readme-template.md).

### Common README Mistakes

| Mistake | Fix |
|---|---|
| Buries install under a long intro | Put quickstart at the top |
| "See the wiki" | Inline the minimum, link for depth |
| Missing prerequisites | List required versions explicitly |
| No troubleshooting section | Add top 3 common failures |
| Rot -- commands don't work | CI-test the quickstart |

---

## 7. API Documentation

### Sources of Truth

- **OpenAPI 3.1** spec checked in as `production_artifacts/api/openapi.yaml`
- Generated reference rendered via Redoc, Scalar, or similar
- Human-written quickstart that walks through the most common flow

### Every Endpoint Needs

- Purpose (one line)
- Auth requirements
- Request schema + example
- Response schema + example (success and error)
- Error codes with meanings
- Rate limits (if any)
- Idempotency notes (if applicable)

---

## 8. Changelog Discipline

Follow [Keep a Changelog](https://keepachangelog.com) + [Semantic Versioning](https://semver.org):

```
## [1.2.0] - 2025-03-14

### Added
- New /export endpoint for CSV downloads.

### Changed
- /users now returns `createdAt` as ISO 8601 string (was epoch ms).

### Deprecated
- /legacy/export -- use /export instead, will be removed in 2.0.

### Removed
- /beta/flags -- superseded by feature flags service.

### Fixed
- Race condition when two users rename the same resource simultaneously.

### Security
- Upgraded dependency X to patch CVE-2025-XXXX.
```

**Rules**:
- Never edit past release sections
- Every entry is written from the reader's perspective, not the committer's
- Breaking changes are flagged, migration steps linked

---

## 9. `llms.txt` for AI Consumers

Modern docs include a machine-readable summary at `/llms.txt` so AI agents
(including this one) can ingest the project quickly.

Minimum structure:

```
# Project Name

> One-paragraph description of what this is and who it's for.

## Docs

- [Quickstart](/README.md): Run it locally in 10 minutes
- [Architecture](/production_artifacts/Solution_Architecture.md): System design
- [API Reference](/production_artifacts/docs/api/): Endpoint docs

## Key Concepts

- [Domain model](/production_artifacts/Database_ER_Diagram.md)
- [Auth model](/production_artifacts/docs/auth.md)

## Optional

- [ADRs](/production_artifacts/ADRs/)
- [Runbooks](/production_artifacts/docs/runbooks/)
```

---

## 10. Writing Style Rules

| Rule | Why |
|---|---|
| Active voice | "Run the migration" not "The migration should be run" |
| Second person ("you") | Direct, conversational |
| Present tense | "The API returns" not "The API will return" |
| Short sentences | <25 words where possible |
| No hedging weasel words | "usually", "might", "should probably" -- commit or cut |
| Define jargon once, then use it | Or link to glossary |
| Show, don't just tell | Code samples > prose descriptions |
| Lead with outcomes | Start sections with what the reader gets |

---

## 11. Quality Bar

Before marking documentation as done:

- [ ] Every doc names its audience clearly
- [ ] README quickstart works on a clean machine
- [ ] All code snippets run exactly as written
- [ ] All internal links resolve
- [ ] No dead / stale sections (old version numbers, deprecated flags)
- [ ] API reference matches the actual implementation
- [ ] Changelog updated for the current release
- [ ] ADRs cross-referenced from architecture doc
- [ ] `llms.txt` updated to reflect new or moved docs
- [ ] Docs committed under the right folder per contract

---

## 12. Bundled Reference

| File | Contents |
|---|---|
| [references/doc-templates.md](references/doc-templates.md) | README, Changelog, Runbook, Contribution, llms.txt templates |
| [assets/readme-template.md](assets/readme-template.md) | Quick-start README template |

---

## 13. Deliverables

Every completed documentation task produces:

1. Updated or new `README.md` at repo root
2. Updated `CHANGELOG.md`
3. Refreshed `production_artifacts/docs/` content matching current code
4. `llms.txt` at repo root if not present
5. Updated `production_artifacts/memory/AI_CONTEXT.md` with doc state
