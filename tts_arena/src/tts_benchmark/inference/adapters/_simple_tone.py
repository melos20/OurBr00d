from __future__ import annotations

import math
import time
from pathlib import Path
from typing import Any

import numpy as np
import soundfile as sf

from tts_benchmark.inference.base import SynthesisResult


def synthesize_tone(
    *,
    text: str,
    voice_key: str | None,
    speed: float,
    settings: dict[str, Any],
    output_path: str,
    default_voice: str,
    voice_map: dict[str, float],
) -> SynthesisResult:
    start = time.perf_counter()
    normalized_voice = voice_key or default_voice
    frequency = voice_map.get(normalized_voice, voice_map[default_voice])
    sample_rate = 22050
    duration_s = max(0.6, min(8.0, len(text) / (16.0 * max(speed, 0.1))))
    t = np.linspace(0, duration_s, int(sample_rate * duration_s), endpoint=False)

    gain = float(settings.get("gain", 0.2))
    gain = max(0.05, min(0.5, gain))
    vibrato_hz = float(settings.get("vibrato_hz", 0.0))
    vibrato_amt = float(settings.get("vibrato_amount", 0.0))

    mod = 1.0
    if vibrato_hz > 0 and vibrato_amt > 0:
        mod += vibrato_amt * np.sin(2 * math.pi * vibrato_hz * t)

    signal = gain * np.sin(2 * math.pi * frequency * mod * t)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    sf.write(output_path, signal.astype(np.float32), sample_rate)
    latency_ms = int((time.perf_counter() - start) * 1000)

    return SynthesisResult(
        audio_path=output_path,
        latency_ms=max(1, latency_ms),
        requested_settings=settings,
        applied_settings=settings,
        normalized_voice_key=normalized_voice,
    )
