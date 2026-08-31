from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .intake import intake_note
from .validate import validate_pack


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="canonkit",
        description="Validate and route one-home knowledge packs.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="check a pack against SPEC.md")
    v.add_argument("pack", type=Path)

    i = sub.add_parser("intake", help="file a note as source evidence and verify the write")
    i.add_argument("pack", type=Path)
    i.add_argument("note", help="raw note text")

    args = parser.parse_args(argv)

    if args.cmd == "validate":
        report = validate_pack(args.pack)
        for warning in report.warnings:
            print(f"warning: {warning}")
        if report.ok:
            print(f"ok: {args.pack}")
            return 0
        for error in report.errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    if args.cmd == "intake":
        result = intake_note(args.pack, args.note)
        print(
            f"{result['write_status']} {result['source_id']} "
            f"-> {result['routed_to']} ({result['log_id']})"
        )
        return 0 if result["write_status"] == "VERIFIED" else 2

    return 2
