# Agent instructions — security program research

Read `README.md`, `research-policy.yml`, and `registry/SCHEMA.md` at the beginning of each task. Then read and validate `registry/programs.jsonl` **before external discovery**.

This repository manages **security / bug-bounty programs only**.

Do not use it to manage vulnerability findings, PoCs, exploit evidence, per-bug reports, severity ratings, submission dossiers, or vendor-response threads for individual vulnerabilities.

Its primary invariant is:

> **Never present a previously recorded program as a new discovery merely because it appears under a different name, URL, announcement, repository, or campaign page.**

`registry/programs.jsonl` is the authoritative program identity and prior-research register. Conversation memory, model memory, browser history, and previous chat threads are not substitutes for it.

## Mandatory preflight

Before external discovery:

1. Read `research-policy.yml`.
2. Read `registry/programs.jsonl`.
3. Run `python3 scripts/validate_registry.py`.
4. Build a known-program identity set from every registry entry, including inactive, rejected, third-party, no-reward, low-value, scam-risk, paused, and otherwise non-actionable records.
5. Only then research new candidates.

If the registry fails validation, repair it before adding new entries.

## Duplicate prevention — mandatory

For every candidate, resolve program identity using the strongest available identifiers:

1. exact normalized security / bounty URL;
2. canonical project root domain;
3. GitHub organization and repository;
4. security-contact email domain;
5. organization identity;
6. explicit aliases;
7. normalized project name.

Run `python3 scripts/check_duplicate.py` before promoting a candidate to `NEW`.

### Matching rules

- A strong exact identifier match means the program is already known.
- Project-name similarity by itself is not sufficient to suppress a candidate. Treat it as `POSSIBLE_DUPLICATE` and resolve identity.
- A rebrand, domain migration, repository rename, or new security page does not create a new program identity when official evidence links it to an existing program.
- Distinct programs run by one organization may remain separate when scope, terms, eligibility, submission path, or campaign identity is independently actionable.
- Never create a second registry entry merely for a repeated announcement of the same program.
- Shared hosting/platform domains such as GitHub or a third-party bounty platform must not be treated as a project identity by themselves.

## Program outcomes

Use these classifications:

- `NEW`: no existing program identity match after duplicate resolution.
- `UPDATED`: known program with a verified material program-level change.
- `KNOWN_NO_CHANGE`: known program and no material change.
- `POSSIBLE_DUPLICATE`: weak identity evidence requiring resolution.
- `REJECTED`: researched but excluded by policy.

A material program update can include:

- launch, reopening, pause, closure, or status change;
- reward range, reward pool, payout asset, or payout method change;
- technical scope added or removed;
- submission channel change;
- KYC, identity, eligibility, or geographic requirement change;
- new protocol component, chain, bridge, node, wallet, cryptographic implementation, or deployed version added to program scope;
- material rewrite of official program terms;
- an independently actionable new campaign with its own scope or terms.

Cosmetic website changes, repeated announcements, unchanged mirror pages, and social reposts are not material updates.

## Program data only

Track program-level fields such as:

- program name and aliases;
- organization / operator;
- official program and project URLs;
- canonical domains and GitHub repositories;
- status;
- scope and exclusions;
- rewards and payout assets;
- KYC / eligibility requirements;
- submission method;
- disclosure rules;
- source URLs;
- first-seen / last-verified / recheck dates;
- verified material-change history.

Do not add per-vulnerability fields such as finding ID, severity, vulnerable function, PoC, exploit trace, report body, submission reference, or vendor disposition.

## Research quality and freshness

Prefer primary sources in this order:

1. official security / bounty terms;
2. official project documentation;
3. official GitHub organization or repository;
4. official project announcements;
5. reputable secondary sources when primary evidence is unavailable.

For claims such as `new`, `launched today`, `updated`, `active`, `paused`, or reward availability:

- capture the source URL;
- record the observed / verified date;
- distinguish source publication date from local first-seen date;
- do not infer publication dates from search-result ordering;
- when the source is undated, say so explicitly.

A known program may appear in results under `UPDATED` only when a material change is verified.

## Registry discipline

Keep useful negative research. A program that is inactive, unattractive, low-value, third-party, or currently unpaid may still be worth retaining so it is not researched repeatedly.

Never delete a registry record merely because a program becomes inactive or unattractive. Update status and timestamps instead.

Permanent IDs use `BP-0001`, `BP-0002`, etc. Never renumber or reuse IDs.

Before adding a registry entry:

1. run duplicate check;
2. resolve official identity;
3. capture primary sources;
4. record `first_seen` and `last_verified`;
5. set the appropriate status;
6. create `programs/<slug>/PROGRAM.md` only if richer human-readable program notes are useful.

`registry/programs.jsonl` remains canonical even when a dossier exists.

## Research policy

`research-policy.yml` is the reusable preference layer. Apply it when deciding what deserves investigation, but do not use preference filtering to erase known program identities.

If a candidate is excluded by policy and is likely to recur in searches, record it with an appropriate status/reason.

## Safety

Researching the existence, terms, funding signals, scope, and submission process of a security program is passive research.

Do not treat this repository as authorization to exploit production systems. Do not generate production traffic, access credentials, bypass controls, exfiltrate data, or perform destructive testing without explicit authorization from the target program.

## Session completion

At the end of a research session:

1. ensure the registry still validates;
2. save any new, updated, or rejected program records;
3. update program-level metadata and source dates;
4. update `research/SESSION_LOG.md` if session notes are useful;
5. add future recheck items to `watchlist/README.md`.

Do not create vulnerability-report artifacts as part of session completion.

## First task when asked to research

Validate the registry, load known program identities, inspect the research policy, search for candidate programs, deduplicate every candidate, and return only:

- genuinely `NEW` programs;
- materially `UPDATED` known programs;
- important unresolved `POSSIBLE_DUPLICATE` cases.

Do not pad results with already-known unchanged programs.
