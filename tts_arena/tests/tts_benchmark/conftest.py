from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from tts_benchmark.api.app import create_app  # noqa: E402
from tts_benchmark.core.config import RuntimeConfig  # noqa: E402


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    config = RuntimeConfig(
        data_dir=tmp_path / "data",
        output_dir=tmp_path / "outputs",
    )
    app = create_app(config=config)
    return TestClient(app)
