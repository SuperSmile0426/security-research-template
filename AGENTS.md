# Agent instructions — security program research

Read `README.md`, `research-policy.yml`, and `registry/SCHEMA.md` at the beginning of each research task. Then read and validate `registry/programs.jsonl` **before performing external discovery**.

This workspace tracks security and bug-bounty programs across repeated research sessions. Its primary invariant is:

> **Never present a previously recorded program as a new discovery merely because it appears under a different name, URL, announcement, or repository.**

`registry/programs.jsonl` is the authoritative identity and prior-research register. Conversation memory, model memory, browser history, and previous chat threads are not substitutes for it.

## Mandatory preflight

Before external discovery:

1. Read `research-policy.yml`.
2. Read `registry/programs.jsonl`.
3. Run `python3 scripts/validate_registry.py`.
4. Build an exclusion / known-identity set from every registry entry, including entries that are inactive, rejected, third-party, no-reward, low-value, scam-risk, paused, or otherwise not currently actionable.
5. Only then perform external research.

If the registry fails validation, report the failure and repair it before adding new entries.

## Duplicate prevention — mandatory

For every candidate, resolve identity using the strongest available identifiers:

1. exact normalized bounty/security URL;
2. canonical root domain;
3. GitHub organization and repository;
4. security-contact email domain;
5. organization identity;
6. explicit aliases;
7. normalized project name.

Run `python3 scripts/check_duplicate.py` before promoting a candidate to a new result.

### Matching rules

- A strong exact identifier match means the project is already known.
- Project-name similarity by itself is **not** enough to suppress a candidate. Treat it as `POSSIBLE_DUPLICATE` and resolve identity.
- A rebrand, domain migration, repository rename, or new security page does not create a new program identity if official evidence links it to an existing organization/project.
- Distinct programs run by the same organization may remain separate entries when their scope, program terms, or submission paths are meaningfully independent.
- Never create a second registry entry just to represent a new announcement for an existing program.

## New versus updated

Do not conflate identity with freshness.

Use these outcomes:

- `NEW`: no existing identity match after duplicate resolution.
- `UPDATED`: known identity with a verified material change.
- `KNOWN_NO_CHANGE`: known identity and no material change.
- `POSSIBLE_DUPLICATE`: weak match requiring identity resolution.
- `REJECTED`: researched but excluded by policy.

A material update can include:

- program launch, reopening, pause, or closure;
- reward range / pool / payout asset change;
- scope added or removed;
- submission channel changed;
- KYC, eligibility, geographic, or payout requirement changed;
- new protocol component, chain, bridge, node, wallet, cryptographic implementation, or major deployed version added;
- official security page or terms materially rewritten;
- explicit new audit campaign / contest that is independently actionable.

Cosmetic website changes, repeated announcements, social reposts, and unchanged mirror pages are not material updates.

## Research quality and freshness

Prefer primary sources in this order:

1. official security / bounty terms;
2. official project documentation;
3. official GitHub organization or repository;
4. official project announcements;
5. reputable secondary sources when primary evidence is unavailable.

For claims such as "launched today", "new", "updated", "active", "paused", or reward availability:

- capture the source URL;
- record the observed / verified date;
- distinguish source publication date from the date you first saw it;
- do not infer publication dates from search-result ordering;
- when the source is undated, say so explicitly.

A program that is already in the registry can still appear in results only under `UPDATED` when a material change is verified.

## Registry discipline

Keep researched negative results. Status values include actionable and non-actionable states so future sessions do not waste time rediscovering them.

Never delete a registry record merely because a program becomes inactive or unattractive. Update status and timestamps instead.

Permanent IDs use `BP-0001`, `BP-0002`, etc. Never renumber or reuse IDs.

Before writing a registry entry:

1. run duplicate check;
2. capture official identifiers;
3. add evidence / source URLs;
4. record `first_seen` and `last_verified`;
5. set the correct status;
6. create or update the human dossier under `programs/<slug>/PROGRAM.md` when the project merits ongoing tracking.

## Research policy

`research-policy.yml` is the user's reusable preference layer. Apply it when ranking what deserves investigation, but do not use preference filtering to erase known identities.

If a candidate is excluded by policy, record it with the appropriate status/reason when it is likely to recur in future searches.

## Safety

Researching the existence, terms, funding signals, scope, and submission process of security programs is passive research.

Do not treat this repository as authorization to exploit production systems. Do not generate production traffic, access credentials, bypass controls, exfiltrate data, or perform destructive testing without explicit authorization from the target program.

## Session completion

At the end of a research session:

1. ensure the registry still validates;
2. record new / updated / rejected candidates;
3. update `research/SESSION_LOG.md`;
4. add future recheck items to `watchlist/README.md`;
5. clearly separate verified facts, unresolved questions, and inferred assessments in any report.

## First task when asked to research

Validate the registry, load the known identity set, inspect the research policy, search for candidate programs, deduplicate every candidate, and return only:

- genuinely `NEW` programs;
- materially `UPDATED` known programs;
- important unresolved `POSSIBLE_DUPLICATE` cases.

Do not pad results with already-known unchanged programs.
