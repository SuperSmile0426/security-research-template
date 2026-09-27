import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_duplicate import check_candidate  # noqa: E402
from normalize_url import fingerprints, normalize_github, normalize_name, normalize_url, registrable_domain  # noqa: E402


class NormalizeTests(unittest.TestCase):
    def test_normalize_url_drops_tracking_and_fragment(self):
        self.assertEqual(normalize_url("http://www.Example.org/security/?utm_source=x#top"), "https://example.org/security")

    def test_root_domain(self):
        self.assertEqual(registrable_domain("https://security.example.co.jp/a"), "example.co.jp")

    def test_github(self):
        self.assertEqual(normalize_github("https://github.com/Example-Labs/Core.git"), "example-labs/core")

    def test_name(self):
        self.assertEqual(normalize_name("Example Protocol (Labs)"), "exampleprotocollabs")

    def test_shared_host_is_not_project_domain(self):
        fp = fingerprints(name="Project A", urls=["https://github.com/project-a/core/security"])
        self.assertNotIn("github.com", fp["domains"])
        self.assertIn("https://github.com/project-a/core/security", fp["urls"])


class DuplicateTests(unittest.TestCase):
    def setUp(self):
        self.rows = [{
            "id": "BP-0001", "name": "Example Protocol", "organization": "Example Labs", "aliases": ["Example"],
            "program_urls": ["https://example.org/security"], "domains": ["example.org"],
            "github": ["example-labs/core"], "security_contacts": ["security@example.org"], "scope": ["l1"],
            "status": "active", "first_seen": "2026-09-26", "last_verified": "2026-09-26",
            "recheck_after": None, "sources": [], "notes": "",
        }]

    def test_domain_is_duplicate(self):
        candidate = fingerprints(name="Different Branding", urls=["https://docs.example.org/bounty"])
        self.assertEqual(check_candidate(self.rows, candidate)["outcome"], "DUPLICATE")

    def test_name_only_is_possible(self):
        candidate = fingerprints(name="Example Protocol")
        self.assertEqual(check_candidate(self.rows, candidate)["outcome"], "POSSIBLE_DUPLICATE")

    def test_unrelated_is_new(self):
        candidate = fingerprints(name="Other Chain", urls=["https://other.example/security"])
        self.assertEqual(check_candidate(self.rows, candidate)["outcome"], "NEW")

    def test_unrelated_github_security_pages_do_not_collide_by_host(self):
        known = [{
            "id": "BP-0002", "name": "Project A", "organization": "Project A", "aliases": [],
            "program_urls": ["https://github.com/project-a/core/security"], "domains": [],
            "github": ["project-a/core"], "security_contacts": [], "scope": ["protocol"],
            "status": "watching", "first_seen": "2026-09-26", "last_verified": "2026-09-26",
            "recheck_after": None, "sources": [], "notes": "",
        }]
        candidate = fingerprints(name="Project B", urls=["https://github.com/project-b/core/security"], github=["project-b/core"])
        self.assertEqual(check_candidate(known, candidate)["outcome"], "NEW")


if __name__ == "__main__":
    unittest.main()
