# Implementation Plan: TTS Benchmark Tool

**Branch**: `001-tts-benchmark-tool` | **Date**: 2026-04-24 | **Spec**: [specs/001-tts-benchmark-tool/spec.md](specs/001-tts-benchmark-tool/spec.md)
**Input**: Feature specification from `specs/001-tts-benchmark-tool/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Create an independent, on-prem TTS benchmark tool that provides a Gradio-based UI for users to test predefined or custom texts across HuggingFace models like Kokoro, OmniVoice, OpenMoss, and Qwen. The tool features an evaluation system using a 1-5 scale and provides an API via FastAPI to integrate with the broader project architecture, storing metrics in a local SQLite database.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: FastAPI, Gradio, SQLAlchemy (or sqlite3/SQLModel), PyTorch/Transformers (for model inference)
**Storage**: SQLite for persisted evaluations file; local FileSystem (`/outputs/`) for optional audio persistence.
**Testing**: pytest
**Target Platform**: Linux/macOS local environments with viable CPU/GPU compute (VRAM for 80M-100M models).
**Project Type**: independent web-service / grad-app
**Performance Goals**: Generate audio within reasonable real-time limits locally; UI loads < 2s.
**Constraints**: Run entirely decoupled from existing `services/orchestrator` or `services/knowledge_ingest`. Must dynamically load weights based on user choice via an adapter pattern.
**Scale/Scope**: Few users (internal testing & CI/CD API calls); minimal persistent DB size.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

No violations detected. Standard practices for a Python REST/UI sub-service fit perfectly.

## Project Structure

### Documentation (this feature)

```text
specs/001-tts-benchmark-tool/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
services/tts_benchmark/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py         # FastAPI Endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── database.py       # SQLite connection/setup
│   ├── inference/
│   │   ├── __init__.py
│   │   ├── base.py           # Abstract TTSModelAdapter
│   │   └── adapters/
│   │       ├── kokoro.py
│   │       └── openmoss.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── evaluation.py     # DB Entity definition
│   └── ui/
│       ├── __init__.py
│       └── app.py            # Gradio blocks UI
├── tests/
│   ├── conftest.py
│   └── test_api.py
├── main.py                   # Uvicorn entrypoint (mounts Gradio to FastAPI)
└── requirements.txt
```

**Structure Decision**: 
A standalone package directory inside `services/` (i.e., `services/tts_benchmark/`) to keep it logically separated from `knowledge_ingest` and `orchestrator`, adhering to the FR-008 constraint (independent operation).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*(None required; simple FastAPI mounting a Gradio app with SQLite and PyTorch adapters)*
