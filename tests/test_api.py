from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_shape():
    res = client.get("/api/health")
    assert res.status_code == 200
    body = res.json()
    assert body["ok"] is True
    assert "birdnet_loaded" in body
    assert "gemma_available" in body


def test_index_served():
    res = client.get("/")
    assert res.status_code == 200
    assert "Touch Grass Birder" in res.text


def test_sightings_roundtrip(tmp_path, monkeypatch):
    import app.sightings as sightings
    from pathlib import Path

    monkeypatch.setattr(sightings, "SIGHTINGS_FILE", Path(tmp_path) / "s.jsonl")
    sightings.add("House Finch", "Haemorhous mexicanus", 0.64, "on the fence")
    records = sightings.list_all()
    assert len(records) == 1
    assert records[0]["common_name"] == "House Finch"
