# Como Usar o Squad Dev com Diferentes IAs

Esta Squad foi desenhada para ser **portátil** — a mesma pasta funciona em
qualquer IA que leia arquivos do projeto. Este guia mostra **como ativar a Squad
em cada ferramenta**.

> Princípio: a fonte da verdade é `.agents/agents.md` + `.agents/workflows/`
> + `.agents/skills/`. Qualquer IA que leia esses arquivos vira a Squad.

---

## Sumário

1. [Claude Code (terminal)](#1-claude-code-terminal)
2. [Claude Desktop (MCP filesystem)](#2-claude-desktop-mcp-filesystem)
3. [Cursor](#3-cursor)
4. [GitHub Copilot no VS Code](#4-github-copilot-no-vs-code)
5. [Google Antigravity](#5-google-antigravity)
6. [Gemini (CLI + AI Studio)](#6-gemini-cli--ai-studio)
7. [ChatGPT (Plus / Team / Enterprise)](#7-chatgpt-plus--team--enterprise)
8. [Windsurf / Cody / outras IAs de IDE](#8-windsurf--cody--outras-ias-de-ide)
9. [Qualquer IA genérica (copy & paste)](#9-qualquer-ia-generica-copy--paste)
10. [Dicas universais](#10-dicas-universais)

---

## 1. Claude Code (terminal)

**Melhor experiência nativa.** Claude Code descobre e carrega skills
automaticamente quando você invoca um slash command como `/dev-squad`.

### Setup

1. Copie a pasta `Squad_Dev/` para a raiz do seu projeto (ou use-a como raiz).
2. Abra o terminal no diretório e rode:

   ```bash
   claude
   ```

3. Inicie a Squad:

   ```
   /dev-squad Quero criar um app de gestão de tarefas para equipes
   ```

### Como funciona por dentro

- Claude Code varre `.claude/skills/` E `.agents/skills/` do projeto
- Cada `SKILL.md` tem YAML frontmatter com `name` + `description` + triggers
- Quando sua mensagem bate com triggers de uma skill, Claude carrega
  o conteúdo integral dela (progressive disclosure)
- Arquivos em `references/` são lidos só quando necessário

### Comandos úteis
| Comando | Ação |
|---|---|
| `/dev-squad <ideia>` | Pipeline completo (spec → deploy) |
| `/startcycle <ideia>` | Alias |
| `/securityscan` | Scan pontual de segurança |
| `/designpage` | Landing page standalone |
| `/buildapp` | App mobile |

---

## 2. Claude Desktop (MCP filesystem)

Claude Desktop não tem skills nativas ainda, mas com um servidor MCP de
filesystem ele lê toda a Squad como contexto de projeto.

### Setup

1. Instale o **Filesystem MCP server** seguindo a doc oficial da Anthropic.
2. Configure `claude_desktop_config.json` apontando para o diretório do
   projeto que contém `Squad_Dev/`.
3. Inicie uma conversa dizendo:

   ```
   Leia os arquivos em Squad_Dev/.agents/agents.md e
   Squad_Dev/.agents/workflows/startcycle.md. A partir de agora você é
   a Squad Dev. Vamos começar: [sua ideia].
   ```

4. Em cada nova thread, peça para ler `Squad_Dev/production_artifacts/memory/AI_CONTEXT.md`
   para retomar o contexto.

---

## 3. Cursor

Cursor suporta **Rules** (instruções persistentes) e **@-mentions** de arquivos.

### Setup

1. Coloque a `Squad_Dev/` na raiz do projeto.
2. Crie `.cursor/rules/squad-dev.mdc` com:

   ```mdc
   ---
   description: Squad Dev agents and workflow
   globs: ["**/*"]
   alwaysApply: true
   ---

   Você é a Squad Dev. Antes de qualquer ação:
   1. Leia `Squad_Dev/.agents/agents.md` para identificar o agente certo.
   2. Leia a skill correspondente em `Squad_Dev/.agents/skills/<skill>/SKILL.md`.
   3. Leia `Squad_Dev/production_artifacts/memory/AI_CONTEXT.md` para retomar contexto.
   4. Todo código do projeto vai em `Squad_Dev/app_build/`.
   5. Toda documentação vai em `Squad_Dev/production_artifacts/`.
   6. Security Gate é bloqueante antes de deploy.
   ```

3. No chat, use @-refs para puxar skills específicas:

   ```
   Aja como @solution-architect (ver @Squad_Dev/.agents/skills/solution_architect/SKILL.md).
   Projete a arquitetura para: [ideia].
   ```

### Dicas Cursor

- Composer Mode + @Folder da `Squad_Dev/` = IA lê tudo de uma vez
- YOLO mode bom para fases rotineiras (scaffolding); desative em tarefas críticas

---

## 4. GitHub Copilot no VS Code

Copilot Chat suporta **Custom Instructions** e **@workspace**.

### Setup

1. Abra o projeto com `Squad_Dev/` no VS Code.
2. Crie `.github/copilot-instructions.md` na raiz do repo:

   ```markdown
   # Copilot Instructions — Squad Dev

   Este repositório usa a Squad Dev (pasta `Squad_Dev/`).

   Regras:
   - Todo código do projeto fica em `Squad_Dev/app_build/`.
   - Documentação em `Squad_Dev/production_artifacts/`.
   - Memória viva: `Squad_Dev/production_artifacts/memory/AI_CONTEXT.md`.
   - Agentes definidos em `Squad_Dev/.agents/agents.md`.
   - Skills em `Squad_Dev/.agents/skills/<name>/SKILL.md`.
   - Security Gate é obrigatório antes de qualquer deploy.

   Quando receber uma tarefa, identifique o agente adequado em `agents.md`
   e siga o workflow da skill correspondente.
   ```

3. No Copilot Chat:

   ```
   @workspace Leia agents.md e a skill solution_architect. Projete a
   arquitetura do seguinte: [ideia].
   ```

### Dicas Copilot

- VS Code 1.90+ já lê `.github/copilot-instructions.md` automaticamente
- Use Chat Participants (@workspace, @terminal) para ampliar contexto
- `Ctrl+I` para inline edit dentro do arquivo

---

## 5. Google Antigravity

Antigravity é o IDE agentic da Google — entende pastas `.agent/` e `.agents/`.

### Setup

1. Abra o projeto contendo `Squad_Dev/` no Antigravity.
2. Os arquivos `.agents/agents.md` e `.agents/skills/` são reconhecidos como
   contexto de agentes disponíveis.
3. Invoque o agente no chat:

   ```
   Ative a Squad Dev conforme Squad_Dev/.agents/agents.md.
   Vamos iniciar: [sua ideia].
   ```

4. Antigravity expõe agentes via menu; aponte-os para as SKILLs quando possível.

### Dicas Antigravity

- Aproveite as "Missions" para workflows longos (startcycle funciona bem assim)
- O agente tem acesso a terminal, browser e filesystem por padrão
- Ative o Security Gate como checkpoint explícito antes de deploy

---

## 6. Gemini (CLI + AI Studio)

### Gemini CLI

1. Instale o Gemini CLI oficial.
2. No diretório do projeto:

   ```bash
   gemini --system-instruction "$(cat Squad_Dev/.agents/agents.md)"
   ```

   Ou passe como contexto via `--file`.

3. Inicie a tarefa:

   ```
   Leia Squad_Dev/.agents/workflows/startcycle.md e execute a Fase 0
   para: [ideia].
   ```

### Google AI Studio (web)

1. Abra [aistudio.google.com](https://aistudio.google.com).
2. Cole o conteúdo de `.agents/agents.md` no campo **System Instructions**.
3. Faça upload dos SKILL.md relevantes quando necessário.
4. Use Gemini 1.5+ Pro — a janela de contexto longa cabe toda a Squad.

---

## 7. ChatGPT (Plus / Team / Enterprise)

ChatGPT não lê arquivos do filesystem, mas aceita upload + Projects.

### Setup via Projects (recomendado)

1. Crie um novo **Project** e nomeie "Squad Dev — [NomeDoProjeto]".
2. Em **Project Instructions**, cole:

   ```
   Você é a Squad Dev. Os arquivos anexados definem:
   - agents.md: os 12 agentes da squad
   - startcycle.md: o pipeline completo
   - SKILL.md: instruções por agente

   Antes de cada resposta, identifique o agente correto e siga sua SKILL.
   Quando terminar uma fase, descreva o que salvaria em
   production_artifacts/memory/AI_CONTEXT.md.

   Como eu vou colar respostas em arquivos do meu repo local, entregue
   saídas prontas para copiar (markdown, código) sempre que possível.
   ```

3. Faça upload dos arquivos chave:
   - `.agents/agents.md`
   - `.agents/workflows/startcycle.md`
   - `.agents/skills/dev-squad/SKILL.md`
   - SKILL.md dos agentes que você vai usar

4. Inicie:
   ```
   Ative o fluxo /dev-squad com: [sua ideia]
   ```

### Alternativa: custom GPT

Crie um **Custom GPT** com `.agents/agents.md` no System Prompt e os SKILL.md
na Knowledge Base. Torna a Squad invocável com um clique.

---

## 8. Windsurf / Cody / outras IAs de IDE

### Windsurf (Cascade)

1. Abra o projeto com `Squad_Dev/`.
2. Crie `.windsurfrules` na raiz (similar ao Cursor):

   ```
   Você é a Squad Dev. Leia Squad_Dev/.agents/agents.md antes de agir.
   Código em Squad_Dev/app_build/, docs em Squad_Dev/production_artifacts/.
   ```

3. Cascade lê a pasta completa de forma agentic.

### Sourcegraph Cody

1. Adicione `Squad_Dev/` ao context filter do Cody.
2. Crie um **Custom Command** apontando para `.agents/workflows/startcycle.md`.
3. Use `@-mention` para puxar skill específica.

### Zed AI / Supermaven / outros

A maioria aceita um arquivo de instruções por projeto. Aponte-o para
`.agents/agents.md` e a Squad ativa.

---

## 9. Qualquer IA genérica (copy & paste)

Se a IA não lê arquivos:

### Passo 1 — System Prompt

Cole isto como system prompt ou primeira mensagem:

```
Você é a Squad Dev, uma equipe de 12 agentes especializados em desenvolvimento
de software. Os agentes são:

@product-owner, @product-manager, @solution-architect, @documentation-writer,
@database-specialist, @backend-specialist, @frontend-specialist,
@ai-page-designer, @mobile-developer, @qa-engineer, @security-specialist,
@devops-engineer.

Fluxo padrão: spec → arquitetura → implementação paralela (backend, frontend,
mobile, db) → QA → Security Gate (bloqueante) → deploy.

Regras:
- Código sempre em app_build/
- Documentação sempre em production_artifacts/
- Memória viva em production_artifacts/memory/AI_CONTEXT.md
- Security Gate é obrigatório antes de qualquer deploy

Para cada tarefa, anuncie qual agente está atuando e siga o padrão:
Required Inputs → Workflow → Deliverables → Quality Bar.
```

### Passo 2 — Contexto por fase

Cole o conteúdo de `SKILL.md` do agente ativo quando mudar de fase.

### Passo 3 — Memória

Ao mudar de IA ou de sessão, comece colando o conteúdo atual de
`AI_CONTEXT.md`.

---

## 10. Dicas universais

### Mantenha a memória viva

Depois de cada interação significativa, peça à IA para **atualizar**
`production_artifacts/memory/AI_CONTEXT.md` com:

- Stack aprovada
- Sprint atual + status
- Onde parou exatamente
- Próximos passos
- Decisões importantes do dia

Isso é o que torna a Squad realmente portátil.

### Use Progressive Disclosure

Nunca peça à IA para carregar **todas** as skills de uma vez. Ela deve:

1. Ler `.agents/agents.md` (curto)
2. Identificar o agente/skill relevante
3. Carregar só a SKILL.md daquele agente
4. Abrir `references/` da skill só quando precisar de detalhe

### Sessões curtas > sessões épicas

Modelos degradam com contexto muito longo. Feche a sessão ao fim de cada fase,
salve o estado em `AI_CONTEXT.md`, abra nova sessão na próxima.

### Sempre valide Security Gate

Independente da IA, antes de deployar produção:

```
Execute o protocolo .agents/skills/dev-squad/references/security-gate.md
no código atual de app_build/ e entregue o Security_Gate_Report.md.
```

### Troubleshooting

| Sintoma | Causa provável | Fix |
|---|---|---|
| "IA não conhece os agentes" | Não leu `agents.md` | Cole o arquivo como contexto |
| "IA refaz o que já foi feito" | Perdeu `AI_CONTEXT.md` | Cole-o no início da sessão |
| "IA pula o Security Gate" | Não tratou como bloqueante | Reitere no prompt: "gate é bloqueante" |
| "IA coloca código fora de `app_build/`" | Regra de estrutura ignorada | Cole a seção "Regras Fundamentais" do README |
| "Skills conflitam entre si" | Carregou várias ao mesmo tempo | Load apenas a do agente ativo |

---

## Matriz de Capacidades

| IA | Lê filesystem | Skills auto | Rules/Instrução persistente | Agentic (terminal/tools) |
|---|---|---|---|---|
| Claude Code | Sim | Sim | CLAUDE.md | Sim |
| Claude Desktop + MCP | Sim (via MCP) | Não | Project | Parcial |
| Cursor | Sim | Não | `.cursor/rules/*.mdc` | Sim |
| GitHub Copilot (VS Code) | @workspace | Não | `.github/copilot-instructions.md` | Sim |
| Antigravity | Sim | Parcial (agentes) | Workspace | Sim |
| Gemini CLI | Via CLI flags | Não | `--system-instruction` | Sim |
| AI Studio | Upload | Não | System Instructions | Não |
| ChatGPT (Projects) | Upload | Não | Project Instructions | Parcial |
| ChatGPT (Custom GPT) | Knowledge base | Não | System Prompt | Parcial |
| Windsurf | Sim | Não | `.windsurfrules` | Sim |
| Cody | Sim | Via Commands | Context filters | Parcial |

> "Skills auto" = a IA carrega uma SKILL.md sozinha quando o trigger bate.
> "Parcial" = depende da config do usuário ou de MCP/extensões.

---

## Quando pedir ajuda ao Squad

Prompts que funcionam em qualquer IA, desde que ela tenha lido `agents.md`:

- "Aja como @solution-architect. Projete a arquitetura para: [X]"
- "Aja como @backend-specialist. Implemente o endpoint: [X]"
- "Execute Security Gate do Sprint atual"
- "Retome conforme `AI_CONTEXT.md`"
- "Ative o pipeline /dev-squad para: [ideia]"

Se a IA estiver confusa, lembre-a: "você é a Squad Dev, os agentes estão em
`.agents/agents.md`, as skills em `.agents/skills/`."

---

**Versão**: 1.0 — compatível com Squad Dev v3
