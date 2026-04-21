# Guia de Geração de Arquivos Word (.docx) para Currículos

Este guia descreve como gerar arquivos Word profissionais a partir dos dados do currículo.

---

## Opção 1: Script Python Automatizado (Recomendado)

Use o script `scripts/gerar_docx.py` passando os dados do currículo em JSON.

### Dependência necessária
```bash
pip install python-docx
```

### Como usar
```bash
python scripts/gerar_docx.py --dados curriculo_dados.json --saida meu_curriculo.docx --estilo corporativo
```

### Estilos disponíveis
- `minimalista` — Branco, Inter, muito espaço
- `corporativo` — Azul profissional, Calibri, estruturado
- `criativo` — Sidebar colorida, título em destaque
- `executivo` — Preto & cinza, clássico, premium

---

## Opção 2: Template Word Manual

Se não for possível rodar Python, forneça ao usuário:

### Configurações de documento
```
Tamanho: A4
Margens: Superior 2cm | Inferior 2cm | Esquerda 2,5cm | Direita 2cm
```

### Estilos de texto por seção

**Nome (Cabeçalho)**
- Fonte: Calibri Light ou Inter
- Tamanho: 24-28pt
- Cor: #1A2B4A (azul escuro profissional) ou #1F1F1F (quase preto)
- Negrito: Sim

**Títulos de Seção (Experiência, Formação, etc.)**
- Fonte: Calibri ou Roboto
- Tamanho: 11pt
- Cor: #1A2B4A ou cor principal escolhida
- Negrito: Sim
- Caixa alta: Sim (VERSALETE ou maiúsculas)
- Espaçamento antes: 12pt | depois: 4pt
- Linha inferior: 0,5pt, cor principal

**Cargo / Empresa**
- Cargo: 10pt, Negrito
- Empresa: 10pt, Itálico, cor secundária
- Período: 9pt, alinhado à direita

**Bullets de atividades**
- Fonte: Calibri, 9,5-10pt
- Recuo: 0,5cm
- Marcador: • (ponto médio)
- Espaçamento entre linhas: 1,15

**Informações de contato**
- Fonte: 9pt
- Ícones simples ou separados por | ou •

---

## Opção 3: Ferramentas Online Gratuitas

Se preferir usar ferramentas online para design premium:

| Ferramenta | Link | Melhor para |
|-----------|------|-------------|
| Canva | canva.com | Design visual, templates bonitos |
| Resume.io | resume.io | ATS + design automático |
| Overleaf | overleaf.com | LaTeX profissional |
| Novoresume | novoresume.com | Tech, startup |
| Reactive Resume | rxresu.me | Open source, gratuito |

---

## Exportação para PDF

### Do Word:
1. `Arquivo > Salvar como > PDF`
2. Opções: "Otimizar para: Qualidade padrão"
3. Marcar: "Tags de estrutura de documento para acessibilidade"

### Qualidade premium via Acrobat:
- Comprimir imagens: 150 DPI mínimo
- Incorporar todas as fontes
- Não proteger com senha (ATS não consegue ler)

---

## Dicas Críticas de Formatação

### Compatibilidade ATS
- ❌ Não use tabelas para layout (ATS confunde a leitura)
- ❌ Não coloque informações em cabeçalho/rodapé do Word (ATS ignora)
- ❌ Não use caixas de texto flutuantes
- ❌ Não use imagens essenciais (foto pode ser incluída, mas não informações vitais em imagem)
- ✅ Use parágrafos simples e listas com marcadores
- ✅ Use estilos de título padrão do Word
- ✅ Salve como .docx (não .doc)

### Para versão criativa (não ATS)
Se o currículo for enviado diretamente a recrutadores humanos (não por plataforma ATS), pode usar design mais elaborado com colunas, cores e ícones.
