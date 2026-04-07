#!/usr/bin/env python3
"""
transcribe.py — Script principal de transcrição de áudio/vídeo usando OpenAI Whisper.

Uso:
    python transcribe.py --input <arquivo> --output <saída> [opções]

Exemplos:
    python transcribe.py --input reuniao.mp3 --output transcricao.md
    python transcribe.py --input video.mp4 --output legendas.srt --format srt --language pt
    python transcribe.py --input audio.wav --output saida.txt --model medium
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Importações opcionais com mensagem amigável
try:
    import whisper
except ImportError:
    print("[ERRO] OpenAI Whisper não encontrado.")
    print("Instale com: pip install openai-whisper")
    sys.exit(1)

from utils import (
    check_dependencies,
    format_timestamp,
    get_audio_info,
    generate_report,
    print_progress,
)


SUPPORTED_FORMATS = {
    "audio": [".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac", ".wma", ".opus"],
    "video": [".mp4", ".mkv", ".avi", ".mov", ".webm", ".ts", ".mts", ".m4v"],
}

OUTPUT_FORMATS = ["txt", "srt", "vtt", "json", "md"]


def load_model(model_name: str):
    """Carrega o modelo Whisper com feedback de progresso."""
    print(f"[INFO] Carregando modelo Whisper '{model_name}'...")
    model = whisper.load_model(model_name)
    print(f"[OK]   Modelo '{model_name}' carregado.")
    return model


def transcribe_file(
    input_path: str,
    model,
    language: str = None,
    task: str = "transcribe",
) -> dict:
    """
    Transcreve um arquivo de áudio/vídeo.

    Args:
        input_path: Caminho do arquivo de entrada.
        model: Modelo Whisper carregado.
        language: Código do idioma (ex: 'pt', 'en'). None = detecção automática.
        task: 'transcribe' ou 'translate' (para inglês).

    Returns:
        Dict com resultado da transcrição (texto, segmentos, idioma detectado, etc.)
    """
    input_path = str(Path(input_path).resolve())

    options = {"task": task}
    if language:
        options["language"] = language

    print(f"[INFO] Transcrevendo: {os.path.basename(input_path)}")
    result = model.transcribe(input_path, **options)
    print(f"[OK]   Transcrição concluída. Idioma detectado: {result.get('language', 'desconhecido')}")
    return result


def save_output(result: dict, output_path: str, output_format: str, input_path: str):
    """Salva o resultado da transcrição no formato especificado."""
    output_path = Path(output_path)
    # Ajusta extensão se necessário
    if output_path.suffix.lower().lstrip(".") != output_format:
        output_path = output_path.with_suffix(f".{output_format}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_format == "txt":
        _save_txt(result, output_path)
    elif output_format == "srt":
        _save_srt(result, output_path)
    elif output_format == "vtt":
        _save_vtt(result, output_path)
    elif output_format == "json":
        _save_json(result, output_path)
    elif output_format == "md":
        _save_md(result, output_path, input_path)

    print(f"[OK]   Arquivo salvo: {output_path}")
    return str(output_path)


def _save_txt(result: dict, output_path: Path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result["text"].strip())


def _save_srt(result: dict, output_path: Path):
    segments = result.get("segments", [])
    lines = []
    for i, seg in enumerate(segments, start=1):
        start = format_timestamp(seg["start"], format="srt")
        end = format_timestamp(seg["end"], format="srt")
        text = seg["text"].strip()
        lines.append(f"{i}\n{start} --> {end}\n{text}\n")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def _save_vtt(result: dict, output_path: Path):
    segments = result.get("segments", [])
    lines = ["WEBVTT\n"]
    for seg in segments:
        start = format_timestamp(seg["start"], format="vtt")
        end = format_timestamp(seg["end"], format="vtt")
        text = seg["text"].strip()
        lines.append(f"{start} --> {end}\n{text}\n")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def _save_json(result: dict, output_path: Path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def _save_md(result: dict, output_path: Path, input_path: str):
    report = generate_report(result, input_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)


def main():
    parser = argparse.ArgumentParser(
        description="Transcreve arquivos de áudio/vídeo usando OpenAI Whisper.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--input", "-i", required=True,
        help="Caminho do arquivo de áudio ou vídeo."
    )
    parser.add_argument(
        "--output", "-o", required=True,
        help="Caminho do arquivo de saída (incluindo nome e extensão)."
    )
    parser.add_argument(
        "--model", "-m", default="base",
        choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
        help="Tamanho do modelo Whisper. Padrão: base."
    )
    parser.add_argument(
        "--language", "-l", default=None,
        help="Idioma do áudio (ex: pt, en, es). Padrão: detecção automática."
    )
    parser.add_argument(
        "--format", "-f", default="md",
        choices=OUTPUT_FORMATS,
        help="Formato de saída: txt, srt, vtt, json, md. Padrão: md."
    )
    parser.add_argument(
        "--translate", action="store_true",
        help="Traduz o áudio para inglês em vez de transcrever no idioma original."
    )
    parser.add_argument(
        "--no-check", action="store_true",
        help="Pula a verificação de dependências."
    )

    args = parser.parse_args()

    # Verifica dependências
    if not args.no_check:
        ok, missing = check_dependencies()
        if not ok:
            print(f"[ERRO] Dependências faltando: {', '.join(missing)}")
            print("       Execute: python utils.py --check-deps para mais detalhes.")
            sys.exit(1)

    # Verifica arquivo de entrada
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[ERRO] Arquivo não encontrado: {input_path}")
        sys.exit(1)

    ext = input_path.suffix.lower()
    all_supported = SUPPORTED_FORMATS["audio"] + SUPPORTED_FORMATS["video"]
    if ext not in all_supported:
        print(f"[AVISO] Extensão '{ext}' pode não ser suportada.")
        print(f"        Formatos suportados: {', '.join(all_supported)}")

    # Executa transcrição
    task = "translate" if args.translate else "transcribe"
    model = load_model(args.model)
    result = transcribe_file(str(input_path), model, language=args.language, task=task)

    # Salva resultado
    saved_path = save_output(result, args.output, args.format, str(input_path))

    print(f"\n✅ Transcrição concluída!")
    print(f"   Arquivo: {saved_path}")
    print(f"   Idioma:  {result.get('language', 'N/A')}")
    print(f"   Palavras: ~{len(result['text'].split())}")


if __name__ == "__main__":
    main()
