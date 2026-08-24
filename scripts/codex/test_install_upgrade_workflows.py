#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INSTALLER = ROOT / "scripts/install_codex_pack.py"
LANGUAGES = ("en", "fr", "de", "es", "pt")
LEGACY_LAYOUTS = ROOT / "scripts/codex/fixtures/install_upgrade/legacy_layouts.json"


def run_installer(target: Path, mode: str | None) -> subprocess.CompletedProcess[str]:
    args = [
        sys.executable,
        str(INSTALLER),
        "--source",
        str(ROOT),
        "--target",
        str(target),
        "--profile",
        "default",
    ]
    if mode:
        args.append(mode)
    return subprocess.run(
        args,
        text=True,
        capture_output=True,
        timeout=120,
    )


def legacy_lots_yaml(layout: dict) -> str:
    project_key = "project_key: LEGACY\n" if layout["has_project_key"] else ""
    lot_naming = (
        "lot_naming:\n"
        "  pattern: LEGACY-<AREA>-<SEQ>\n"
        "  sequence_digits: 3\n"
        if layout["has_project_key"]
        else ""
    )
    return (
        f'version: "{layout["sr_lots_version"]}"\n'
        "project: Legacy project\n"
        f"{project_key}"
        f"{lot_naming}"
        "lots:\n"
        f'  - lot_id: "{layout["lot_id"]}"\n'
        "    title: Preserve legacy scope\n"
        "    status: proposed\n"
        "    objective: Preserve the validated legacy scope during SR upgrade.\n"
        "    acceptance_criteria:\n"
        "      - Existing requirements remain present.\n"
        "    verification_commands:\n"
        "      - git diff --check\n"
        "    stop_conditions:\n"
        "      - A project-owned file is lost.\n"
    )


def materialize_legacy_layout(target: Path, layout: dict) -> dict[str, str]:
    codex = target / "docs/codex"
    codex.mkdir(parents=True)
    if layout["source_release"]:
        (codex / "SR_PACK_VERSION.json").write_text(
            json.dumps({"version": layout["source_release"]}), encoding="utf-8"
        )
    agents = (
        "# Local project rules\n\n"
        "USER_LOCAL_RULE: keep this instruction.\n\n"
        "<!-- AURORA_SR_PACK_START -->\n"
        "## SR Bootstrap obligatoire\n"
        "- Legacy managed block.\n"
        "<!-- AURORA_SR_PACK_END -->\n"
    )
    lots = legacy_lots_yaml(layout)
    task_progress = "OPEN_USER_REQUIREMENT: preserve this validated request.\n"
    handoff = "Legacy handoff: resume the open user requirement.\n"
    skill = (
        "---\n"
        "name: custom-legacy-skill\n"
        "description: Use this preserved local project skill for legacy domain checks, when its project trigger applies, and verify its output against repository evidence before closure.\n"
        "---\n"
    )
    skill_agent = (
        "interface:\n"
        "  display_name: Custom Legacy Skill\n"
        "  short_description: Preserve legacy project domain verification\n"
    )
    (target / "AGENTS.md").write_text(agents, encoding="utf-8")
    (codex / "SR_LOTS.yaml").write_text(lots, encoding="utf-8")
    task = codex / "tasks/2026-01-01_user-legacy/progress.md"
    task.parent.mkdir(parents=True)
    task.write_text(task_progress, encoding="utf-8")
    handoff_path = target / ".handoffs/legacy.md"
    handoff_path.parent.mkdir(parents=True)
    handoff_path.write_text(handoff, encoding="utf-8")
    skill_path = codex / "project-skills/custom-legacy-skill/SKILL.md"
    skill_path.parent.mkdir(parents=True)
    skill_path.write_text(skill, encoding="utf-8")
    skill_agent_path = skill_path.parent / "agents/openai.yaml"
    skill_agent_path.parent.mkdir(parents=True)
    skill_agent_path.write_text(skill_agent, encoding="utf-8")
    return {
        "agents": agents,
        "lots": lots,
        "task": task_progress,
        "handoff": handoff,
        "skill": skill,
        "skill_agent": skill_agent,
    }


