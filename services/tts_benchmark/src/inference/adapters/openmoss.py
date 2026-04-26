from src.inference.base import TTSModelAdapter
import numpy as np

class OpenMossAdapter(TTSModelAdapter):
    def __init__(self):
        super().__init__()
        # Lazy load the pipeline - initialize on first use to avoid multiprocessing issues at startup
        self.pipe = None

    @property
    def model_id(self) -> str:
        return "openmoss"
    
    def _ensure_loaded(self):
        """Lazily load the pipeline on first use."""
        if self.pipe is None:
            from transformers import pipeline, AutoTokenizer
            # Using OuteTTS-0.2-500M as the Qwen fallback
            # Use slow tokenizer to bypass the Rust backend exception
            tokenizer = AutoTokenizer.from_pretrained("OuteAI/OuteTTS-0.2-500M", use_fast=False, trust_remote_code=True)
            self.pipe = pipeline("text-to-speech", model="OuteAI/OuteTTS-0.2-500M", tokenizer=tokenizer, trust_remote_code=True)
        
    def generate(self, text: str) -> tuple[int, np.ndarray]:
        self._ensure_loaded()
        result = self.pipe(text)
        audio = result["audio"].squeeze().astype(np.float32)
        sample_rate = result["sampling_rate"]
        return sample_rate, audio
