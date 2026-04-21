<p align="center">
  <img src="https://img.shields.io/badge/Skill-Gerador_de_Currículos-0078D4?style=for-the-badge&logo=readme&logoColor=white" alt="Skill Badge"/>
  <img src="https://img.shields.io/badge/ATS-Otimizado-00C853?style=for-the-badge&logo=checkmarx&logoColor=white" alt="ATS Badge"/>
  <img src="https://img.shields.io/badge/Saída-.md_.docx_.pdf-FF6F00?style=for-the-badge&logo=files&logoColor=white" alt="Output Badge"/>
</p>

<h1 align="center">📄 Gerador Avançado de Currículos</h1>
<h3 align="center">ATS + Design System + SEO — Skill para Agentes de IA</h3>

<p align="center">
  Skill especializada em criar currículos profissionais otimizados para sistemas ATS (Applicant Tracking Systems), recrutadores humanos e mecanismos de busca de vagas — com design refinado e alta taxa de conversão em entrevistas.
</p>

---

## 🎯 O que esta Skill faz?

Transforma dados profissionais em currículos **estratégicos e visualmente refinados**, seguindo um fluxo guiado de 7 etapas:

| Etapa | Descrição |
|:-----:|-----------|
| 1 | **Detecção de dados** — identifica se o usuário já tem currículo, LinkedIn ou portfólio existente |
| 2 | **Coleta inteligente** — guia a coleta em blocos organizados, perguntando apenas o necessário |
| 3 | **Design System** — escolha de estilo visual, paleta de cores, tipografia e densidade |
| 4 | **Geração otimizada** — currículo com verbos de ação, métricas, palavras-chave ATS integradas |
| 5 | **Múltiplas saídas** — Markdown, Word (.docx) e PDF |
| 6 | **Revisão automática** — checklist ATS + checklist visual |
| 7 | **Extras** — versão em inglês, adaptação para vagas, sugestão para LinkedIn |

---

## ✨ Principais Funcionalidades

- 🔍 **Otimização ATS** — palavras-chave estratégicas, estrutura compatível com parsers de ATS (Gupy, LinkedIn, Indeed, Workday)
- 🎨 **4 estilos visuais** — Minimalista, Corporativo Moderno, Criativo, Executivo
- 📊 **Bullets de impacto** — verbos de ação + resultados mensuráveis (padrão STAR)
- 🌐 **SEO para currículos** — termos buscados por recrutadores incorporados naturalmente
- 🇧🇷🇺🇸 **Bilíngue** — geração em português e inglês
- 📎 **Adaptação por vaga** — cole a descrição da vaga e o currículo é reajustado automaticamente
- 🤖 **Coleta inteligente** — reaproveita dados de currículos antigos, LinkedIn ou GitHub
- 📄 **Script Python** — geração automatizada de `.docx` com `python-docx`

---

## 📁 Estrutura do Projeto

```
gerador-curriculo/
├── SKILL.md                          # Instruções principais da skill
├── README.md                         # Este arquivo
├── evals/
│   └── evals.json                    # Casos de teste para validação
├── references/
│   ├── ats_keywords.md               # Banco de palavras-chave por área profissional
│   └── docx_guide.md                 # Guia de formatação Word e PDF
└── scripts/
    └── gerar_docx.py                 # Script Python para gerar .docx profissional
```

---

## 🚀 Como Usar

### Pré-requisito

Esta skill foi projetada para funcionar com **agentes de IA** compatíveis com o formato de Skills em Markdown (ex: Claude Code, Gemini CLI, ou qualquer agente que suporte `.agent/skills/`).

### Instalação

1. **Clone ou copie** a pasta `gerador-curriculo/` para o diretório de skills do seu agente:

```bash
# Exemplo de estrutura esperada
.agent/
  skills/
    gerador-curriculo/
      SKILL.md
      references/
      scripts/
      evals/
```

2. **(Opcional)** Para geração automática de `.docx`, instale a dependência Python:

```bash
pip install python-docx
```

### Ativação

A skill é acionada automaticamente quando o usuário menciona qualquer um destes termos:

| Gatilho | Exemplo |
|---------|---------|
| `currículo` | *"Preciso criar meu currículo"* |
| `CV` | *"Quero atualizar meu CV"* |
| `curriculum vitae` | *"Fazer meu curriculum vitae"* |
| `resume` | *"Build my resume"* |
| `otimizar para ATS` | *"Otimizar currículo para ATS"* |
| `adaptar para vaga` | *"Adaptar currículo para essa vaga"* |
| `currículo em inglês` | *"Preciso de um currículo em inglês"* |
| `revisar currículo` | *"Revisar meu currículo antigo"* |

