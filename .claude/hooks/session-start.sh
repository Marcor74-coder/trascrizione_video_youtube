#!/bin/bash
set -euo pipefail

# Esegui solo in sessioni remote Claude Code
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"

echo "[session-start] Installo dipendenze..."
python -m pip install -r requirements.txt --quiet

echo "[session-start] Avvio routine YouTube..."
python routine.py

echo "[session-start] Routine completata."
