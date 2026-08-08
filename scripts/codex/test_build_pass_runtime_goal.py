#!/usr/bin/env python3
import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/codex/build_pass_runtime_goal.py"


LOTS_YAML = """\
lots:
  - lot_id: APP-LOT-001
    title: Foundation
    status: done
    objective: Prepare foundation.
    acceptance_criteria:
      - Foundation works.
    verification_commands:
      - python3 -m pytest
    stop_conditions:
      - gate_failure
  - lot_id: APP-LOT-002
    title: Feature A
    status: validated
    objective: Build feature A.
    depends_on:
      - APP-LOT-001
    acceptance_criteria:
      - Feature A works.
    verification_commands:
      - python3 -m pytest
    stop_conditions:
      - gate_failure
  - lot_id: APP-LOT-003
    title: Feature B
    status: validated
    objective: Build feature B.
    depends_on:
      - APP-LOT-002
    acceptance_criteria:
      - Feature B works.
    verification_commands:
      - python3 -m pytest
    stop_conditions:
      - gate_failure
"""


def passes_yaml(status: str = "validated") -> str:
    return f"""\
passes:
  - pass_id: APP-PASS-001
    title: Feature pass
    status: {status}
    priority: high
    lots:
      - APP-LOT-002
      - APP-LOT-003
    sequencing:
      strategy: topological_with_foundation_first
      rationale:
        - Shared E2E.
      dependency_overrides: []
      open_questions: []
    preflight:
      required_before_start:
        - APP-LOT-001 done.
      secrets_required: []
      external_actions_required: []
      human_validation_required: []
      migrations_required: []
      open_questions: []
    shared_sources:
      - docs/CURRENT_STATE.md
    e2e_strategy:
      mode: grouped_at_pass_end
      items:
        - Run grouped user E2E after both lots.
    stop_on:
      - gate_failure
"""


class BuildPassRuntimeGoalTest(unittest.TestCase):
    def run_script(self, root: Path, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root), *args, "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def write_project(self, root: Path, status: str = "validated") -> None:
        (root / "docs/codex").mkdir(parents=True)
        (root / "docs/codex/SR_LOTS.yaml").write_text(LOTS_YAML, encoding="utf-8")
        (root / "docs/codex/SR_PASSES.yaml").write_text(passes_yaml(status), encoding="utf-8")

    def test_builds_goal_command_below_1000_chars(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_project(root)
            result = self.run_script(
                root,
                "--pass-id",
                "APP-PASS-001",
                "--output",
                "docs/codex/tasks/2026-08-08_app-pass-001/pass_runtime_goal.md",
            )
            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            data = json.loads(result.stdout)
            self.assertTrue(data["ok"])
            self.assertLessEqual(data["goal_command_chars"], 1000)
            output = root / data["output"]
            self.assertTrue(output.exists())
            text = output.read_text(encoding="utf-8")
            self.assertIn("max_goal_command_chars: 1000", text)
            self.assertIn("hard_limit: 4000", text)
            self.assertIn("grouped_at_pass_end", text)
            self.assertIn("`user_testing`", text)
            self.assertIn("Ne pas enchainer une passe suivante", text)

    def test_rejects_planned_pass_without_explicit_dry_run_flag(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_project(root, "planned")
            result = self.run_script(
                root,
                "--pass-id",
                "APP-PASS-001",
                "--output",
                "docs/codex/tasks/2026-08-08_app-pass-001/pass_runtime_goal.md",
            )
            self.assertNotEqual(0, result.returncode)
            data = json.loads(result.stdout)
            self.assertFalse(data["ok"])
            self.assertTrue(any("not allowed for runtime goal" in error for error in data["errors"]), data)

    def test_allows_planned_pass_for_dry_run(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_project(root, "planned")
            result = self.run_script(
                root,
                "--pass-id",
                "APP-PASS-001",
                "--output",
                "docs/codex/tasks/2026-08-08_app-pass-001/pass_runtime_goal.md",
                "--allow-planned",
            )
            self.assertEqual(0, result.returncode, result.stderr + result.stdout)

    def test_goal_length_gate_fails_when_limit_is_too_small(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_project(root)
            result = self.run_script(
                root,
                "--pass-id",
                "APP-PASS-001",
                "--output",
                "docs/codex/tasks/2026-08-08_app-pass-001/pass_runtime_goal.md",
                "--max-goal-command-chars",
                "10",
            )
            self.assertNotEqual(0, result.returncode)
            data = json.loads(result.stdout)
            self.assertFalse(data["ok"])
            self.assertTrue(any("max_goal_command_chars" in error for error in data["errors"]), data)


if __name__ == "__main__":
    unittest.main()
