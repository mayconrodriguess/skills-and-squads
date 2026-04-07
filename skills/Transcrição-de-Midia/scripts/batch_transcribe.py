#!/usr/bin/env python3
"""
batch_transcribe.py — Transcreve todos os arquivos de áudio/vídeo em uma pasta.

Uso:
    python batch_transcribe.py --input-dir <pasta> --output-dir <destino> [opções]

Exemplos:
    python batch_transcribe.py --input-dir audios/ --output-dir transcricoes/
    python batch_transcribe.py --input-dir reunioes/ --output-dir atas/ --language pt --model small --format md
"""

import argparse
import os
import sys
import json
from pathlib import Path
from datetime import datetime

try:
    import whisper
except ImportError:
    print("[ERRO] OpenAI Whisper não encontrado.")
    print("Instale com: pip install openai-whisper")
    sys.exit(1)

from utils import check_dependencies, generate_report


SUPPORTED_EXTENSIONS = [
    ".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac", ".wma", ".opus",
    ".mp4", ".mkv", ".avi", ".mov", ".webm", ".ts", ".mts", ".m4v",
]


def discover_files(input_dir: Path, extensions: list = None) -> list:
    """Descobre todos os arquivos de mídia suportados em um diretório."""
    exts = extensions or SUPPORTED_EXTENSIONS
    found = []
    for f in input_dir.iterdir():
        if f.is_file() and f.suffix.lower() in exts:
            found.append(f)
    found.sort()
    return found


