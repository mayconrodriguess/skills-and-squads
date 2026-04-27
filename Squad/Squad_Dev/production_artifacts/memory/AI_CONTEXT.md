# AI Context — [Nome do Projeto]

> Este arquivo é a **memória viva** da Squad.
> Todo agente deve lê-lo ao iniciar e atualizá-lo ao concluir sua fase.
> Se você é uma IA nova retomando este projeto — comece por aqui.

---

**Última atualização:** [YYYY-MM-DD HH:MM]
**Agente que atualizou:** [@nome-do-agente]
**Sprint atual:** [N]
**Status:** [Planejamento | Desenvolvimento | QA | Security Gate | Sprint Review | Pré-Publicação | Deploy | Concluído]

---

## Resumo do Projeto

[2-3 frases descrevendo o que este projeto faz e para quem.]

## Stack Tecnológica Aprovada

- **Backend:** [ex: Node.js 22 + Fastify + PostgreSQL]
- **Frontend:** [ex: Next.js 15 (App Router) + Tailwind CSS]
- **Mobile:** [ex: React Native (Expo) / Não aplicável]
- **Banco de dados:** [ex: PostgreSQL 16 no Neon / SQLite]
- **Deploy:** [ex: Google Cloud Run + Docker]
- **CI/CD:** [ex: GitHub Actions + Semgrep + Dependabot]

## Documentos Importantes

| Documento             | Caminho                                                 | Status                        |
| --------------------- | ------------------------------------------------------- | ----------------------------- |
| Especificação Técnica | `production_artifacts/Technical_Specification.md`       | [✅ Aprovado / 🔄 Em revisão] |
| Arquitetura           | `production_artifacts/Solution_Architecture.md`         | [✅ / 🔄 / ❌ Pendente]       |
| Backlog               | `production_artifacts/Product_Backlog.md`               | [✅ / 🔄 / ❌]                |
| Roadmap de Sprints    | `production_artifacts/Sprint_Roadmap.md`                | [✅ / 🔄 / ❌]                |
| Último QA Report      | `production_artifacts/sprint-N/QA_Report.md`            | [✅ / ❌]                     |
| Último Security Gate  | `production_artifacts/sprint-N/Security_Gate_Report.md` | [✅ / ⚠️ / ❌]                |

## Sprint Atual — Objetivos

**Sprint [N] — [nome ou tema do sprint]**

Features deste Sprint:

- [ ] Feature A
- [ ] Feature B
- [ ] Feature C

## Onde Paramos

[Descreva o estado exato: qual fase foi completada, o que está em progresso, o que está bloqueado.]

Exemplo:

> Sprint 2 — Development concluído. QA Gate passou. Aguardando Security Gate.
> `@security-specialist` precisa rodar o protocolo em `.agents/skills/dev-squad/references/security-gate.md`

## Próximos Passos

1. [Ação imediata para o próximo agente/sessão]
2. [Segunda ação]
3. [Terceira ação]

## Decisões Importantes Tomadas

[Decisões arquiteturais, de produto ou de processo que não estão óbvias no código.]

| Decisão                            | Justificativa                    | ADR                        |
| ---------------------------------- | -------------------------------- | -------------------------- |
| [ex: PostgreSQL em vez de MongoDB] | [ex: precisa de transações ACID] | [ex: ADRs/001-database.md] |

## Riscos e Dívida Técnica Conhecida

| Item                       | Tipo      | Severidade | Sprint Previsto |
| -------------------------- | --------- | ---------- | --------------- |
| [ex: Autenticação sem MFA] | Segurança | Alta       | Sprint 3        |

## Contexto Crítico

[Informações que uma IA nova PRECISA saber para não cometer erros ou repetir discussões já resolvidas.]

- [ex: O usuário preferiu SQLite em vez de PostgreSQL por ser um projeto desktop offline]
- [ex: A feature X foi deliberadamente removida do escopo — não sugerir novamente]
- [ex: O deploy é via Cloud Run, não Vercel — não criar arquivos vercel.json]

---

_Atualizar este arquivo após cada fase concluída._
_Histórico de sprints: `production_artifacts/memory/sprints/`_
