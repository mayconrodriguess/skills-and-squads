# Skill: DevOps Deployment

## Objective
Your goal as the DevOps Master is to intelligently package the application and deploy it based on the chosen stack and deployment target.

## Rules of Engagement
- **Input**: Read the `production_artifacts/Technical_Specification.md`, `production_artifacts/Solution_Architecture.md`, and inspect the files in `app_build/`.
- **Safety First**: Always verify before executing. Never rush deployment.
- **Default**: Deploy locally unless the user explicitly requests Cloud Run or another platform.

## Instructions

### 1. Stack Detection
- Inspect the Solution Architecture and the files in `app_build/` to determine:
  - Language/Runtime (Node.js, Python, Bun, etc.)
  - Framework (Next.js, Fastify, FastAPI, Django, etc.)
  - Database (if any requires setup)
  - Package manager (npm, pnpm, yarn, pip, etc.)

### 2. Environment Setup
- Create `.env` file from the environment variables reference in the Deployment Guide (if exists).
- Verify all required environment variables are set (use placeholder values for secrets).

### 3. Install Dependencies
Navigate into `app_build/` and run the appropriate command:
- **Node.js**: `npm install` (or `pnpm install` / `yarn install`)
- **Python**: `pip install -r requirements.txt` (or `poetry install`)
- **Other**: Whatever is appropriate for the detected stack.

### 4. Database Setup (if applicable)
- Run migrations if the project includes them.
- Seed initial data if a seed script exists.

### 5. Build (if applicable)
- **Next.js**: `npm run build`
- **TypeScript**: `npx tsc` (if separate compilation step)
- **Other**: Run the build command specified in `package.json` or equivalent.

### 6. Host Locally
Execute the appropriate command to start a background server:
- **Node.js**: `npm run dev` or `npm start`
- **Python**: `python3 app.py` or `uvicorn main:app --reload`
- **Next.js**: `npm run dev`
- **Other**: Whatever is appropriate.

### 7. Verify Deployment
- Check that the server starts without errors.
- Verify the health endpoint (if exists) returns 200.
- Confirm the application is accessible on the reported URL.

### 8. Report
Output the result to the user:
```
🚀 DEPLOYMENT SUCCESSFUL!
- Stack: [detected stack]
- URL: [clickable localhost link]
- Status: Running
- To stop: [kill command or Ctrl+C instructions]
```

If deployment fails:
```
❌ DEPLOYMENT FAILED
- Error: [error description]
- Attempted fix: [what you tried]
- Suggestion: [next steps]
```

---

## Alternative: Cloud Run Deployment
If the user requests production deployment to Google Cloud Run:

1. **Verify Environment**: Ensure necessary files are in `app_build/`.
2. **Containerize**: Navigate to `app_build/` and run `gcloud run deploy --source .`.
3. **Configure**: Automatically select default region and allow unauthenticated invocations.
4. **Report**: Output the live production Google Cloud Run URL to the user.
