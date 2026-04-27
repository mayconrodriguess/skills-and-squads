# Subagentes Squad Dev — Guia Universal

Esta pasta contém prompts de subagente para uso em qualquer IA.
Para o Claude Code, os subagentes ficam em `.claude/agents/` e são ativados automaticamente.
Para qualquer outra IA, abra uma nova conversa, cole o prompt correspondente e faça a pergunta.

## Por que subagentes?

A janela de contexto da sessão principal é um recurso limitado.
Sem subagente: o agente lê 15 arquivos, faz 10 buscas, tudo entra no contexto principal.
Com subagente: nova janela, faz toda a investigação, retorna só o resumo.
A sessão principal registra apenas a pergunta e a resposta.

## Quando usar cada subagente

| Subagente            | Use quando                                                     | Prompt                       |
| -------------------- | -------------------------------------------------------------- | ---------------------------- |
| **explore**          | "Onde está X no código?" / "Qual arquivo faz Y?"               | `explore-prompt.md`          |
| **code-reviewer**    | Antes de abrir PR, revisão de Sprint                           | `code-reviewer-prompt.md`    |
| **spec-analyst**     | "O que o spec diz sobre X?" / "Quais ACs cobrem Y?"            | `spec-analyst-prompt.md`     |
| **security-scanner** | Cheque rápido de segurança / antes do Security Gate            | `security-scanner-prompt.md` |
| **test-generator**   | "Gere testes para o módulo X"                                  | `test-generator-prompt.md`   |
| **doc-writer**       | "Gere o README" / "Atualize o Deployment Guide"                | `doc-writer-prompt.md`       |
| **db-analyst**       | "Revise o schema" / "Há N+1 no código?"                        | `db-analyst-prompt.md`       |
| **api-mapper**       | "Quais endpoints existem?" / "O endpoint X está implementado?" | `api-mapper-prompt.md`       |

## Como usar em outras IAs

1. Abra uma **nova conversa** (janela de contexto limpa)
2. Cole o conteúdo do prompt correspondente como primeira mensagem
3. Faça sua pergunta específica
4. O subagente salva contexto em `production_artifacts/memory/subagents/`
5. Copie o resumo retornado de volta para a sessão principal

## Pasta de contexto dos subagentes

Todos os subagentes salvam seus achados em:
`production_artifacts/memory/subagents/`

Isso garante que o resultado persiste entre sessões e IAs.
