# Security Program Research Template

A reusable workspace for discovering, deduplicating, and tracking security / bug-bounty **programs** over time.

> **This repository manages programs, not vulnerability reports.**

The local program registry is authoritative for identity and prior research. Agent memory is not.

## Purpose

Repeated security-program research tends to fail when:

1. the same program is surfaced again under another name, URL, or repository;
2. previously rejected, inactive, no-reward, or low-value programs are forgotten and researched again;
3. a known program changes materially, but simplistic duplicate filtering hides the update.

This template solves those problems by separating **program identity** from **program changes**.

It is not intended to store vulnerabilities, PoCs, exploit evidence, finding severity, submission reports, or per-vulnerability status.

## What is tracked

For each program, track only program-level information such as:

- identity, organization, aliases, domains, and repositories;
- official security / bounty URLs;
- active, upcoming, paused, closed, rejected, or other status;
- technical scope and exclusions;
- reward range, payout asset, and payout method;
- KYC / eligibility requirements;
- submission channel and disclosure rules;
- first-seen, last-verified, and recheck dates;
- primary sources;
- material changes to previously known program terms.

## Repository map

- `AGENTS.md` — canonical operating instructions for AI agents.
- `.github/copilot-instructions.md` — GitHub Copilot compatibility layer.
- `.github/prompts/research-bounties.prompt.md` — reusable program-discovery prompt.
- `research-policy.yml` — inclusion, exclusion, payout, scope, and freshness preferences.
- `registry/programs.jsonl` — **authoritative program database**.
- `registry/aliases.json` — optional alias / organization mappings.
- `registry/SCHEMA.md` — registry field contract.
- `programs/PROGRAM_TEMPLATE.md` — optional human-readable dossier for one program.
- `programs/README.md` — explains when a dossier is worth creating.
- `research/candidates/` — temporary candidate identity research.
- `research/daily/` — optional discovery-session notes.
- `research/SESSION_LOG.md` — chronological research-session log.
- `watchlist/README.md` — programs to recheck later.
- `scripts/normalize_url.py` — canonicalization / fingerprint helpers.
- `scripts/check_duplicate.py` — deterministic program duplicate check.
- `scripts/add_program.py` — add a genuinely new program.
- `scripts/validate_registry.py` — registry integrity and identity-collision checker.
- `tests/test_registry_tools.py` — standard-library tests for identity logic.

## Canonical storage model

`registry/programs.jsonl` is the source of truth. One line equals one program identity.

You do **not** need a Markdown file for every registry record. Create `programs/<slug>/PROGRAM.md` only when a program needs richer human notes, complex terms, or a longer history than is convenient inside JSONL.

Do not create files for individual vulnerability findings or submissions in this repository.

## Identity model

A candidate can have several fingerprints:

- normalized official program URL;
- canonical project domain;
- GitHub organization/repository;
- security-contact domain;
- exact alias / normalized project name.

Strong identifiers can establish that a program is already known. Name similarity alone must not automatically suppress a candidate; it produces `POSSIBLE_DUPLICATE` until identity is resolved.

Shared platforms such as GitHub or third-party bounty platforms are not treated as project domains. Exact hosted URLs and repository identities are matched separately.

## Program discovery outcomes

- `NEW` — no known program identity match exists.
- `UPDATED` — a known program has a verified material change.
- `KNOWN_NO_CHANGE` — already known and materially unchanged.
- `POSSIBLE_DUPLICATE` — weak identity match requiring resolution.
- `REJECTED` — researched but excluded by policy; keep it recorded to prevent rediscovery.

A material update may include a change to program status, scope, reward, payout, KYC/eligibility, submission channel, program terms, or independently actionable campaign.

## Quick start

Validate the registry:

```bash
python3 scripts/validate_registry.py
```

Check a candidate before researching it deeply:

```bash
python3 scripts/check_duplicate.py \
  --name "Example Protocol" \
  --url "https://example.org/security" \
  --github "example-labs/core"
```

Add a genuinely new program:

```bash
python3 scripts/add_program.py \
  --name "Example Protocol" \
  --organization "Example Labs" \
  --url "https://example.org/security" \
  --github "example-labs/core" \
  --status active
```

Run tests:

```bash
python3 -m unittest discover -s tests -v
```

## Research workflow

1. Read `AGENTS.md`, `research-policy.yml`, and `registry/programs.jsonl`.
2. Validate the registry.
3. Search for candidate programs.
4. Run `scripts/check_duplicate.py` before deep research.
5. Resolve possible duplicates using official project identity.
6. If known, determine whether program-level terms changed materially.
7. If genuinely new, add it to the registry.
8. Record useful negative research too, so it is not rediscovered later.
9. Update `last_verified`, status, sources, or `recheck_after` when appropriate.

## Safety and evidence

This is a passive program-research workspace, not authorization to test live systems.

Prefer primary sources: official security pages, project documentation, official GitHub repositories, official program terms, and official announcements. Distinguish source publication date from local `first_seen` and `last_verified` dates.

## Data format

`registry/programs.jsonl` uses JSON Lines so each program is an independent JSON object that is easy to append, diff, validate, and process.

Program IDs are permanent. Never renumber or reuse them.
