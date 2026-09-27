#!/usr/bin/env python3
"""Add a program to the registry only after deterministic duplicate checks."""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys

from check_duplicate import check_candidate, load_registry
from normalize_url import fingerprints, registrable_domain

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "registry" / "programs.jsonl"
PROGRAM_TEMPLATE = ROOT / "programs" / "PROGRAM_TEMPLATE.md"

ALLOWED_STATUS = {
    "active", "watching", "upcoming", "paused", "inactive", "closed", "rejected", "ineligible",
    "third-party", "no-reward", "low-value", "scam-risk", "unknown",
}


def next_id(rows: list[dict]) -> str:
    maximum = 0
    for row in rows:
        m = re.fullmatch(r"BP-(\d+)", str(row.get("id", "")))
        if m:
            maximum = max(maximum, int(m.group(1)))
    return f"BP-{maximum + 1:04d}"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "program"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    p.add_argument("--name", required=True)
    p.add_argument("--organization", default="")
    p.add_argument("--alias", action="append", default=[])
    p.add_argument("--url", action="append", default=[])
    p.add_argument("--domain", action="append", default=[])
    p.add_argument("--github", action="append", default=[])
    p.add_argument("--security-contact", action="append", default=[])
    p.add_argument("--scope", action="append", default=[])
    p.add_argument("--source", action="append", default=[])
    p.add_argument("--status", default="unknown", choices=sorted(ALLOWED_STATUS))
    p.add_argument("--first-seen", default=date.today().isoformat())
    p.add_argument("--last-verified", default=date.today().isoformat())
    p.add_argument("--recheck-after", default=None)
    p.add_argument("--notes", default="")
    p.add_argument("--no-dossier", action="store_true")
    return p


def main() -> int:
    args = build_parser().parse_args()
    rows = load_registry(args.registry)
    candidate_fp = fingerprints(name=args.name, aliases=args.alias, urls=args.url, domains=args.domain,
                                github=args.github, contacts=args.security_contact)
    duplicate = check_candidate(rows, candidate_fp)
    if duplicate["outcome"] != "NEW":
        print(f"Refusing to add: {duplicate['outcome']}", file=sys.stderr)
        for match in duplicate["matches"]:
            print(f"- {match['id']} {match['name']}", file=sys.stderr)
        print("Resolve identity or update the existing entry instead.", file=sys.stderr)
        return 1

    inferred_domains = {registrable_domain(v) for v in args.url if registrable_domain(v)}
    inferred_domains |= {registrable_domain(v) for v in args.domain if registrable_domain(v)}
    record = {
        "id": next_id(rows), "name": args.name, "organization": args.organization,
        "aliases": sorted(set(args.alias)), "program_urls": sorted(set(args.url)),
        "domains": sorted(inferred_domains), "github": sorted(set(args.github)),
        "security_contacts": sorted(set(args.security_contact)), "scope": sorted(set(args.scope)),
        "status": args.status, "first_seen": args.first_seen, "last_verified": args.last_verified,
        "recheck_after": args.recheck_after, "sources": sorted(set(args.source)), "notes": args.notes,
    }
    args.registry.parent.mkdir(parents=True, exist_ok=True)
    with args.registry.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"Added {record['id']} {record['name']}")
    if not args.no_dossier:
        dossier_dir = ROOT / "programs" / slugify(args.name)
        dossier_dir.mkdir(parents=True, exist_ok=True)
        dossier = dossier_dir / "PROGRAM.md"
        if not dossier.exists():
            template = PROGRAM_TEMPLATE.read_text(encoding="utf-8")
            template = template.replace("[Program / project name]", args.name, 1)
            template = template.replace("`BP-XXXX`", f"`{record['id']}`", 1)
            dossier.write_text(template, encoding="utf-8")
            print(f"Created {dossier.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
