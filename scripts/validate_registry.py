#!/usr/bin/env python3
"""Validate registry structure, IDs, dates, and strong-identity collisions."""

from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import re
import sys

from normalize_url import fingerprints

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "programs.jsonl"
ALLOWED_STATUS = {
    "active", "watching", "upcoming", "paused", "inactive", "closed", "rejected", "ineligible",
    "third-party", "no-reward", "low-value", "scam-risk", "unknown",
}
REQUIRED = {
    "id", "name", "organization", "aliases", "program_urls", "domains", "github", "security_contacts",
    "scope", "status", "first_seen", "last_verified", "recheck_after", "sources", "notes",
}
LIST_FIELDS = {"aliases", "program_urls", "domains", "github", "security_contacts", "scope", "sources"}


def read_rows(path: Path) -> tuple[list[tuple[int, dict]], list[str]]:
    rows = []
    errors = []
    if not path.exists():
        return rows, [f"missing registry: {path}"]
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_no}: invalid JSON: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"line {line_no}: record must be a JSON object")
            continue
        rows.append((line_no, data))
    return rows, errors


def valid_date(value) -> bool:
    if value is None:
        return True
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def main() -> int:
    rows, errors = read_rows(REGISTRY)
    seen_ids: dict[str, int] = {}
    strong_index: dict[tuple[str, str], tuple[str, int]] = {}
    for line_no, row in rows:
        missing = sorted(REQUIRED - set(row))
        if missing:
            errors.append(f"line {line_no}: missing fields: {', '.join(missing)}")
        rid = row.get("id")
        if not isinstance(rid, str) or not re.fullmatch(r"BP-\d{4,}", rid):
            errors.append(f"line {line_no}: invalid id {rid!r}")
        elif rid in seen_ids:
            errors.append(f"line {line_no}: duplicate id {rid}; first seen on line {seen_ids[rid]}")
        else:
            seen_ids[rid] = line_no
        if not isinstance(row.get("name"), str) or not row.get("name", "").strip():
            errors.append(f"line {line_no}: name must be a non-empty string")
        if row.get("status") not in ALLOWED_STATUS:
            errors.append(f"line {line_no}: invalid status {row.get('status')!r}")
        for field in LIST_FIELDS:
            if field in row and not isinstance(row[field], list):
                errors.append(f"line {line_no}: {field} must be a list")
        for field in ("first_seen", "last_verified", "recheck_after"):
            if field in row and not valid_date(row[field]):
                errors.append(f"line {line_no}: {field} must be YYYY-MM-DD or null")
        fp = fingerprints(
            name=row.get("name", ""),
            aliases=row.get("aliases", []) if isinstance(row.get("aliases", []), list) else [],
            urls=row.get("program_urls", []) if isinstance(row.get("program_urls", []), list) else [],
            domains=row.get("domains", []) if isinstance(row.get("domains", []), list) else [],
            github=row.get("github", []) if isinstance(row.get("github", []), list) else [],
            contacts=row.get("security_contacts", []) if isinstance(row.get("security_contacts", []), list) else [],
        )
        for kind in ("urls", "domains", "github", "contact_domains"):
            for value in fp[kind]:
                key = (kind, value)
                if key in strong_index:
                    other_id, other_line = strong_index[key]
                    errors.append(f"line {line_no}: strong identity collision {kind}={value!r} with {other_id} on line {other_line}")
                else:
                    strong_index[key] = (str(rid), line_no)
    if errors:
        print("Registry validation FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Registry validation OK ({len(rows)} records)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
