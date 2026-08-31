from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from . import REQUIRED_FILES
from .tables import ROW_STATUSES, SOURCE_CLASSES, WRITE_GATES, read_csv, split_ids


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_pack(pack_dir: str | Path) -> Report:
    root = Path(pack_dir)
    report = Report()

    if not root.is_dir():
        report.errors.append(f"pack does not exist: {root}")
        return report

    for name in REQUIRED_FILES:
        if not (root / name).exists():
            report.errors.append(f"missing required file: {name}")
    if report.errors:
        return report

    sources = read_csv(root / "sources.csv")
    concepts = read_csv(root / "concepts.csv")
    rules = read_csv(root / "rules.csv")
    index = read_csv(root / "file_index.csv")
    system_map = read_csv(root / "system_map.csv")
    intake = read_csv(root / "intake_log.csv")
    router = (root / "router.md").read_text(encoding="utf-8")

    source_ids = [row.get("source_id", "") for row in sources]
    concept_ids = [row.get("concept_id", "") for row in concepts]
    rule_ids = [row.get("rule_id", "") for row in rules]

    _require_unique(report, "sources.source_id", source_ids)
    _require_unique(report, "concepts.concept_id", concept_ids)
    _require_unique(report, "rules.rule_id", rule_ids)
    _require_unique(report, "intake_log.log_id", [row.get("log_id", "") for row in intake])
    _require_unique(report, "file_index.entry_id", [row.get("entry_id", "") for row in index])
    _require_unique(report, "system_map.domain", [row.get("domain", "") for row in system_map])

    for row in sources:
        sid = row.get("source_id", "")
        if row.get("class") not in SOURCE_CLASSES:
            report.errors.append(f"{sid}: bad source class {row.get('class')}")
        if row.get("status") not in ROW_STATUSES:
            report.errors.append(f"{sid}: bad status {row.get('status')}")
        if not (row.get("raw_text") or "").strip():
            report.errors.append(f"{sid}: empty raw_text")

    for row in concepts:
        cid = row.get("concept_id", "")
        if row.get("status") not in ROW_STATUSES:
            report.errors.append(f"{cid}: bad status {row.get('status')}")
        if not (row.get("definition") or "").strip():
            report.errors.append(f"{cid}: empty definition")
        _check_source_links(report, cid, row.get("source_ids", ""), source_ids)

    for row in rules:
        rid = row.get("rule_id", "")
        for col in ("trigger", "action", "verification"):
            if not (row.get(col) or "").strip():
                report.errors.append(f"{rid}: missing {col}")
        if row.get("status") not in ROW_STATUSES:
            report.errors.append(f"{rid}: bad status {row.get('status')}")
        _check_source_links(report, rid, row.get("source_ids", ""), source_ids)

    owner_ids = set(concept_ids) | set(rule_ids) | set(source_ids)
    for row in intake:
        lid = row.get("log_id", "")
        if row.get("write_status") not in WRITE_GATES:
            report.errors.append(f"{lid}: bad write_status {row.get('write_status')}")
        if row.get("source_id") not in source_ids:
            report.errors.append(f"{lid}: source {row.get('source_id')} not in sources.csv")
        owner = row.get("owner_id") or ""
        routed = row.get("routed_to") or ""
        if owner and owner not in owner_ids:
            report.errors.append(f"{lid}: owner {owner} has no home")
        if routed == "concepts.csv" and owner and owner not in concept_ids:
            report.errors.append(f"{lid}: routed to concepts.csv but owner is not a concept")
        if routed == "rules.csv" and owner and owner not in rule_ids:
            report.errors.append(f"{lid}: routed to rules.csv but owner is not a rule")
        if row.get("write_status") == "VERIFIED" and not (row.get("verified_at") or "").strip():
            report.errors.append(f"{lid}: VERIFIED without verified_at")

    if "concepts.csv" not in router or "rules.csv" not in router:
        report.warnings.append("router.md should name concepts.csv and rules.csv")
    if len(router.splitlines()) > 120:
        report.warnings.append("router.md is getting long; keep it a router")

    homes = [row.get("canonical_home", "") for row in system_map]
    if len(homes) != len(set(homes)) and homes.count("sources.csv") > 2:
        report.warnings.append("several domains share sources.csv; split when they earn owners")

    return report


def _require_unique(report: Report, label: str, values: list[str]) -> None:
    seen: set[str] = set()
    for value in values:
        if not value:
            report.errors.append(f"{label}: empty id")
            continue
        if value in seen:
            report.errors.append(f"{label}: duplicate {value}")
        seen.add(value)


def _check_source_links(report: Report, owner_id: str, raw: str, source_ids: list[str]) -> None:
    links = split_ids(raw)
    if not links:
        report.errors.append(f"{owner_id}: missing source_ids")
        return
    for link in links:
        if link not in source_ids:
            report.errors.append(f"{owner_id}: unknown source {link}")
