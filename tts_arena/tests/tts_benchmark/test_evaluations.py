from __future__ import annotations

from fastapi.testclient import TestClient


def _create_run(client: TestClient) -> str:
    response = client.post(
        "/v1/synthesize",
        json={
            "text": "Evaluation source text",
            "model_key": "kokoro-82m",
            "speed": 1.0,
            "settings": {},
        },
    )
    assert response.status_code == 200
    return response.json()["run_id"]


def test_create_evaluation_contract(client: TestClient) -> None:
    run_id = _create_run(client)

    response = client.post(
        "/v1/evaluations",
        json={
            "run_id": run_id,
            "latency_rating": 5,
            "naturalness_rating": 4,
            "tone_quality_rating": 4,
            "stability_rating": 3,
            "reviewer_note": "good",
        },
    )
    assert response.status_code == 201

    body = response.json()
    assert set(body.keys()) == {
        "evaluation_id",
        "run_id",
        "created_at",
        "latency_rating",
        "naturalness_rating",
        "tone_quality_rating",
        "stability_rating",
        "reviewer_note",
    }


def test_create_evaluation_out_of_range_validation(client: TestClient) -> None:
    run_id = _create_run(client)

    response = client.post(
        "/v1/evaluations",
        json={
            "run_id": run_id,
            "latency_rating": 0,
            "naturalness_rating": 4,
            "tone_quality_rating": 4,
            "stability_rating": 3,
        },
    )
    assert response.status_code == 422


def test_create_evaluation_unknown_run(client: TestClient) -> None:
    response = client.post(
        "/v1/evaluations",
        json={
            "run_id": "missing-run",
            "latency_rating": 3,
            "naturalness_rating": 3,
            "tone_quality_rating": 3,
            "stability_rating": 3,
        },
    )
    assert response.status_code == 404


def test_get_evaluation_with_run_contract(client: TestClient) -> None:
    run_id = _create_run(client)
    create = client.post(
        "/v1/evaluations",
        json={
            "run_id": run_id,
            "latency_rating": 3,
            "naturalness_rating": 4,
            "tone_quality_rating": 4,
            "stability_rating": 5,
        },
    )
    assert create.status_code == 201
    evaluation_id = create.json()["evaluation_id"]

    response = client.get(f"/v1/evaluations/{evaluation_id}")
    assert response.status_code == 200
    body = response.json()
    assert "evaluation" in body
    assert "generation_run" in body
    assert body["generation_run"]["run_id"] == run_id
