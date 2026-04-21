# Como Usar o Squad Dev com Diferentes IAs

A Squad é portátil. A mesma pasta `Squad_Dev/` funciona em qualquer IA que leia arquivos do projeto. Este guia mostra só o que precisa ser configurado em cada ferramenta, nada a mais.

> Fonte da verdade: `.agents/agents.md` + `.agents/workflows/` + `.agents/skills/`.
> Qualquer IA que leia esses arquivos vira a Squad.

---

## Regra persistente (texto padrão)

O texto abaixo é o mesmo pra todas as IAs. O que muda é onde salvar:

```
Você é a Squad Dev. Antes de qualquer ação:
1. Leia Squad_Dev/.agents/agents.md para identificar o agente certo.
2. Leia a skill em Squad_Dev/.agents/skills/<skill>/SKILL.md.
3. Leia Squad_Dev/production_artifacts/memory/AI_CONTEXT.md para retomar contexto.
4. Código em Squad_Dev/app_build/.
5. Documentação em Squad_Dev/production_artifacts/.
6. Security Gate é bloqueante antes de deploy.
```

---

## 1. Claude Code (terminal)

Nativo. Skills auto-detectadas.

1. Cole a `Squad_Dev/` na raiz do projeto.
2. Rode `claude` na raiz.
3. Use `/dev-squad <ideia>`.

Não precisa configurar nada. Claude lê `.agents/skills/` automaticamente.

---

## 2. Google Antigravity

Antigravity lê `.agents/` e segue os workflows nativamente. É a configuração mais simples depois do Claude Code.

1. Cole a `Squad_Dev/` na raiz do workspace.
2. Abra o workspace no Antigravity. Os agentes em `.agents/agents.md` aparecem disponíveis.
3. Invoque o workflow no chat:

   ```
   Execute Squad_Dev/.agents/workflows/startcycle.md para: [ideia].
   Identifique os agentes em .agents/agents.md e siga as skills em .agents/skills/.
   ```

4. Para Security Gate:

   ```
   Execute Squad_Dev/.agents/workflows/sprint-security-gate.md no Sprint atual.
   ```

Antigravity tem terminal, browser e filesystem por padrão. Tratamento de Missions longas funciona bem com o `startcycle.md`.

---

## 3. Cursor

1. Cole a `Squad_Dev/` na raiz do projeto.
2. Crie `.cursor/rules/squad-dev.mdc`:

   ```mdc
   ---
   description: Squad Dev agents and workflow
   globs: ["**/*"]
   alwaysApply: true
   ---

   Você é a Squad Dev. Antes de qualquer ação:
   1. Leia Squad_Dev/.agents/agents.md.
   2. Leia a skill em Squad_Dev/.agents/skills/<skill>/SKILL.md.
   3. Leia Squad_Dev/production_artifacts/memory/AI_CONTEXT.md.
   4. Código em Squad_Dev/app_build/.
   5. Docs em Squad_Dev/production_artifacts/.
   6. Security Gate bloqueante antes de deploy.
   ```

3. No chat:

   ```
   Aja como @solution-architect (@Squad_Dev/.agents/skills/solution_architect/SKILL.md).
   Projete a arquitetura para: [ideia].
   ```

---

## 4. VS Code + GitHub Copilot

1. Cole a `Squad_Dev/` na raiz do projeto.
2. Crie `.github/copilot-instructions.md` na raiz do repo com o texto padrão (seção "Regra persistente" acima).
3. No Copilot Chat:

   ```
   @workspace Aja como solution-architect seguindo
   #file:Squad_Dev/.agents/skills/solution_architect/SKILL.md.
   Projete a arquitetura para: [ideia].
   ```

---

## 5. Windsurf (Cascade)

1. Cole a `Squad_Dev/` na raiz do projeto.
2. Crie `.windsurfrules` na raiz com o texto padrão.
3. No Cascade, use `@` pra anexar arquivos:

   ```
   Aja como solution-architect. Leia @SKILL.md em
   Squad_Dev/.agents/skills/solution_architect/. Projete: [ideia].
   ```

---

## 6. Claude Desktop (MCP filesystem)

1. Configure o MCP filesystem apontando pra raiz do projeto.
2. Em cada nova thread, cole o texto padrão e a tarefa:

   ```
   [texto padrão]

   Aja como solution-architect e projete a arquitetura para: [ideia].
   ```

---

## 7. Gemini CLI / AI Studio

### Gemini CLI

1. Cole a `Squad_Dev/` na raiz do projeto.
2. Crie `GEMINI.md` na raiz com o texto padrão.
3. Rode `gemini` na raiz. O `GEMINI.md` é lido automaticamente.
4. Invoque:

   ```
   @Squad_Dev/.agents/skills/solution_architect/SKILL.md
   Projete a arquitetura para: [ideia].
   ```

### AI Studio (web)

1. Cole `.agents/agents.md` em System Instructions.
2. Faça upload da SKILL.md do agente ativo quando mudar de fase.

---

## 8. ChatGPT (Projects)

1. Crie um Project.
2. Faça upload de `.agents/agents.md`, `.agents/workflows/startcycle.md` e as SKILL.md que vai usar.
3. Em Project Instructions, cole o texto padrão.
4. Inicie: `Ative /dev-squad para: [ideia]`.

---

## 9. Qualquer outra IA

Se a ferramenta não tem arquivo de regras, cole o texto padrão como primeira mensagem da sessão. Reitere quando a IA esquecer.

---

## Matriz resumida

| IA | Onde salvar a regra | Invocação |
|---|---|---|
| Claude Code | (nativo) | `/dev-squad <ideia>` |
| Antigravity | (nativo) | "Execute .agents/workflows/startcycle.md" |
| Cursor | `.cursor/rules/squad-dev.mdc` | `@skill` + pedido |
| Copilot (VS Code) | `.github/copilot-instructions.md` | `@workspace #file:SKILL.md` |
| Windsurf | `.windsurfrules` | `@SKILL.md` + pedido |
| Claude Desktop | System prompt da thread | Cole texto padrão + tarefa |
| Gemini CLI | `GEMINI.md` | `@SKILL.md` + pedido |
| AI Studio | System Instructions | Upload SKILL.md por fase |
| ChatGPT Projects | Project Instructions | Upload + ative workflow |

---

## Dicas universais

**Aprendizado por correção (nativo em toda sessão).** Quando você corrigir o agente duas vezes sobre a mesma coisa, ou usar "sempre", "nunca", "toda vez", o agente salva automaticamente a regra em `AI_CONTEXT.md` na seção "Regras Aprendidas" e a aplica em toda sessão seguinte. Você também pode pedir direto: "salva isso na memória" ou "lembra disso". A regra entra no contexto de qualquer IA que ler o `AI_CONTEXT.md` a partir daí.

**Memória viva.** Ao fim de cada fase, peça: "Atualize `production_artifacts/memory/AI_CONTEXT.md` com stack, sprint atual, onde paramos e próximos passos."

**Progressive disclosure.** Não carregue todas as skills de uma vez. Carregue só a do agente ativo. Abra `references/` quando precisar de detalhe.

**Sessões curtas.** Feche a sessão ao fim de cada fase, salve em `AI_CONTEXT.md`, abra nova sessão na próxima.

**Security Gate.** Antes de qualquer deploy:

```
Execute Squad_Dev/.agents/workflows/sprint-security-gate.md no código atual
de app_build/ e entregue o Security_Gate_Report.md.
```

---

**Versão**: 2.0, compatível com Squad Dev v3.
