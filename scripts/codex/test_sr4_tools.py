import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts/codex" / f"{name}.py")
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


class SR4ToolsTests(unittest.TestCase):
    def test_compactor_preserves_unique_error_and_exit_code(self):
        text = "\n".join(["warning repeated"] * 100 + ["fatal UNIQUE_MIDDLE"] + ["info"] * 100)
        self.assertIn("fatal UNIQUE_MIDDLE", module("aurora_token_run").compact(text))
        with tempfile.TemporaryDirectory() as tmp:
            command = [
                sys.executable,
                str(ROOT / "scripts/codex/aurora_token_run.py"),
                "--",
                sys.executable,
                "-c",
                "print('fatal diagnostic'); raise SystemExit(7)",
            ]
            result = subprocess.run(command, cwd=tmp, capture_output=True, text=True)
            self.assertEqual(result.returncode, 7)
            self.assertIn("fatal diagnostic", result.stdout)
            self.assertEqual(len(list((Path(tmp) / "output/codex/raw").glob("*.log"))), 1)

    def test_resume_requires_explicit_selection_when_ambiguous(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("a", "b"):
                path = root / "tasks" / name / "NEXT_SESSION_PROMPT.md"
                path.parent.mkdir(parents=True)
                path.write_text(name)
            command = [sys.executable, str(ROOT / "scripts/codex/find_next_session_prompt.py"), "--root", tmp, "--json"]
            result = json.loads(subprocess.check_output(command))
            self.assertTrue(result["ambiguous"])
            self.assertIsNone(result["selected"])

    def test_routes_reference_only_existing_procedures(self):
        routes = json.loads((ROOT / "core/SR_ROUTES.json").read_text())
        sources = {source for route in routes["routes"] for source in route["sources"]}
        self.assertLessEqual(len(sources), 11)
        for relative in sources:
            self.assertTrue((ROOT / "core" / relative).is_file(), relative)

    def test_task_state_is_compact(self):
        path = ROOT / "tasks/_TEMPLATE/task_state.yaml"
        self.assertLessEqual(len(path.read_text().splitlines()), 20)
        for marker in ("objective:", "scope:", "requirements:", "evidence:", "verification:", "next_action:"):
            self.assertIn(marker, path.read_text())


if __name__ == "__main__":
    unittest.main()
