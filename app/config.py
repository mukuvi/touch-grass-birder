from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = Path(os.environ.get("BIRDER_DATA_DIR", BASE_DIR / "data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

SIGHTINGS_FILE = DATA_DIR / "sightings.jsonl"
UPLOAD_DIR = DATA_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

LLAMA_BIN = os.environ.get("LLAMA_BIN", str(Path.home() / ".llama-app" / "llama"))

GEMMA_CTX = int(os.environ.get("GEMMA_CTX", "2048"))
GEMMA_TIMEOUT = int(os.environ.get("GEMMA_TIMEOUT", "180"))
LLAMA_THREADS = int(os.environ.get("LLAMA_THREADS", str(os.cpu_count() or 4)))

DEFAULT_MIN_CONF = float(os.environ.get("MIN_CONF", "0.25"))

GEMMA4_API_KEY = os.environ.get("GEMMA4_API_KEY") or os.environ.get("GEMINI_API_KEY") or None
GEMMA4_MODEL = os.environ.get("GEMMA4_MODEL", "")
GEMMA4_TIMEOUT = int(os.environ.get("GEMMA4_TIMEOUT", "120"))

BIRDNET_LAT = os.environ.get("BIRDNET_LAT")
BIRDNET_LON = os.environ.get("BIRDNET_LON")


def gemma_model_path() -> str | None:
    explicit = os.environ.get("GEMMA_MODEL")
    if explicit:
        return explicit if Path(explicit).exists() else None
    models_dir = BASE_DIR / "models"
    if models_dir.is_dir():
        for candidate in sorted(models_dir.glob("*.gguf")):
            return str(candidate)
    return None
