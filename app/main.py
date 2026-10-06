from __future__ import annotations

import shutil
import subprocess
import uuid
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from httpx import HTTPError

from . import config, fieldnotes, identify, sightings, vision

app = FastAPI(title="Touch Grass Birder", version="0.1.0")

STATIC_DIR = Path(__file__).resolve().parent / "static"


def _transcode_to_wav(src: Path) -> Path:
    dst = src.with_suffix(".wav")
    if src.suffix.lower() == ".wav":
        return src
    if not shutil.which("ffmpeg"):
        raise HTTPException(status_code=500, detail="ffmpeg is required to decode non-WAV audio")
    cmd = ["ffmpeg", "-y", "-i", str(src), "-ac", "1", "-ar", "48000", str(dst)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0 or not dst.exists():
        raise HTTPException(status_code=400, detail="Could not decode the audio file")
    return dst


@app.get("/api/health")
def health() -> dict:
    return {
        "ok": True,
        "birdnet_loaded": identify.is_loaded(),
        "gemma_available": fieldnotes.gemma_available(),
        "gemma_model": fieldnotes.model_name(),
        "gemma4_available": vision.available(),
        "gemma4_model": vision.model_name(),
        "offline": True,
    }


@app.post("/api/identify")
def api_identify(
    audio: UploadFile = File(...),
    min_conf: float = Form(config.DEFAULT_MIN_CONF),
    note: bool = Form(True),
) -> dict:
    suffix = Path(audio.filename or "clip.webm").suffix or ".webm"
    upload_path = config.UPLOAD_DIR / f"{uuid.uuid4().hex}{suffix}"
    with upload_path.open("wb") as fh:
        shutil.copyfileobj(audio.file, fh)

    try:
        wav_path = _transcode_to_wav(upload_path)
        result = identify.identify(wav_path, min_conf=min_conf)
    finally:
        for path in {upload_path, upload_path.with_suffix(".wav")}:
            try:
                path.unlink()
            except OSError:
                pass

    top = result["detections"][0] if result["detections"] else None
    if note and top:
        top["field_note"] = fieldnotes.field_note(
            top["common_name"], top["scientific_name"], top["confidence"]
        )

    return result


@app.post("/api/vision")
def api_vision(image: UploadFile = File(...)) -> dict:
    suffix = Path(image.filename or "photo.jpg").suffix or ".jpg"
    upload_path = config.UPLOAD_DIR / f"{uuid.uuid4().hex}{suffix}"
    with upload_path.open("wb") as fh:
        shutil.copyfileobj(image.file, fh)

    try:
        return vision.identify_image(upload_path)
    except HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Gemma 4 request failed: {exc}")
    finally:
        try:
            upload_path.unlink()
        except OSError:
            pass


@app.get("/api/sightings")
def api_sightings() -> dict:
    return {"sightings": sightings.list_all()}


@app.post("/api/sightings")
def api_add_sighting(
    common_name: str = Form(...),
    scientific_name: str = Form(""),
    confidence: float = Form(0.0),
    note: str = Form(""),
) -> dict:
    return sightings.add(common_name, scientific_name, confidence, note or None)


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")


def run() -> None:
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    run()
