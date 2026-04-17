---
name: dev-squad
description: >
  Orquestra a Squad Dev completa — do conceito ao deploy com segurança garantida.
  Use SEMPRE que mencionar: squad, pipeline, sprint, desenvolver projeto, publicar aplicação,
  montar equipe, /devsquad, /startcycle, ciclo de desenvolvimento, equipe de TI,
  planejamento de sprints, backlog, ou qualquer combinação de desenvolvimento + testes + publicação.
---

# Dev Squad — Orquestrador

Pipeline completo em `.agents/workflows/startcycle.md`.

## Agentes da Squad

| Agente | Skill | Quando Atua |
|--------|-------|-------------|
| `@product-owner` | `write_specs`, `dev-squad` | Início — define backlog e sprints |
| `@product-manager` | `write_specs` | Detalha cada sprint (User Stories + AC) |
| `@solution-architect` | `solution_architect` | Arquitetura + DevSecOps blueprint |
| `@documentation-writer` | `documentation_writer` | Docs em `production_artifacts/` |
| `@database-specialist` | `database_specialist` | Schema, migrations, Docker |
| `@backend-specialist` | `backend_specialist` | APIs, serviços, autenticação |
| `@frontend-specialist` | `frontend_specialist` | UI/UX web + integração |
| `@ai-page-designer` | `ai_page_designer` | Landing pages e páginas estáticas |
| `@mobile-developer` | `mobile_developer` | iOS/Android + publicação stores |
| `@qa-engineer` | `qa_engineer` | Testes + bugfix por Sprint |
| `@security-specialist` | `security_specialist` | 🔶 Gate por Sprint + 🔴 Pré-publicação |
| `@devops-engineer` | `devops_deploy` | Build, deploy, CI/CD |

## Estrutura de Pastas

```
Squad_Dev/
├── .agents/
│   ├── agents.md              ← perfis dos 12 agentes
│   ├── skills/                ← uma skill por agente
│   └── workflows/
│       ├── startcycle.md      ← pipeline completo
│       └── sprint-security-gate.md
├── app_build/                 ← TODO código do projeto aqui
├── production_artifacts/
│   ├── memory/
│   │   ├── AI_CONTEXT.md      ← contexto atual (atualizado por toda IA)
│   │   ├── project-brief.md   ← resumo do projeto
│   │   └── sprints/           ← histórico de sprints
│   └── ...                    ← toda documentação aqui
└── README.md
```

## Regras Fundamentais

1. **Código** → sempre em `app_build/`
2. **Documentação** → sempre em `production_artifacts/`
3. **Memória/Contexto** → `production_artifacts/memory/AI_CONTEXT.md`
4. **Security Gate** → obrigatório ao final de CADA Sprint
5. **Auditoria Pré-Publicação** → obrigatória antes de qualquer deploy em produção

## Paralelismo de Sprints

O `@product-owner` pode definir streams independentes no mesmo Sprint:
```
Sprint N:
  ├── Stream A: @backend-specialist + @database-specialist
  └── Stream B: @frontend-specialist
  → Paralelo quando não há dependência bloqueante
  → Convergem no @qa-engineer ao final
```

## Comandos

| Comando | O que faz |
|---------|-----------|
| `/devsquad <ideia>` | Inicia o pipeline completo |
| `/startcycle <ideia>` | Alias para /devsquad |
| `/securitygate N` | Executa Security Gate do Sprint N |
| `/securityscan` | Scan de segurança pontual |
| `/designpage` | Aciona @ai-page-designer standalone |
| `/buildapp` | Aciona @mobile-developer standalone |

## Referências de Segurança

- Security Gate por Sprint: `.agents/skills/dev-squad/references/security-gate.md`
- Auditoria Pré-Publicação: `.agents/skills/dev-squad/references/pre-publish-audit.md`
