from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


WRITE_GATES = {"ATTEMPTED", "COMPLETED", "VERIFIED", "FAILED"}
ROW_STATUSES = {"DRAFT", "ACTIVE", "SUPERSEDED", "FROZEN", "REJECTED"}
SOURCE_CLASSES = {
    "DIRECT_REPORT",
    "QUOTED",
    "INTERPRETATION",
    "HYPOTHESIS",
    "EVIDENCE",
    "CORRECTION",
    "DESIGN_PRINCIPLE",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: Iterable[str], rows: list[dict[str, str]]) -> None:
    fieldnames = list(fieldnames)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def split_ids(raw: str) -> list[str]:
    if not raw:
        return []
    return [part.strip() for part in raw.replace(";", ",").split(",") if part.strip()]


def next_id(prefix: str, existing: Iterable[str]) -> str:
    numbers = []
    for item in existing:
        if item.startswith(prefix):
            tail = item[len(prefix) :].lstrip("-")
            if tail.isdigit():
                numbers.append(int(tail))
    return f"{prefix}{max(numbers, default=0) + 1:03d}"
