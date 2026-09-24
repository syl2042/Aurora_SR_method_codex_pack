import shutil
import tempfile
import unittest
from pathlib import Path

from sr_route_check import check, select

ROOT = Path(__file__).resolve().parents[2]


class RoutingTests(unittest.TestCase):
    def test_fast_path_and_triggered_routes(self):
        self.assertEqual(select(ROOT, [])["sources"], [])
        cases = {
            "diagnosis": {"evidence"},
            "architecture": {"impact", "propagation"},
            "ui": {"ui"},
            "pass": {"passes", "execution"},
            "memory": {"memory"},
            "verification": {"verification"},
            "activation": {"build"},
            "resume": {"resume"},
        }
        for event, expected in cases.items():
            with self.subTest(event=event):
                actual = {Path(item).stem for item in select(ROOT, [event])["sources"]}
                self.assertEqual(actual, expected)

    def test_combined_routes_are_deduplicated(self):
        result = select(ROOT, ["mutation", "architecture", "knowledge"])
        self.assertEqual(
            {Path(item).stem for item in result["sources"]},
            {"authority", "impact", "propagation", "evidence"},
        )

    def test_unknown_trigger_fails_closed(self):
        with self.assertRaises(ValueError):
            select(ROOT, ["unknown"])

    def test_every_required_module_is_reachable(self):
        self.assertEqual(check(ROOT), [])
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = root / "docs/codex"
            base.mkdir(parents=True)
            shutil.copy(ROOT / "core/SR_ROUTES.json", base / "SR_ROUTES.json")
            shutil.copytree(ROOT / "core/procedures", base / "procedures")
            missing = base / "procedures/build.md"
            missing.unlink()
            self.assertTrue(any("build" in error for error in check(root)))


if __name__ == "__main__":
    unittest.main()