class InstallUpgradeWorkflowTests(unittest.TestCase):
    def test_default_mode_is_a_read_only_preview(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "preview"
            target.mkdir()
            result = run_installer(target, None)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("dry run: no files written", result.stdout)
            self.assertEqual([], list(target.iterdir()))

    def test_fresh_install_targets_sr_370_contracts(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "fresh"
            target.mkdir()
            result = run_installer(target, "--write")
            self.assertEqual(result.returncode, 0, result.stderr)
            version = json.loads((target / "docs/codex/SR_PACK_VERSION.json").read_text())
            self.assertEqual(version["version"], "3.7.0")
            contract = (target / "docs/codex/tasks/_TEMPLATE/sr_contract.json").read_text()
            self.assertIn('"implementation_status"', contract)
            self.assertIn('"evidence_status"', contract)
            self.assertTrue((target / "docs/codex/prompts/00_install_codex_environment.md").exists())
            self.assertTrue((target / "docs/codex/CHANGELOG.md").exists())
            self.assertTrue((target / "scripts/codex/validate_release_docs.py").exists())
            post_check = subprocess.run(
                [sys.executable, "scripts/codex/sr_post_install_check.py", "--root", ".", "--json"],
                cwd=target,
                text=True,
                capture_output=True,
                timeout=120,
            )
            self.assertEqual(post_check.returncode, 0, post_check.stdout + post_check.stderr)

    def test_fresh_write_refuses_existing_sr_installation(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "existing"
            marker = target / "docs/codex/SR_METHOD.md"
            marker.parent.mkdir(parents=True)
            marker.write_text("project-owned legacy method\n", encoding="utf-8")
            result = run_installer(target, "--write")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("existing SR installation detected", result.stderr)
            self.assertEqual(marker.read_text(encoding="utf-8"), "project-owned legacy method\n")

    def test_heterogeneous_targets_upgrade_independently_and_preserve_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            targets = []
            for name, old_version in (("legacy", "3.2.1"), ("recent", "3.6.0")):
                target = Path(tmp) / name
                codex = target / "docs/codex"
                codex.mkdir(parents=True)
                (codex / "SR_PACK_VERSION.json").write_text(
                    json.dumps({"version": old_version}), encoding="utf-8"
                )
                lot_text = f"schema_version: legacy-{name}\nlots: []\n"
                (codex / "SR_LOTS.yaml").write_text(lot_text, encoding="utf-8")
                open_contract = codex / "tasks/2026-01-01_open/sr_contract.json"
                open_contract.parent.mkdir(parents=True)
                open_text = json.dumps({"open_requirement_ids": [f"REQ-{name.upper()}-OPEN"]})
                open_contract.write_text(open_text, encoding="utf-8")
                targets.append((target, lot_text, open_contract, open_text))

            for target, expected_lots, open_contract, open_text in targets:
                result = run_installer(target, "--upgrade")
                self.assertEqual(result.returncode, 0, result.stderr)
                version = json.loads((target / "docs/codex/SR_PACK_VERSION.json").read_text())
                self.assertEqual(version["version"], "3.7.0")
                self.assertEqual(
                    (target / "docs/codex/SR_LOTS.yaml").read_text(encoding="utf-8"),
                    expected_lots,
                )
                self.assertEqual(open_contract.read_text(encoding="utf-8"), open_text)

    def test_official_legacy_layouts_upgrade_additively_with_green_postcheck(self):
        layouts = json.loads(LEGACY_LAYOUTS.read_text(encoding="utf-8"))
        for layout in layouts:
            with self.subTest(layout=layout["name"]), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp) / layout["name"]
                target.mkdir()
                before = materialize_legacy_layout(target, layout)

                result = run_installer(target, "--upgrade")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("USER_LOCAL_RULE", (target / "AGENTS.md").read_text(encoding="utf-8"))
                self.assertIn("Fact Gate", (target / "AGENTS.md").read_text(encoding="utf-8"))
                self.assertIn("Lot Completion Gate", (target / "AGENTS.md").read_text(encoding="utf-8"))
                self.assertIn("## [3.7.0]", (target / "docs/codex/CHANGELOG.md").read_text(encoding="utf-8"))
                self.assertEqual((target / "docs/codex/SR_LOTS.yaml").read_text(encoding="utf-8"), before["lots"])
                self.assertEqual(
                    (target / "docs/codex/tasks/2026-01-01_user-legacy/progress.md").read_text(encoding="utf-8"),
                    before["task"],
                )
                self.assertEqual((target / ".handoffs/legacy.md").read_text(encoding="utf-8"), before["handoff"])
                self.assertEqual(
                    (target / "docs/codex/project-skills/custom-legacy-skill/SKILL.md").read_text(encoding="utf-8"),
                    before["skill"],
                )
                self.assertEqual(
                    (target / "docs/codex/project-skills/custom-legacy-skill/agents/openai.yaml").read_text(encoding="utf-8"),
                    before["skill_agent"],
                )
                passes = (target / "docs/codex/SR_PASSES.yaml").read_text(encoding="utf-8")
                self.assertIn("passes: []", passes)
                self.assertNotIn("- pass_id:", passes)

                pass_check = subprocess.run(
                    [
                        sys.executable,
                        "scripts/codex/validate_pass_contract.py",
                        "--file",
                        "docs/codex/SR_PASSES.yaml",
                        "--lots-file",
                        "docs/codex/SR_LOTS.yaml",
                    ],
                    cwd=target,
                    text=True,
                    capture_output=True,
                    timeout=120,
                )
                self.assertEqual(pass_check.returncode, 0, pass_check.stdout + pass_check.stderr)
                post_check = subprocess.run(
                    [
                        sys.executable,
                        "scripts/codex/sr_post_install_check.py",
                        "--root",
                        ".",
                        "--json",
                        "--no-report",
                    ],
                    cwd=target,
                    text=True,
                    capture_output=True,
                    timeout=120,
                )
                self.assertEqual(post_check.returncode, 0, post_check.stdout + post_check.stderr)

    def test_empty_pass_registry_is_valid_before_product_passes_are_defined(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            passes = target / "SR_PASSES.yaml"
            lots = target / "SR_LOTS.yaml"
            passes.write_text('version: "0.2"\nproject: Legacy\npasses: []\n', encoding="utf-8")
            lots.write_text(legacy_lots_yaml({"sr_lots_version": "0.1", "lot_id": "EXAMPLE-01", "has_project_key": False}), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/codex/validate_pass_contract.py"),
                    "--file",
                    str(passes),
                    "--lots-file",
                    str(lots),
                ],
                text=True,
                capture_output=True,
                timeout=120,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_reader_paths_are_explicit_in_every_distributed_language(self):
        for language in LANGUAGES:
            fresh = (ROOT / f"prompts/{language}/00_install_codex_environment.md").read_text()
            upgrade = (ROOT / f"prompts/{language}/05_upgrade_codex_environment.md").read_text()
            installation = (ROOT / f"INSTALLATION.{language}.md").read_text() if language != "en" else (ROOT / "INSTALLATION.md").read_text()
            readme = (ROOT / f"README.{language}.md").read_text() if language != "en" else (ROOT / "README.md").read_text()
            for marker in ("3.7.0", "3.1.0", "implementation_status", "evidence_status", "--write"):
                self.assertIn(marker, fresh, f"{language} fresh prompt missing {marker}")
                self.assertIn(marker, installation, f"{language} installation guide missing {marker}")
            self.assertIn("passes: []", fresh, f"{language} fresh prompt must keep the pass registry empty")
            self.assertIn("passes: []", installation, f"{language} installation guide must explain the empty pass registry")
            for marker in ("repository", "2.2.0", "3.7.0", "3.1.0", "implementation_status", "evidence_status", "validated_requests", "passes: []", "sr_post_install_check.py"):
                self.assertIn(marker, upgrade, f"{language} upgrade prompt missing {marker}")
            self.assertIn("3.7.0", readme, f"{language} README missing 3.7.0")
            self.assertIn("2.2.0", readme, f"{language} README missing legacy upgrade coverage")


if __name__ == "__main__":
    unittest.main()
