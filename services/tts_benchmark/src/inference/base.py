from typing import Protocol, runtime_checkable
import numpy as np

@runtime_checkable
class TTSModelAdapter(Protocol):
    @property
    def model_id(self) -> str:
        """The identifier of the model."""
        ...
        
    def generate(self, text: str) -> tuple[int, np.ndarray]:
        """
        Takes input text and generates audio.
        Returns:
            Tuple of (sample_rate, audio_data_as_numpy_array)
        """
        ...