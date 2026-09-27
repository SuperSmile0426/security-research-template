# Repository instructions

`AGENTS.md` is the canonical operating contract for this repository. Follow it for all security-program research tasks.

Before external discovery, read:

- `AGENTS.md`
- `research-policy.yml`
- `registry/SCHEMA.md`
- `registry/programs.jsonl`

Mandatory invariant: do not present an already recorded program as `NEW`. Run `python3 scripts/check_duplicate.py` for candidates and `python3 scripts/validate_registry.py` before and after registry edits.

Known programs may still be reported as `UPDATED` when a material change is verified. Keep rejected, inactive, no-reward, third-party, low-value, or scam-risk records so they are not rediscovered repeatedly.

Prefer official / primary sources and distinguish publication date, first-seen date, and last-verified date. Never infer a precise launch/update date from search ordering alone.
