#!/usr/bin/env python3
"""Scan an Auroramind repo for UI/design-system inventory signals.

This script is intentionally lightweight and read-only. It does not judge design
quality alone; it produces evidence for the Aurora Design audit workflow.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter
from pathlib import Path
from typing import Any

IGNORED_DIRS = {".git", ".next", ".turbo", "node_modules", "dist", "build", "coverage", ".venv", "venv", "__pycache__"}
TEXT_EXTS = {".ts", ".tsx", ".js", ".jsx", ".css", ".md", ".json", ".mjs", ".cjs"}
CODE_EXTS = {".ts", ".tsx", ".js", ".jsx"}
IMPORT_PATTERNS = {
    "tremor": re.compile(r"from\s+[\"']@tremor/react[\"']|require\([\"']@tremor/react[\"']\)"),
    "kibo": re.compile(r"from\s+[\"'](?:kibo-ui|@kibo-ui/[^\"']+)[\"']|require\([\"'](?:kibo-ui|@kibo-ui/[^\"']+)[\"']\)"),
    "shadcn_ui": re.compile(r"@/components/ui/|components/ui/"),
    "aurora": re.compile(r"Aurora[A-Z][A-Za-z0-9_]*"),
    "magic_or_motion": re.compile(r"magicui|aceternity|framer-motion|motion/react|from\s+[\"']motion[\"']"),
}
HARDCODED_COLOR_RE = re.compile(r"(?:bg|text|border|ring|stroke|fill)-(?:red|green|blue|yellow|orange|amber|emerald|rose|purple|violet|cyan|sky|slate|gray|zinc|neutral)-\d{2,3}|#[0-9a-fA-F]{3,8}")
CUSTOM_COMPONENT_HINTS = {
    "page_header": re.compile(r"function\s+\w*PageHeader|const\s+\w*PageHeader|<\w*PageHeader"),
    "metric_card": re.compile(r"function\s+\w*(Metric|Kpi|KPI)Card|const\s+\w*(Metric|Kpi|KPI)Card|<\w*(Metric|Kpi|KPI)Card"),
    "status_badge": re.compile(r"function\s+\w*Status\w*Badge|const\s+\w*Status\w*Badge|<\w*Status\w*Badge|<Badge"),
    "data_table": re.compile(r"function\s+\w*DataTable|const\s+\w*DataTable|<\w*DataTable|<Table"),
    "empty_state": re.compile(r"function\s+\w*Empty\w*State|const\s+\w*Empty\w*State|<\w*Empty\w*State"),
    "action_drawer": re.compile(r"function\s+\w*(ActionDrawer|Drawer|Sheet)|const\s+\w*(ActionDrawer|Drawer|Sheet)|<Sheet|<Drawer"),
}

def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS and not d.startswith(".")]
        path = Path(dirpath)
        for filename in filenames:
            fp = path / filename
            if fp.suffix.lower() in TEXT_EXTS: yield fp

def read_text(path: Path) -> str:
    try: return path.read_text(encoding="utf-8", errors="ignore")
    except Exception: return ""

def rel(root: Path, path: Path) -> str: return str(path.relative_to(root)).replace(os.sep, "/")

def load_package_json(root: Path) -> dict[str, Any]:
    candidates = [root / "package.json", root / "frontend" / "package.json", root / "ui" / "package.json"]
    for candidate in candidates:
        if candidate.exists():
            try:
                data = json.loads(read_text(candidate)); deps = {}; deps.update(data.get("dependencies", {})); deps.update(data.get("devDependencies", {}))
                return {"path": rel(root, candidate), "name": data.get("name"), "dependencies": deps}
            except Exception as exc: return {"path": rel(root, candidate), "error": str(exc), "dependencies": {}}
    return {"path": None, "dependencies": {}}

def detect_framework(package: dict[str, Any]) -> list[str]:
    deps = package.get("dependencies", {}) or {}; found = []
    for name in ["next", "react", "vite", "@remix-run/react", "tailwindcss", "@tremor/react", "kibo-ui", "@tanstack/react-table", "recharts", "echarts"]:
        if name in deps: found.append(f"{name}@{deps[name]}")
    return found

def scan(root: Path) -> dict[str, Any]:
    root = root.resolve(); package = load_package_json(root); files = list(iter_files(root))
    result = {"repo_root": str(root), "package": package, "framework_signals": detect_framework(package), "paths": {"shared_ui": [], "ui_manifests": [], "components_ui": [], "app_pages": [], "theme_files": [], "tailwind_configs": []}, "imports": {key: [] for key in IMPORT_PATTERNS}, "custom_component_hints": {key: [] for key in CUSTOM_COMPONENT_HINTS}, "hardcoded_color_hits": [], "aurora_component_mentions": Counter(), "counts": {}}
    for fp in files:
        r = rel(root, fp); normalized = "/" + r; lower = r.lower()
        if "/shared/ui/" in normalized or lower == "shared/ui/readme.md": result["paths"]["shared_ui"].append(r)
        if lower.endswith("ui-manifest.json"): result["paths"]["ui_manifests"].append(r)
        if "/components/ui/" in normalized: result["paths"]["components_ui"].append(r)
        if "/app/" in normalized and lower.endswith("page.tsx"): result["paths"]["app_pages"].append(r)
        if "theme" in lower and fp.suffix.lower() in CODE_EXTS.union({".css", ".json", ".mjs"}): result["paths"]["theme_files"].append(r)
        if lower.endswith(("tailwind.config.ts", "tailwind.config.js", "tailwind.config.mjs")): result["paths"]["tailwind_configs"].append(r)
        text = read_text(fp)
        if not text: continue
        for key, pattern in IMPORT_PATTERNS.items():
            if pattern.search(text): result["imports"][key].append(r)
        for key, pattern in CUSTOM_COMPONENT_HINTS.items():
            if pattern.search(text): result["custom_component_hints"][key].append(r)
        if fp.suffix.lower() in CODE_EXTS.union({".css"}):
            hits = HARDCODED_COLOR_RE.findall(text)
            if hits: result["hardcoded_color_hits"].append({"file": r, "count": len(hits), "examples": sorted(set(hits))[:12]})
        for name in re.findall(r"Aurora[A-Z][A-Za-z0-9_]*", text): result["aurora_component_mentions"][name] += 1
    result["aurora_component_mentions"] = dict(result["aurora_component_mentions"].most_common())
    result["counts"] = {"text_files_scanned": len(files), "shared_ui_files": len(result["paths"]["shared_ui"]), "ui_manifest_files": len(result["paths"]["ui_manifests"]), "components_ui_files": len(result["paths"]["components_ui"]), "app_page_files": len(result["paths"]["app_pages"]), "theme_files": len(result["paths"]["theme_files"]), "tailwind_configs": len(result["paths"]["tailwind_configs"]), "direct_tremor_import_files": len(result["imports"]["tremor"]), "direct_kibo_import_files": len(result["imports"]["kibo"]), "shadcn_import_files": len(result["imports"]["shadcn_ui"]), "hardcoded_color_files": len(result["hardcoded_color_hits"])}
    return result

def write_markdown(inventory: dict[str, Any], output: Path) -> None:
    counts = inventory["counts"]
    lines = ["# Aurora UI Inventory", "", f"Repository root: `{inventory['repo_root']}`", "", "## Framework signals", ""]
    lines.extend([f"- {item}" for item in inventory["framework_signals"]] if inventory["framework_signals"] else ["- No package framework signals detected"])
    lines.extend(["", "## Counts", "", "| Signal | Count |", "|---|---:|"])
    for key, value in counts.items(): lines.append(f"| {key} | {value} |")
    lines.extend(["", "## Important paths", ""])
    for group, paths in inventory["paths"].items():
        lines.append(f"### {group}"); lines.extend([f"- `{p}`" for p in paths[:40]] if paths else ["- none detected"]); lines.append("")
    lines.extend(["## Direct import signals", ""])
    for key, paths in inventory["imports"].items():
        lines.append(f"### {key} ({len(paths)})"); lines.extend([f"- `{p}`" for p in paths[:30]] if paths else ["- none detected"]); lines.append("")
    lines.extend(["## Custom component hints", ""])
    for key, paths in inventory["custom_component_hints"].items():
        lines.append(f"### {key} ({len(paths)})"); lines.extend([f"- `{p}`" for p in paths[:30]] if paths else ["- none detected"]); lines.append("")
    if inventory["hardcoded_color_hits"]:
        lines.extend(["## Hardcoded color hits", ""])
        for item in inventory["hardcoded_color_hits"][:50]: lines.append(f"- `{item['file']}`: {item['count']} hits")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")

def main() -> int:
    parser = argparse.ArgumentParser(description="Scan UI inventory for Aurora Design audits"); parser.add_argument("repo_root"); parser.add_argument("--output"); parser.add_argument("--markdown"); args = parser.parse_args(); root = Path(args.repo_root)
    if not root.exists(): raise SystemExit(f"repo root does not exist: {root}")
    inventory = scan(root)
    if args.output: Path(args.output).write_text(json.dumps(inventory, indent=2, ensure_ascii=False), encoding="utf-8")
    else: print(json.dumps(inventory, indent=2, ensure_ascii=False))
    if args.markdown: write_markdown(inventory, Path(args.markdown))
    return 0

if __name__ == "__main__": raise SystemExit(main())
