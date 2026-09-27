# Repository instructions

`AGENTS.md` is the canonical operating contract for this repository.

This repository manages **security / bug-bounty programs only**. Do not create or maintain vulnerability findings, PoCs, exploit evidence, per-bug reports, severity tracking, or submission dossiers here.

Before external discovery, read:

- `AGENTS.md`
- `research-policy.yml`
- `registry/SCHEMA.md`
- `registry/programs.jsonl`

Mandatory invariant: do not present an already recorded program as `NEW`.

Run `python3 scripts/check_duplicate.py` for candidates and `python3 scripts/validate_registry.py` before and after registry edits.

Known programs may still surface as `UPDATED` when a material **program-level** change is verified. Keep rejected, inactive, no-reward, third-party, low-value, or scam-risk records so they are not repeatedly rediscovered.

Prefer official / primary sources and distinguish publication date, local first-seen date, and last-verified date. Never infer a precise launch/update date from search ordering alone.

`registry/programs.jsonl` is canonical. Files under `programs/` are optional human-readable program dossiers, not vulnerability reports.
