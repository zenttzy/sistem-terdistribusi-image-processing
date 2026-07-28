#!/usr/bin/env bash
set -euo pipefail

sudo dnf install -y python3 python3-pip redis
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
sudo systemctl enable --now redis

echo "Instalasi selesai. Aktifkan environment dengan: source .venv/bin/activate"

