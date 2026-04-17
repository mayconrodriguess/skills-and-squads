# 🔴 Pré-Publicação — Auditoria de Segurança Completa

> Executado pelo `@security-specialist` **uma vez antes do primeiro deploy em produção**
> e repetido a cada release major ou mudança significativa de infraestrutura.
> É **BLOQUEANTE**: nenhum deploy acontece sem aprovação aqui.

---

## 1. DAST — Análise Dinâmica (Aplicação em Execução)

Pré-requisito: aplicação rodando em ambiente de staging/local.

**Testes a realizar:**
- Fuzzing de parâmetros de entrada (campos de formulário, query strings, headers)
- Testes de autenticação: brute-force protection, session fixation, token leakage
- Testes de autorização: acesso a recursos de outro usuário, privilege escalation
- Testes de injeção em runtime: SQLi, XSS reflected/stored, SSTI
- Testes de upload de arquivo: validação de tipo, tamanho, execução remota
- Testes de rate limiting: bypass, abuse de endpoints sensíveis

**Ferramentas recomendadas (se disponíveis):**
- OWASP ZAP (scan automático)
- Burp Suite Community
- Nuclei (templates de CVEs conhecidos)

---

## 2. Threat Modeling — STRIDE

Para cada fluxo crítico da aplicação, aplique STRIDE:

| Fluxo | Spoofing | Tampering | Repudiation | Info Disclosure | DoS | Elevation of Privilege |
|-------|----------|-----------|-------------|-----------------|-----|------------------------|
| Login/Auth | | | | | | |
| Pagamento/Transação | | | | | | |
| Upload de arquivo | | | | | | |
| APIs públicas | | | | | | |
| Admin/Backoffice | | | | | | |

Para cada ameaça identificada: **risco = probabilidade × impacto**, e defina a mitigação.

---

## 3. Revisão de Infraestrutura

### Configurações de Contêiner/Cloud
- [ ] Imagem Docker sem vulnerabilidades críticas conhecidas (scan da imagem)
- [ ] Usuário não-root definido no Dockerfile
- [ ] Segredos de produção nunca estão na imagem (use secrets manager)
- [ ] Network policies configuradas (mínimo privilégio)
- [ ] Health checks e liveness probes definidos

### Gestão de Segredos
- [ ] Todas as credenciais em vault ou secrets manager (não em `.env` de produção versionado)
- [ ] Rotação de segredos documentada
- [ ] Chaves de API com escopos mínimos necessários

### TLS/HTTPS
- [ ] HTTPS forçado em todos os endpoints (redirect 301)
- [ ] TLS 1.2+ obrigatório; TLS 1.0/1.1 desabilitados
- [ ] HSTS configurado
- [ ] Certificado válido e renovação automatizada

### Headers de Segurança HTTP
- [ ] `Content-Security-Policy` definida
- [ ] `X-Content-Type-Options: nosniff`
- [ ] `X-Frame-Options: DENY` ou `SAMEORIGIN`
- [ ] `Referrer-Policy` configurado
- [ ] `Permissions-Policy` configurado

---

## 4. Pipeline CI/CD — Security Gates Automatizados

Verifique se o pipeline de CI/CD inclui:

- [ ] SAST automatizado (ex: Semgrep, SonarQube, CodeQL)
- [ ] SCA automatizado (ex: Dependabot, Snyk, OWASP Dependency-Check)
- [ ] Secrets scan automatizado (ex: GitGuardian, truffleHog)
- [ ] Scan de imagem de contêiner (ex: Trivy, Grype)
- [ ] SBOM gerado a cada build (Software Bill of Materials)
- [ ] Deploy bloqueado se severity CRÍTICA encontrada

---

## 5. Conformidade Final

### ISO 27001:2022 — Controles de Operações (A.12) e Desenvolvimento (A.14/A.8)

| Controle | Atendido? | Evidência |
|----------|-----------|-----------|
| A.8.25 Desenvolvimento seguro | | |
| A.8.29 Testes de segurança | | |
| A.8.31 Separação de ambientes | | |
| A.12.1 Procedimentos operacionais documentados | | |
| A.12.6 Gestão de vulnerabilidades técnicas | | |

### NIST CSF — Avaliação Completa

| Função | Subcategoria | Status |
|--------|-------------|--------|
| **Identify** | ID.AM: Inventário de ativos | |
| **Identify** | ID.RA: Avaliação de risco | |
| **Protect** | PR.AC: Gestão de identidade e controle de acesso | |
| **Protect** | PR.DS: Segurança de dados | |
| **Protect** | PR.IP: Processos e procedimentos de proteção da informação | |
| **Detect** | DE.AE: Anomalias e eventos | |
| **Detect** | DE.CM: Monitoramento contínuo de segurança | |
| **Respond** | RS.RP: Plano de resposta | |
| **Recover** | RC.RP: Plano de recuperação | |

### LGPD / GDPR (se aplicável)

- [ ] Dados pessoais mapeados (quais, onde, por quanto tempo)
- [ ] Base legal de tratamento definida para cada categoria
- [ ] Consentimento implementado corretamente (se aplicável)
- [ ] Direitos do titular implementados (acesso, correção, exclusão)
- [ ] Política de privacidade publicada
- [ ] DPO/Encarregado designado (se obrigatório)

---

## 6. Plano de Resposta a Incidentes (pré-publicação)

Antes de ir a produção, defina e documente:

- [ ] Contatos de emergência (quem chamar em caso de incidente)
- [ ] Runbook de rollback (como reverter o deploy)
- [ ] Monitoramento e alertas configurados (uptime, erros 5xx, anomalias)
- [ ] Backup de dados configurado e testado
- [ ] Log de auditoria habilitado para ações críticas

---

## Template do Relatório de Auditoria Pré-Publicação

```markdown
# Pre-Publication Security Audit Report
**Data:** YYYY-MM-DD
**Versão do Release:** vX.Y.Z
**Auditor:** @security-specialist
**Resultado:** ✅ APROVADO PARA PRODUÇÃO | ❌ BLOQUEADO

## Resumo Executivo
[Status geral, principais achados, postura de segurança]

## DAST
[Achados dinâmicos ou "Nenhuma vulnerabilidade crítica em runtime"]

## Threat Modeling (STRIDE)
[Ameaças identificadas, mitigações aplicadas, riscos residuais aceitos]

## Infraestrutura
[Status dos controles de container, TLS, headers, segredos]

## CI/CD Security Gates
[Gates configurados e validados no pipeline]

## Conformidade
### ISO 27001: [Compliant / Partial / Non-Compliant]
### NIST CSF: [Maturity Level estimado]
### LGPD/GDPR: [Compliant / N/A]

## Bloqueantes para Publicação
- [ ] Item crítico — ação obrigatória antes do deploy

## Riscos Residuais Aceitos
- Risco: [descrição] | Probabilidade: [A/M/B] | Impacto: [A/M/B] | Aceito por: [nome/data]

## Recomendações Pós-Publicação (não bloqueantes)
- Item 1
```

Salve em: `production_artifacts/Pre_Publish_Security_Audit.md`
