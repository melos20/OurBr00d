from __future__ import annotations

from pathlib import Path

from tts_benchmark.core.config import RuntimeConfig


def ensure_runtime_directories(config: RuntimeConfig) -> None:
    """Create runtime directories required for DB and audio artifacts."""
    for path in (config.data_dir, config.output_dir, config.output_dir / "runs"):
        Path(path).mkdir(parents=True, exist_ok=True)
