#!/usr/bin/env python3
"""Render a QA report from the bundled template."""

from __future__ import annotations

import argparse
from pathlib import Path


def load_template(template_path: str | None) -> str:
    if template_path:
        return Path(template_path).read_text(encoding="utf-8")
    default_template = Path(__file__).resolve().parent.parent / "assets" / "qa-report-template.md"
    return default_template.read_text(encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--files-audited", type=int, required=True)
    parser.add_argument("--bugs-fixed", type=int, required=True)
    parser.add_argument("--unit-tests", type=int, required=True)
    parser.add_argument("--integration-tests", type=int, required=True)
    parser.add_argument("--e2e-tests", type=int, required=True)
    parser.add_argument("--security-issues", type=int, required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--root-cause", default="Not provided.")
    parser.add_argument("--fix-summary", default="Not provided.")
    parser.add_argument("--verification", default="Not provided.")
    parser.add_argument("--template", help="Optional path to a custom template.")
    parser.add_argument("--output", help="Optional path to save the rendered report.")
    return parser.parse_args()


def render(template: str, args: argparse.Namespace) -> str:
    replacements = {
        "{{files_audited}}": str(args.files_audited),
        "{{bugs_fixed}}": str(args.bugs_fixed),
        "{{unit_tests}}": str(args.unit_tests),
        "{{integration_tests}}": str(args.integration_tests),
        "{{e2e_tests}}": str(args.e2e_tests),
        "{{security_issues}}": str(args.security_issues),
        "{{status}}": args.status,
        "{{root_cause}}": args.root_cause,
        "{{fix_summary}}": args.fix_summary,
        "{{verification}}": args.verification,
    }

    rendered = template
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)
    return rendered


def main() -> int:
    args = parse_args()
    output = render(load_template(args.template), args)

    if args.output:
        output_path = Path(args.output).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
