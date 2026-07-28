#!/usr/bin/env bash
set -euo pipefail

sudo apt update
sudo apt install -y python3-venv python3-pip redis-server libgl1
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
sudo systemctl enable --now redis-server

echo "Instalasi selesai. Aktifkan environment dengan: source .venv/bin/activate"

