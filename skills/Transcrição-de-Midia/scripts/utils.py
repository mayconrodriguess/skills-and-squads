#!/usr/bin/env python3
"""
utils.py — Funções auxiliares para a skill Transcrição-de-Midia.

Inclui:
- Verificação de dependências (whisper, ffmpeg)
- Formatação de timestamps (SRT, VTT)
- Geração de relatórios Markdown
- Informações de arquivos de áudio
"""

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


# ─── Verificação de Dependências ──────────────────────────────────────────────

def check_dependencies() -> tuple[bool, list[str]]:
    """
    Verifica se whisper e ffmpeg estão instalados.

    Returns:
        (bool: tudo OK, list: lista de dependências faltando)
    """
    missing = []

    # Verifica whisper
    try:
        import whisper  # noqa: F401
    except ImportError:
        missing.append("openai-whisper (pip install openai-whisper)")

    # Verifica ffmpeg
    if not shutil.which("ffmpeg"):
        missing.append("ffmpeg (winget install ffmpeg  OU  choco install ffmpeg)")

    return len(missing) == 0, missing


# ─── Formatação de Timestamps ─────────────────────────────────────────────────

def format_timestamp(seconds: float, format: str = "srt") -> str:
    """
    Formata um número de segundos como timestamp para SRT ou VTT.

    Args:
        seconds: Tempo em segundos (float).
        format: 'srt' usa vírgula como separador decimal; 'vtt' usa ponto.

    Returns:
        String no formato HH:MM:SS,mmm (SRT) ou HH:MM:SS.mmm (VTT).
    """
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = round((seconds - int(seconds)) * 1000)

    sep = "," if format == "srt" else "."
    return f"{hours:02d}:{minutes:02d}:{secs:02d}{sep}{millis:03d}"


# ─── Informações do Arquivo de Áudio ─────────────────────────────────────────

def get_audio_info(file_path: str) -> dict:
    """
    Retorna informações básicas do arquivo de áudio/vídeo via ffprobe.

    Returns:
        Dict com 'duration_seconds', 'duration_str', 'format', 'size_mb'
        ou {'error': mensagem} se ffprobe não estiver disponível.
    """
    if not shutil.which("ffprobe"):
        return {"error": "ffprobe não encontrado (instale ffmpeg)"}

    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration,format_name,size",
            "-of", "default=noprint_wrappers=1",
            str(file_path),
        ]
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode()
        info = {}
        for line in output.strip().splitlines():
            key, _, val = line.partition("=")
            info[key.strip()] = val.strip()

        duration = float(info.get("duration", 0))
        size_bytes = int(info.get("size", 0))

        return {
            "duration_seconds": duration,
            "duration_str": _seconds_to_hms(duration),
            "format": info.get("format_name", "desconhecido"),
            "size_mb": round(size_bytes / 1_048_576, 2),
        }
    except Exception as e:
        return {"error": str(e)}


def _seconds_to_hms(seconds: float) -> str:
    """Converte segundos para string legível (1h 23min 45s)."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    parts = []
    if h:
        parts.append(f"{h}h")
    if m:
        parts.append(f"{m}min")
    parts.append(f"{s}s")
    return " ".join(parts)


# ─── Geração de Relatório Markdown ───────────────────────────────────────────

def generate_report(result: dict, input_path: str) -> str:
    """
    Gera um relatório Markdown estruturado a partir do resultado Whisper.

    Args:
        result: Dicionário retornado por model.transcribe().
        input_path: Caminho original do arquivo de mídia.

    Returns:
        String com o relatório em Markdown.
    """
    filename = os.path.basename(input_path)
    detected_lang = result.get("language", "N/A")
    text = result.get("text", "").strip()
    segments = result.get("segments", [])
    word_count = len(text.split())
    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    audio_info = get_audio_info(input_path)
    duration_str = audio_info.get("duration_str", "N/A")
    size_mb = audio_info.get("size_mb", "N/A")

    lines = [
        f"# Transcrição: {filename}",
        "",
        "## Metadados",
        "",
        f"| Campo              | Valor                    |",
        f"|--------------------|--------------------------|",
        f"| **Arquivo**        | `{filename}`              |",
        f"| **Data**           | {now}                    |",
        f"| **Duração**        | {duration_str}           |",
        f"| **Tamanho**        | {size_mb} MB             |",
        f"| **Idioma detectado**| {detected_lang.upper() if detected_lang != 'N/A' else 'N/A'} |",
        f"| **Palavras**       | ~{word_count}             |",
        "",
        "---",
        "",
        "## Transcrição Completa",
        "",
        text,
        "",
    ]

    # Adiciona segmentos com timestamps se disponíveis
    if segments:
        lines += [
            "---",
            "",
            "## Transcrição Segmentada (com timestamps)",
            "",
        ]
        for seg in segments:
            start = format_timestamp(seg["start"], format="vtt")
            end = format_timestamp(seg["end"], format="vtt")
            seg_text = seg["text"].strip()
            lines.append(f"**[{start} → {end}]** {seg_text}")
            lines.append("")

    lines += [
        "---",
        "",
        "*Gerado por Transcrição-de-Midia skill usando OpenAI Whisper*",
    ]

    return "\n".join(lines)


# ─── Progress Helper ──────────────────────────────────────────────────────────

def print_progress(message: str, status: str = "INFO"):
    """Imprime mensagem de progresso formatada."""
    icons = {"INFO": "ℹ️ ", "OK": "✅", "WARN": "⚠️ ", "ERROR": "❌"}
    icon = icons.get(status, "  ")
    print(f"{icon} [{status}] {message}")


# ─── CLI para verificação de dependências ─────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Utilitários da skill Transcrição-de-Midia.")
    parser.add_argument("--check-deps", action="store_true", help="Verifica dependências.")
    parser.add_argument("--audio-info", metavar="ARQUIVO", help="Exibe info de um arquivo de mídia.")
    args = parser.parse_args()

    if args.check_deps:
        print("\n=== Verificação de Dependências ===\n")
        ok, missing = check_dependencies()
        if ok:
            print("✅ Todas as dependências estão instaladas!\n")
        else:
            print("❌ Dependências faltando:\n")
            for dep in missing:
                print(f"   • {dep}")
            print()

    if args.audio_info:
        info = get_audio_info(args.audio_info)
        print(f"\n=== Info: {args.audio_info} ===")
        for k, v in info.items():
            print(f"  {k}: {v}")
