#!/usr/bin/env python3
"""Reproducible document-load proxy; never presented as API billing telemetry."""
import argparse
import json
from pathlib import Path

OLD_BASE = [
    "AGENTS.template.md", "SR_BOOTSTRAP.md", "PROJECT_PROFILE.template.yaml",
    "CURRENT_STATE.template.md", "WORKFLOW_CODEX.md", "SR_METHOD.md",
    "SR_DEVELOPMENT_METHOD.md", "SR_AGENT_METHOD.md", "SKILL_MAP.template.md",
    "SKILL_DIGEST.md", "CODEBASE_MAP.md", "CODEBASE_MAP.generated.md",
]
SCENARIOS = {
    "simple": (["AGENTS.template.md"], ["AGENTS.template.md"]),
    "small_change": (OLD_BASE, ["AGENTS.template.md", "SR_BOOTSTRAP.md", "SR_ROUTES.json", "procedures/authority.md", "procedures/verification.md"]),
    "business": (OLD_BASE + ["DOMAIN_EXPERTISE_BOOTSTRAP.md"], ["AGENTS.template.md", "SR_BOOTSTRAP.md", "SR_ROUTES.json", "DOMAIN_EXPERTISE_BOOTSTRAP.md", "procedures/impact.md", "procedures/verification.md"]),
    "ui": (OLD_BASE + ["SR_HARNESS_METHOD.md", "LOT_EXECUTION_METHOD.md"], ["AGENTS.template.md", "SR_BOOTSTRAP.md", "SR_ROUTES.json", "procedures/ui.md", "procedures/verification.md"]),
    "resume": (["AGENTS.template.md", "SR_BOOTSTRAP.md", "CURRENT_STATE.template.md"], ["AGENTS.template.md", "SR_BOOTSTRAP.md", "SR_ROUTES.json", "procedures/resume.md", "procedures/memory.md"]),
    "agent": (OLD_BASE + ["AI_AGENT_RUNTIME_METHOD.md", "DOMAIN_EXPERTISE_BOOTSTRAP.md"], ["AGENTS.template.md", "SR_BOOTSTRAP.md", "SR_ROUTES.json", "SR_AGENT_METHOD.md", "AI_AGENT_RUNTIME_METHOD.md", "procedures/impact.md", "procedures/verification.md"]),
    "pass": (OLD_BASE + ["SR_HARNESS_METHOD.md", "LOT_EXECUTION_METHOD.md"], ["AGENTS.template.md", "SR_BOOTSTRAP.md", "SR_ROUTES.json", "SR_HARNESS_METHOD.md", "LOT_EXECUTION_METHOD.md", "procedures/passes.md", "procedures/execution.md", "procedures/verification.md"]),
}


def measure(before: Path, after: Path) -> dict:
    results = []
    for name, (old_docs, new_docs) in SCENARIOS.items():
        old_docs = list(dict.fromkeys(old_docs))
        new_docs = list(dict.fromkeys(new_docs))
        old_chars = sum(len((before / path).read_text()) for path in old_docs)
        new_chars = sum(len((after / path).read_text()) for path in new_docs)
        results.append({
            "scenario": name,
            "before_characters": old_chars,
            "after_characters": new_chars,
            "before_tokens_proxy": round(old_chars / 4),
            "after_tokens_proxy": round(new_chars / 4),
            "reduction_percent": round(100 * (old_chars - new_chars) / old_chars, 2),
            "before_documents": old_docs,
            "after_documents": new_docs,
        })
    return {
        "measurement": "exact characters of declared document sets; tokens are a characters/4 proxy",
        "limits": [
            "not model execution, cached-token telemetry, or billing",
            "project sources, selected skills, logs, tool schemas, and user messages are excluded",
            "scenarios model intended routing and do not prove equivalent behavior",
        ],
        "scenarios": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    print(json.dumps(measure(Path(args.baseline) / "core", Path(args.root) / "core"), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
