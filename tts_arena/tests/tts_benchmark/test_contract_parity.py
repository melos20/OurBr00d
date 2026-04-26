from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient
import yaml


def test_openapi_parity(client: TestClient) -> None:
    contract_path = (
        Path(__file__).resolve().parents[3]
        / "specs"
        / "001-tts-benchmark-eval-tool"
        / "contracts"
        / "tts-benchmark.openapi.yaml"
    )
    contract = yaml.safe_load(contract_path.read_text())

    expected_paths = set(contract["paths"].keys())
    openapi = client.get("/openapi.json")
    assert openapi.status_code == 200
    implemented_paths = set(openapi.json()["paths"].keys())

    assert expected_paths.issubset(implemented_paths)
