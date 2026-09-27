# Security Research Template

A reusable workspace for discovering and tracking security / bug-bounty programs without repeatedly rediscovering the same projects.

The core design principle is simple:

> **The local registry is authoritative for identity and prior research. Agent memory is not.**

This repository is intended for AI-assisted research with Codex, ChatGPT-connected coding agents, GitHub Copilot agents, or a human researcher.

## What this template solves

Repeated security-program research tends to fail in three ways:

1. the same program is surfaced again under a different name, URL, or GitHub repository;
2. previously rejected / inactive / no-reward projects are forgotten and researched again;
3. genuinely useful changes to a known program are hidden by simplistic "duplicate" filtering.

This template separates **identity** from **change detection**.

A known project is not new, but it may still be worth reporting as **UPDATED** when its reward, scope, submission channel, status, payout requirements, or other material terms change.

## Repository map

- `AGENTS.md` — canonical operating instructions for AI agents.
- `.github/copilot-instructions.md` — GitHub Copilot compatibility layer.
- `research-policy.yml` — research preferences, inclusion rules, exclusions, and freshness policy.
- `registry/programs.jsonl` — authoritative machine-readable program registry.
- `registry/aliases.json` — optional cross-project aliases and organization-name mappings.
- `registry/SCHEMA.md` — registry field contract.
- `programs/PROGRAM_TEMPLATE.md` — human-readable dossier template for a researched program.
- `research/candidates/CANDIDATE_TEMPLATE.md` — working record before a candidate is accepted into the registry.
- `research/daily/DAILY_TEMPLATE.md` — daily research log template.
- `research/SESSION_LOG.md` — chronological session log.
- `watchlist/README.md` — projects worth rechecking later.
- `reports/RESEARCH_TEMPLATE.md` — copy-ready research result format.
- `scripts/normalize_url.py` — canonicalization / fingerprint helpers.
- `scripts/check_duplicate.py` — deterministic duplicate check.
- `scripts/add_program.py` — safely add a new registry entry after duplicate checks.
- `scripts/validate_registry.py` — registry integrity and collision checker.
- `tests/test_registry_tools.py` — standard-library tests for identity logic.

## Identity model

A candidate can have several fingerprints:

- normalized program URL;
- canonical domain;
- GitHub organization/repository;
- security-contact domain;
- exact alias / normalized project name.

Strong identifiers (for example the same GitHub repository or canonical domain) can prove an existing identity. Name similarity alone must **not** automatically suppress a candidate; it should produce a possible-duplicate warning that needs identity resolution.

## Research result classes

Use exactly these high-level outcomes:

- `NEW` — no known identity match exists.
- `UPDATED` — identity is already known, but a material change is verified.
- `KNOWN_NO_CHANGE` — known program with no material change.
- `POSSIBLE_DUPLICATE` — weak identity evidence only; investigate before adding.
- `REJECTED` — researched but excluded by policy. Keep it in the registry so it is not rediscovered.

## Quick start

Validate the empty / current registry:

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

## Recommended research workflow

1. Read `AGENTS.md`, `research-policy.yml`, and `registry/programs.jsonl`.
2. Run a registry validation.
3. Search for candidate programs.
4. Before deep research, run `scripts/check_duplicate.py`.
5. Resolve any possible duplicate using official domains, GitHub ownership, documentation, and security contacts.
6. For a known identity, compare current facts with its registry/dossier and report only material changes.
7. For a genuinely new identity, add it with `scripts/add_program.py`.
8. Record rejected or low-value candidates too; otherwise they will be rediscovered later.
9. Update the session log and any watchlist recheck date.

## Safety and evidence

This is a research-management template, not authorization to test live systems. Discovery and verification should stay passive unless a program explicitly authorizes active testing.

Prefer primary sources: official security pages, official documentation, official GitHub repositories, official program terms, and official announcements. Record access / verification dates and do not present an inferred publication date as verified.

## Data format choice

`registry/programs.jsonl` uses JSON Lines so one program is one independent JSON object per line. It is easy for agents and scripts to append, diff, validate, and process without loading a custom database.

Do not hand-edit IDs after they are assigned. IDs are permanent and never reused.
