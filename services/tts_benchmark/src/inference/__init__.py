from src.inference.base import TTSModelAdapter
from src.inference.adapters.kokoro import KokoroAdapter
from src.inference.adapters.openmoss import OpenMossAdapter
from src.core.config import settings

_adapters: dict[str, TTSModelAdapter] = {}

def register_adapter(adapter: TTSModelAdapter):
    _adapters[adapter.model_id] = adapter

register_adapter(KokoroAdapter(voice=settings.KOKORO_VOICE, speed=settings.KOKORO_SPEED))
register_adapter(OpenMossAdapter())

def get_available_models() -> list[str]:
    return list(_adapters.keys())

def generate_audio(model_id: str, text: str) -> tuple[int, bytes]:
    if model_id not in _adapters:
        raise ValueError(f"Model ID '{model_id}' not found.")
    return _adapters[model_id].generate(text)
