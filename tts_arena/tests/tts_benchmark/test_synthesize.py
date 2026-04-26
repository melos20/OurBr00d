from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient


SYNTH_PAYLOAD = {
    "text": "Hello benchmark world",
    "model_key": "kokoro-82m",
    "voice_key": "af_bella",
    "speed": 1.0,
    "settings": {"gain": 0.2},
}


def test_synthesize_success_returns_metadata(client: TestClient) -> None:
    response = client.post("/v1/synthesize", json=SYNTH_PAYLOAD)
    assert response.status_code == 200

    body = response.json()
    assert "run_id" in body
    assert body["latency_ms"] >= 1
    assert Path(body["audio_path"]).exists()

    metadata = body["metadata"]
    assert "requested_settings" in metadata
    assert "applied_settings" in metadata
    assert metadata["normalized_voice_key"] == "af_bella"


def test_synthesize_validation_errors(client: TestClient) -> None:
    invalid = dict(SYNTH_PAYLOAD)
    invalid["speed"] = 3.0
    response = client.post("/v1/synthesize", json=invalid)
    assert response.status_code == 422

    malformed = {
        "text": "hello",
        "model_key": "kokoro-82m",
        "speed": 1.0,
        "settings": "not-an-object",
    }
    response = client.post("/v1/synthesize", json=malformed)
    assert response.status_code == 422
