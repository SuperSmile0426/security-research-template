#!/usr/bin/env python3
"""Normalization helpers for security-program identity matching.

Standard-library only.
"""

from __future__ import annotations

import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

TRACKING_PREFIXES = ("utm_",)
TRACKING_KEYS = {"ref", "source", "campaign", "fbclid", "gclid"}
GITHUB_HOSTS = {"github.com", "www.github.com"}
COMMON_MULTI_PART_SUFFIXES = {
    "co.uk", "org.uk", "ac.uk", "com.au", "net.au", "org.au",
    "co.jp", "ne.jp", "or.jp", "com.br", "com.sg", "com.hk",
}

# Shared publishing / disclosure / bounty platforms are not project identity.
# Their exact URLs can still be strong fingerprints, and GitHub repo identity is
# handled independently by `normalize_github`.
SHARED_ROOT_DOMAINS = {
    "github.com", "gitlab.com", "bitbucket.org",
    "google.com", "forms.gle", "notion.site", "notion.so",
    "medium.com", "mirror.xyz",
    "x.com", "twitter.com", "discord.com", "discord.gg", "t.me",
    "immunefi.com", "cantina.xyz", "sherlock.xyz", "code4rena.com",
    "codehawks.com", "bugcrowd.com", "hackerone.com", "hackenproof.com",
    "hats.finance",
}


def normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").lower())


def _with_scheme(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    if "://" not in value:
        return "https://" + value
    return value


def normalize_url(value: str) -> str:
    if not value:
        return ""
    parsed = urlsplit(_with_scheme(value))
    host = (parsed.hostname or "").lower().rstrip(".")
    if host.startswith("www."):
        host = host[4:]
    port = parsed.port
    if port and not ((parsed.scheme == "http" and port == 80) or (parsed.scheme == "https" and port == 443)):
        host = f"{host}:{port}"
    path = re.sub(r"/+", "/", parsed.path or "/")
    if path != "/":
        path = path.rstrip("/")
    kept = []
    for key, val in parse_qsl(parsed.query, keep_blank_values=True):
        kl = key.lower()
        if kl in TRACKING_KEYS or any(kl.startswith(p) for p in TRACKING_PREFIXES):
            continue
        kept.append((key, val))
    kept.sort()
    query = urlencode(kept, doseq=True)
    return urlunsplit(("https", host, path, query, ""))


def hostname(value: str) -> str:
    if not value:
        return ""
    parsed = urlsplit(_with_scheme(value))
    host = (parsed.hostname or "").lower().rstrip(".")
    return host[4:] if host.startswith("www.") else host


def registrable_domain(value: str) -> str:
    if not value:
        return ""
    if "@" in value and "://" not in value:
        host = value.rsplit("@", 1)[1].lower().rstrip(".")
    else:
        host = hostname(value)
    if not host:
        return ""
    parts = host.split(".")
    if len(parts) <= 2:
        return host
    tail2 = ".".join(parts[-2:])
    if tail2 in COMMON_MULTI_PART_SUFFIXES and len(parts) >= 3:
        return ".".join(parts[-3:])
    return tail2


def security_contact_domain(value: str) -> str:
    value = (value or "").strip().lower()
    if "@" in value and "://" not in value:
        return registrable_domain(value)
    return registrable_domain(value)


def normalize_github(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    if "github.com" in value.lower():
        parsed = urlsplit(_with_scheme(value))
        if (parsed.hostname or "").lower() not in GITHUB_HOSTS:
            return ""
        parts = [p for p in parsed.path.split("/") if p]
    else:
        parts = [p for p in value.split("/") if p]
    if not parts:
        return ""
    owner = parts[0].lower()
    if len(parts) == 1:
        return owner + "/*"
    repo = re.sub(r"\.git$", "", parts[1], flags=re.I).lower()
    return f"{owner}/{repo}"


def _identity_root(value: str) -> str:
    root = registrable_domain(value)
    if not root or root in SHARED_ROOT_DOMAINS:
        return ""
    return root


def fingerprints(*, name: str = "", aliases: list[str] | None = None, urls: list[str] | None = None,
                 domains: list[str] | None = None, github: list[str] | None = None,
                 contacts: list[str] | None = None) -> dict[str, set[str]]:
    aliases = aliases or []
    urls = urls or []
    domains = domains or []
    github = github or []
    contacts = contacts or []
    norm_urls = {normalize_url(v) for v in urls if normalize_url(v)}
    roots = {_identity_root(v) for v in urls if _identity_root(v)}
    roots |= {_identity_root(v) for v in domains if _identity_root(v)}
    contact_domains = {security_contact_domain(v) for v in contacts if security_contact_domain(v)}
    gh = {normalize_github(v) for v in github if normalize_github(v)}
    names = {normalize_name(v) for v in [name, *aliases] if normalize_name(v)}
    return {"urls": norm_urls, "domains": roots, "github": gh, "contact_domains": contact_domains, "names": names}
