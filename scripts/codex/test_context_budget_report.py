#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).with_name("context_budget_report.py")


def write_session(
    codex_home: Path,
    *,
    cwd: Path,
    input_tokens: int,
    cached: int,
    name: str = "session.jsonl",
    primary_rate_limit: float = 7.0,
    secondary_rate_limit: float = 45.0,
) -> None:
    session_dir = codex_home / "sessions" / "2026" / "05" / "26"
    session_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    events = [
        {
            "timestamp": now,
            "type": "turn_context",
            "payload": {
                "cwd": str(cwd),
                "model_context_window": 258400,
            },
        },
        {
            "timestamp": now,
            "type": "event_msg",
            "payload": {
                "type": "token_count",
                "info": {
                    "total_token_usage": {
                        "input_tokens": 150_000_000,
                        "cached_input_tokens": 149_000_000,
                    },
                    "last_token_usage": {
                        "input_tokens": input_tokens,
                        "cached_input_tokens": cached,
                        "output_tokens": 1000,
                        "reasoning_output_tokens": 100,
                        "total_tokens": input_tokens + 1100,
                    },
                },
                "rate_limits": {
                    "primary": {"used_percent": primary_rate_limit},
                    "secondary": {"used_percent": secondary_rate_limit},
                },
            },
        },
    ]
    (session_dir / name).write_text("\n".join(json.dumps(event) for event in events), encoding="utf-8")


class ContextBudgetReportTests(unittest.TestCase):
    def run_report(self, codex_home: Path, root: Path, *extra: str) -> tuple[int, dict]:
        env = {**os.environ, "CODEX_HOME": str(codex_home)}
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root), "--json", *extra],
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        self.assertTrue(proc.stdout, proc.stderr)
        return proc.returncode, json.loads(proc.stdout)

    def test_cached_input_is_discounted_for_stop_decision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            repo = base / "repo"
            repo.mkdir()
            codex_home = base / "codex"
            write_session(codex_home, cwd=repo, input_tokens=230_000, cached=228_000)

            code, report = self.run_report(codex_home, repo)

        self.assertEqual(code, 0)
        self.assertEqual(report["status"], "green")
        self.assertGreater(report["raw_context_percent"], 80)
        self.assertLess(report["effective_context_percent"], 15)
        self.assertEqual(report["total_token_usage"]["input_tokens"], 150_000_000)
        self.assertEqual(report["rate_limits"]["primary"]["used_percent"], 7.0)
        self.assertEqual(report["hybrid_budget"]["signals"], [])

    def test_total_token_usage_is_not_used_for_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            repo = base / "repo"
            repo.mkdir()
            codex_home = base / "codex"
            write_session(codex_home, cwd=repo, input_tokens=10_000, cached=9_000)

            code, report = self.run_report(codex_home, repo)

        self.assertEqual(code, 0)
        self.assertEqual(report["status"], "green")
        self.assertLess(report["effective_context_percent"], 2)

    def test_uncached_large_session_still_flags_risk(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            repo = base / "repo"
            repo.mkdir()
            codex_home = base / "codex"
            write_session(codex_home, cwd=repo, input_tokens=230_000, cached=0)

            code, report = self.run_report(codex_home, repo)

        self.assertEqual(code, 2)
        self.assertEqual(report["status"], "orange")
        self.assertIn("effective_context_window_orange", report["hybrid_budget"]["signals"])

    def test_ambiguous_exact_cwd_sessions_remain_unreliable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            repo = base / "repo"
            repo.mkdir()
            codex_home = base / "codex"
            write_session(codex_home, cwd=repo, input_tokens=10_000, cached=9_000, name="a.jsonl")
            write_session(codex_home, cwd=repo, input_tokens=11_000, cached=9_500, name="b.jsonl")

            code, report = self.run_report(codex_home, repo)

        self.assertEqual(code, 3)
        self.assertEqual(report["status"], "ambiguous")
        self.assertFalse(report["selection_reliable"])

    def test_compact_output_is_single_line(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            repo = base / "repo"
            repo.mkdir()
            codex_home = base / "codex"
            write_session(codex_home, cwd=repo, input_tokens=10_000, cached=9_000)
            env = {**os.environ, "CODEX_HOME": str(codex_home)}
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--root", str(repo), "--compact"],
                text=True,
                capture_output=True,
                env=env,
                check=False,
            )

        self.assertEqual(proc.returncode, 0, proc.stderr)
        lines = [line for line in proc.stdout.splitlines() if line.strip()]
        self.assertEqual(len(lines), 1)
        self.assertIn("context=green", lines[0])
        self.assertIn("action=continue", lines[0])
        self.assertIn("basis=effective+uncached+cache+turns+lots", lines[0])
        self.assertIn("raw_diag=", lines[0])
        self.assertIn("signals=none", lines[0])
        self.assertNotIn(" raw=", lines[0])
        self.assertIn("rl=7.0/45.0", lines[0])
        self.assertIn("reliable=true", lines[0])


if __name__ == "__main__":
    unittest.main()