def batch_transcribe(
    input_dir: str,
    output_dir: str,
    model_name: str = "base",
    language: str = None,
    output_format: str = "md",
    extensions: list = None,
):
    """
    Transcreve todos os arquivos de mídia em input_dir e salva em output_dir.

    Args:
        input_dir: Diretório com arquivos de mídia.
        output_dir: Diretório onde serão salvos os resultados.
        model_name: Tamanho do modelo Whisper.
        language: Idioma (None = detecção automática).
        output_format: Formato de saída (txt, srt, vtt, json, md).
        extensions: Lista de extensões a filtrar (None = todas suportadas).
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        print(f"[ERRO] Diretório não encontrado: {input_path}")
        sys.exit(1)

    files = discover_files(input_path, extensions)
    if not files:
        print(f"[AVISO] Nenhum arquivo de mídia encontrado em: {input_path}")
        return

    print(f"\n📁 Encontrados {len(files)} arquivo(s) em '{input_path}'")
    print(f"📂 Saída em: '{output_path}'")
    print(f"🤖 Modelo: {model_name} | Idioma: {language or 'auto'} | Formato: {output_format}\n")
    print("─" * 60)

    # Carrega modelo uma só vez (evita recarregar para cada arquivo)
    print(f"[INFO] Carregando modelo '{model_name}'...")
    model = whisper.load_model(model_name)
    print(f"[OK]   Modelo carregado.\n")

    results_summary = []
    failed = []

    for i, file in enumerate(files, start=1):
        print(f"[{i}/{len(files)}] Transcrevendo: {file.name}")
        try:
            options = {}
            if language:
                options["language"] = language

            result = model.transcribe(str(file), **options)
            detected_lang = result.get("language", "N/A")
            word_count = len(result["text"].split())

            # Define nome do arquivo de saída
            out_file = output_path / f"{file.stem}.{output_format}"

            # Salva no formato adequado
            if output_format == "txt":
                out_file.write_text(result["text"].strip(), encoding="utf-8")
            elif output_format == "srt":
                _write_srt(result, out_file)
            elif output_format == "vtt":
                _write_vtt(result, out_file)
            elif output_format == "json":
                out_file.write_text(
                    json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
                )
            elif output_format == "md":
                report = generate_report(result, str(file))
                out_file.write_text(report, encoding="utf-8")

            print(f"    ✅ Salvo: {out_file.name} | Idioma: {detected_lang} | ~{word_count} palavras")
            results_summary.append({
                "arquivo": file.name,
                "saida": out_file.name,
                "idioma": detected_lang,
                "palavras": word_count,
                "status": "OK",
            })
        except Exception as e:
            print(f"    ❌ ERRO: {e}")
            failed.append({"arquivo": file.name, "erro": str(e)})

    # Relatório final consolidado
    print("\n" + "─" * 60)
    print(f"\n📊 RESUMO — {len(files)} arquivo(s) processado(s)")
    print(f"   ✅ Sucesso: {len(results_summary)}")
    print(f"   ❌ Falhas:  {len(failed)}")

    # Salva relatório consolidado
    summary_path = output_path / "_relatorio_batch.md"
    _write_summary_report(results_summary, failed, summary_path, input_dir, model_name, language)
    print(f"\n📄 Relatório consolidado salvo em: {summary_path}\n")


def _write_srt(result, out_file):
    from utils import format_timestamp
    lines = []
    for i, seg in enumerate(result.get("segments", []), start=1):
        start = format_timestamp(seg["start"], format="srt")
        end = format_timestamp(seg["end"], format="srt")
        lines.append(f"{i}\n{start} --> {end}\n{seg['text'].strip()}\n")
    out_file.write_text("\n".join(lines), encoding="utf-8")


def _write_vtt(result, out_file):
    from utils import format_timestamp
    lines = ["WEBVTT\n"]
    for seg in result.get("segments", []):
        start = format_timestamp(seg["start"], format="vtt")
        end = format_timestamp(seg["end"], format="vtt")
        lines.append(f"{start} --> {end}\n{seg['text'].strip()}\n")
    out_file.write_text("\n".join(lines), encoding="utf-8")


def _write_summary_report(successes, failures, path, input_dir, model, language):
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    lines = [
        "# Relatório de Transcrição em Lote",
        "",
        f"**Data:** {now}  ",
        f"**Pasta de entrada:** `{input_dir}`  ",
        f"**Modelo:** `{model}`  ",
        f"**Idioma:** `{language or 'automático'}`  ",
        "",
        "---",
        "",
        f"## ✅ Transcrições bem-sucedidas ({len(successes)})",
        "",
        "| Arquivo | Saída | Idioma | Palavras |",
        "|---------|-------|--------|----------|",
    ]
    for r in successes:
        lines.append(f"| `{r['arquivo']}` | `{r['saida']}` | {r['idioma']} | ~{r['palavras']} |")

    if failures:
        lines += [
            "",
            f"## ❌ Falhas ({len(failures)})",
            "",
            "| Arquivo | Erro |",
            "|---------|------|",
        ]
        for f in failures:
            lines.append(f"| `{f['arquivo']}` | {f['erro']} |")

    lines += ["", "---", "*Gerado por Transcrição-de-Midia skill*"]
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Transcreve em lote todos os arquivos de áudio/vídeo de uma pasta.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--input-dir", "-i", required=True, help="Pasta com arquivos de mídia.")
    parser.add_argument("--output-dir", "-o", required=True, help="Pasta para salvar transcrições.")
    parser.add_argument(
        "--model", "-m", default="base",
        choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
    )
    parser.add_argument("--language", "-l", default=None, help="Idioma (ex: pt). Padrão: auto.")
    parser.add_argument(
        "--format", "-f", default="md",
        choices=["txt", "srt", "vtt", "json", "md"],
        help="Formato de saída. Padrão: md.",
    )
    parser.add_argument(
        "--ext", nargs="+",
        help="Filtrar por extensões (ex: .mp3 .wav). Padrão: todas suportadas.",
    )
    parser.add_argument("--no-check", action="store_true", help="Pula verificação de dependências.")

    args = parser.parse_args()

    if not args.no_check:
        ok, missing = check_dependencies()
        if not ok:
            print(f"[ERRO] Dependências faltando: {', '.join(missing)}")
            sys.exit(1)

    exts = args.ext if args.ext else None
    batch_transcribe(
        args.input_dir,
        args.output_dir,
        model_name=args.model,
        language=args.language,
        output_format=args.format,
        extensions=exts,
    )


if __name__ == "__main__":
    main()
