#!/usr/bin/env python3
"""Check a candidate program against the local authoritative registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from normalize_url import fingerprints

DEFAULT_REGISTRY = Path(__file__).resolve().parents[1] / "registry" / "programs.jsonl"


def load_registry(path: Path) -> list[dict]:
    rows = []
    if not path.exists():
        return rows
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        try:
            rows.append(json.loads(raw))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{number}: invalid JSON: {exc}") from exc
    return rows


def entry_fingerprints(entry: dict) -> dict[str, set[str]]:
    return fingerprints(
        name=entry.get("name", ""), aliases=entry.get("aliases", []), urls=entry.get("program_urls", []),
        domains=entry.get("domains", []), github=entry.get("github", []), contacts=entry.get("security_contacts", []),
    )


def compare(candidate: dict[str, set[str]], entry: dict) -> dict:
    known = entry_fingerprints(entry)
    matches: dict[str, list[str]] = {}
    for key in candidate:
        overlap = sorted(candidate[key] & known[key])
        if overlap:
            matches[key] = overlap
    strong_keys = {"urls", "domains", "github", "contact_domains"}
    strong = sorted(strong_keys & set(matches))
    name_only = "names" in matches and not strong
    result = "DUPLICATE" if strong else ("POSSIBLE_DUPLICATE" if name_only else "NO_MATCH")
    return {
        "result": result,
        "id": entry.get("id"),
        "name": entry.get("name"),
        "status": entry.get("status"),
        "strong_match_types": strong,
        "matches": matches,
    }


def check_candidate(rows: list[dict], candidate: dict[str, set[str]]) -> dict:
    comparisons = [compare(candidate, row) for row in rows]
    duplicates = [c for c in comparisons if c["result"] == "DUPLICATE"]
    possibles = [c for c in comparisons if c["result"] == "POSSIBLE_DUPLICATE"]
    if duplicates:
        return {"outcome": "DUPLICATE", "matches": duplicates}
    if possibles:
        return {"outcome": "POSSIBLE_DUPLICATE", "matches": possibles}
    return {"outcome": "NEW", "matches": []}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    p.add_argument("--name", default="")
    p.add_argument("--alias", action="append", default=[])
    p.add_argument("--url", action="append", default=[])
    p.add_argument("--domain", action="append", default=[])
    p.add_argument("--github", action="append", default=[])
    p.add_argument("--security-contact", action="append", default=[])
    p.add_argument("--json", action="store_true", dest="as_json")
    return p


def main() -> int:
    args = build_parser().parse_args()
    candidate = fingerprints(name=args.name, aliases=args.alias, urls=args.url, domains=args.domain,
                             github=args.github, contacts=args.security_contact)
    if not any(candidate.values()):
        print("Provide at least one identity field.", file=sys.stderr)
        return 2
    result = check_candidate(load_registry(args.registry), candidate)
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["outcome"])
        for match in result["matches"]:
            print(f"- {match['id']} {match['name']} [{match['status']}]")
            for kind, values in sorted(match["matches"].items()):
                print(f"  {kind}: {', '.join(values)}")
    return 1 if result["outcome"] in {"DUPLICATE", "POSSIBLE_DUPLICATE"} else 0


if __name__ == "__main__":
    raise SystemExit(main())
