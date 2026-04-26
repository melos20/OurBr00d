from __future__ import annotations

import time
from typing import Any

from qwen_tts.models import Qwen3TTS
from qwen_tts.utils import save_audio

from tts_benchmark.inference.base import BaseTTSAdapter, SynthesisResult


class QwenTTSAdapter(BaseTTSAdapter):
    model_key = "qwen-tts"
    display_name = "Qwen TTS"

    _voices = ["Female_01", "Male_01", "Female_02", "Male_02"]

    def __init__(self):
        self._model = None

    def _get_model(self) -> Qwen3TTS:
        if self._model is None:
            self._model = Qwen3TTS.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice")
        return self._model

    def list_voices(self) -> list[str]:
        return self._voices

    def normalize_settings(self, settings: dict[str, Any]) -> dict[str, Any]:
        return {
            "language": str(settings.get("language", "English")),
            "instruct": str(settings.get("instruct", "Speak in a natural tone.")),
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
        norm_settings = self.normalize_settings(settings)

        # Qwen3 generation
        audio_data = model.generate_custom_voice(
            text=text,
            language=norm_settings["language"],
            speaker=voice_key or "Female_01",
            instruct=norm_settings["instruct"]
        )

        save_audio(audio_data, output_path)

        latency_ms = int((time.perf_counter() - start) * 1000)

        return SynthesisResult(
            audio_path=output_path,
            latency_ms=max(1, latency_ms),
            requested_settings=settings,
            applied_settings=norm_settings,
            normalized_voice_key=voice_key or "Female_01",
        )

