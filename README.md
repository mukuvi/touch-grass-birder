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

No API key, no upload, no network. A closed bird ID API needs a round trip, and
on a trail there is no round trip. Running locally also means the location of a
rare sighting never leaves the device.

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

## API

| Method | Path             | Purpose                        |
| ------ | ---------------- | ------------------------------ |
| GET    | /api/health      | Model status                   |
| POST   | /api/identify    | Multipart audio to detections  |
| GET    | /api/sightings   | Field log                      |
| POST   | /api/sightings   | Save a sighting                |

## Configuration

Set these environment variables to override defaults: `LLAMA_BIN`, `GEMMA_MODEL`,
`MIN_CONF`, `LLAMA_THREADS`, `BIRDER_DATA_DIR`.

## Tests

```bash
make test
```

## License

MIT
