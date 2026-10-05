#!/usr/bin/env bash
set -euo pipefail

REPO="${GEMMA_REPO:-ggml-org/gemma-3-1b-it-GGUF}"
FILE="${GEMMA_FILE:-gemma-3-1b-it-Q4_K_M.gguf}"
DEST_DIR="$(cd "$(dirname "$0")/.." && pwd)/models"
mkdir -p "$DEST_DIR"

if [ -f "$DEST_DIR/$FILE" ]; then
  echo "Already present: $DEST_DIR/$FILE"
  exit 0
fi

URL="https://huggingface.co/${REPO}/resolve/main/${FILE}?download=true"
echo "Downloading ${REPO}/${FILE} to ${DEST_DIR}"
curl -L --fail --progress-bar "$URL" -o "$DEST_DIR/$FILE"
echo "Done: $DEST_DIR/$FILE"
