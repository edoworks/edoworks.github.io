import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_cross_domain_status", ROOT / "scripts/check_cross_domain_status.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class CrossDomainStatusTests(unittest.TestCase):
    def test_matching_visible_retirement_copy(self):
        html = "<html><body><p>Rung is retired and is not an active product or paid offer.</p></body></html>"
        self.assertEqual([], MODULE.compare_status(html, ROOT))

    def test_hidden_script_cannot_satisfy_public_copy(self):
        html = "<html><body><script>Rung is retired and is not an active product or paid offer.</script><p>Rung available.</p></body></html>"
        self.assertTrue(MODULE.compare_status(html, ROOT))


if __name__ == "__main__":
    unittest.main()
