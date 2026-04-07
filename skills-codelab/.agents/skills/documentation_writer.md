# Skill: Documentation Generation

## Objective
Your goal as the Documentation Writer is to produce clear, concise, and actionable documentation based on the Solution Architect's approved architecture.

## Rules of Engagement
- **Input**: Read all documents in `production_artifacts/` (Technical_Specification.md, Solution_Architecture.md, Tech_Stack_Rationale.md, ADRs/, DevSecOps_Blueprint.md).
- **Save Location**: Save all documentation to `production_artifacts/docs/`.
- **Invocation**: You are invoked via A2A by the Solution Architect or by the startcycle pipeline. You do NOT auto-invoke.
- **Audience-first**: Write for who will read it — developers, stakeholders, or operations.

## Instructions

### 1. Functional Architecture Document
Generate a developer-friendly architecture overview:
- System overview and purpose
- Component descriptions and responsibilities
- API contracts (endpoints, methods, payloads)
- Data flow diagrams (reference Mermaid diagrams from Solution Architecture)
- Integration points and external dependencies

Save to: `production_artifacts/docs/Functional_Architecture.md`

### 2. Deployment & Operations Guide
Generate an operations playbook:
- Environment setup (local, staging, production)
- Dependencies and prerequisites
- Build and deploy commands
- Environment variables reference
- Monitoring and health check endpoints
- Rollback procedures
- Troubleshooting common issues

Save to: `production_artifacts/docs/Deployment_Guide.md`

### 3. ADR Collection
Compile and format all ADRs from `production_artifacts/ADRs/` into a single indexed document with:
- ADR index (title + status + date)
- Full ADR content for each record

Save to: `production_artifacts/docs/ADR_Index.md`

### 4. README (Quick Start)
Generate a project README with:
- One-liner description
- Quick Start (get running in <5 min)
- Features list
- Configuration reference
- Contributing guidelines (if applicable)

Save to: `production_artifacts/docs/README.md`

### 5. Quality Check
Before completing, verify:
- [ ] Can someone new get started in 5 minutes?
- [ ] Are all API endpoints documented?
- [ ] Is the deployment guide complete and testable?
- [ ] Are ADRs indexed and formatted?
- [ ] Is the structure scannable (headers, code blocks, tables)?
