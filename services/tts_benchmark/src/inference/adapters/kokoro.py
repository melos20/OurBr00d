from src.inference.base import TTSModelAdapter
import numpy as np
from kokoro import KPipeline

class KokoroAdapter(TTSModelAdapter):
    def __init__(self, voice: str = 'af_bella', speed: float = 0.9, lang_code: str = 'a'):
        super().__init__()
        # Load the model directly using KPipeline
        self.pipe = KPipeline(lang_code=lang_code)
        self.voice = voice
        self.speed = speed

    @property
    def model_id(self) -> str:
        return f"kokoro-82m ({self.voice} @ {self.speed}x)"
        
    def generate(self, text: str) -> tuple[int, np.ndarray]:
        # af_bella: warm, natural female voice (recommended for ElevenLabs-like quality)
        # af_heart: bright female voice
        # am_adam: warm male voice
        # bf_emma: energetic female voice
        # bm_george: deep male voice
        gen = self.pipe(text, voice=self.voice, speed=self.speed)
        
        # Collect all audio chunks in case the text is broken into multiple parts
        audio_chunks = []
        for _, _, audio in gen:
            audio_chunks.append(audio)
            
        if not audio_chunks:
            return 24000, np.zeros(0, dtype=np.float32)
            
        audio_out = np.concatenate(audio_chunks).astype(np.float32)
        sample_rate = 24000  # Kokoro uses 24kHz
        return sample_rate, audio_out
