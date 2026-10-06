from __future__ import annotations

import base64
from pathlib import Path
from typing import Any

import httpx

from . import config

SYSTEM = (
    "You are a terse field guide for a birder standing outdoors. "
    "Identify the bird species in the photo. Reply with 2-4 short sentences: "
    "the likely species with a confidence qualifier, the field marks you based it on, "
    "and one memorable note about its behavior or where to find it. "
    "No preamble, no markdown, no lists."
)

_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

_MIMES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
}


def available() -> bool:
    return bool(config.GEMMA4_API_KEY and config.GEMMA4_MODEL)


def model_name() -> str | None:
    return config.GEMMA4_MODEL or None


def _mime_for(image_path: Path) -> str:
    return _MIMES.get(image_path.suffix.lower(), "image/jpeg")


def _extract_text(data: dict[str, Any]) -> str:
    try:
        parts = data["candidates"][0]["content"]["parts"]
    except (KeyError, IndexError, TypeError):
        return str(data)
    return "".join(str(p.get("text", "")) for p in parts).strip()


def _species_of(text: str) -> str | None:
    if not text:
        return None
    line = text.splitlines()[0].strip().lstrip("-*").strip()
    return line or None


def identify_image(image_path: str | Path) -> dict[str, Any]:
    if not available():
        return {"configured": False, "model": None, "species": None, "note": None}

    path = Path(image_path)
    b64 = base64.b64encode(path.read_bytes()).decode()
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": SYSTEM},
                    {"inline_data": {"mime_type": _mime_for(path), "data": b64}},
                ]
            }
        ]
    }

    resp = httpx.post(
        _API_URL.format(model=config.GEMMA4_MODEL),
        headers={"x-goog-api-key": config.GEMMA4_API_KEY},
        json=payload,
        timeout=config.GEMMA4_TIMEOUT,
    )
    resp.raise_for_status()

    text = _extract_text(resp.json())
    return {
        "configured": True,
        "model": config.GEMMA4_MODEL,
        "species": _species_of(text),
        "note": text,
    }