---
description: >
  Executa o Security Gate obrigatório ao final de cada Sprint.
  Ativar com: /securitygate <numero-do-sprint>
  É BLOQUEANTE — Sprint não está concluído sem aprovação aqui.
---

# Sprint Security Gate

**Agir como `@security-specialist`** | Skill: `security_specialist`

Protocolo completo: `.agents/skills/dev-squad/references/security-gate.md`

---

## Pré-Requisitos

- [ ] `production_artifacts/Technical_Specification.md`
- [ ] `production_artifacts/Solution_Architecture.md`
- [ ] `production_artifacts/sprint-N/Sprint_Plan.md`
- [ ] `production_artifacts/sprint-N/QA_Report.md` ← QA deve ter passado
- [ ] `app_build/` com código do Sprint

Itens ausentes → reportar ao usuário antes de prosseguir.

---

## Execução

1. **SAST** — análise estática em `app_build/`
2. **SCA** — CVEs nas dependências
3. **Secrets Scan** — credenciais expostas
4. **OWASP Top 10** — checklist aplicado ao escopo
5. **ISO 27001 + NIST CSF + CIS** — controles aplicáveis
6. Salvar `production_artifacts/sprint-N/Security_Gate_Report.md`

---

## Veredito

### ✅ APROVADO
Sprint concluído. Notificar `@product-owner` para Sprint Review.

### ⚠️ APROVADO COM RESSALVAS
Riscos MÉDIO/BAIXO aceitos — documentar em Sprint Report.
Sprint avança, dívida entra no backlog do próximo Sprint.

### ❌ BLOQUEADO
Achado CRÍTICO ou ALTO.
Sprint NÃO concluído.
Retornar ao especialista responsável com lista de correções obrigatórias.
Após correções → executar este gate novamente.

---

## Atualizar Memória

Após conclusão, atualizar `production_artifacts/memory/AI_CONTEXT.md`
com resultado do gate e próximo passo.
