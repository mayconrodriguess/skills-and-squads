# Modelos Whisper — Comparativo

O OpenAI Whisper oferece cinco tamanhos de modelo, cada um com diferente relação entre velocidade, qualidade e recursos necessários.

---

## Tabela Comparativa

| Modelo     | Parâmetros | RAM necessária | Velocidade (relativa) | Qualidade PT-BR | Recomendado para                         |
|------------|------------|----------------|-----------------------|-----------------|------------------------------------------|
| `tiny`     | 39M        | ~1 GB          | ★★★★★ (mais rápido)  | Regular         | Testes rápidos, recursos muito limitados |
| `base`     | 74M        | ~1 GB          | ★★★★☆                | Boa             | **Uso geral (padrão recomendado)**       |
| `small`    | 244M       | ~2 GB          | ★★★☆☆                | Muito boa       | Áudio com sotaque, qualidade moderada    |
| `medium`   | 769M       | ~5 GB          | ★★☆☆☆                | Excelente       | Reuniões, entrevistas, alta qualidade    |
| `large`    | 1550M      | ~10 GB         | ★☆☆☆☆ (mais lento)  | Máxima          | Produção profissional (GPU recomendada)  |
| `large-v2` | 1550M      | ~10 GB         | ★☆☆☆☆                | Máxima+         | Melhor versão geral do large             |
| `large-v3` | 1550M      | ~10 GB         | ★☆☆☆☆                | Máxima++        | Versão mais recente, melhor em PT-BR     |

---

## Detalhes por Modelo

### `tiny`
- **Velocidade:** ~32x mais rápido que o áudio em CPU
- **Uso:** Protótipos, testes de pipeline, transcrições onde velocidade é crítica
- **Limitação:** Muitos erros em PT-BR com sotaques regionais ou microfone baixo

### `base` ← **Padrão da skill**
- **Velocidade:** ~16x mais rápido que o áudio em CPU
- **Uso:** Ideal para a maioria dos casos de uso cotidianos
- **Download:** ~150MB (baixado na primeira execução)

### `small`
- **Velocidade:** ~6x mais rápido que o áudio em CPU
- **Uso:** Quando `base` comete erros frequentes — boa opção intermediária
- **Download:** ~480MB

### `medium`
- **Velocidade:** ~2x mais rápido que o áudio em CPU
- **Uso:** Reuniões corporativas, entrevistas, conteúdo profissional
- **Download:** ~1.5GB

### `large-v3` ← **Máxima qualidade**
- **Velocidade:** ~1x (precisa de GPU para uso prático)
- **Uso:** Produção, transcrições críticas, legendamento profissional
- **Download:** ~3GB
- **VRAM GPU:** ~10GB recomendado (NVIDIA)

---

## Quando usar GPU vs CPU?

| Situação                    | Recomendação                           |
|-----------------------------|----------------------------------------|
| GPU NVIDIA com VRAM ≥ 4GB  | Use `medium` ou `large`                |
| GPU com VRAM < 4GB          | Use `small` ou `base`                  |
| Apenas CPU                  | Use `base` ou `tiny`                   |
| CPU moderna (i7+/Ryzen 7+)  | `small` é viável com paciência         |

---

## Como especificar o modelo

```bash
# Usando base (padrão)
python scripts/transcribe.py --input audio.mp3 --output out.md

# Usando medium para maior qualidade
python scripts/transcribe.py --input audio.mp3 --output out.md --model medium

# Usando large-v3 para máxima qualidade
python scripts/transcribe.py --input audio.mp3 --output out.md --model large-v3
```

---

## Localização dos modelos baixados

Os modelos são armazenados em cache automaticamente:
- **Windows:** `%USERPROFILE%\.cache\whisper\`
- **Linux/Mac:** `~/.cache/whisper/`

Para pré-baixar um modelo sem transcrever:
```python
import whisper
whisper.load_model("medium")
```
