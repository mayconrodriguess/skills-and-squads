# 🚀 Squad Dev v1.4

**Uma equipe de TI completa em uma pasta.**
14 agentes especializados, A2A formalizado, janela de contexto por agente, anti-alucinação por padrão.
Cole dentro do seu projeto, chame a Squad e comece a desenvolver.

---

## O que é isso?

Squad_Dev v1.4 é um conjunto de **14 agentes de IA** que trabalham juntos como uma equipe de desenvolvimento real. Você pode usar a **Squad completa** (`/startcycle`) ou invocar **agentes individuais** (`/architect`, `/backend`, etc.).

### Os 14 agentes

| #   | Agente                  | Slash                          | O que faz                                                    |
| --- | ----------------------- | ------------------------------ | ------------------------------------------------------------ |
| 1   | `@product-owner`        | `/po`                          | Planeja Sprints e paraleliza trabalho                        |
| 2   | `@product-manager`      | `/pm`                          | Detalha User Stories e Critérios de Aceite                   |
| 3   | `@solution-architect`   | `/architect`                   | Define arquitetura e DevSecOps                               |
| 4   | `@documentation-writer` | `/docs`                        | Documenta tudo automaticamente                               |
| 5   | `@database-specialist`  | `/database`                    | Schema, migrations, seed, backup, Docker, indexes (DB-first) |
| 6   | `@backend-specialist`   | `/backend`                     | APIs, autenticação, serviços                                 |
| 7   | `@frontend-specialist`  | `/frontend`                    | UI/UX web com design fundamentado                            |
| 8   | `@ai-page-designer`     | `/designpage`                  | Landing pages e páginas estáticas                            |
| 9   | `@design-hunter`        | `/designhunter`                | Caça Design Systems em Awwwards/CSS Awards/Behance           |
| 10  | `@mobile-developer`     | `/mobile` ou `/buildapp`       | iOS/Android + publicação nas stores                          |
| 11  | `@qa-engineer`          | `/qa`                          | Testes automatizados e correção de bugs                      |
| 12  | `@security-specialist`  | `/security` ou `/securityscan` | DevSecOps, ISO 27001, OWASP _(bloqueante)_                   |
| 13  | `@devops-engineer`      | `/devops`                      | Build, deploy local/cloud, CI/CD                             |
| 14  | `@research-specialist`  | `/research`                    | Pesquisa online verificada (anti-alucinação)                 |

---

## Como Usar

### 1. Cole a pasta no seu projeto

```
MeuProjeto/
├── Squad_Dev_v1.4/   ← copie esta pasta aqui
├── src/
└── ...
```

### 2. Abra qualquer IA com suporte a arquivos

```bash
cd MeuProjeto
claude  # ou cursor, copilot, etc.
```

### 3a. Squad completa (pipeline)

```
/startcycle Sistema de agendamento online para clínicas
```

Roda: PO → PM → Architect → DBA → Backend → Frontend → QA → Security → DevOps.

### 3b. Agente individual

```
/architect Desenhe a arquitetura do módulo de pagamentos
/database Crie o schema multi-tenant com RLS
/research Qual a versão LTS atual do Node.js?
/designhunter Cace referências para um SaaS B2B sério
```

### Comandos disponíveis

| Comando                                                          | Ação                                         |
| ---------------------------------------------------------------- | -------------------------------------------- |
| `/startcycle <ideia>`                                            | Pipeline completo PO → Deploy                |
| `/devsquad <ideia>`                                              | Alias para `/startcycle`                     |
| `/po` `/pm` `/architect` `/docs`                                 | Planejamento                                 |
| `/database` `/backend` `/frontend` `/designpage` `/designhunter` | Build                                        |
| `/mobile` `/buildapp`                                            | Apps iOS/Android                             |
| `/qa` `/security` `/securityscan` `/securitygate N`              | Validação                                    |
| `/devops`                                                        | Deploy/CI/CD                                 |
| `/research <pergunta>`                                           | Pesquisa online verificada                   |
| `/commit-push-pr`                                                | Commit + push + PR (requer QA + Security ✅) |

---

## Estrutura da Pasta

