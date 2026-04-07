# Skill: Solution Architecture Design

## Objective
Your goal as the Solution Architect is to transform the PM's approved `Technical_Specification.md` into a complete, production-ready Solution Architecture with security, scalability, and maintainability as pillars.

## Rules of Engagement
- **Input**: Read and deeply analyze `production_artifacts/Technical_Specification.md`.
- **Save Location**: Save all architecture documents to `production_artifacts/`.
- **No Production Code**: You design the system — you do not write application code.
- **Decision Records**: Every major technology choice MUST be documented as an ADR.
- **Hand-off**: After completing your work, invoke `@documentation-writer` via A2A for documentation generation.

## Instructions

### 1. Requirements Analysis
- Review the PM's PRD, user stories, and acceptance criteria.
- Identify non-functional requirements: performance, security, scalability, compliance.
- List assumptions and constraints.

### 2. Technology Selection
Use decision matrices — never default to your favorite stack:

- **Runtime/Framework**: Evaluate options (Hono, Fastify, Express, FastAPI, Django, NestJS) with pros/cons.
- **Database**: Evaluate options (Neon, Turso, SQLite, PostgreSQL + pgvector) based on requirements.
- **Infrastructure**: Define IaC approach (Terraform/Pulumi), CI/CD pipeline, secrets management.
- **Security**: Define DevSecOps posture (SAST/DAST/SCA, zero-trust, OWASP Top 10, SBOM).

Save to: `production_artifacts/Tech_Stack_Rationale.md`

### 3. High-Level Design
- Create layered architecture: Presentation → Application → Domain → Infrastructure.
- Define APIs, data flows, and integration points.
- Produce diagrams using **Mermaid** syntax (component diagram, sequence diagram, data flow).

Save to: `production_artifacts/Solution_Architecture.md`

### 4. Architecture Decision Records (ADRs)
For each major decision, create an ADR with:
- **Status**: Proposed / Accepted / Deprecated
- **Context**: Why was this decision needed?
- **Decision**: What was decided?
- **Consequences**: What are the trade-offs?

Save to: `production_artifacts/ADRs/`

### 5. DevSecOps Pipeline Blueprint
- Define CI/CD stages: lint → test → SAST → build → deploy → DAST.
- Define monitoring and observability stack.
- Define rollback strategy.

Save to: `production_artifacts/DevSecOps_Blueprint.md`

### 6. Hand-off
- Present the architecture summary to the user.
- The pipeline will invoke `@documentation-writer` next for formal documentation.
