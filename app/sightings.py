from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from .config import SIGHTINGS_FILE


def add(common_name: str, scientific_name: str, confidence: float, note: str | None) -> dict:
    record = {
        "id": uuid.uuid4().hex,
        "common_name": common_name,
        "scientific_name": scientific_name,
        "confidence": confidence,
        "note": note,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    with SIGHTINGS_FILE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")
    return record


def list_all(limit: int = 50) -> list[dict]:
    if not SIGHTINGS_FILE.exists():
        return []
    records: list[dict] = []
    with SIGHTINGS_FILE.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records[-limit:][::-1]
