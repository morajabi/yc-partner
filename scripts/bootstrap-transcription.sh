#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$ROOT_DIR/.source/venv"
PIP_CACHE_DIR="$ROOT_DIR/.source/pip-cache"

mkdir -p "$ROOT_DIR/.source" "$PIP_CACHE_DIR"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  python3 -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install --upgrade pip
PIP_CACHE_DIR="$PIP_CACHE_DIR" "$VENV_DIR/bin/python" -m pip install -r "$ROOT_DIR/scripts/requirements-transcription.txt"

echo "Installed transcription tools into $VENV_DIR"
echo "Run: $VENV_DIR/bin/python scripts/transcribe_youtube.py <youtube-url>"
