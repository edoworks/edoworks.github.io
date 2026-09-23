import importlib.util
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_site_claims", ROOT / "scripts/check_site_claims.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class SiteClaimTests(unittest.TestCase):
    def fixture(self, directory: str) -> Path:
        target = Path(directory) / "site"
        shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        return target

    def test_canonical_site_passes(self):
        self.assertEqual([], MODULE.validate(ROOT))

    def test_download_and_sla_claims_are_rejected(self):
        with TemporaryDirectory() as directory:
            root = self.fixture(directory)
            support = root / "nownest/support/index.html"
            support.write_text(support.read_text() + "free to download; support replies within 24 hours")
            errors = MODULE.validate(root)
            self.assertGreaterEqual(sum("unsupported NowNest claim" in error for error in errors), 2)

    def test_positive_availability_and_apple_approval_are_rejected(self):
        with TemporaryDirectory() as directory:
            root = self.fixture(directory)
            home = root / "nownest/index.html"
            home.write_text(home.read_text() + "Available now. Approved by Apple.")
            errors = MODULE.validate(root)
            self.assertGreaterEqual(sum("unsupported NowNest claim" in error for error in errors), 2)

    def test_contradictory_release_and_sla_variants_are_rejected(self):
        with TemporaryDirectory() as directory:
            root = self.fixture(directory)
            home = root / "nownest/index.html"
            home.write_text(
                home.read_text()
                + "NowNest is available to download. Apple acceptance is complete. "
                + "The app has been released. We answer within one business day."
            )
            errors = MODULE.validate(root)
            self.assertGreaterEqual(sum("unsupported NowNest claim" in error for error in errors), 4)

    def test_dead_rung_hostname_is_rejected(self):
        with TemporaryDirectory() as directory:
            root = self.fixture(directory)
            home = root / "index.html"
            home.write_text(home.read_text() + '<a href="https://rung.edoworks.com">Rung</a>')
            self.assertTrue(any("failing rung" in error for error in MODULE.validate(root)))

    def test_missing_discovery_records_are_rejected(self):
        with TemporaryDirectory() as directory:
            root = self.fixture(directory)
            sitemap = root / "sitemap.xml"
            sitemap.write_text(sitemap.read_text().replace("https://edoworks.com/nownest/terms/", ""))
            errors = MODULE.validate(root)
            self.assertTrue(any("sitemap omits" in error for error in errors))

    def test_unsupported_trademark_and_individual_deletion_claims_are_rejected(self):
        with TemporaryDirectory() as directory:
            root = self.fixture(directory)
            terms = root / "nownest/terms/index.html"
            terms.write_text(terms.read_text() + '"NowNest" is a trademark of Foculoom LLC.')
            support = root / "nownest/support/index.html"
            support.write_text(support.read_text() + "Testers can delete individual saved ideas.")
            errors = MODULE.validate(root)
            self.assertGreaterEqual(sum("stale or unsupported" in error for error in errors), 2)

    def test_paraphrased_deletion_and_trademark_symbol_claims_are_rejected(self):
        with TemporaryDirectory() as directory:
            root = self.fixture(directory)
            support = root / "nownest/support/index.html"
            support.write_text(support.read_text() + "You can delete saved ideas one at a time. NowNest™")
            errors = MODULE.validate(root)
            self.assertGreaterEqual(sum("unsupported NowNest claim pattern" in error for error in errors), 2)

    def test_full_public_contract_is_required(self):
        with TemporaryDirectory() as directory:
            root = self.fixture(directory)
            home = root / "nownest/index.html"
            home.write_text(home.read_text().replace("Save again", "Keep it"))
            privacy = root / "nownest/privacy/index.html"
            privacy.write_text(
                privacy.read_text()
                .replace("does not schedule or send notifications", "stays quiet")
                .replace("network access", "remote connection")
            )
            terms = root / "nownest/terms/index.html"
            terms.write_text(terms.read_text().replace("does not claim trademark registration or adoption", "makes no brand statement"))
            errors = MODULE.validate(root)
            self.assertEqual(4, sum("public contract is incomplete" in error for error in errors))

    def test_truthful_deletion_and_trademark_disclaimers_are_allowed(self):
        with TemporaryDirectory() as directory:
            root = self.fixture(directory)
            support = root / "nownest/support/index.html"
            support.write_text(support.read_text() + "You cannot delete saved ideas individually.")
            terms = root / "nownest/terms/index.html"
            terms.write_text(terms.read_text() + "NowNest is not a trademark of Foculoom LLC.")
            errors = MODULE.validate(root)
            self.assertFalse(any("unsupported NowNest claim pattern" in error for error in errors))

    def test_stale_public_product_language_is_rejected(self):
        with TemporaryDirectory() as directory:
            root = self.fixture(directory)
            home = root / "nownest/index.html"
            home.write_text(home.read_text() + "Park ideas. Park Interruptions. Review Later.")
            errors = MODULE.validate(root)
            self.assertGreaterEqual(sum("stale or unsupported" in error for error in errors), 3)

    def test_home_requires_featured_nownest_record(self):
        with TemporaryDirectory() as directory:
            root = self.fixture(directory)
            home = root / "index.html"
            home.write_text(home.read_text().replace('class="product-spotlight" id="nownest"', 'class="product-summary"'))
            self.assertTrue(any("home does not feature" in error for error in MODULE.validate(root)))

    def test_shared_theme_and_art_are_required(self):
        with TemporaryDirectory() as directory:
            root = self.fixture(directory)
            (root / "nownest/assets/sophie-nest.svg").unlink()
            support = root / "nownest/support/index.html"
            support.write_text(support.read_text().replace('<link rel="stylesheet" href="/nownest/styles.css">', ""))
            errors = MODULE.validate(root)
            self.assertTrue(any("product asset is missing" in error for error in errors))
            self.assertTrue(any("shared product theme" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
