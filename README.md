# Touch Grass Birder

A bird call identifier that runs on your own machine. Hold your phone up for a
few seconds, get the species, then put the phone away and go find it.

Built for the Hacktoberfest 2026 open source AI challenge, week 1: Touch Grass.

## How it works

Everything runs locally.

- BirdNET, the open acoustic classifier from the Cornell Lab of Ornithology,
  runs through ONNX Runtime.
- Gemma 3 1B, an open weight model, runs through llama.cpp for short field
  notes.
- Gemma 4, a lightweight multimodal open model, can identify birds from a photo
  via the Gemini API when a key is configured (optional; audio never needs it).

No API key, no upload, no network for audio. A closed bird ID API needs a round
trip, and on a trail there is no round trip. Running locally also means the
location of a rare sighting never leaves the device.

## Architecture

```
browser records 6s and encodes WAV
        |
        v
FastAPI  ->  BirdNET (acoustic, ONNX, local)  ->  species and confidence
        ->  Gemma 3 1B (llama.cpp, local)      ->  field note
        ->  data/sightings.jsonl               ->  field log
```

## Requirements

- Python 3.11 to 3.13 and uv
- ffmpeg, to decode browser recordings to WAV
- Optional: the llama.cpp binary (default ~/.llama-app/llama) plus a Gemma GGUF
  for field notes

## Quick start

```bash
make setup
make run
```

Open http://127.0.0.1:8000. BirdNET downloads its model on the first
identification and caches it, so the first call is slow.

## Field notes

```bash
make models
make run
```

That downloads Gemma 3 1B (Q4_K_M, about 0.8 GB) into ./models. Without it the
app still identifies birds and just skips the note.

## Photo ID

With `GEMMA4_API_KEY` and `GEMMA4_MODEL` set, the photo tile identifies a bird
from an image:

```bash
curl -F "image=@bird.jpg" http://127.0.0.1:8000/api/vision
```

## API

| Method | Path             | Purpose                        |
| ------ | ---------------- | ------------------------------ |
| GET    | /api/health      | Model status                   |
| POST   | /api/identify    | Multipart audio to detections  |
| POST   | /api/vision      | Multipart image to a Gemma 4 field note |
| GET    | /api/sightings   | Field log                      |
| POST   | /api/sightings   | Save a sighting                |

## Configuration

Set these environment variables to override defaults: `LLAMA_BIN`, `GEMMA_MODEL`,
`MIN_CONF`, `LLAMA_THREADS`, `BIRDER_DATA_DIR`.

Photo ID (Gemma 4): set `GEMMA4_API_KEY` (or `GEMINI_API_KEY`) and `GEMMA4_MODEL`
to the Gemma 4 model id from the Gemma quickstart. Without them the app still
identifies audio and the photo tile reports "not configured".

## Security

- API keys are read from the environment only and are never committed. Add keys
  in the Render dashboard, not in `render.yaml`.
- The Gemma 4 key is sent as the `x-goog-api-key` header, never in the URL.
- Uploaded audio and images are written under `data/uploads/` with randomized
  names and deleted after every request.
- Browser-rendered model output (notes, species names) is HTML-escaped.

## Tests

```bash
make test
```

## License

MIT