---

## 💬 Exemplos de Uso

### Criar do zero
```
Quero criar meu currículo profissional. Sou desenvolvedor backend 
com 4 anos de experiência em Python e AWS. Tenho interesse em vagas 
remotas de nível sênior.
```

### Melhorar currículo existente
```
Tenho um currículo antigo, quero que você revise e melhore. 
Aqui está o texto:
[cola o conteúdo do currículo]
```

### Adaptar para vaga específica
```
Adapta meu currículo para esta vaga de Product Manager:
[cola a descrição da vaga]
```

### Gerar versão em inglês
```
Preciso de uma versão em inglês do meu currículo para vagas internacionais.
```

---

## 🎨 Estilos Visuais Disponíveis

| Estilo | Descrição | Recomendado para |
|--------|-----------|-----------------|
| **Minimalista** | Limpo, tipografia elegante, muito espaço em branco | Tech, Startups, Design |
| **Corporativo Moderno** | Estruturado, cores sóbrias, altamente profissional | Corporações, Consultorias |
| **Criativo** | Sidebar colorida, ícones, destaque visual | Marketing, Design, Comunicação |
| **Executivo** | Clássico, premium, transmite autoridade | C-Level, Finanças, Jurídico |

---

## 📄 Script de Geração `.docx`

O script `scripts/gerar_docx.py` gera currículos em Word automaticamente:

```bash
python scripts/gerar_docx.py \
  --dados dados_curriculo.json \
  --saida meu_curriculo.docx \
  --estilo corporativo
```

### Formato do JSON de entrada

```json
{
  "nome": "Maria Silva",
  "telefone": "(11) 99999-0000",
  "email": "maria@email.com",
  "cidade": "São Paulo, SP",
  "linkedin": "linkedin.com/in/mariasilva",
  "resumo": "Profissional com 8 anos de experiência em...",
  "competencias": ["Python", "AWS", "Docker", "Scrum", "CI/CD"],
  "experiencias": [
    {
      "cargo": "Engenheira de Software Sênior",
      "empresa": "TechCorp",
      "periodo": "jan/2021 – Atual",
      "atividades": [
        "Liderei equipe de 6 devs na migração de monolito para microsserviços",
        "Reduzi tempo de deploy em 70% implementando pipeline CI/CD"
      ]
    }
  ],
  "formacao": [
    {
      "curso": "Ciência da Computação",
      "instituicao": "USP",
      "ano": "2016"
    }
  ],
  "certificacoes": [
    {
      "nome": "AWS Solutions Architect",
      "instituicao": "Amazon",
      "ano": "2023"
    }
  ],
  "idiomas": ["Português — Nativo", "Inglês — Avançado (C1)"]
}
```

---

## 🔑 Banco de Palavras-Chave ATS

O arquivo `references/ats_keywords.md` contém termos estratégicos organizados por área:

- 💻 Tecnologia (Backend, Frontend, Mobile, DevOps, Data/IA)
- 📈 Marketing & Vendas
- 💼 Gestão & Liderança
- 💰 Finanças & Contabilidade
- ⚖️ Jurídico
- 🏥 Saúde
- 🎓 Educação
- 🏗️ Engenharia & Manufatura
- 🛡️ Recursos Humanos

---

## 🧪 Testes e Validação

O arquivo `evals/evals.json` contém 3 cenários de teste:

| # | Cenário | Objetivo |
|---|---------|----------|
| 1 | Dev fullstack criando do zero | Valida o fluxo completo de coleta e geração |
| 2 | Currículo antigo fraco para revisar | Valida a capacidade de diagnóstico e reescrita |
| 3 | Psicóloga migrando para RH | Valida adaptação de carreira e posicionamento estratégico |

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Algumas ideias:

- Adicionar palavras-chave ATS para novas áreas profissionais
- Novos estilos visuais no script `gerar_docx.py`
- Templates LaTeX para saída premium em PDF
- Tradução da skill para outros idiomas
- Novos casos de teste em `evals/`

---

## 📝 Licença

Este projeto é de uso livre para fins pessoais e educacionais.

---

<p align="center">
  <sub>Feito com ❤️ para maximizar oportunidades profissionais</sub>
</p>
