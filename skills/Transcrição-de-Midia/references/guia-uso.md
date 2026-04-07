# Guia de Uso — Transcrição-de-Midia

Este guia cobre a instalação, configuração e uso da skill em diferentes cenários reais.

---

## 1. Instalação

### Requisitos
- Python 3.8 ou superior
- pip
- ffmpeg

### Instalar Python e pip
Se ainda não tiver Python: [https://python.org/downloads](https://python.org/downloads)

### Instalar ffmpeg (Windows)

**Opção A — winget (recomendado):**
```bash
winget install ffmpeg
```

**Opção B — Chocolatey:**
```bash
choco install ffmpeg
```

**Opção C — Manual:**
1. Acesse [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Baixe a versão Windows
3. Extraia e adicione a pasta `bin/` ao PATH do sistema

### Instalar OpenAI Whisper

```bash
pip install openai-whisper
```

> **Nota:** Na primeira execução, o modelo escolhido será baixado automaticamente (~150MB para `base`).

### Verificar instalação

```bash
python scripts/utils.py --check-deps
```

---

## 2. Exemplos por Cenário

### Áudio do WhatsApp (.ogg / .opus)

```bash
python scripts/transcribe.py \
  --input "mensagem.ogg" \
  --output "mensagem.md" \
  --language pt \
  --model base
```

### Reunião gravada (.mp4 / .mkv)

```bash
python scripts/transcribe.py \
  --input "reuniao_2026-03-14.mp4" \
  --output "ata_reuniao.md" \
  --language pt \
  --model medium
```

### Podcast em inglês → transcrição em inglês

```bash
python scripts/transcribe.py \
  --input "podcast_ep42.mp3" \
  --output "podcast_ep42.txt" \
  --language en \
  --format txt
```

### Gerar legendas para vídeo (SRT)

```bash
python scripts/transcribe.py \
  --input "palestra.mp4" \
  --output "palestra.srt" \
  --format srt \
  --language pt
```

### Gerar legendas WebVTT para HTML5

```bash
python scripts/transcribe.py \
  --input "treinamento.mp4" \
  --output "treinamento.vtt" \
  --format vtt
```

### Transcrição em lote — pasta de entrevistas

```bash
python scripts/batch_transcribe.py \
  --input-dir "entrevistas/" \
  --output-dir "transcricoes/" \
  --language pt \
  --model small \
  --format md
```

---

## 3. Formatos de Entrada Suportados

| Categoria | Extensões                                      |
|-----------|------------------------------------------------|
| Áudio     | `.mp3` `.wav` `.m4a` `.ogg` `.flac` `.aac` `.opus` `.wma` |
| Vídeo     | `.mp4` `.mkv` `.avi` `.mov` `.webm` `.ts` `.m4v` |

> **Dica:** O Whisper extrai o áudio automaticamente de arquivos de vídeo via ffmpeg.

---

## 4. Formatos de Saída

| Formato | Extensão | Ideal para                          |
|---------|----------|-------------------------------------|
| Markdown | `.md`   | Relatórios, documentação, Obsidian  |
| Texto   | `.txt`   | Leitura simples, copiar/colar       |
| SRT     | `.srt`   | Legendas para players de vídeo      |
| VTT     | `.vtt`   | Legendas para HTML5 / YouTube       |
| JSON    | `.json`  | Integração programática, APIs       |

---

## 5. Troubleshooting

### Erro: "ffmpeg not found"
- Instale o ffmpeg e certifique-se de que está no PATH
- Teste: abra o terminal e digite `ffmpeg -version`

### Erro: "CUDA out of memory"
- Use um modelo menor (`--model base` ou `--model tiny`)
- Ou force CPU: `WHISPER_DEVICE=cpu python scripts/transcribe.py ...`

### Transcrição com muitos erros
- Tente um modelo maior (`--model medium` ou `--model large`)
- Especifique o idioma explicitamente: `--language pt`
- Limpe o áudio antes (remova ruídos de fundo com Audacity, etc.)

### Arquivo de vídeo não reconhecido
- Converta para mp4 com: `ffmpeg -i input.avi output.mp4`

---

## 6. Extraindo metadados de um arquivo

```bash
python scripts/utils.py --audio-info "meu_audio.mp3"
```

Retornará: duração, tamanho, formato.
