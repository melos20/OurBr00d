from __future__ import annotations

from fastapi.testclient import TestClient


def test_metadata_persistence_and_replay(client: TestClient) -> None:
    synth = client.post(
        "/v1/synthesize",
        json={
            "text": "Metadata persistence test",
            "model_key": "qwen-tts",
            "voice_key": "qwen_male",
            "speed": 1.2,
            "settings": {"gain": 0.31, "vibrato_hz": 2.0},
        },
    )
    assert synth.status_code == 200
    run_body = synth.json()

    evaluate = client.post(
        "/v1/evaluations",
        json={
            "run_id": run_body["run_id"],
            "latency_rating": 4,
            "naturalness_rating": 4,
            "tone_quality_rating": 5,
            "stability_rating": 4,
        },
    )
    assert evaluate.status_code == 201

    detail = client.get(f"/v1/evaluations/{evaluate.json()['evaluation_id']}")
    assert detail.status_code == 200
    body = detail.json()

    assert body["generation_run"]["input_text"] == "Metadata persistence test"
    assert body["generation_run"]["model_key"] == "qwen-tts"
    assert body["generation_run"]["voice_key"] == "qwen_male"
    assert body["generation_run"]["speed"] == 1.2
    assert body["generation_run"]["settings"] == {"gain": 0.31, "vibrato_hz": 2.0}

    metadata = body["generation_run"]["metadata"]
    assert "requested_settings" in metadata
    assert "applied_settings" in metadata
    assert metadata["applied_settings"]["normalized_voice_key"] == "qwen_male"
