from __future__ import annotations

from tts_benchmark.core.registry import AdapterRegistration, AdapterRegistry
from tts_benchmark.inference.adapters.kokoro_82m import Kokoro82MAdapter
from tts_benchmark.inference.base import BaseTTSAdapter
from tts_benchmark.inference.adapters.moss_tts_nano_100m import (
    MOSS_TTS_AVAILABLE,
    MossTTSNano100MAdapter,
)

try:
    from tts_benchmark.inference.adapters.chatterbox import ChatterBoxAdapter
except ImportError:
    ChatterBoxAdapter = None

try:
    from tts_benchmark.inference.adapters.qwen_tts import QwenTTSAdapter
except ImportError:
    QwenTTSAdapter = None


def build_default_registry() -> AdapterRegistry:
    registry = AdapterRegistry()
    adapters: list[BaseTTSAdapter] = [
        Kokoro82MAdapter(),
    ]
    if MOSS_TTS_AVAILABLE:
        adapters.append(MossTTSNano100MAdapter())
    if ChatterBoxAdapter is not None:
        adapters.append(ChatterBoxAdapter())
    if QwenTTSAdapter is not None:
        adapters.append(QwenTTSAdapter())

    for adapter in adapters:
        registry.register(
            AdapterRegistration(
                model_key=adapter.model_key,
                display_name=adapter.display_name,
                adapter=adapter,
                is_enabled=True,
            )
        )
    return registry
