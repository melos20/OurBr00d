from __future__ import annotations

from fastapi.testclient import TestClient


def test_get_models_contract(client: TestClient) -> None:
    response = client.get("/v1/models")
    assert response.status_code == 200

    payload = response.json()
    assert "models" in payload
    assert len(payload["models"]) >= 2

    model = payload["models"][0]
    assert set(model.keys()) == {"model_key", "display_name", "voices"}
    assert isinstance(model["voices"], list)
