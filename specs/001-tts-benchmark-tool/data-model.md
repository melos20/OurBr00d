# Data Model

This document outlines the core entities and state transitions for the TTS Benchmark Tool.

## Core Entities

### Evaluation
The user's subjective rating of a specific audio generation.

- **id** (UUID/String): Unique identifier.
- **text_input** (String): The text that was synthesized.
- **model_id** (String): The ID of the model used (e.g., `kokoro-82m`).
- **score_speed** (Integer, 1-5): Score for Response Speed.
- **score_human_like** (Integer, 1-5): Score for Human-like quality.
- **score_warmth** (Integer, 1-5): Score for Warm Tone.
- **score_no_hiccups** (Integer, 1-5): Score for Absence of hiccups.
- **audio_persisted** (Boolean): Whether the audio file was saved.
- **audio_file_path** (String, Optional): Path to the saved audio file, if `audio_persisted` is true.
- **created_at** (Timestamp): When the evaluation was recorded.

### GenerationRequest
The payload structure used specifically for API interactions and UI actions.

- **text** (String): The input text to synthesize.
- **model_id** (String): The model selected for generation.

### GenerationResponse
The resulting payload structure specifically for API interactions.

- **audio_url** (String): Expected path/URL to the synthesized audio.
- **generation_time_ms** (Integer): Processing time taken by the model.
- **model_loaded_from_cache** (Boolean): Flag indicating if model download was required or loaded locally.
- **status** (String): E.g., `success`, `error`.
