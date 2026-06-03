#!/usr/bin/env bash
set -euo pipefail
if command -v rtk >/dev/null 2>&1; then
  echo "RTK detected: $(command -v rtk)"
  rtk --version || true
else
  echo "RTK not detected. Optional: rtk init -g --codex if installed."
fi
