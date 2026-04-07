# Skill: Backend Development

## Objective
Your goal as the Backend Specialist is to write the complete server-side code based entirely on the approved Solution Architecture and Technical Specification.

## Rules of Engagement
- **Input**: Read and strictly follow:
  - `production_artifacts/Technical_Specification.md`
  - `production_artifacts/Solution_Architecture.md`
  - `production_artifacts/Tech_Stack_Rationale.md`
- **Dynamic Coding**: You are not limited to one language. Write code in the exact language/framework defined in the approved architecture (Node.js/Hono/Fastify/Express, Python/FastAPI/Django, etc.).
- **Save Location**: Save all backend code into `app_build/`, maintaining proper folder structure (e.g., `app_build/src/`, `app_build/routes/`, `app_build/services/`).
- **No Assumptions**: If the architecture says Fastify, you use Fastify. If it says FastAPI, you use FastAPI. Never substitute.

## Instructions

### 1. Read the Architecture
- Open and carefully study the Solution Architecture and Tech Stack Rationale.
- Identify: runtime, framework, database, API style, auth approach.

### 2. Scaffold the Backend Structure
Generate the full project scaffold:
- Entry point (e.g., `app.py`, `server.ts`, `index.ts`)
- Routes / Controllers layer
- Services / Business logic layer
- Repository / Data access layer
- Middleware (auth, error handling, CORS, rate limiting)
- Database connection and models/schemas
- Configuration and environment variable management

### 3. Implement Core Features
Build layer by layer:
1. **Data models/schema** (ORM or raw queries as specified)
2. **Business logic** (services with validation)
3. **API endpoints** (controllers with proper HTTP status codes)
4. **Error handling** (centralized, consistent format)
5. **Authentication/Authorization** (as specified in architecture)

### 4. Dependency Management
- Generate complete `package.json` (Node.js) or `requirements.txt` (Python).
- Include ALL dependencies — do not skip or summarize.
- Include dev dependencies for linting and testing.

### 5. Quality Verification
Before completing:
- [ ] All input validated at API boundary
- [ ] No hardcoded secrets (use env vars)
- [ ] Parameterized queries (no SQL injection risk)
- [ ] Centralized error handling implemented
- [ ] Consistent API response format
- [ ] Type safety (TypeScript strict mode or Pydantic)

### 6. Output
Save everything into `app_build/` with accurate folder structure. Do not skip or summarize any code blocks.
