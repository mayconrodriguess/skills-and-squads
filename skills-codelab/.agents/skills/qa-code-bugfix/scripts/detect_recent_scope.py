#!/usr/bin/env python3
"""Detect the current author and summarize recent repository changes."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def resolve_repo(repo: Path) -> Path:
    if not repo.exists():
        raise RuntimeError(f"Repository path does not exist: {repo}")
    if not repo.is_dir():
        raise RuntimeError(f"Repository path is not a directory: {repo}")
    try:
        top_level = run_git(repo, "rev-parse", "--show-toplevel")
    except RuntimeError as exc:
        raise RuntimeError(f"Not a git repository: {repo}") from exc
    return Path(top_level).resolve()


def resolve_author(repo: Path, explicit_author: str | None) -> tuple[str, str]:
    if explicit_author:
        return explicit_author, "argument"

    try:
        email = run_git(repo, "config", "user.email")
    except RuntimeError:
        email = ""

    if email:
        return email, "git config user.email"

    try:
        name = run_git(repo, "config", "user.name")
    except RuntimeError:
        name = ""

    if name:
        return name, "git config user.name"

    username = os.environ.get("GIT_AUTHOR_NAME") or os.environ.get("USERNAME") or os.environ.get("USER")
    if username:
        return username, "environment"

    raise RuntimeError("Unable to determine author from git config or environment.")


def collect_commits(repo: Path, author: str, since: str) -> list[dict[str, object]]:
    output = run_git(
        repo,
        "log",
        f"--since={since}",
        f"--author={re.escape(author)}",
        "--date=short",
        "--pretty=format:__COMMIT__%n%H%x09%ad%x09%s",
        "--name-only",
    )
    if not output:
        return []

    commits: list[dict[str, object]] = []
    current: dict[str, object] | None = None

    for line in output.splitlines():
        if line == "__COMMIT__":
            if current:
                current["files"] = sorted(set(current["files"]))  # type: ignore[index]
                commits.append(current)
            current = {"hash": "", "date": "", "subject": "", "files": []}
            continue

        if current is None:
            continue

        if not current["hash"]:
            parts = line.split("\t", 2)
            if len(parts) == 3:
                current["hash"], current["date"], current["subject"] = parts
            continue

        if line.strip():
            current["files"].append(line.strip())  # type: ignore[index]

    if current:
        current["files"] = sorted(set(current["files"]))  # type: ignore[index]
        commits.append(current)

    return commits


def build_summary(repo: Path, author: str, author_source: str, since: str) -> dict[str, object]:
    commits = collect_commits(repo, author, since)
    unique_files = sorted({path for commit in commits for path in commit["files"]})  # type: ignore[index]

    return {
        "repo": str(repo),
        "author": author,
        "author_source": author_source,
        "since": since,
        "commit_count": len(commits),
        "files_changed_count": len(unique_files),
        "files_changed": unique_files,
        "commits": commits,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository path. Defaults to current directory.")
    parser.add_argument("--author", help="Explicit author string to use with git log.")
    parser.add_argument("--since", default="1.week", help="Git --since value. Defaults to 1.week.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    return parser.parse_args()


def print_text(summary: dict[str, object]) -> None:
    print(f"Repository: {summary['repo']}")
    print(f"Author: {summary['author']} ({summary['author_source']})")
    print(f"Since: {summary['since']}")
    print(f"Commits: {summary['commit_count']}")
    print(f"Files changed: {summary['files_changed_count']}")

    files_changed = summary["files_changed"]
    if files_changed:
        print("Touched files:")
        for path in files_changed:
            print(f"- {path}")

    commits = summary["commits"]
    if commits:
        print("Commits:")
        for commit in commits:
            print(f"- {commit['date']} {commit['hash'][:8]} {commit['subject']}")


def main() -> int:
    args = parse_args()
    repo = Path(args.repo).resolve()

    try:
        repo = resolve_repo(repo)
        author, author_source = resolve_author(repo, args.author)
        summary = build_summary(repo, author, author_source, args.since)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print_text(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
