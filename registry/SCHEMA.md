# Program registry schema

`programs.jsonl` is the authoritative identity register. It contains one JSON object per line.

## Required fields

Every record must contain:

```json
{
  "id": "BP-0001",
  "name": "Example Protocol",
  "organization": "Example Labs",
  "aliases": [],
  "program_urls": [],
  "domains": [],
  "github": [],
  "security_contacts": [],
  "scope": [],
  "status": "active",
  "first_seen": "2026-09-26",
  "last_verified": "2026-09-26",
  "recheck_after": null,
  "sources": [],
  "notes": ""
}
```

## IDs

- Format: `BP-` plus four or more digits.
- IDs are permanent.
- Never renumber or reuse an ID.
- New IDs increment the current maximum.

## Status

Allowed values:

- `active`
- `watching`
- `upcoming`
- `paused`
- `inactive`
- `closed`
- `rejected`
- `ineligible`
- `third-party`
- `no-reward`
- `low-value`
- `scam-risk`
- `unknown`

These states are deliberately broader than "active / inactive": negative research is valuable because it prevents repeated rediscovery.

## Identity fields

### `aliases`

Known project / program names, old names, abbreviations, or branded campaign names.

### `program_urls`

Official bounty, security, responsible-disclosure, audit-campaign, or submission URLs. Store full source URLs; scripts normalize them when comparing.

### `domains`

Canonical domains associated with program identity. Do not include unrelated analytics/CDN domains.

### `github`

GitHub identities in `owner/repo` form. Organization-only values may be stored as `owner/*` when the entire organization is the relevant identifier.

### `security_contacts`

Security email addresses or official contact URLs. Email domains contribute to identity matching.

## Research metadata

### `first_seen`

The date this local research registry first identified the project. This is **not** automatically the program launch date.

### `last_verified`

The most recent date on which program facts were checked against current sources.

### `recheck_after`

Optional ISO date for an intentionally deferred candidate / watch item.

### `sources`

Official or supporting source URLs used to verify the current entry.

## Optional fields

Programs may add structured fields such as:

```json
{
  "rewards": {
    "min": null,
    "max": null,
    "currency": []
  },
  "payout": {
    "type": "crypto",
    "assets": ["USDC"],
    "kyc": "unknown"
  },
  "submission": {
    "method": "email",
    "target": "security@example.org"
  },
  "material_change": {
    "last_changed": null,
    "summary": ""
  }
}
```

The validator permits extra fields so the registry can evolve without a migration for every research attribute.

## Duplicate semantics

A program identity is considered strongly matched when one or more strong identifiers coincide, for example:

- same normalized official program URL;
- same canonical domain;
- same GitHub repository / organization identity;
- same security-contact domain.

An exact normalized name/alias match without a strong identifier is only a possible duplicate and requires identity resolution.
