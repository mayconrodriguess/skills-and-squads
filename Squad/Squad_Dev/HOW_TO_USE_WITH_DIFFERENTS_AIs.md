# Squad Dev v1.4 — Guia Completo de Instalação e Uso

Uma equipe de TI completa em uma pasta. **14 agentes**, A2A formalizado, janela de contexto por agente, anti-alucinação por padrão. Cole `Squad_Dev_v1.4/` no projeto, configure a IA que você usa, e comece a desenvolver.

> **Fonte da verdade:** `.agents/agents.md` + `.agents/A2A_PROTOCOL.md` + `.agents/workflows/` + `.agents/skills/`
> Qualquer IA que ler esses arquivos vira a Squad.

## Os 14 agentes

| #   | Agente                  | Slash                       | Função                                   |
| --- | ----------------------- | --------------------------- | ---------------------------------------- |
| 1   | `@product-owner`        | `/po`                       | Sprints e paralelização                  |
| 2   | `@product-manager`      | `/pm`                       | User Stories + ACs                       |
| 3   | `@solution-architect`   | `/architect`                | Arquitetura e DevSecOps                  |
| 4   | `@documentation-writer` | `/docs`                     | Documentação contínua                    |
| 5   | `@database-specialist`  | `/database`                 | Schema/migrations/seed/backup (DB-first) |
| 6   | `@backend-specialist`   | `/backend`                  | APIs, auth, serviços                     |
| 7   | `@frontend-specialist`  | `/frontend`                 | UI/UX web                                |
| 8   | `@ai-page-designer`     | `/designpage`               | Landing pages standalone                 |
| 9   | `@design-hunter`        | `/designhunter`             | Caça DSs em Awwwards/CSS Awards/Behance  |
| 10  | `@mobile-developer`     | `/mobile` `/buildapp`       | iOS/Android                              |
| 11  | `@qa-engineer`          | `/qa`                       | Testes e correção                        |
| 12  | `@security-specialist`  | `/security` `/securityscan` | OWASP/ISO 27001 (bloqueante)             |
| 13  | `@devops-engineer`      | `/devops`                   | CI/CD, deploy                            |
| 14  | `@research-specialist`  | `/research`                 | Pesquisa online verificada               |

---

## Regra persistente — texto padrão (serve pra todas as IAs)

O texto abaixo é o mesmo em toda ferramenta. O que muda é **onde salvar**.

### Como iniciar o pipeline completo

```
Execute Squad_Dev_v1.4/.agents/workflows/startcycle.md para: [ideia]
```

Isso ativa os 14 agentes em sequência: PO → PM → Architect → DBA → Backend → Frontend → QA → Security → DevOps.

### Como invocar um agente individual

```
Aja como @solution-architect. Leia Squad_Dev_v1.4/.agents/skills/solution_architect/SKILL.md e projete: [tarefa]
Aja como @database-specialist. Leia Squad_Dev_v1.4/.agents/skills/database_specialist/SKILL.md e crie: [tarefa]
Aja como @research-specialist. Leia Squad_Dev_v1.4/.agents/skills/research_specialist/SKILL.md e pesquise: [pergunta]
```

### Regra base que deve estar em toda ferramenta

```
Você é a Squad Dev v1.4. Antes de qualquer ação:
1. Leia Squad_Dev_v1.4/.agents/agents.md — identifique o agente certo.
2. Leia a skill em Squad_Dev_v1.4/.agents/skills/<skill>/SKILL.md.
3. Leia Squad_Dev_v1.4/production_artifacts/memory/AI_CONTEXT.md — retome contexto.
4. Se há DB: @database-specialist roda ANTES de @backend-specialist.
5. Informação externa? Invoque @research-specialist (nunca alucine).
6. Cada agente atualiza production_artifacts/memory/agents/<nome>-context.md ao terminar.
7. Código em Squad_Dev_v1.4/app_build/. Docs em Squad_Dev_v1.4/production_artifacts/.
8. Security Gate é bloqueante antes de deploy.
```

---

## 1. Claude Code (instalação completa)

Suporte nativo — subagentes, slash commands, hooks e CLAUDE.md auto-detectados. **O próprio Claude Code faz a instalação por você.**

### Passo 1 — Cole a pasta no projeto

```
MeuProjeto/
├── Squad_Dev_v1.4/     ← copie aqui
├── src/
└── ...
```

### Passo 2 — Abra o Claude Code e peça pra instalar

```bash
cd MeuProjeto
claude
```

Então diga ao Claude Code (uma única vez):

