#!/usr/bin/env python3
"""Create a baseline QA test directory structure under app_build."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_layouts() -> dict[str, object]:
    assets_path = Path(__file__).resolve().parent.parent / "assets" / "test-layouts.json"
    return json.loads(assets_path.read_text(encoding="utf-8"))


def detect_stack(app_build: Path) -> str:
    if (app_build / "package.json").exists():
        return "node"
    python_markers = [
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt",
        "setup.py",
    ]
    if any((app_build / marker).exists() for marker in python_markers):
        return "python"
    return "node"


def create_layout(app_build: Path, stack: str) -> list[Path]:
    layouts = load_layouts()
    selected = layouts[stack]
    directories = selected["directories"]
    created: list[Path] = []

    for relative_dir in directories:
        directory = app_build / relative_dir
        directory.mkdir(parents=True, exist_ok=True)
        gitkeep = directory / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.write_text("", encoding="utf-8")
            created.append(gitkeep)
        else:
            created.append(directory)

    return created


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("app_build", help="Path to the app_build directory.")
    parser.add_argument(
        "--stack",
        choices=["auto", "node", "python"],
        default="auto",
        help="Project stack. Defaults to auto detection.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    app_build = Path(args.app_build).resolve()
    app_build.mkdir(parents=True, exist_ok=True)

    stack = detect_stack(app_build) if args.stack == "auto" else args.stack
    created = create_layout(app_build, stack)

    print(f"Stack: {stack}")
    print(f"Target: {app_build}")
    print(f"Entries ensured: {len(created)}")
    for entry in created:
        print(f"- {entry}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
