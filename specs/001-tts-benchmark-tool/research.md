# Phase 0: Research & Architecture

## Web Framework & API
- **Decision**: FastAPI + Gradio (mounted as a sub-app)
- **Rationale**: FastAPI provides a robust, standard REST API for integration into the main architecture. Gradio provides a very rapid, out-of-the-box UI for audio playback and form inputs (evaluations) with minimal frontend code. Gradio apps can be mounted as sub-paths on FastAPI applications.
- **Alternatives considered**: 
  - *Streamlit*: Great for UI but less standard for pure REST APIs.
  - *Pure FastAPI + React/Vue*: Overkill for a benchmark tool; higher overhead.

## TTS Model Inference & Extensibility
- **Decision**: Adapter Pattern for Models
- **Rationale**: Since the tool must support Kokoro, OmniVoice, OpenMoss, and Qwen, which might have differing initialization and inference APIs from HuggingFace, an abstract `TTSModelAdapter` base class will be used. New models can be added in the future by simply implementing this adapter. Model weights will be downloaded lazily using HuggingFace's caching mechanism.
- **Alternatives considered**:
  - *Hardcoding via `transformers` Pipeline*: Not all latest models (like Kokoro or OmniVoice) integrate perfectly into the standard `text-to-speech` pipeline immediately. An adapter pattern allows customs loading logic.

## Persistence for Evaluations
- **Decision**: SQLite via `sqlite3` (or lightweight ORM like `SQLModel`/`Peewee`)
- **Rationale**: Built into Python, zero setup, single-file DB. Perfect for an independent benchmark tool that must persist data. Audio will be optionally persisted to a local `outputs/` directory.
- **Alternatives considered**:
  - *JSON/CSV*: Functional but harder to query and manage concurrency if multiple evaluations happen (less critical here, but SQLite is safer and very easy).
  - *PostgreSQL*: Overkill for an independent benchmark tool.