```
Squad_Dev_v1.4/
├── .agents/
│   ├── agents.md                    ← 14 perfis de agentes
│   ├── A2A_PROTOCOL.md              ← matriz quem-fala-com-quem
│   ├── skills/                      ← uma skill por agente
│   │   ├── write_specs/             (PO + PM)
│   │   ├── solution_architect/
│   │   ├── documentation_writer/
│   │   ├── database_specialist/
│   │   ├── backend_specialist/
│   │   ├── frontend_specialist/
│   │   ├── ai_page_designer/
│   │   ├── design_hunter/
│   │   ├── mobile_developer/
│   │   ├── qa_engineer/
│   │   ├── security_specialist/
│   │   ├── devops_deploy/
│   │   ├── research_specialist/
│   │   └── dev-squad/               ← orquestrador
│   └── workflows/
│       ├── startcycle.md            ← pipeline completo
│       └── sprint-security-gate.md
│
├── .claude/
│   ├── commands/                    ← 20 slash commands
│   └── settings.json                ← hooks (Prettier/ESLint/blocks)
│
├── app_build/                       ← TODO código do projeto aqui
│
├── production_artifacts/
│   ├── memory/
│   │   ├── AI_CONTEXT.md            ← índice global enxuto
│   │   ├── project-brief.md
│   │   ├── agents/                  ← janela de contexto por agente
│   │   │   ├── _template.md
│   │   │   ├── product-owner-context.md
│   │   │   ├── solution-architect-context.md
│   │   │   └── ...
│   │   ├── sprints/
│   │   │   └── sprint-N-context.md
│   │   ├── research/                ← cache de pesquisas verificadas
│   │   └── subagents/               ← findings de subagentes
│   └── design_library/              ← DSs extraídos pelo design-hunter
│
├── subagents/                       ← prompts universais (qualquer IA)
├── CLAUDE.md                        ← config auto-loaded no Claude Code
├── HOW_TO_USE_WITH_DIFFERENTS_AIs.md
└── README.md
```

---

## Janela de Contexto por Agente (continuidade entre LLMs)

Cada agente mantém o próprio arquivo em `production_artifacts/memory/agents/<agente>-context.md` com:

- Última tarefa concluída
- Decisões tomadas (com justificativa)
- A2A handoffs (inbox/outbox)
- Pendências e próximo passo
- Contexto crítico anti-alucinação
- Arquivos tocados
- Cache de research consultado

**Resultado:** se você trocar de Claude para Gemini para GPT no meio do projeto, qualquer agente retoma exatamente de onde parou lendo seu próprio context file.

---

## A2A — Comunicação entre agentes

Toda invocação cross-agent usa o formato padrão definido em `.agents/A2A_PROTOCOL.md`:

```
De: @agente-origem
Contexto: [1-2 linhas]
Pergunta: [1 frase]
Decisão dependente: [o que será decidido com a resposta]
Formato esperado: [bullets / tabela / diagrama]
Urgência: bloqueante | informativa
```

A invocação é registrada no contexto do remetente (outbox) e do destinatário (inbox).

---

## DB-first (regra bloqueante)

Quando o projeto tem banco de dados, `@database-specialist` **roda antes** de `@backend-specialist` e entrega:

1. Schema versionado (DDL + ER diagram)
2. Migrations idempotentes
3. Seed de dados de teste
4. Backup automatizado
5. Docker Compose com volumes persistentes
6. Indexes nas FKs e queries críticas
7. Constraints e validações em nível de DB
8. RLS / multi-tenant quando aplicável

`@backend-specialist` só inicia após handoff A2A do DBA.

---

## Anti-alucinação

Antes de **qualquer** decisão técnica que dependa de informação externa (versão de lib, CVE, preço, benchmark), o agente invoca `@research-specialist`. Sem URL, não decide.

Cache de pesquisas em `production_artifacts/memory/research/<yyyy-mm-dd>-<tópico>.md`.

---

## Subagentes globais (Claude Code)

Cada subagente roda em janela de contexto isolada. Disponíveis em qualquer projeto após instalação:

| Subagente                 | Quando usar                               |
| ------------------------- | ----------------------------------------- |
| `@squad-explore`          | Encontrar onde algo está no código        |
| `@squad-code-reviewer`    | Revisão antes de PR                       |
| `@squad-spec-analyst`     | Analisar spec sem trazer tudo ao contexto |
| `@squad-security-scanner` | Varredura rápida de segurança             |
| `@squad-test-generator`   | Gerar testes por módulo ou Sprint         |
| `@squad-doc-writer`       | Gerar README, OpenAPI, deployment guide   |
| `@squad-db-analyst`       | Revisar schema, N+1, migrations           |
| `@squad-api-mapper`       | Mapear todos os endpoints existentes      |
| `@squad-design-hunter`    | Caçar Design Systems em sites premiados   |
| `@squad-researcher`       | Pesquisa online verificada                |

