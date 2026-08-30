#!/bin/bash
# KAVACH-AI Sovereign Industrial Workbench Launcher
cd "$(dirname "$0")"

echo "================================================================="
echo "  KAVACH-AI: Sovereign Air-Gapped Industrial & PSU Workbench     "
echo "  Foundation Model: Gemma 3 (4B Parameter Low-RAM Class)         "
echo "  Air-Gap Security: Strict Local Loopback (127.0.0.1) Only       "
echo "================================================================="

source .venv/bin/activate
export PYTHONUNBUFFERED=1

echo "Starting Sovereign Gateway at http://127.0.0.1:8000 ..."
.venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000