```
Instale a Squad Dev v1.4 neste projeto.
A pasta Squad_Dev_v1.4/ já está aqui.
Leia Squad_Dev_v1.4/CLAUDE.md para entender o que precisa ser feito.
```

Claude vai entender e executar automaticamente:

1. Copiar `.claude/commands/` para a raiz do projeto → slash commands disponíveis imediatamente
2. Criar/mesclar `.claude/settings.json` com os hooks (Prettier, ESLint, bloqueios)
3. Criar `CLAUDE.md` na raiz apontando para a Squad
4. Registrar os 10 subagentes globais em `~/.claude/agents/`

> **Por que isso funciona?** Claude Code lê e executa arquivos. O `CLAUDE.md` dentro da Squad descreve exatamente o que instalar — Claude usa suas ferramentas de arquivo para fazer isso sem precisar de scripts ou CLI extras.

### Passo 3 — Use (já instalado)

Pipeline completo:

```
/startcycle Sistema de agendamento online para clínicas
```

Agente individual:

```
/architect  Projete a arquitetura do módulo de pagamentos
/database   Crie o schema multi-tenant com RLS
/backend    Implemente o endpoint de autenticação JWT
/research   Qual a versão LTS do Node.js hoje?
/designhunter  Cace referências para SaaS B2B sério
```

Security Gate bloqueante:

```
/securitygate 1
```

**Todos os slash commands disponíveis:**

| Comando                                                          | Ação                          |
| ---------------------------------------------------------------- | ----------------------------- |
| `/startcycle <ideia>`                                            | Pipeline completo PO → Deploy |
| `/devsquad <ideia>`                                              | Alias para `/startcycle`      |
| `/po` `/pm` `/architect` `/docs`                                 | Planejamento (individual)     |
| `/database` `/backend` `/frontend` `/designpage` `/designhunter` | Build (individual)            |
| `/mobile` `/buildapp`                                            | Apps iOS/Android              |
| `/qa` `/security` `/securityscan` `/securitygate N`              | Validação                     |
| `/devops`                                                        | Deploy/CI/CD                  |
| `/research <pergunta>`                                           | Pesquisa online verificada    |
| `/commit-push-pr`                                                | Commit + push + PR            |

**Subagentes globais (chame com `@` em qualquer projeto):**

```
@squad-explore          → encontrar onde está qualquer lógica
@squad-code-reviewer    → revisão antes de PR
@squad-spec-analyst     → analisar especificação
@squad-security-scanner → varredura OWASP / ISO 27001
@squad-test-generator   → gerar testes por módulo
@squad-doc-writer       → README, OpenAPI, changelog
@squad-db-analyst       → schema, N+1, migrations
@squad-api-mapper       → mapear endpoints da API
@squad-design-hunter    → caçar Design Systems em sites premiados
@squad-researcher       → pesquisa online verificada
```

**Hooks ativos automaticamente após instalação:**

- Prettier após cada Edit/Write
- ESLint --fix em `.ts/.tsx/.js/.jsx`
- Bloqueio de `.env`, `id_rsa`, `node_modules`
- Bloqueio de `rm -rf /`, force push em main, DROP DATABASE
- Log em `production_artifacts/memory/command-log.txt`
- Notificação desktop ao terminar tarefa

### Instalação manual (alternativa)

Se preferir instalar sem pedir ao Claude, os arquivos prontos estão em:

| O que copiar                           | Para onde                                       |
| -------------------------------------- | ----------------------------------------------- |
| `Squad_Dev_v1.4/.claude/commands/`     | `MeuProjeto/.claude/commands/`                  |
| `Squad_Dev_v1.4/.claude/settings.json` | `MeuProjeto/.claude/settings.json`              |
| `Squad_Dev_v1.4/subagents/*-prompt.md` | `~/.claude/agents/squad-*.md` (com frontmatter) |

Subagentes precisam do frontmatter YAML em `~/.claude/agents/`:

```markdown
---
name: squad-researcher
description: Pesquisa online verificada — docs oficiais, versões, CVEs
---

[conteúdo de subagents/researcher-prompt.md]
```

---

## 2. Google Antigravity

Nativo. Lê `.agents/` e segue os workflows como Missions.

1. Cole `Squad_Dev_v1.4/` na raiz do workspace e abra no Antigravity.
2. Invoque o pipeline completo:

   ```
   Execute Squad_Dev_v1.4/.agents/workflows/startcycle.md para: [ideia].
   Identifique os agentes em .agents/agents.md e siga as skills em .agents/skills/.
   ```

