# 🚀 Squad Dev

**Uma equipe de TI completa em uma pasta.**
Cole dentro do seu projeto, chame a Squad e comece a desenvolver.

---

## O que é isso?

Squad_Dev é um conjunto de agentes de IA especializados que trabalham juntos como uma equipe de desenvolvimento real:

- **Product Owner** → planeja Sprints e paraleliza trabalho
- **Product Manager** → detalha User Stories e Critérios de Aceite
- **Solution Architect** → define arquitetura e DevSecOps
- **Documentation Writer** → documenta tudo automaticamente
- **Database Specialist** → schema, migrations, backups
- **Backend Specialist** → APIs, autenticação, serviços
- **Frontend Specialist** → UI/UX web com design fundamentado
- **AI Page Designer** → landing pages e páginas estáticas
- **Mobile Developer** → iOS/Android + publicação nas stores
- **QA Engineer** → testes automatizados e correção de bugs
- **Security Specialist** → DevSecOps, ISO 27001, OWASP *(bloqueante)*
- **DevOps Engineer** → build, deploy local/cloud, CI/CD

---

## Como Usar

### 1. Cole a pasta no seu projeto

```
MeuProjeto/
├── Squad_Dev/     ← copie esta pasta aqui
├── src/
└── ...
```

### 2. Abra qualquer IA com suporte a arquivos

```bash
cd MeuProjeto
claude  # ou cursor, copilot, etc.
```

### 3. Inicie a Squad

```
/devsquad Quero criar um app de gestão de tarefas para equipes
```

ou

```
/startcycle Sistema de agendamento online para clínicas
```

### Outros Comandos

| Comando | O que faz |
|---------|-----------|
| `/devsquad <ideia>` | Pipeline completo |
| `/startcycle <ideia>` | Alias para /devsquad |
| `/commit-push-pr` | Commit + push + PR + notificação Slack |
| `/securitygate N` | Security Gate do Sprint N |
| `/securityscan` | Scan de segurança pontual |
| `/designpage` | Cria landing page standalone |
| `/buildapp` | Desenvolve app mobile |

---

## Estrutura da Pasta

```
Squad_Dev/
├── .agents/
│   ├── agents.md                    ← 12 perfis de agentes
│   ├── skills/                      ← uma skill por agente
│   │   ├── write_specs/
│   │   ├── solution_architect/
│   │   ├── documentation_writer/
│   │   ├── database_specialist/
│   │   ├── backend_specialist/
│   │   ├── frontend_specialist/
│   │   ├── ai_page_designer/
│   │   ├── mobile_developer/
│   │   ├── qa_engineer/
│   │   ├── security_specialist/
│   │   ├── devops_deploy/
│   │   ├── generate_code/
│   │   ├── audit_code/
│   │   └── dev-squad/               ← orquestrador
│   └── workflows/
│       ├── startcycle.md            ← pipeline completo
│       └── sprint-security-gate.md
│
├── app_build/                       ← TODO código do projeto aqui
│
├── production_artifacts/
│   ├── memory/
│   │   ├── AI_CONTEXT.md            ← índice enxuto: % por Sprint + pointers (ler sempre primeiro)
│   │   ├── project-brief.md         ← resumo do projeto
│   │   └── sprints/
│   │       ├── sprint-1-context.md  ← contexto detalhado do Sprint (carrega sob demanda)
│   │       ├── sprint-2-context.md
│   │       └── ...
│   └── ...                          ← toda documentação aqui
│
├── API_KEYS_SETUP.md
└── README.md
```

---

## Subagentes (economia de contexto)

Cada tarefa de exploração, revisão ou geração roda em janela de contexto própria.
A sessão principal registra só a pergunta e o resumo.

| Subagente | Quando usar |
|---|---|
| `explore` | Encontrar onde algo está no código |
| `code-reviewer` | Revisão antes de PR (contexto limpo, sem viés) |
| `spec-analyst` | Analisar spec sem trazer tudo ao contexto |
| `security-scanner` | Varredura rápida de segurança |
| `test-generator` | Gerar testes por módulo ou Sprint |
| `doc-writer` | Gerar README, OpenAPI, Deployment Guide, changelog |
| `db-analyst` | Revisar schema, N+1, migrations |
| `api-mapper` | Mapear todos os endpoints existentes |

