#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="${SERVICE_NAME:-aurora-sr-cockpit}"
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
NODE_BIN="${NODE_BIN:-$(command -v node)}"
NODE_DIR="$(dirname "$NODE_BIN")"
HOST="${SR_COCKPIT_HOST:-127.0.0.1}"
PORT="${SR_COCKPIT_PORT:-18787}"
APPS_ROOT="${SR_COCKPIT_APPS_ROOT:-/home/ubuntu/apps}"
SERVICE_PATH="/etc/systemd/system/${SERVICE_NAME}.service"

if [[ -z "$NODE_BIN" || ! -x "$NODE_BIN" ]]; then
  echo "node introuvable. Definis NODE_BIN=/chemin/vers/node puis relance." >&2
  exit 1
fi

cat <<SERVICE | sudo tee "$SERVICE_PATH" >/dev/null
[Unit]
Description=Aurora SR Cockpit
After=network.target

[Service]
Type=simple
User=${USER}
WorkingDirectory=${APP_DIR}
Environment=NODE_ENV=production
Environment=SR_COCKPIT_HOST=${HOST}
Environment=SR_COCKPIT_PORT=${PORT}
Environment=SR_COCKPIT_APPS_ROOT=${APPS_ROOT}
Environment=PATH=${NODE_DIR}:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=${NODE_BIN} server/index.js
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
SERVICE

sudo systemctl daemon-reload
sudo systemctl enable --now "$SERVICE_NAME"
sudo systemctl --no-pager --full status "$SERVICE_NAME"
