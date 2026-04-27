# Squad Dev v1.4 — Configuração Automática

Este diretório usa o **Squad Dev v1.4**: 14 agentes especializados, A2A formalizado, janela de contexto por agente, slash commands individuais, anti-alucinação por padrão.

## Squad localizado em

```
C:\.DADOS\Claude\Squad_Dev_v1.4\
```

## Leia sempre ao iniciar sessão

1. `production_artifacts/memory/AI_CONTEXT.md` — status global do projeto
2. Se há Sprint ativo: `production_artifacts/memory/sprints/sprint-N-context.md`
3. Se vai trabalhar como agente específico: `production_artifacts/memory/agents/<agente>-context.md`
4. `.agents/A2A_PROTOCOL.md` — quem fala com quem

## Os 14 agentes

| #   | Agente                  | Slash command                  |
| --- | ----------------------- | ------------------------------ |
| 1   | `@product-owner`        | `/po`                          |
| 2   | `@product-manager`      | `/pm`                          |
| 3   | `@solution-architect`   | `/architect`                   |
| 4   | `@documentation-writer` | `/docs`                        |
| 5   | `@database-specialist`  | `/database`                    |
| 6   | `@backend-specialist`   | `/backend`                     |
| 7   | `@frontend-specialist`  | `/frontend`                    |
| 8   | `@ai-page-designer`     | `/designpage`                  |
| 9   | `@design-hunter`        | `/designhunter`                |
| 10  | `@mobile-developer`     | `/mobile` ou `/buildapp`       |
| 11  | `@qa-engineer`          | `/qa`                          |
| 12  | `@security-specialist`  | `/security` ou `/securityscan` |
| 13  | `@devops-engineer`      | `/devops`                      |
| 14  | `@research-specialist`  | `/research`                    |

## Comandos de pipeline

| Comando               | Ação                                                                  |
| --------------------- | --------------------------------------------------------------------- |
| `/startcycle <ideia>` | Pipeline completo: PO → PM → Architect → Dev → QA → Security → Deploy |
| `/devsquad <ideia>`   | Alias para /startcycle                                                |
| `/securitygate N`     | Security Gate bloqueante do Sprint N                                  |
| `/commit-push-pr`     | Commit + push + PR (requer QA + Security aprovados)                   |

## Subagentes globais (Claude Code, qualquer projeto)

```
@squad-explore          @squad-code-reviewer    @squad-spec-analyst
@squad-security-scanner @squad-test-generator   @squad-doc-writer
@squad-db-analyst       @squad-api-mapper       @squad-design-hunter
@squad-researcher
```

## Regras fundamentais

| Regra             | Onde                                                            |
| ----------------- | --------------------------------------------------------------- |
| Código do app     | `app_build/`                                                    |
| Documentação      | `production_artifacts/`                                         |
| Memória global    | `production_artifacts/memory/AI_CONTEXT.md`                     |
| Janela por agente | `production_artifacts/memory/agents/<agente>-context.md`        |
| A2A               | toda invocação registrada no contexto de origem e destino       |
| DB-first          | se há DB, `@database-specialist` antes do `@backend-specialist` |
| Anti-alucinação   | info externa? → invocar `@research-specialist`                  |
| Security Gate     | bloqueante antes de deploy                                      |

## Continuidade entre LLMs

Qualquer IA que ler:

1. `AI_CONTEXT.md` (visão global)
2. `sprints/sprint-N-context.md` (Sprint ativo)
3. `agents/<agente>-context.md` (handoff do agente)
4. A skill em `.agents/skills/<skill>/SKILL.md`

…retoma exatamente de onde parou.

## Hooks ativos (automáticos)

- Prettier após Edit/Write
- ESLint --fix em `.ts/.tsx/.js/.jsx`
- Bloqueio de `.env`, `id_rsa`, `node_modules`
- Bloqueio de `rm -rf /`, force push em main, DROP DATABASE
- Log de comandos em `production_artifacts/memory/command-log.txt`
