# [Nome do Agente] — Janela de Contexto

> Template padronizado por agente. Cada agente mantém o seu próprio arquivo em
> `production_artifacts/memory/agents/<nome-do-agente>-context.md`.
>
> **Regra de ouro:** se a LLM é trocada no meio do projeto, a próxima consegue
> continuar só lendo este arquivo + `AI_CONTEXT.md` + a skill ativa.

---

**Agente:** @<nome-do-agente>
**Skill principal:** `<skill_folder>`
**Última atualização:** YYYY-MM-DD HH:MM
**Sprint ativo:** N
**Status do agente:** [idle | trabalhando | aguardando A2A | bloqueado]

---

## 1. Última tarefa executada

**Quando:** YYYY-MM-DD HH:MM
**O que foi feito:** [1-3 frases]
**Artefatos gerados/modificados:**

- [caminho/do/arquivo.md]
- [caminho/do/outro.ts]

---

## 2. Decisões tomadas nesta sessão

| #   | Decisão                              | Motivo                               | Revogável?              |
| --- | ------------------------------------ | ------------------------------------ | ----------------------- |
| 1   | Ex: escolhi Prisma em vez de Drizzle | Maturidade + integração com Supabase | Sim, até FASE 4 começar |

---

## 3. Handoffs A2A

### Recebidos (inbox)

| Data | De  | Pergunta/Pedido | Status                | Resposta |
| ---- | --- | --------------- | --------------------- | -------- |
|      |     |                 | pendente / respondido | link     |

### Enviados (outbox)

| Data | Para | Pergunta/Pedido | Status                | Resposta recebida |
| ---- | ---- | --------------- | --------------------- | ----------------- |
|      |      |                 | aguardando / recebido | resumo            |

---

## 4. Pendências abertas

- [ ] [tarefa clara e acionável]
- [ ] [outra pendência]

---

## 5. Próximo passo concreto

Quando esta sessão (ou a próxima) retomar o trabalho deste agente, começar por:

> [1 frase — arquivo, função, decisão a tomar]

---

## 6. Contexto crítico para não alucinar

Informações que **qualquer LLM precisa saber** pra não reinventar ou errar:

- [ex: "API está em Fastify, não Express. Não use middleware pattern"]
- [ex: "Schema do DB usa snake_case nas colunas mas ORM converte pra camelCase"]
- [ex: "Cliente odeia glassmorphism — regra salva em AI_CONTEXT.md"]

---

## 7. Arquivos que este agente tocou neste Sprint

Para facilitar rastreio sem precisar rodar `git diff`:

- `app_build/src/auth/login.ts` — criado
- `production_artifacts/ADRs/ADR-003-auth-strategy.md` — criado
- `production_artifacts/Solution_Architecture.md` — atualizado seção "Auth"

---

## 8. Research cache (se aplicável)

Pesquisas online feitas ou recebidas nesta sessão:

- `production_artifacts/memory/research/2026-04-24-bcrypt-vs-argon2.md`

---

## 9. Bloqueios (se status = bloqueado)

**Bloqueio:** [descrição]
**Esperando de:** @<agente> ou usuário
**O que destravaria:** [condição]
