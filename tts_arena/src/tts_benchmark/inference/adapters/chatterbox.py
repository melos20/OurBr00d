from __future__ import annotations

import time
from typing import Any

import torch
import torchaudio
from chatterbox.tts import ChatterboxTTS

from tts_benchmark.inference.base import BaseTTSAdapter, SynthesisResult


class ChatterBoxAdapter(BaseTTSAdapter):
    model_key = "chatterbox"
    display_name = "ChatterBox"

    _voices = ["neutral", "bright", "deep", "soft"]

    def __init__(self):
        self._model = None
        self._device = "cuda" if torch.cuda.is_available() else "cpu"

    def _get_model(self) -> ChatterboxTTS:
        if self._model is None:
            # Note: This will download weights from HF if not present
            self._model = ChatterboxTTS.from_pretrained(device=self._device)
        return self._model

    def list_voices(self) -> list[str]:
        return self._voices

    def normalize_settings(self, settings: dict[str, Any]) -> dict[str, Any]:
        return {
            "exaggeration": float(settings.get("exaggeration", 0.5)),
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
        exaggeration = float(settings.get("exaggeration", 0.5))
        
        # Chatterbox generation
        # Assuming the library handles basic synthesis without a voice prompt as default
        wav = model.generate(text, exaggeration=exaggeration)
        
        # Save audio
        # model.sr is the sample rate
        torchaudio.save(output_path, wav.cpu(), model.sr)
        
        latency_ms = int((time.perf_counter() - start) * 1000)

        return SynthesisResult(
            audio_path=output_path,
            latency_ms=max(1, latency_ms),
            requested_settings=settings,
            applied_settings={"exaggeration": exaggeration},
            normalized_voice_key=voice_key or "default",
        )