3. Security Gate:

   ```
   Execute Squad_Dev_v1.4/.agents/workflows/sprint-security-gate.md no Sprint atual.
   ```

> Antigravity tem terminal, browser e filesystem por padrão. Missions longas funcionam bem com `startcycle.md`.

---

## 3. Cursor

1. Cole `Squad_Dev_v1.4/` na raiz do projeto.
2. Crie `.cursor/rules/squad-dev.mdc`:

   ```mdc
   ---
   description: Squad Dev agents and workflow
   globs: ["**/*"]
   alwaysApply: true
   ---

   Você é a Squad Dev. Antes de qualquer ação:
   1. Leia Squad_Dev_v1.4/.agents/agents.md.
   2. Leia a skill em Squad_Dev_v1.4/.agents/skills/<skill>/SKILL.md.
   3. Leia Squad_Dev_v1.4/production_artifacts/memory/AI_CONTEXT.md.
   4. Código em Squad_Dev_v1.4/app_build/.
   5. Docs em Squad_Dev_v1.4/production_artifacts/.
   6. Security Gate bloqueante antes de deploy.
   ```

3. No chat:

   ```
   Aja como @solution-architect (@Squad_Dev_v1.4/.agents/skills/solution_architect/SKILL.md).
   Projete a arquitetura para: [ideia].
   ```

---

## 4. VS Code + GitHub Copilot

1. Cole `Squad_Dev_v1.4/` na raiz do projeto.
2. Crie `.github/copilot-instructions.md` com o texto padrão da seção "Regra persistente".
3. No Copilot Chat:

   ```
   @workspace Aja como solution-architect seguindo
   #file:Squad_Dev_v1.4/.agents/skills/solution_architect/SKILL.md.
   Projete a arquitetura para: [ideia].
   ```

---

## 5. Windsurf (Cascade)

1. Cole `Squad_Dev_v1.4/` na raiz do projeto.
2. Crie `.windsurfrules` na raiz com o texto padrão.
3. No Cascade:

   ```
   Aja como solution-architect. Leia @SKILL.md em
   Squad_Dev_v1.4/.agents/skills/solution_architect/. Projete: [ideia].
   ```

---

## 6. Claude Desktop (MCP filesystem)

1. Configure o servidor MCP filesystem apontando pra raiz do projeto que contém `Squad_Dev_v1.4/`.
2. Em cada nova thread, cole o texto padrão seguido da tarefa:

   ```
   [texto padrão da Squad Dev]

   Aja como solution-architect e projete a arquitetura para: [ideia].
   ```

---

## 7. Gemini CLI / AI Studio

### Gemini CLI

1. Cole `Squad_Dev_v1.4/` na raiz do projeto.
2. Crie `GEMINI.md` na raiz com o texto padrão. Lido automaticamente.
3. Rode `gemini` na raiz e invoque:

   ```
   @Squad_Dev_v1.4/.agents/skills/solution_architect/SKILL.md
   Projete a arquitetura para: [ideia].
   ```

### AI Studio (web)

1. Cole `.agents/agents.md` em System Instructions.
2. Faça upload da SKILL.md do agente ativo ao mudar de fase.

---

## 8. ChatGPT (Projects)

1. Crie um Project.
2. Faça upload de `.agents/agents.md`, `.agents/workflows/startcycle.md` e as SKILL.md que vai usar.
3. Em Project Instructions, cole o texto padrão.
4. Inicie:

   ```
   Ative /dev-squad para: [ideia]
   ```

---

## 9. Qualquer outra IA

Se a ferramenta não tem arquivo de regras, cole o texto padrão como **primeira mensagem** da sessão. Reitere quando a IA esquecer.

---

## Matriz resumida

| IA                    | Onde salvar a regra               | Invocação                   |
| --------------------- | --------------------------------- | --------------------------- |
| **Claude Code**       | `CLAUDE.md` + `~/.claude/agents/` | `/devsquad <ideia>`         |
| **Antigravity**       | Nativo                            | Execute `startcycle.md`     |
| **Cursor**            | `.cursor/rules/squad-dev.mdc`     | `@skill` + pedido           |
| **Copilot (VS Code)** | `.github/copilot-instructions.md` | `@workspace #file:SKILL.md` |
| **Windsurf**          | `.windsurfrules`                  | `@SKILL.md` + pedido        |
| **Claude Desktop**    | System prompt da thread           | Texto padrão + tarefa       |
| **Gemini CLI**        | `GEMINI.md`                       | `@SKILL.md` + pedido        |
| **AI Studio**         | System Instructions               | Upload SKILL.md por fase    |
| **ChatGPT Projects**  | Project Instructions              | Upload + ative workflow     |

