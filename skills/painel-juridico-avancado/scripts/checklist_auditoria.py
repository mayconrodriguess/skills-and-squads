"""
Checklist de Auditoria de Risco Comunicacional
Uso: auxiliar na verificação de textos antes da entrega

Execute mentalmente ou como referência ao revisar qualquer comunicação.
"""

CHECKLIST_AUDITORIA = {
    "elementos_proibidos": [
        "Acusações diretas sem respaldo factual",
        "Imputação explícita de crime",
        "Linguagem emocional (raiva, frustração, indignação explícita)",
        "Julgamentos pessoais sobre o caráter da pessoa",
        "Ameaças explícitas ('vou te processar', 'você vai se arrepender')",
        "Ameaças implícitas que possam ser interpretadas como coação",
        "Reconhecimento de culpa ('foi minha culpa', 'erramos')",
        "Reconhecimento de obrigação não confirmada juridicamente",
        "Confissão de conhecimento de irregularidade própria",
        "Linguagem que possa ser interpretada como chantagem",
    ],
    "elementos_recomendados": [
        "Saudação formal e respeitosa",
        "Contextualização objetiva do assunto",
        "Exposição factual cronológica e neutra",
        "Uso de formulações neutras ('aparente', 'possível', 'eventual')",
        "Solicitação de esclarecimento (não exigência agressiva)",
        "Menção à 'reserva de direitos' ao invés de ameaças",
        "Encerramento cordial e colaborativo",
        "Data e identificação clara do remetente",
    ],
    "substituicoes_sugeridas": {
        "vocês fizeram errado": "situação que merece verificação",
        "isso é ilegal": "possível inconsistência legal",
        "foi culpa de vocês": "situação decorrente de",
        "exijo": "solicito",
        "vou te processar": "reservo-me ao direito de adotar as medidas cabíveis",
        "ameaço": "sem prejuízo das medidas legais",
        "você errou": "verifico a necessidade de esclarecimento",
        "admito que erramos": "verifico a necessidade de análise da situação",
        "sei que foi você": "as circunstâncias indicam",
    },
    "perguntas_de_verificacao": [
        "Este texto poderia ser usado contra mim em juízo?",
        "Alguma frase admite culpa involuntariamente?",
        "O texto mantém postura técnica e institucional?",
        "Há alguma palavra que expresse emoção negativa excessiva?",
        "O destinatário poderia interpretar alguma frase como ameaça?",
        "Há alguma afirmação que eu não consiga provar objetivamente?",
        "O texto preserva meus direitos sem expor os do destinatário desnecessariamente?",
    ]
}

ESTRUTURA_RESPOSTA = [
    "1️⃣  Reconstrução Factual",
    "2️⃣  Análise Individual dos Especialistas",
    "3️⃣  Debate Técnico entre Agentes",
    "4️⃣  Matriz de Conduta Jurídica",
    "5️⃣  Mapa de Risco Jurídico",
    "6️⃣  Estratégia Jurídica Recomendada",
    "7️⃣  Parecer Jurídico Consolidado",
]

CLASSIFICACAO_RISCO = {
    "baixo": "🟢 Baixo risco — conduta dentro dos parâmetros legais",
    "medio": "🟡 Médio risco — possível enquadramento, provas insuficientes",
    "alto": "🔴 Alto risco — conduta potencialmente ilícita com provas razoáveis",
    "muito_alto": "🚨 Alto risco de responsabilização judicial — ação recomendada",
}
