# 🔶 Security Gate — Protocolo por Sprint

> Executado pelo `@security-specialist` ao final de cada Sprint.
> Este gate é **BLOQUEANTE**: nenhum Sprint é considerado concluído sem aprovação aqui.

---

## 1. SAST — Análise Estática de Código

**Objetivo:** Detectar vulnerabilidades no código-fonte sem executar a aplicação.

Verifique manualmente ou com ferramentas:
- Injection flaws (SQL, NoSQL, Command, LDAP)
- Uso inseguro de funções criptográficas (MD5, SHA1, ECB mode)
- Deserialização insegura
- Validação insuficiente de entrada nos limites da aplicação
- Controle de acesso inexistente ou mal implementado
- Código morto com lógica de segurança desativada
- Erros capturados mas não tratados adequadamente

**Saída:** Lista de `[CRÍTICO | ALTO | MÉDIO | BAIXO]` com linha e arquivo.

---

## 2. SCA — Análise de Composição de Software

**Objetivo:** Identificar dependências com vulnerabilidades conhecidas (CVEs).

Passos:
1. Liste todas as dependências diretas e transitivas (`package.json`, `requirements.txt`, etc.)
2. Verifique CVEs conhecidas para cada versão utilizada
3. Para cada CVE encontrado, classifique: CVSS Score + impacto no projeto
4. Recomende upgrade ou mitigação

**Saída:** Tabela de dependências vulneráveis com CVE ID, CVSS, e ação recomendada.

---

## 3. Secrets Scan

**Objetivo:** Garantir que nenhuma credencial, token ou chave esteja hardcoded.

Itens a verificar:
- API Keys e tokens em variáveis, strings, comentários
- Senhas hardcoded em arquivos de configuração
- Chaves privadas ou certificados commitados
- Conexões de banco com credenciais embutidas
- `.env` files que não deveriam estar no repositório

**Saída:** Lista de ocorrências com arquivo, linha e recomendação de remoção/rotação.

---

## 4. OWASP Top 10 — Checklist Aplicado

Para cada item abaixo, marque: ✅ Mitigado / ⚠️ Parcial / ❌ Vulnerável / N/A

| # | Categoria | Status | Evidência |
|---|-----------|--------|-----------|
| A01 | Broken Access Control | | |
| A02 | Cryptographic Failures | | |
| A03 | Injection | | |
| A04 | Insecure Design | | |
| A05 | Security Misconfiguration | | |
| A06 | Vulnerable & Outdated Components | | |
| A07 | Identification & Authentication Failures | | |
| A08 | Software & Data Integrity Failures | | |
| A09 | Security Logging & Monitoring Failures | | |
| A10 | Server-Side Request Forgery (SSRF) | | |

---

## 5. Conformidade ISO 27001

Controles aplicáveis ao contexto de desenvolvimento (Anexo A relevante):

| Controle | Descrição | Status |
|----------|-----------|--------|
| A.8.25 | Ciclo de vida de desenvolvimento seguro | |
| A.8.26 | Requisitos de segurança de aplicações | |
| A.8.27 | Arquitetura de sistema segura e princípios de engenharia | |
| A.8.28 | Codificação segura | |
| A.8.29 | Testes de segurança em desenvolvimento e aceitação | |
| A.8.30 | Desenvolvimento terceirizado | |
| A.8.31 | Separação de ambientes de dev, teste e produção | |
| A.8.32 | Gestão de mudanças | |
| A.8.33 | Informações de teste | |
| A.8.34 | Proteção de sistemas de informação durante testes de auditoria | |

---

## 6. NIST CSF — Funções Aplicáveis

| Função | Subcategoria Relevante | Status |
|--------|----------------------|--------|
| **Identify** | Inventário de ativos e dados sensíveis do Sprint | |
| **Protect** | Controles de acesso, criptografia, validação | |
| **Detect** | Logging de eventos de segurança implementado | |

---

## 7. CIS Benchmarks — Stack-Específico

Aplicar conforme stack do projeto:

**Node.js:**
- `no eval()`, `no Function()` com input dinâmico
- Helmet.js ou equivalente para HTTP headers
- Rate limiting configurado
- Variáveis de ambiente para segredos (nunca `process.env` fallback inseguro)

**Python:**
- Uso de `ast.literal_eval` em vez de `eval`
- Pydantic para validação de dados
- Segredos via `os.environ` ou vault

**Docker/Containers:**
- Imagem não executa como root
- `no --privileged` sem justificativa documentada
- Secrets não em variáveis de ambiente de imagem (usar secrets mount)
- Health check definido

**APIs REST:**
- Autenticação em todos os endpoints protegidos
- CORS configurado restritivamente (não `*` em produção)
- Paginação para evitar dump de dados

---

## Template do Relatório de Security Gate

```markdown
# Security Gate Report — Sprint N
**Data:** YYYY-MM-DD
**Revisor:** @security-specialist
**Resultado:** ✅ APROVADO | ⚠️ APROVADO COM RESSALVAS | ❌ BLOQUEADO

## Resumo Executivo
[2-3 linhas com o resultado geral]

## Achados por Categoria
### SAST
[Tabela de achados ou "Nenhum achado crítico"]

### SCA
[Dependências vulneráveis ou "Todas as dependências estão em versões seguras"]

### Secrets Scan
[Achados ou "Nenhum segredo exposto detectado"]

### OWASP Top 10
[Tabela preenchida]

### ISO 27001 / NIST CSF / CIS
[Itens não conformes ou "Todos os controles aplicáveis estão satisfeitos"]

## Itens Bloqueantes (impedem avanço)
- [ ] Item 1 — arquivo:linha — ação requerida

## Itens de Melhoria (não bloqueantes)
- [ ] Item 1 — ação sugerida

## Dívida de Segurança Rastreada
[Itens aceitos pelo negócio com risco documentado]
```

Salve em: `production_artifacts/sprint-N/Security_Gate_Report.md`
