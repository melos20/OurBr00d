from __future__ import annotations

from dataclasses import dataclass

from tts_benchmark.inference.base import BaseTTSAdapter
from tts_benchmark.models.api_schemas import ModelInfo


@dataclass(frozen=True)
class AdapterRegistration:
    model_key: str
    display_name: str
    adapter: BaseTTSAdapter
    is_enabled: bool = True


class AdapterRegistry:
    def __init__(self) -> None:
        self._registrations: dict[str, AdapterRegistration] = {}

    def register(self, registration: AdapterRegistration) -> None:
        self._registrations[registration.model_key] = registration

    def get(self, model_key: str) -> AdapterRegistration | None:
        registration = self._registrations.get(model_key)
        if registration is None or not registration.is_enabled:
            return None
        return registration

    def list_models(self) -> list[ModelInfo]:
        return [
            ModelInfo(
                model_key=reg.model_key,
                display_name=reg.display_name,
                voices=reg.adapter.list_voices(),
            )
            for reg in self._registrations.values()
            if reg.is_enabled
        ]
