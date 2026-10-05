from __future__ import annotations

import os
import subprocess

from . import config

SYSTEM = (
    "You are a terse field guide for a birder standing outdoors. "
    "Given a species, reply with 2-3 short sentences: what it sounds like, "
    "where and when you would hear it, and one memorable field mark. "
    "No preamble, no markdown, no lists."
)


def gemma_available() -> bool:
    model = config.gemma_model_path()
    return bool(model) and os.path.exists(config.LLAMA_BIN)


def model_name() -> str | None:
    path = config.gemma_model_path()
    return os.path.basename(path) if path else None


def field_note(common_name: str, scientific_name: str = "", confidence: float | None = None) -> str | None:
    model = config.gemma_model_path()
    if not model or not os.path.exists(config.LLAMA_BIN):
        return None

    conf_line = f" (confidence {confidence:.0%})" if confidence is not None else ""
    prompt = f"Species: {common_name} ({scientific_name}){conf_line}."

    cmd = [
        config.LLAMA_BIN,
        "cli",
        "-m",
        model,
        "-sys",
        SYSTEM,
        "-p",
        prompt,
        "-n",
        "160",
        "-c",
        str(config.GEMMA_CTX),
        "-t",
        str(config.LLAMA_THREADS),
        "--no-display-prompt",
        "-st",
        "--simple-io",
        "--temp",
        "0.6",
    ]

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=config.GEMMA_TIMEOUT,
            check=False,
        )
    except (subprocess.TimeoutExpired, OSError):
        return None

    text = (proc.stdout or "").strip()
    if not text:
        return None
    if prompt in text:
        text = text.split(prompt, 1)[-1].strip()
    return text
