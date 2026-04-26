from __future__ import annotations

import time
from typing import Any

import soundfile as sf
from kokoro import KPipeline

from tts_benchmark.inference.base import BaseTTSAdapter, SynthesisResult


class Kokoro82MAdapter(BaseTTSAdapter):
    model_key = "kokoro-82m"
    display_name = "Kokoro 82M"

    # Common voices for Kokoro-82M
    _voices = [
        "af_heart", "af_bella", "af_nicole", "af_sky",
        "am_adam", "am_michael", "bf_emma", "bf_isabella",
        "bm_george", "bm_lewis"
    ]

    def __init__(self):
        self._pipeline = None

    def _get_pipeline(self) -> KPipeline:
        if self._pipeline is None:
            # Default to American English 'a'
            self._pipeline = KPipeline(lang_code='a')
        return self._pipeline

    def list_voices(self) -> list[str]:
        return self._voices

    def normalize_settings(self, settings: dict[str, Any]) -> dict[str, Any]:
        return {
            "speed": float(settings.get("speed", 1.0)),
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
        
        pipeline = self._get_pipeline()
        voice = voice_key or "af_heart"
        
        # Kokoro generator yields chunks
        generator = pipeline(
            text, voice=voice,
            speed=speed, split_pattern=r'\n+'
        )
        
        all_audio = []
        for _, _, audio in generator:
            all_audio.append(audio)
            
        import numpy as np
        if not all_audio:
            raise RuntimeError("Kokoro failed to generate audio")
            
        combined_audio = np.concatenate(all_audio)
        
        sf.write(output_path, combined_audio, 24000)
        
        latency_ms = int((time.perf_counter() - start) * 1000)

        return SynthesisResult(
            audio_path=output_path,
            latency_ms=max(1, latency_ms),
            requested_settings=settings,
            applied_settings={"speed": speed},
            normalized_voice_key=voice,
        )
