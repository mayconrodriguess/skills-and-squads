# Metodologia de Revisão Contratual — Sistema 🟢🟡🔴

> Baseado em padrões comerciais brasileiros e internacionais.
> Adaptado ao Código Civil Brasileiro, LGPD e Lei de Arbitragem.

---

## Sistema de Classificação de Desvios

### 🟢 VERDE — Aceitável
A cláusula está alinhada com o padrão ou é mais favorável ao usuário.
Variações menores que não aumentam materialmente o risco.

**Ação:** Registrar para ciência. Sem necessidade de negociação.

**Exemplos:**
- Cap de responsabilidade em 18 meses quando o padrão é 12 meses
- Prazo de vigência de 24 meses (mais proteção que o mínimo de 12)
- Foro no domicílio do contratado

---

### 🟡 AMARELO — Negociar
A cláusula está fora do padrão preferencial mas dentro de faixa negociável.
Requer atenção e provavelmente negociação, mas não é bloqueante.

**Ação:** Gerar redline específico. Fornecer posição de fallback.
Estimar impacto de aceitar versus negociar.

**Exemplos:**
- Multa rescisória de 1 mês quando o padrão é 3 meses
- Prazo de aviso prévio de 30 dias quando o padrão é 60 dias
- Foro neutro aceitável mas não o preferido
- Reajuste anual pelo IGP-M em vez de IPCA

---

### 🔴 VERMELHO — Escalar / Atenção Máxima
A cláusula está fora da faixa aceitável ou representa risco material.
Requer revisão por advogado, aprovação de sócio ou decisão executiva.

**Ação:** Explicar o risco específico. Fornecer redação alternativa de mercado.
Estimar exposição. Recomendar caminho de escalada.

**Exemplos:**
- Ausência de limitação de responsabilidade
- Indenização unilateral irrestrita sem teto
- Justa causa com termos vagos e subjetivos ("a critério da contratante")
- Ausência de DPA quando há tratamento de dados pessoais (LGPD)
- Non-compete irrestrito sem limitação temporal ou geográfica
- Foro em comarca inconveniente com arbitragem de regras favoráveis ao redator

---

## Formato de Redline

Para cada ponto de negociação, usar o formato abaixo:

```
**Cláusula**: [Número e nome da cláusula]
**Classificação**: 🟡 AMARELO / 🔴 VERMELHO
**Texto atual**: "[transcrição exata do contrato]"
**Redline proposto**: "[linguagem alternativa específica e pronta para inserção]"
**Fundamento**: [1-2 frases explicando o porquê — adequado para compartilhar com a contraparte]
**Prioridade**: [Inegociável / Preferência forte / Concessão estratégica]
**Fallback**: [Posição alternativa se o redline principal for rejeitado]
```

---

## Framework de Prioridade de Negociação

### Tier 1 — Inegociáveis (Deal Breakers)
Itens onde não se prossegue sem resolução:
- Proteções de responsabilidade ausentes ou insuficientes
- Requisitos de proteção de dados (LGPD) não atendidos
- Cláusulas de PI que podem comprometer ativos essenciais
- Termos que conflitam com obrigações regulatórias

### Tier 2 — Preferências Fortes
Itens que afetam materialmente o risco mas têm espaço de negociação:
- Ajuste do cap de responsabilidade dentro da faixa
- Escopo e reciprocidade da indenização
- Flexibilidade rescisória
- Direitos de auditoria e compliance

### Tier 3 — Concessões Estratégicas
Itens que melhoram a posição mas podem ser concedidos estrategicamente:
- Foro preferido (se a alternativa for aceitável)
- Preferências de prazo de aviso
- Melhorias definicionais menores
- Requisitos de apólice de seguro

**Estratégia de negociação:**
Lidere com itens do Tier 1.
Troque concessões do Tier 3 para garantir vitórias no Tier 2.
Nunca conceda no Tier 1 sem escalada para decisor.

---

## Cláusulas Críticas — Checklist Brasileiro

### Limitação de Responsabilidade
- [ ] Existe cap de responsabilidade?
- [ ] O cap é recíproco ou assimétrico?
- [ ] Há exclusão de danos indiretos/consequenciais?
- [ ] Quais são as exceções ao cap?

### Rescisão
- [ ] Há multa por rescisão imotivada?
- [ ] A justa causa é definida taxativamente?
- [ ] Há prazo de aviso prévio adequado?
- [ ] Quais obrigações sobrevivem à rescisão?

### Propriedade Intelectual
- [ ] PI pré-existente está protegida?
- [ ] Quem detém a PI desenvolvida na prestação?
- [ ] Há cláusula de work-for-hire excessivamente ampla?

### Proteção de Dados (LGPD)
- [ ] Há tratamento de dados pessoais?
- [ ] As bases legais estão definidas?
- [ ] Há prazo de notificação de incidentes?
- [ ] Há obrigações de exclusão ao término?

### Remuneração
- [ ] O valor está claramente definido?
- [ ] A data de pagamento é específica?
- [ ] Há multa por atraso?
- [ ] Há previsão de reajuste anual?

### Foro e Resolução de Conflitos
- [ ] O foro é favorável ao usuário?
- [ ] Há previsão de mediação prévia?
- [ ] Lei aplicável é claramente o direito brasileiro?
