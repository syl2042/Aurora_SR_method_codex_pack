#!/usr/bin/env python3
"""Create a first-pass Aurora Design audit draft from scan_ui_inventory.py JSON.

The score is heuristic. It is meant to start the audit, not replace human/Codex
judgment after inspecting representative pages.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

AREAS = [
    ("Shell and navigation", 15),
    ("Page headers and hierarchy", 10),
    ("Cards, metrics, and KPIs", 10),
    ("Tables, lists, filters", 12),
    ("Badges and status language", 8),
    ("Analytics/dashboard quality", 10),
    ("Advanced UX", 8),
    ("AI/data patterns", 10),
    ("Theme/token discipline", 10),
    ("Technical maintainability", 7),
]


def bounded(value: float) -> int:
    return int(max(0, min(10, round(value))))


def score(inventory: dict[str, Any]) -> dict[str, Any]:
    counts = inventory.get("counts", {})
    imports = inventory.get("imports", {})
    hints = inventory.get("custom_component_hints", {})
    aurora_mentions = inventory.get("aurora_component_mentions", {})
    deps = (inventory.get("package", {}) or {}).get("dependencies", {}) or {}

    components_ui = counts.get("components_ui_files", 0)
    shared_ui = counts.get("shared_ui_files", 0)
    manifests = counts.get("ui_manifest_files", 0)
    hardcoded = counts.get("hardcoded_color_files", 0)
    tremor_files = counts.get("direct_tremor_import_files", 0)
    kibo_files = counts.get("direct_kibo_import_files", 0)
    shadcn_files = counts.get("shadcn_import_files", 0)

    has_sidebar = any("sidebar" in p.lower() for p in inventory.get("paths", {}).get("components_ui", [])) or any("AuroraAppShell" in k for k in aurora_mentions)
    has_theme = counts.get("theme_files", 0) > 0 or "next-themes" in deps
    has_tremor = "@tremor/react" in deps or tremor_files > 0
    has_table = "@tanstack/react-table" in deps or hints.get("data_table")
    has_command = "cmdk" in deps or any("command" in p.lower() for p in inventory.get("paths", {}).get("components_ui", []))
    has_ai = bool(imports.get("aurora")) or any(term in " ".join(inventory.get("paths", {}).get("app_pages", [])).lower() for term in ["agent", "trace", "source", "rag", "assistant"])

    area_scores = {}
    notes = {}

    area_scores["Shell and navigation"] = bounded(4 + (3 if has_sidebar else 0) + (2 if shared_ui else 0) + (1 if manifests else 0))
    notes["Shell and navigation"] = "Sidebar/shell signals detected" if has_sidebar else "No clear shared shell/sidebar signal detected"

    ph_count = len(hints.get("page_header", []))
    area_scores["Page headers and hierarchy"] = bounded(3 + min(4, ph_count) + (2 if any("AuroraPageHeader" in k for k in aurora_mentions) else 0) - (1 if ph_count > 8 else 0))
    notes["Page headers and hierarchy"] = f"{ph_count} page header hints detected"

    metric_count = len(hints.get("metric_card", []))
    area_scores["Cards, metrics, and KPIs"] = bounded(3 + min(4, metric_count) + (2 if any("AuroraMetric" in k or "AuroraKpi" in k for k in aurora_mentions) else 0))
    notes["Cards, metrics, and KPIs"] = f"{metric_count} metric/KPI hints detected"

    table_count = len(hints.get("data_table", []))
    area_scores["Tables, lists, filters"] = bounded(3 + (3 if has_table else 0) + min(3, table_count) + (1 if any("AuroraDataTable" in k for k in aurora_mentions) else 0))
    notes["Tables, lists, filters"] = f"{table_count} table/list hints detected"

    badge_count = len(hints.get("status_badge", []))
    area_scores["Badges and status language"] = bounded(4 + min(3, badge_count) + (2 if any("AuroraStatusBadge" in k for k in aurora_mentions) else 0) - (1 if badge_count > 12 else 0))
    notes["Badges and status language"] = f"{badge_count} badge/status hints detected"

    area_scores["Analytics/dashboard quality"] = bounded(4 + (3 if has_tremor else 0) + (1 if "recharts" in deps else 0) + (1 if "echarts" in deps else 0) - (1 if tremor_files > 6 else 0))
    notes["Analytics/dashboard quality"] = f"Tremor direct import files: {tremor_files}"

    area_scores["Advanced UX"] = bounded(3 + (2 if has_command else 0) + (2 if "@dnd-kit/core" in deps else 0) + (2 if kibo_files else 0))
    notes["Advanced UX"] = f"Command/Kibo signals: command={has_command}, kibo_files={kibo_files}"

    area_scores["AI/data patterns"] = bounded(3 + (2 if has_ai else 0) + (2 if any("Agent" in k for k in aurora_mentions) else 0) + (2 if any("Source" in k for k in aurora_mentions) else 0))
    notes["AI/data patterns"] = "AI/data route or Aurora pattern signals detected" if has_ai else "Few AI/data pattern signals detected"

    area_scores["Theme/token discipline"] = bounded(5 + (3 if has_theme else 0) + (1 if manifests else 0) - min(5, hardcoded // 5))
    notes["Theme/token discipline"] = f"Theme files: {counts.get('theme_files', 0)}, hardcoded color files: {hardcoded}"

    area_scores["Technical maintainability"] = bounded(3 + (2 if shared_ui else 0) + (2 if manifests else 0) + (1 if components_ui > 10 else 0) - (1 if shadcn_files > 50 else 0))
    notes["Technical maintainability"] = f"shared_ui={shared_ui}, manifests={manifests}, components_ui={components_ui}"

    weighted = 0.0
    total_weight = sum(weight for _, weight in AREAS)
    for area, weight in AREAS:
        weighted += area_scores[area] * weight
    global_score = round((weighted / (10 * total_weight)) * 100)

    if global_score >= 85:
        level = "premium"
    elif global_score >= 70:
        level = "good"
    elif global_score >= 55:
        level = "acceptable"
    else:
        level = "weak"

    return {"global_score": global_score, "level": level, "area_scores": area_scores, "notes": notes}


def markdown(inventory: dict[str, Any], result: dict[str, Any]) -> str:
    counts = inventory.get("counts", {})
    package = inventory.get("package", {}) or {}
    deps = package.get("dependencies", {}) or {}
    lines = [
        "# Aurora Design Audit — Draft", "", "## 1. Executive summary", "",
        f"**Score:** {result['global_score']} / 100  ", f"**Level:** {result['level']}  ",
        "**Main risk:** validate this heuristic draft by inspecting representative pages before migration.  ",
        "**Recommended next step:** complete the evidence-based audit template and identify quick wins.", "",
        "## 2. Scope and evidence", "", f"- Repository root: `{inventory.get('repo_root')}`",
        f"- Package file: `{package.get('path')}`", "- Script: `scan_ui_inventory.py` + `score_design_coherence.py`", "",
        "## 3. Stack and UI inventory", "", "| Area | Detected | Notes |", "|---|---|---|",
        f"| Framework signals | {', '.join(inventory.get('framework_signals', [])) or 'none'} | From package.json |",
        f"| shadcn/Radix | {'yes' if any(k.startswith('@radix-ui/') for k in deps) else 'unknown'} | {counts.get('components_ui_files', 0)} components/ui files |",
        f"| Tremor | {'yes' if '@tremor/react' in deps else 'no'} | {counts.get('direct_tremor_import_files', 0)} direct import files |",
        f"| Kibo | {'yes' if 'kibo-ui' in deps else 'no'} | {counts.get('direct_kibo_import_files', 0)} direct import files |",
        f"| Theme system | {'yes' if counts.get('theme_files', 0) else 'unknown'} | {counts.get('theme_files', 0)} theme-related files |",
        f"| Shared UI | {'yes' if counts.get('shared_ui_files', 0) else 'no'} | {counts.get('shared_ui_files', 0)} shared/ui files |", "",
        "## 4. Scorecard", "", "| Area | Score / 10 | Findings |", "|---|---:|---|",
    ]
    for area, _weight in AREAS:
        lines.append(f"| {area} | {result['area_scores'][area]} | {result['notes'][area]} |")
    lines.extend(["", "## 5. Quick wins to verify", ""])
    quick = []
    if counts.get("direct_tremor_import_files", 0): quick.append("Wrap direct Tremor imports behind `aurora-analytics` components.")
    if counts.get("hardcoded_color_files", 0): quick.append("Replace hardcoded colors with theme tokens or status/tone props.")
    if inventory.get("custom_component_hints", {}).get("page_header"): quick.append("Standardize page headers with `AuroraPageHeader`.")
    if inventory.get("custom_component_hints", {}).get("metric_card"): quick.append("Generalize metric/KPI cards into `AuroraMetricCard`.")
    if not quick: quick.append("Inspect representative pages manually and compare with Aurora component tiers.")
    for i, item in enumerate(quick, 1): lines.append(f"{i}. {item}")
    lines.extend(["", "## 6. Manual completion required", "", "This draft is generated from repository signals. Complete the full audit by inspecting key pages, screenshots, and actual UX flows before migration."])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Score Aurora Design coherence from inventory JSON")
    parser.add_argument("inventory_json", help="Path to JSON from scan_ui_inventory.py")
    parser.add_argument("--output", help="Write markdown draft to this path")
    parser.add_argument("--json", help="Write score JSON to this path")
    args = parser.parse_args()
    inventory = json.loads(Path(args.inventory_json).read_text(encoding="utf-8"))
    result = score(inventory)
    if args.json: Path(args.json).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    text = markdown(inventory, result)
    if args.output: Path(args.output).write_text(text, encoding="utf-8")
    else: print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
