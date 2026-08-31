from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .tables import next_id, read_csv, write_csv
from .validate import validate_pack


def intake_note(pack_dir: str | Path, note: str) -> dict[str, str]:
    """Append a source and an attempted intake row, then verify the source row."""
    root = Path(pack_dir)
    note = (note or "").strip()
    if not note:
        raise ValueError("note is empty")

    before = validate_pack(root)
    if not before.ok:
        raise ValueError("pack is already invalid: " + "; ".join(before.errors))

    sources_path = root / "sources.csv"
    log_path = root / "intake_log.csv"
    sources = read_csv(sources_path)
    logs = read_csv(log_path)

    source_id = next_id("SRC-", [row["source_id"] for row in sources])
    log_id = next_id("LOG-", [row["log_id"] for row in logs])
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    source_fields = ["source_id", "captured_at", "class", "status", "raw_text", "notes"]
    log_fields = [
        "log_id",
        "captured_at",
        "source_id",
        "routed_to",
        "owner_id",
        "write_status",
        "verified_at",
        "summary",
    ]

    sources.append(
        {
            "source_id": source_id,
            "captured_at": now,
            "class": "DIRECT_REPORT",
            "status": "DRAFT",
            "raw_text": note,
            "notes": "Routed by canonkit intake. Not canon.",
        }
    )
    write_csv(sources_path, source_fields, sources)

    logs.append(
        {
            "log_id": log_id,
            "captured_at": now,
            "source_id": source_id,
            "routed_to": "sources.csv",
            "owner_id": source_id,
            "write_status": "ATTEMPTED",
            "verified_at": "",
            "summary": _clip(note),
        }
    )
    write_csv(log_path, log_fields, logs)

    # Read-back gate. If this fails, mark FAILED and do not claim success.
    readback_sources = read_csv(sources_path)
    found = next((row for row in readback_sources if row.get("source_id") == source_id), None)
    logs = read_csv(log_path)
    target = next(row for row in logs if row.get("log_id") == log_id)
    if found and found.get("raw_text") == note:
        target["write_status"] = "VERIFIED"
        target["verified_at"] = now
        target["summary"] = f"Verified source {source_id}. Still DRAFT, not promoted."
    else:
        target["write_status"] = "FAILED"
        target["summary"] = f"Read-back failed for {source_id}"
    write_csv(log_path, log_fields, logs)

    after = validate_pack(root)
    if not after.ok:
        raise ValueError("intake left the pack invalid: " + "; ".join(after.errors))

    return {
        "source_id": source_id,
        "log_id": log_id,
        "write_status": target["write_status"],
        "routed_to": "sources.csv",
    }


def _clip(text: str, limit: int = 120) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 3] + "..."