---

## API Keys & Variáveis de Ambiente

> ⚠️ **NUNCA** commitar `.env` com valores reais. Adicione ao `.gitignore`.

Crie `app_build/.env` com as variáveis do seu projeto:

```env
# LLM / AI
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GEMINI_API_KEY=

# Banco de Dados
DATABASE_URL=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

# Autenticação
JWT_SECRET=
JWT_EXPIRES_IN=7d
SESSION_SECRET=

# Cloud / Deploy
GCP_PROJECT_ID=
GCP_REGION=us-central1
CLOUD_RUN_SERVICE_NAME=

# Serviços Externos
SMTP_HOST=
SMTP_PORT=
SMTP_USER=
SMTP_PASSWORD=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=

# Aplicação
NODE_ENV=development
PORT=3000
APP_URL=http://localhost:3000
LOG_LEVEL=debug
```

**Onde cada agente usa:**

| Variável         | Agente                                        | Como obter                                                           |
| ---------------- | --------------------------------------------- | -------------------------------------------------------------------- |
| `DATABASE_URL`   | `@database-specialist`, `@backend-specialist` | [Neon](https://neon.tech) / [Supabase](https://supabase.com) / local |
| `JWT_SECRET`     | `@backend-specialist`                         | `openssl rand -base64 32`                                            |
| `GCP_PROJECT_ID` | `@devops-engineer`                            | [Google Cloud Console](https://console.cloud.google.com)             |

**Em produção, use secrets manager:**

- **Cloud Run** → `gcloud secrets create MY_SECRET --data-file=.env`
- **Docker/VPS** → Docker Secrets ou `.env` fora do repositório
- **Vercel/Railway** → Dashboard de variáveis de ambiente

**Nunca:**

- ❌ Commitar `.env` com valores reais
- ❌ Hardcodar keys no código
- ❌ Deixar keys em comentários
- ❌ Compartilhar keys em chats ou mensagens

**Checklist de setup:**

- [ ] Criar `app_build/.env` (não versionado)
- [ ] Preencher variáveis necessárias para o projeto
- [ ] Adicionar `app_build/.env` ao `.gitignore`
- [ ] Configurar CI/CD com secrets manager

---

## Dicas universais

**Aprendizado por correção.** Quando você corrigir o agente duas vezes sobre a mesma coisa, ou usar "sempre", "nunca", "toda vez", o agente salva automaticamente a regra em `AI_CONTEXT.md` na seção "Regras Aprendidas". Você também pode pedir: "salva isso na memória".

**Memória viva.** Ao fim de cada fase:

```
Atualize Squad_Dev_v1.4/production_artifacts/memory/AI_CONTEXT.md
com stack, sprint atual, onde paramos e próximos passos.
```

**Progressive disclosure.** Não carregue todas as skills de uma vez. Carregue só a do agente ativo. Abra `references/` quando precisar de detalhe.

**Sessões curtas.** Feche ao fim de cada fase, salve em `AI_CONTEXT.md`, abra nova sessão na próxima.

**Continuidade entre IAs.** Qualquer IA que ler `AI_CONTEXT.md` + `sprints/sprint-N-context.md` retoma exatamente de onde parou.

**Security Gate antes de qualquer deploy:**

```
Execute Squad_Dev_v1.4/.agents/workflows/sprint-security-gate.md no código atual
de app_build/ e entregue o Security_Gate_Report.md.
```

---

## Janela de contexto por agente (continuidade entre LLMs)

Cada agente mantém o próprio arquivo em `production_artifacts/memory/agents/<agente>-context.md`. Inclui última tarefa, decisões, A2A inbox/outbox, pendências, contexto crítico anti-alucinação. Trocou de Claude para Gemini para GPT? Qualquer agente retoma exatamente do ponto.

## DB-first (regra bloqueante)

Se o projeto tem banco, `@database-specialist` roda **antes** do `@backend-specialist`. Entrega: schema versionado, migrations idempotentes, seed, backup, Docker Compose com volumes, indexes, constraints, RLS quando aplicável. Backend só inicia após handoff A2A do DBA.

## Anti-alucinação

Antes de qualquer decisão técnica que dependa de informação externa (versão de lib, CVE, preço, benchmark), o agente invoca `@research-specialist` (`/research`). Sem URL, não decide. Cache em `production_artifacts/memory/research/<yyyy-mm-dd>-<tópico>.md`.

---

_Squad Dev v1.4 · [GitHub](https://github.com/mayconrodriguess/skills-and-squads) · MRS Soluções Integradas_
