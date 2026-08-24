#!/usr/bin/env python3
"""Validate that an Aurora SCREEN_REDESIGN_SPEC contains the V2 decision gates."""
from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED = [
    "## 1. Scope and current evidence",
    "## 2. Product intent",
    "## 3. Current problems",
    "## 4. Information triage",
    "## 5. Design research",
    "### 5.3 Reference Lock",
    "### 5.4 Decision Ledger",
    "## 6. Target information architecture",
    "## 7. Navigation and interaction",
    "## 8. Layout and density",
    "## 9. Component mapping",
    "## 10. Progressive disclosure",
    "## 11. States",
    "## 12. Protected behavior / non-goals",
    "## 13. Target visual",
    "## 14. Acceptance criteria",
]
TRIAGE = ["PROMOTE", "KEEP", "GROUP", "MOVE", "HIDE", "REMOVE"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec")
    args = parser.parse_args()
    path = Path(args.spec)
    text = path.read_text(encoding="utf-8")
    errors = []
    for heading in REQUIRED:
        if heading not in text:
            errors.append(f"missing heading: {heading}")
    if "TARGET PROPOSED" not in text and "TARGET REVISION REQUESTED" not in text and "TARGET APPROVED" not in text:
        errors.append("missing target validation state")
    if not all(token in text for token in TRIAGE):
        errors.append("information triage vocabulary incomplete")
    if "### 3.1 Product / UX audit" not in text or "### 3.2 Visual craft audit" not in text:
        errors.append("missing split Product/UX and Visual Craft audits")
    if "UNSUPPORTED DECISION" in text:
        errors.append("unresolved unsupported design decision")
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
