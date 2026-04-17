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
│   │   ├── AI_CONTEXT.md            ← contexto vivo (ler sempre primeiro)
│   │   ├── project-brief.md         ← resumo do projeto
│   │   └── sprints/                 ← histórico de sprints
│   └── ...                          ← toda documentação aqui
│
├── API_KEYS_SETUP.md
└── README.md
```

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

Esta Squad funciona com qualquer IA que leia arquivos. Guia completo por ferramenta em **[HOW_TO_USE_WITH_DIFFERENT_AIs.md](./HOW_TO_USE_WITH_DIFFERENT_AIs.md)**.

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

O arquivo `production_artifacts/memory/AI_CONTEXT.md` é atualizado após cada fase por cada agente. Ele contém:

- Stack tecnológica aprovada
- Status do Sprint atual
- Onde paramos
- Próximos passos
- Decisões importantes
- Contexto crítico

**Qualquer IA que ler esse arquivo pode retomar o projeto do ponto exato onde parou.**
