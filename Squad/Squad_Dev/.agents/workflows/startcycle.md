---
description: >
  Pipeline completo da Squad Dev — do conceito ao deploy.
  Ativar com: /startcycle <ideia>  ou  /devsquad <ideia>
---

# Squad Dev — Pipeline Completo

Quando o usuário digitar `/startcycle <ideia>` ou `/devsquad <ideia>`, orquestre o pipeline
usando os agentes em `.agents/agents.md` e as skills em `.agents/skills/`.

---

## FASE 0 — Inicialização (Sempre primeiro)

Antes de qualquer trabalho, garantir que a estrutura existe:

```
Squad_Dev/
├── app_build/               ← código do projeto
├── production_artifacts/
│   ├── memory/
│   │   ├── AI_CONTEXT.md    ← CRIAR se não existe
│   │   ├── project-brief.md ← CRIAR se não existe
│   │   └── sprints/         ← pasta para histórico de sprints
└── .agents/
```

Criar `production_artifacts/memory/AI_CONTEXT.md` com o template inicial (ver seção [Memória](#memória)).

---

## FASE 1 — Product Owner: Backlog e Roadmap de Sprints

**Agir como `@product-owner`** | Skill: `write_specs`

1. Receber a `<ideia>` do usuário
2. Elaborar o **Product Backlog** com todas as funcionalidades identificadas
3. Priorizar com MoSCoW (MUST / SHOULD / COULD / WON'T)
4. Decompor em **Sprints** com escopo claro:
   - Quais features em qual Sprint
   - Dependências entre Sprints
   - Quais streams podem rodar em paralelo
5. Identificar agentes necessários para cada Sprint

**Saídas:**
- `production_artifacts/Product_Backlog.md`
- `production_artifacts/Sprint_Roadmap.md`
- `production_artifacts/memory/project-brief.md`
- `production_artifacts/memory/AI_CONTEXT.md` ← atualizar

**⏸ PAUSE: aguardar "Aprovado" do usuário antes de continuar.**

---

## FASE 2 — Product Manager: Detalhamento do Sprint 1

**Agir como `@product-manager`** | Skill: `write_specs`

1. Receber o Sprint 1 do `@product-owner`
2. Elaborar User Stories detalhadas:
   > Como **[persona]**, quero **[ação]**, para que **[benefício]**.
3. Definir Critérios de Aceite (Gherkin: Given / When / Then)
4. Salvar em `production_artifacts/sprint-1/Sprint_Plan.md`
5. Atualizar `production_artifacts/memory/AI_CONTEXT.md`

**⏸ PAUSE: aguardar "Aprovado" antes de continuar.**

---

## FASE 3 — Solution Architect: Arquitetura

**Agir como `@solution-architect`** | Skill: `solution_architect`

> Executar apenas no Sprint 1 ou quando há mudança estrutural.

1. Ler `Technical_Specification.md`
2. Definir stack, DevSecOps posture, ADRs, diagramas Mermaid
3. Determinar se o projeto requer: Web / Mobile / Ambos
4. Invocar `@documentation-writer` (A2A) para gerar documentação
5. Salvar em `production_artifacts/`

**Saídas obrigatórias:**
- `production_artifacts/Solution_Architecture.md`
- `production_artifacts/Tech_Stack_Rationale.md`
- `production_artifacts/ADRs/`
- `production_artifacts/DevSecOps_Pipeline_Blueprint.md`

**⏸ PAUSE: aguardar "Aprovado" antes de prosseguir.**

---

## FASE 4 — Desenvolvimento do Sprint

Execute os especialistas conforme a arquitetura aprovada.
O PO pode **paralelizar** streams sem dependência bloqueante.

### 4a. `@database-specialist` | Skill: `database_specialist`
*(Pular apenas se não há banco de dados ou é BaaS sem schema customizado)*
- Schema, migrations, Docker setup
- Saída: código em `app_build/`

### 4b. `@backend-specialist` | Skill: `backend_specialist`
*(Pular apenas se frontend-only com BaaS)*
- APIs, serviços, autenticação, validação
- Saída: código em `app_build/`

### 4c. Especialistas de cliente *(conforme arquitetura)*

| Tipo | Agente | Skill |
|------|--------|-------|
| **Web App** | `@frontend-specialist` | `frontend_specialist` |
| **Landing Pages** | `@ai-page-designer` | `ai_page_designer` |
| **Mobile** | `@mobile-developer` | `mobile_developer` |

*(Se Web + Mobile → executar sequencialmente 4c-Web → 4c-Mobile)*

### Paralelismo no Sprint
O `@product-owner` pode decidir:
```
Stream A (independente): @backend-specialist implementa auth API
Stream B (independente): @frontend-specialist implementa tela de login
→ Executar em paralelo (entregam no mesmo Sprint)
→ @qa-engineer testa após ambos concluírem
```

---

## FASE 5 — QA Gate (Obrigatório por Sprint)

**Agir como `@qa-engineer`** | Skill: `qa_engineer`

1. Ler spec e arquitetura aprovadas
2. Auditar código contra especificação
3. Criar/atualizar testes em `app_build/`
4. Corrigir defeitos confirmados
5. Salvar `production_artifacts/sprint-N/QA_Report.md`
6. **Só avançar após TODOS os testes passando**

---

## FASE 6 — Security Gate (Obrigatório por Sprint) 🔶 BLOQUEANTE

**Agir como `@security-specialist`** | Skill: `security_specialist`

> ⚠️ Este passo é BLOQUEANTE. O Sprint NÃO está concluído até ser aprovado aqui.

Protocolo completo: `.agents/skills/dev-squad/references/security-gate.md`

1. SAST — análise estática do código
2. SCA — dependências com CVEs
3. Secrets Scan — credenciais expostas
4. OWASP Top 10 — checklist aplicado
5. ISO 27001 + NIST CSF + CIS Benchmarks
6. Salvar `production_artifacts/sprint-N/Security_Gate_Report.md`

**Veredito:**
- ✅ **APROVADO** → avançar para Sprint Review
- ⚠️ **APROVADO COM RESSALVAS** → documentar riscos e avançar
- ❌ **BLOQUEADO** → retornar à Fase 4 para correção

---

## FASE 7 — Sprint Review

**Agir como `@product-owner`**

1. Apresentar: features entregues + QA Report + Security Gate Report
2. `@documentation-writer` atualiza docs em `production_artifacts/`
3. Atualizar `production_artifacts/memory/AI_CONTEXT.md`
4. Atualizar `production_artifacts/memory/sprints/sprint-N-summary.md`

**⏸ PAUSE: aguardar feedback do usuário.**

- Ajustes necessários → retornar à Fase 4 (mini-ciclo)
- Aprovado → próximo Sprint (voltar à Fase 2) **ou** avançar para Deploy (Fase 8/9)

---

## FASE 8 — Auditoria Pré-Publicação 🔴 BLOQUEANTE

> Executar **antes do primeiro deploy em produção** e a cada release major.

**Agir como `@security-specialist`** | Protocolo: `.agents/skills/dev-squad/references/pre-publish-audit.md`

1. DAST — testes dinâmicos na aplicação em execução
2. Threat Modeling — STRIDE nos fluxos críticos
3. Pentest superficial — OWASP Top 10 em runtime
4. Revisão de infraestrutura — containers, segredos, permissões
5. Conformidade: ISO 27001 + NIST CSF + LGPD/GDPR
6. Salvar `production_artifacts/Pre_Publish_Security_Audit.md`

**⏸ PAUSE: apenas prosseguir após aprovação do usuário.**

---

## FASE 9 — Deploy

**Agir como `@devops-engineer`** | Skill: `devops_deploy`

1. Selecionar modo de deploy (Local / Cloud Run / VPS / Store)
2. Build, configurar CI/CD com security gates
3. Deploy e verificar
4. Atualizar `production_artifacts/Deployment_Guide.md`
5. Atualizar `production_artifacts/memory/AI_CONTEXT.md` com estado final

---

## Memória

O arquivo `production_artifacts/memory/AI_CONTEXT.md` deve ser **atualizado após cada interação** com qualquer agente. Ele é o ponto de entrada para qualquer IA retomar o trabalho.

### Estrutura do AI_CONTEXT.md
```markdown
# AI Context — [Nome do Projeto]
**Última atualização:** YYYY-MM-DD HH:MM
**Agente que atualizou:** @nome-do-agente
**Sprint atual:** N
**Status:** [Planejamento | Desenvolvimento | QA | Security | Review | Deploy]

## Resumo do Projeto
[2-3 frases sobre o projeto]

## Stack Tecnológica
- Backend: [ex: Node.js + Fastify + PostgreSQL]
- Frontend: [ex: Next.js 15 + Tailwind]
- Deploy: [ex: Cloud Run + Docker]

## Sprint Atual — Objetivos
[Features deste Sprint]

## Decisões Importantes Tomadas
[ADRs e decisões que não estão no código]

## Onde Paramos
[Último estado exato — qual fase, o que falta]

## Próximos Passos
[O que o próximo agente/sessão deve fazer primeiro]

## Contexto Crítico
[Informações que uma IA nova precisa saber para não repetir erros]
```

---

## Notas Importantes

- **Todos os agentes** respeitam `Constraint` e `Goal` em `.agents/agents.md`
- **`@security-specialist`** nunca pode ser pulado — é bloqueante
- **`production_artifacts/`** é a única fonte da verdade para documentação
- **`app_build/`** é onde todo código do projeto fica
- **`AI_CONTEXT.md`** deve ser atualizado após cada fase
- Cloud Run deployment → usar seção correspondente em `devops_deploy`
- `/designpage` → `@ai-page-designer` standalone
- `/buildapp` → `@mobile-developer` standalone
- `/securityscan` → `@security-specialist` standalone
- `/securitygate N` → Security Gate do Sprint N
