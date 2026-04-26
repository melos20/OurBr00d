from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RuntimeConfig:
    host: str = "127.0.0.1"
    api_port: int = 8000
    ui_port: int = 7860
    min_speed: float = 0.5
    max_speed: float = 2.0
    max_text_length: int = 2000
    data_dir: Path = Path("tts_arena/data")
    output_dir: Path = Path("tts_arena/outputs")

    @property
    def db_path(self) -> Path:
        return self.data_dir / "tts_benchmark.sqlite3"
