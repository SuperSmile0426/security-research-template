---
description: Research fresh or materially updated security programs without repeating known registry entries.
---

Read `AGENTS.md`, `research-policy.yml`, and the complete `registry/programs.jsonl`.

Validate the registry first. Build the known identity set. Research current security / bug-bounty programs that fit the policy, checking every candidate against the local registry before deep investigation.

Return only:

1. `NEW` — genuinely unknown identities;
2. `UPDATED` — known identities with verified material changes;
3. important unresolved `POSSIBLE_DUPLICATE` cases.

Do not return known unchanged programs. Record useful negative research so future runs do not rediscover it. Prefer official sources and give exact evidence for freshness claims.
