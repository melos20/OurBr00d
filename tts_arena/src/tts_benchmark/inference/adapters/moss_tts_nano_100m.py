from __future__ import annotations

import time
from typing import Any

# Assuming a standard library interface for the 2026 model
try:
    from moss_tts import MossTTS
except ImportError:
    MossTTS = None

MOSS_TTS_AVAILABLE = MossTTS is not None

from tts_benchmark.inference.base import BaseTTSAdapter, SynthesisResult


class MossTTSNano100MAdapter(BaseTTSAdapter):
    model_key = "moss-tts-nano-100m"
    display_name = "MOSS TTS Nano 100M"

    _voices = ["multilingual_base"]

    def __init__(self):
        self._model = None

    def _get_model(self) -> Any:
        if self._model is None and MossTTS is not None:
            self._model = MossTTS.from_pretrained("OpenMOSS/MOSS-TTS-Nano-100M")
        return self._model

    def list_voices(self) -> list[str]:
        return self._voices

    def normalize_settings(self, settings: dict[str, Any]) -> dict[str, Any]:
        return {
            "prompt_audio": settings.get("prompt_audio", None),
        }

    def synthesize(
        self,
        *,
        text: str,
        voice_key: str | None,
        speed: float,
        settings: dict[str, Any],
        output_path: str,
    ) -> SynthesisResult:
        start = time.perf_counter()
        
        model = self._get_model()
        if model is None:
            # Fallback for demonstration if library not found yet
            raise RuntimeError("moss_tts library not installed. Please install 'moss-tts'.")
            
        prompt_audio = settings.get("prompt_audio")
        
        # MOSS TTS generation
        model.generate(
            text=text,
            prompt_audio_path=prompt_audio,
            output_path=output_path
        )
        
        latency_ms = int((time.perf_counter() - start) * 1000)

        return SynthesisResult(
            audio_path=output_path,
            latency_ms=max(1, latency_ms),
            requested_settings=settings,
            applied_settings={"prompt_audio": prompt_audio},
            normalized_voice_key=voice_key or "multilingual_base",
        )
