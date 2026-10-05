from __future__ import annotations

import threading
from pathlib import Path
from typing import Any

import pandas as pd

from .config import DEFAULT_MIN_CONF

_lock = threading.Lock()
_model: Any | None = None
_model_label = "acoustic/2.4/litert"


def is_loaded() -> bool:
    return _model is not None


def load_model() -> Any:
    global _model
    if _model is None:
        with _lock:
            if _model is None:
                import birdnet

                _model = birdnet.load("acoustic", "2.4", "tf", library="litert")
    return _model


def _to_records(predictions: Any) -> list[dict[str, Any]]:
    if predictions is None:
        return []
    if isinstance(predictions, pd.DataFrame):
        return predictions.to_dict("records")
    if isinstance(predictions, dict):
        keys = list(predictions.keys())
        if not keys:
            return []
        length = len(predictions[keys[0]])
        return [{k: predictions[k][i] for k in keys} for i in range(length)]
    return [dict(row) for row in predictions]


def _split_species(name: str) -> tuple[str, str]:
    if not name:
        return "", ""
    sci, _, common = name.partition("_")
    return sci.strip(), (common or sci).strip()


def identify(audio_path: str | Path, min_conf: float = DEFAULT_MIN_CONF, top_k: int = 5) -> dict[str, Any]:
    model = load_model()
    result = model.predict(
        str(audio_path),
        top_k=top_k,
        n_producers=1,
        n_workers=1,
        batch_size=1,
        half_precision=True,
        default_confidence_threshold=min_conf,
    )

    try:
        records = result.to_dataframe().to_dict("records")
    except Exception:
        records = _to_records(result)

    detections: list[dict[str, Any]] = []
    for row in records:
        try:
            conf = float(row.get("confidence"))
        except (TypeError, ValueError):
            continue
        if conf < min_conf:
            continue
        sci, common = _split_species(str(row.get("species_name") or row.get("species") or ""))
        detections.append(
            {
                "scientific_name": sci,
                "common_name": common,
                "confidence": round(conf, 4),
                "start": str(row.get("start_time", "")),
                "end": str(row.get("end_time", "")),
            }
        )

    detections.sort(key=lambda d: d["confidence"], reverse=True)
    return {"model": _model_label, "count": len(detections), "detections": detections[:top_k]}
