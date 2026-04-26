from __future__ import annotations

import time
import wave
from pathlib import Path
from typing import Any

try:
    from piper.download_voices import download_voice
    from piper.voice import PiperVoice
except ImportError:
    download_voice = None
    PiperVoice = None

from tts_benchmark.inference.base import BaseTTSAdapter, SynthesisResult

PIPER_TTS_AVAILABLE = PiperVoice is not None and download_voice is not None


class PiperTTSAdapter(BaseTTSAdapter):
    model_key = "piper-tts"
    display_name = "Piper TTS"

    _voices = [
        "en_US-lessac-medium",
        "en_GB-alan-medium",
        "en_US-kathleen-low",
        "de_DE-thorsten-medium",
    ]
    _default_voice = "en_US-lessac-medium"
    _voices_dir = Path("tts_arena/models/piper")

    def __init__(self) -> None:
        self._loaded_voices: dict[str, Any] = {}

    def list_voices(self) -> list[str]:
        return self._voices

    def normalize_settings(self, settings: dict[str, Any]) -> dict[str, Any]:
        return {
            "noise_scale": float(settings.get("noise_scale", 0.667)),
            "length_scale": float(settings.get("length_scale", 1.0)),
            "noise_w": float(settings.get("noise_w", 0.8)),
        }

    def _voice_paths(self, voice_key: str) -> tuple[Path, Path]:
        return (
            self._voices_dir / f"{voice_key}.onnx",
            self._voices_dir / f"{voice_key}.onnx.json",
        )

    def _get_voice(self, voice_key: str) -> Any:
        if PiperVoice is None or download_voice is None:
            raise RuntimeError("piper-tts is not installed.")

        if voice_key not in self._voices:
            raise RuntimeError(f"Unsupported Piper voice: {voice_key}")

        cached = self._loaded_voices.get(voice_key)
        if cached is not None:
            return cached

        self._voices_dir.mkdir(parents=True, exist_ok=True)
        model_path, config_path = self._voice_paths(voice_key)
        if not model_path.exists() or not config_path.exists():
            # Downloads voice model + config from official Piper voice registry.
            download_voice(voice_key, self._voices_dir)

        voice = PiperVoice.load(model_path=model_path, config_path=config_path)
        self._loaded_voices[voice_key] = voice
        return voice

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
        selected_voice = voice_key or self._default_voice
        norm_settings = self.normalize_settings(settings)

        voice = self._get_voice(selected_voice)

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with wave.open(output_path, "wb") as wav_file:
            voice.synthesize_wav(text, wav_file)

        latency_ms = int((time.perf_counter() - start) * 1000)
        return SynthesisResult(
            audio_path=output_path,
            latency_ms=max(1, latency_ms),
            requested_settings=settings,
            applied_settings={**norm_settings, "speed": speed},
            normalized_voice_key=selected_voice,
        )