**Claude Code:** `.claude/agents/` (ativados automaticamente)
**Outras IAs:** `subagents/<nome>-prompt.md` — cole em nova conversa

Contexto salvo em `production_artifacts/memory/subagents/` após cada execução.

---

## Hooks (camada determinística)

A Squad vem com hooks pré-configurados em `.claude/settings.json`.
Diferente de instruções no `CLAUDE.md`, hooks **sempre executam**, sem depender do Claude lembrar.

| Hook | Evento | O que faz |
|---|---|---|
| Prettier | `PostToolUse` em Edit/Write | Formata o arquivo após cada edição |
| ESLint --fix | `PostToolUse` em Edit/Write `.ts/.tsx` | Corrige lint automaticamente |
| Command Log | `PostToolUse` em Bash | Loga todos os comandos em `memory/command-log.txt` |
| Proteção de arquivos | `PreToolUse` em Edit/Write | Bloqueia `.env`, chaves SSH, `node_modules` |
| Comandos perigosos | `PreToolUse` em Bash | Bloqueia force push em main, `DROP DATABASE`, `rm -rf /` |
| Notificação desktop | `Stop` | Avisa quando Claude termina a tarefa |

Para adicionar hooks ou ver exemplos: `.agents/skills/dev-squad/references/hooks-guide.md`

---

## Regras Fundamentais

| Regra | Descrição |
|-------|-----------|
| 📁 Código | Sempre em `app_build/` |
| 📋 Documentação | Sempre em `production_artifacts/` |
| 🧠 Memória | `production_artifacts/memory/AI_CONTEXT.md` |
| 🔐 Security Gate | Obrigatório ao final de CADA Sprint |
| 🔴 Pré-publicação | Auditoria obrigatória antes de qualquer deploy |

---

## Compatibilidade com IAs

Esta Squad funciona com qualquer IA que leia arquivos. Guia completo por ferramenta em **[HOW_TO_USE_WITH_DIFFERENT_AIs.md](./HOW_TO_USE_WITH_DIFFERENT_AIs.md)** ou na versão web **[index.html](./index.html)** (abra no navegador).

| IA | Status |
|----|-----------|
| **Claude Code** | Nativo — skills auto-detectadas |
| **Claude Desktop (MCP)** | Nativo via servidor MCP filesystem |
| **Cursor** | Via @-rules + file refs |
| **GitHub Copilot (VS Code)** | Via custom instructions + @workspace |
| **Google Antigravity** | Via agents e workspace completo |
| **Gemini CLI / AI Studio** | System instruction + file upload |
| **ChatGPT (Plus/Team/Enterprise)** | Projects + file upload |
| **Windsurf / Cody / qualquer IA** | Copiar `.agents/agents.md` como system prompt |

### Migrando para outra IA

1. Leia `production_artifacts/memory/AI_CONTEXT.md` — está tudo lá
2. Compartilhe esse arquivo com a nova IA
3. Diga: "Continue conforme `AI_CONTEXT.md`"

---

## Segurança

Os agentes `@security-specialist` e `@devops-engineer` implementam:

- OWASP Top 10
- ISO/IEC 27001:2022
- NIST CSF 2.0
- CIS Benchmarks
- STRIDE (Threat Modeling)
- LGPD / GDPR

O Security Gate é **bloqueante** — nenhum Sprint é concluído e nenhum deploy acontece sem aprovação do `@security-specialist`.

---

## Memória e Continuidade

A memória é dividida em dois níveis, pra não estourar contexto:

**Nível 1, `AI_CONTEXT.md`** (índice enxuto, sempre leve)
Stack, % de progresso por Sprint, status, onde paramos em 1 linha, pointers pros arquivos detalhados. Máximo 40 linhas. Lido em toda sessão.

**Nível 2, `sprints/sprint-N-context.md`** (detalhe pesado, sob demanda)
Um arquivo por Sprint entregável: user stories, ACs, decisões locais, QA, Security, próximo passo. Carregado só quando o agente está trabalhando naquele Sprint. Sprints passados ficam arquivados.

**Regra de Sprint:** cada Sprint é uma fatia vertical testável e deployável. Janela máxima até produção: 2 a 3 Sprints.

Qualquer IA que ler `AI_CONTEXT.md` + o `sprint-N-context.md` ativo retoma o projeto exatamente de onde parou, sem puxar histórico inteiro.
