---
name: Transcrição-de-Midia
description: >
  Transcreve arquivos de áudio e vídeo para texto usando OpenAI Whisper localmente.
  Use esta skill sempre que o usuário mencionar transcrição, legendar vídeo, converter áudio em texto,
  transcrever reuniões, podcasts, entrevistas, áudios do WhatsApp, gravações de vídeo (mp4, mkv, avi),
  arquivos de áudio (mp3, wav, m4a, ogg, flac) ou qualquer mídia falada.
  Acione também quando o usuário quiser criar legendas (.srt/.vtt), gerar ata de reunião a partir de gravação,
  ou extrair o conteúdo verbal de qualquer mídia. Não exige internet — tudo roda localmente.
---

# Transcrição-de-Midia

Skill para **transcrição automática de áudio e vídeo** usando [OpenAI Whisper](https://github.com/openai/whisper) rodando **localmente** — sem custo por API, sem envio de dados para nuvem.

## Capacidades

| Funcionalidade              | Detalhes                                                    |
|-----------------------------|-------------------------------------------------------------|
| Formatos de entrada         | mp3, wav, m4a, ogg, flac, mp4, mkv, avi, mov, webm, aac   |
| Formatos de saída           | `.txt`, `.srt`, `.vtt`, `.json`, `.md` (relatório)          |
| Idiomas                     | Detecção automática; foco em PT-BR com `--language pt`      |
| Tamanhos de modelo Whisper  | tiny / base / small / medium / large (ver `references/modelos-whisper.md`) |
| Transcrição em lote         | Sim, via `scripts/batch_transcribe.py`                      |

## Dependências necessárias

Antes de transcrever, verifique se as dependências estão instaladas:

```bash
python scripts/utils.py --check-deps
```

Se faltar algo, instale:

```bash
# Whisper
pip install openai-whisper

# ffmpeg (Windows)
winget install ffmpeg
# ou: choco install ffmpeg
# ou baixe em: https://ffmpeg.org/download.html
```

## Como usar

### 1. Transcrição simples

```bash
python scripts/transcribe.py --input "reuniao.mp3" --output "transcricao.md"
```

### 2. Transcrição com idioma especificado e modelo maior

```bash
python scripts/transcribe.py \
  --input "entrevista.mp4" \
  --output "entrevista.md" \
  --language pt \
  --model medium \
  --format md
```

### 3. Gerar legendas (.srt)

```bash
python scripts/transcribe.py --input "video.mp4" --output "legendas.srt" --format srt
```

### 4. Transcrição em lote (pasta inteira)

```bash
python scripts/batch_transcribe.py --input-dir "audios/" --output-dir "transcricoes/" --language pt
```

## Seleção de modelo

| Situação                                 | Modelo recomendado |
|------------------------------------------|--------------------|
| Teste rápido / recursos limitados        | `tiny` ou `base`   |
| Uso geral / PT-BR com boa qualidade      | `base` ou `small`  |
| Alta qualidade / sotaques difíceis       | `medium`           |
| Máxima qualidade (GPU recomendada)       | `large`            |

Consulte `references/modelos-whisper.md` para detalhes de RAM/VRAM e velocidade.

## Fluxo recomendado pelo modelo

1. **Verifique dependências** com `utils.py --check-deps`
2. **Escolha o modelo** baseado nos recursos disponíveis (padrão: `base`)
3. **Execute `transcribe.py`** com os parâmetros adequados
4. **Revise a saída** — para áudios de baixa qualidade, tente modelo maior
5. **Use o template** em `assets/template-relatorio.md` para relatórios formais
6. **Para resumos**, use o prompt em `assets/prompt-resumo.txt` com o modelo de linguagem

## Referências

- `references/guia-uso.md` — Guia completo com exemplos por cenário
- `references/modelos-whisper.md` — Comparativo de modelos Whisper
- `assets/template-relatorio.md` — Template de relatório estruturado
- `assets/prompt-resumo.txt` — Prompt para resumo de transcrições
