#!/usr/bin/env bash
set -euo pipefail
export PYTHONUNBUFFERED=1
streamlit run apps/ask_app.py --server.runOnSave=true
