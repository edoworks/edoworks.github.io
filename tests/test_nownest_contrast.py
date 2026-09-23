import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_nownest_contrast", ROOT / "scripts/check_nownest_contrast.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class NowNestContrastTests(unittest.TestCase):
    def test_canonical_tokens_pass(self):
        css = (ROOT / "nownest/styles.css").read_text(encoding="utf-8")
        self.assertEqual([], MODULE.validate_css_text(css))

    def test_low_contrast_honey_foreground_is_rejected(self):
        css = (ROOT / "nownest/styles.css").read_text(encoding="utf-8")
        css = css.replace("--on-honey: #28231d", "--on-honey: #fff8ea")
        errors = MODULE.validate_css_text(css)
        self.assertTrue(any("on-honey/honey" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
