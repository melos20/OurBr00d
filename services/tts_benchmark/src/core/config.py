import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./tts_benchmark.db")
    AUDIO_OUTPUT_DIR: str = os.getenv("AUDIO_OUTPUT_DIR", "./outputs")
    
    # Kokoro TTS settings
    # Available voices: af_bella (warm/natural), af_heart (bright), am_adam (warm male),
    # bf_emma (energetic), bm_george (deep male), etc.
    KOKORO_VOICE: str = os.getenv("KOKORO_VOICE", "af_bella")
    KOKORO_SPEED: float = float(os.getenv("KOKORO_SPEED", "0.9"))  # 0.5-2.0, lower = warmer
    
settings = Settings()

# Ensure output dir exists
os.makedirs(settings.AUDIO_OUTPUT_DIR, exist_ok=True)