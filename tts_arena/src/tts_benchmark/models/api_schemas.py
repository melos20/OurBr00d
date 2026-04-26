from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class ModelInfo(BaseModel):
    model_key: str
    display_name: str
    voices: list[str]


class ListModelsResponse(BaseModel):
    models: list[ModelInfo]


class SynthesizeRequest(BaseModel):
    text: str = Field(min_length=1)
    model_key: str
    voice_key: str | None = None
    speed: float = Field(ge=0.5, le=2.0)
    settings: dict[str, Any] = Field(default_factory=dict)

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("text must not be blank")
        return trimmed


class SynthesizeMetadata(BaseModel):
    requested_settings: dict[str, Any]
    applied_settings: dict[str, Any]
    normalized_voice_key: str | None = None


class SynthesizeResponse(BaseModel):
    run_id: str
    audio_path: str
    audio_base64: str | None = None
    latency_ms: int
    metadata: SynthesizeMetadata


class EvaluationCreateRequest(BaseModel):
    run_id: str
    latency_rating: int = Field(ge=1, le=5)
    naturalness_rating: int = Field(ge=1, le=5)
    tone_quality_rating: int = Field(ge=1, le=5)
    stability_rating: int = Field(ge=1, le=5)
    reviewer_note: str | None = None


class EvaluationRecordResponse(BaseModel):
    evaluation_id: str
    run_id: str
    created_at: datetime
    latency_rating: int
    naturalness_rating: int
    tone_quality_rating: int
    stability_rating: int
    reviewer_note: str | None = None


class GenerationRunView(BaseModel):
    run_id: str
    input_text: str
    model_key: str
    voice_key: str | None = None
    speed: float
    settings: dict[str, Any]
    metadata: dict[str, Any]
    latency_ms: int
    audio_path: str
    created_at: datetime


class EvaluationWithRunResponse(BaseModel):
    evaluation: EvaluationRecordResponse
    generation_run: GenerationRunView


class ErrorResponse(BaseModel):
    error: str
    detail: str
