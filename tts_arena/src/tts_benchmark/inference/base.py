from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SynthesisResult:
    audio_path: str
    latency_ms: int
    requested_settings: dict[str, Any]
    applied_settings: dict[str, Any]
    normalized_voice_key: str | None


class BaseTTSAdapter(ABC):
    model_key: str
    display_name: str

    @abstractmethod
    def list_voices(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def normalize_settings(self, settings: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def synthesize(
        self,
        *,
        text: str,
        voice_key: str | None,
        speed: float,
        settings: dict[str, Any],
        output_path: str,
    ) -> SynthesisResult:
        raise NotImplementedError