**Outras IAs:** prompts universais em `subagents/<nome>-prompt.md` — cole em nova conversa.

---

## Hooks (camada determinística)

Pré-configurados em `.claude/settings.json`. Diferente de instruções no `CLAUDE.md`, hooks **sempre executam**.

| Hook                 | Evento                                       | O que faz                                                |
| -------------------- | -------------------------------------------- | -------------------------------------------------------- |
| Prettier             | `PostToolUse` Edit/Write                     | Formata após edição                                      |
| ESLint --fix         | `PostToolUse` Edit/Write `.ts/.tsx/.js/.jsx` | Lint automático                                          |
| Command Log          | `PostToolUse` Bash                           | Loga em `memory/command-log.txt`                         |
| Proteção de arquivos | `PreToolUse` Edit/Write                      | Bloqueia `.env`, chaves SSH, `node_modules`              |
| Comandos perigosos   | `PreToolUse` Bash                            | Bloqueia force push em main, `DROP DATABASE`, `rm -rf /` |
| Notificação desktop  | `Stop`                                       | Avisa quando Claude termina                              |

---

## Regras Fundamentais

| Regra                | Descrição                                                       |
| -------------------- | --------------------------------------------------------------- |
| 📁 Código            | Sempre em `app_build/`                                          |
| 📋 Documentação      | Sempre em `production_artifacts/`                               |
| 🧠 Memória global    | `production_artifacts/memory/AI_CONTEXT.md`                     |
| 🪟 Janela por agente | `production_artifacts/memory/agents/<agente>-context.md`        |
| 🔗 A2A               | Toda invocação registrada (inbox + outbox)                      |
| 🗄️ DB-first          | Se há DB, `@database-specialist` antes do `@backend-specialist` |
| 🚫 Anti-alucinação   | Info externa? → `@research-specialist`                          |
| 🔐 Security Gate     | Bloqueante ao final de CADA Sprint                              |
| 🔴 Pré-publicação    | Auditoria obrigatória antes de qualquer deploy                  |

---

## Compatibilidade com IAs

Funciona com qualquer IA que leia arquivos. Guia completo em **[HOW_TO_USE_WITH_DIFFERENTS_AIs.md](./HOW_TO_USE_WITH_DIFFERENTS_AIs.md)** ou versão web **[HOW_TO_USE_WITH_DIFFERENTS_AIs.html](./HOW_TO_USE_WITH_DIFFERENTS_AIs.html)**.

| IA                                 | Status                                                   |
| ---------------------------------- | -------------------------------------------------------- |
| **Claude Code**                    | Nativo — skills + slash commands + hooks auto-detectados |
| **Claude Desktop (MCP)**           | Nativo via servidor MCP filesystem                       |
| **Cursor**                         | Via @-rules + file refs                                  |
| **GitHub Copilot (VS Code)**       | Via custom instructions + @workspace                     |
| **Google Antigravity**             | Via agents e workspace completo                          |
| **Gemini CLI / AI Studio**         | System instruction + file upload                         |
| **ChatGPT (Plus/Team/Enterprise)** | Projects + file upload                                   |
| **Windsurf / Cody / qualquer IA**  | Copiar `.agents/agents.md` como system prompt            |

### Migrando entre IAs no meio do projeto

1. Leia `production_artifacts/memory/AI_CONTEXT.md` (visão global)
2. Leia `sprints/sprint-N-context.md` (Sprint ativo)
3. Leia `agents/<agente>-context.md` (handoff do agente)
4. Diga: "Continue conforme contexto"

---

## Segurança

`@security-specialist` + `@devops-engineer` implementam:

- OWASP Top 10
- ISO/IEC 27001:2022
- NIST CSF 2.0
- CIS Benchmarks
- STRIDE (Threat Modeling)
- LGPD / GDPR

Security Gate é **bloqueante** — nenhum Sprint termina e nenhum deploy acontece sem aprovação do `@security-specialist`.

---

## Memória e Continuidade

Três níveis pra não estourar contexto:

**Nível 1, `AI_CONTEXT.md`** — índice global, máx 40 linhas, lido sempre.
**Nível 2, `sprints/sprint-N-context.md`** — detalhe por Sprint, carregado sob demanda.
**Nível 3, `agents/<agente>-context.md`** — janela própria de cada agente, garante continuidade entre LLMs.

**Regra de Sprint:** cada Sprint é uma fatia vertical testável e deployável. Janela máxima até produção: 2 a 3 Sprints.
