---
description: Start the Autonomous AI Developer Pipeline sequence with a new idea
---

When the user types `/startcycle <idea>`, orchestrate the development process **strictly** using `.agents/agents.md` and `.agents/skills/`.

### Execution Sequence:

1. **Act as the Product Manager (@product-manager)**  
   Execute the `write_specs.md` skill using the `<idea>`.  
   *(Wait for the user to explicitly type "Approved". If the user adds comments or feedback directly to the Markdown file, act as the PM again to re-read and revise the document. Loop this step until they type "Approved".)*
   *Crie um arquivo na Raiz, \AI_CONTEXT.md para salvar o Contexto da conversa, e poder ser usado para consulta por outro Agent. Deve ser salvo a cada nova interação.
   * Crie os arquivos requirements.txt e setup.ipynb na Raiz contendo as especificações do Projeto. Para ser usado na migração ou implantação de um ambiente do zero.

2. **Shift context and act as the Solution Architect (@solution-architect)**  
   Execute the `solution_architect.md` skill.  
   *(Full architecture design: tech stack selection, DevSecOps posture, high-level design, ADRs and Mermaid diagrams.)*  
   *(At this stage, determine if the project requires: Web app, Mobile app, or Both — this defines which specialists will be invoked in steps 5-6.)*

3. **Shift context and act as the Documentation Writer (@documentation-writer)**  
   Execute the `documentation_writer.md` skill to generate:  
   - Functional Architecture Document  
   - Deployment & Operations Guide  
   - ADR collection  
   *(Documentation Type Selection is handled automatically inside this agent via A2A.)*

4. **Pause for user review**  
   Present the architecture + documentation to the user.  
   *(Wait for explicit confirmation: "Approved" or feedback. If feedback is given, loop back to step 2 or 3 as needed.)*

5. **Shift context and act as the Database Specialist (@database-specialist)**  
   Execute the `database_specialist.md` skill.  
   *(Designs schema, selects database technology, creates migrations, generates Docker setup, configures backup scripts.)*  
   *(Skip this step ONLY if the project has no database or uses BaaS like Firebase/Supabase with no custom schema.)*

6. **Shift context and act as the Backend Specialist (@backend-specialist)**  
   Execute the `backend_specialist.md` skill.  
   *(Follows the approved architecture strictly. Uses the database schema from step 5. Saves all backend code into `app_build/`.)*  
   *(Skip this step ONLY if the project is frontend-only with BaaS like Firebase/Supabase.)*

7. **Shift context and build the client application(s)**  
   Based on the approved architecture, invoke the appropriate specialist(s):

   **7a. Web Application** → Act as the **Frontend Specialist (@frontend-specialist)**  
   Execute `frontend_specialist.md`. Saves frontend code into `app_build/`.

   **7b. Professional Web Pages / Landing Pages** → Act as the **AI Page Designer (@ai-page-designer)**  
   Execute `ai_page_designer.md`. Asks for Design System path and user's color, applies recombination, produces standalone HTML pages.  
   *(Can be used alone for static sites or alongside frontend-specialist for app + marketing pages.)*

   **7c. Mobile Application** → Act as the **Mobile Developer (@mobile-developer)**  
   Execute `mobile_developer.md`. Evaluates and selects the optimal framework (React Native/Flutter/Native), builds the app, and generates store publication guides.

   *(If the project requires multiple client types — e.g., Web + Mobile — execute each sub-step in sequence: 6a → 6c or 6b → 6c.)*

8. **Shift context and act as the QA Engineer (@qa-automation-engineer)**  
   Execute the `qa_engineer.md` skill.  
   *(Full automated test suite + code audit against the specification. Covers all platforms built in step 7.)*

9. **Shift context and act as the DevOps Master (@devops-engineer)**  
   Execute the `devops_deploy.md` skill.  
   *(Build, deploy locally, and provide the access URL to the user.)*  
   *(For mobile projects, this includes build instructions and store publication steps.)*

---

### Important Notes:
- All agents communicate via A2A (Agent-to-Agent) as defined in `.agents/agents.md`.
- Never skip the Solution Architect step — it is mandatory between PM approval and Documentation.
- The pipeline only advances after explicit user confirmation at **step 1** and **step 4**.
- Every agent must respect the `Constraint` and `Goal` defined in `.agents/agents.md`.
- If the user requests Cloud Run deployment instead of local, use `deploy_cloud_run.md` at step 8.
- The AI Page Designer can be invoked standalone (outside startcycle) for page creation with `/designpage` command.
- The Mobile Developer can be invoked standalone (outside startcycle) for mobile-only projects with `/buildapp` command.