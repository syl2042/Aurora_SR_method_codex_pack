#!/usr/bin/env python3
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_release_docs import PUBLIC_PROMPTS, RELEASE_HISTORY, audit


ROOT = Path(__file__).resolve().parents[2]
LANGUAGES = ("en", "fr", "de", "es", "pt")


def materialize_minimal_source(root: Path, *, manifest_version: str = "3.7.0") -> None:
    (root / "core").mkdir(parents=True)
    (root / "MANIFEST.json").write_text(
        json.dumps({"version": manifest_version, "files": ["CHANGELOG.md"]}),
        encoding="utf-8",
    )
    (root / "core/SR_PACK_VERSION.json").write_text(
        json.dumps(
            {
                "version": "3.7.0",
                "release_status": "unreleased",
                "released_at": None,
            }
        ),
        encoding="utf-8",
    )
    history = "\n".join(f"## [{version}] - 2026-01-01" for version in RELEASE_HISTORY)
    (root / "CHANGELOG.md").write_text(
        "# Changelog\n\n## [Unreleased]\n\nTarget version: `3.7.0`.\n\n" + history + "\n",
        encoding="utf-8",
    )
    for language in LANGUAGES:
        (root / f"README.{language}.md").write_text(
            f"SR 3.7.0. [Changelog](CHANGELOG.md). prompts/{language}/07_realign_sr_state_after_upgrade.md\n",
            encoding="utf-8",
        )
        (root / f"INSTALLATION.{language}.md").write_text(
            "SR 3.7.0 SR_LOTS.yaml SR_PASSES.yaml 09_define_sr_lots_from_scope.md "
            "08_define_sr_passes_from_lots.md build_pass_runtime_goal.py\n",
            encoding="utf-8",
        )
        for prompt, markers in PUBLIC_PROMPTS.items():
            path = root / "prompts" / language / prompt
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(" ".join(markers), encoding="utf-8")
    (root / "README.md").write_text((root / "README.en.md").read_text(encoding="utf-8"), encoding="utf-8")
    (root / "INSTALLATION.md").write_text(
        (root / "INSTALLATION.en.md").read_text(encoding="utf-8"), encoding="utf-8"
    )


class ReleaseDocumentationTests(unittest.TestCase):
    def test_current_source_pack_is_coherent(self):
        self.assertEqual([], audit(ROOT))

    def test_version_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            materialize_minimal_source(root, manifest_version="3.6.0")
            errors = audit(root)
            self.assertTrue(any("MANIFEST version" in error for error in errors), errors)

    def test_missing_localized_public_prompt_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            materialize_minimal_source(root)
            (root / "prompts/de/07_realign_sr_state_after_upgrade.md").unlink()
            errors = audit(root)
            self.assertTrue(any("prompts/de/07_realign_sr_state_after_upgrade.md" in error for error in errors), errors)

    def test_unreleased_target_requires_null_release_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            materialize_minimal_source(root)
            version_file = root / "core/SR_PACK_VERSION.json"
            payload = json.loads(version_file.read_text(encoding="utf-8"))
            payload["released_at"] = "2026-08-24"
            version_file.write_text(json.dumps(payload), encoding="utf-8")
            errors = audit(root)
            self.assertTrue(any("released_at must be null" in error for error in errors), errors)

    def test_released_target_uses_version_heading(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            materialize_minimal_source(root)
            version_file = root / "core/SR_PACK_VERSION.json"
            payload = json.loads(version_file.read_text(encoding="utf-8"))
            payload["release_status"] = "released"
            payload["released_at"] = "2026-08-24"
            version_file.write_text(json.dumps(payload), encoding="utf-8")
            changelog = root / "CHANGELOG.md"
            changelog.write_text(
                changelog.read_text(encoding="utf-8").replace(
                    "Target version: `3.7.0`.",
                    "## [3.7.0] - 2026-08-24",
                ),
                encoding="utf-8",
            )
            self.assertEqual([], audit(root))

    def test_historical_release_headings_stay_out_of_readmes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            materialize_minimal_source(root)
            readme = root / "README.fr.md"
            readme.write_text(readme.read_text(encoding="utf-8") + "\n## Version 3.6.0\n", encoding="utf-8")
            errors = audit(root)
            self.assertTrue(any("must live in CHANGELOG.md" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
