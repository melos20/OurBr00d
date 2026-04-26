from __future__ import annotations

from fastapi.testclient import TestClient


def test_quickstart_smoke_flow(client: TestClient) -> None:
    health = client.get("/health")
    assert health.status_code == 200

    models = client.get("/v1/models")
    assert models.status_code == 200
    model_key = models.json()["models"][0]["model_key"]

    synth = client.post(
        "/v1/synthesize",
        json={
            "text": "quickstart smoke",
            "model_key": model_key,
            "speed": 1.0,
            "settings": {},
        },
    )
    assert synth.status_code == 200

    eval_create = client.post(
        "/v1/evaluations",
        json={
            "run_id": synth.json()["run_id"],
            "latency_rating": 3,
            "naturalness_rating": 3,
            "tone_quality_rating": 3,
            "stability_rating": 3,
        },
    )
    assert eval_create.status_code == 201

    evaluation_id = eval_create.json()["evaluation_id"]
    detail = client.get(f"/v1/evaluations/{evaluation_id}")
    assert detail.status_code == 200
