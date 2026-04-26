from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from tts_benchmark.api.deps import get_db_session
from tts_benchmark.core.config import RuntimeConfig
from tts_benchmark.core.registry import AdapterRegistry
from tts_benchmark.models.api_schemas import (
    EvaluationCreateRequest,
    EvaluationRecordResponse,
    EvaluationWithRunResponse,
    GenerationRunView,
    ListModelsResponse,
    SynthesizeRequest,
    SynthesizeResponse,
)
from tts_benchmark.storage import repositories

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/v1/models", response_model=ListModelsResponse)
def list_models(request: Request) -> ListModelsResponse:
    registry: AdapterRegistry = request.app.state.registry
    return ListModelsResponse(models=registry.list_models())


@router.post("/v1/synthesize", response_model=SynthesizeResponse)
def synthesize(
    payload: SynthesizeRequest,
    request: Request,
    db: Session = Depends(get_db_session),
) -> SynthesizeResponse:
    config: RuntimeConfig = request.app.state.config
    registry: AdapterRegistry = request.app.state.registry

    if len(payload.text) > config.max_text_length:
        raise HTTPException(status_code=400, detail="text exceeds configured max length")
    if not (config.min_speed <= payload.speed <= config.max_speed):
        raise HTTPException(status_code=400, detail="speed out of bounds")

    registration = registry.get(payload.model_key)
    if registration is None:
        raise HTTPException(status_code=400, detail="unknown model_key")

    requested_settings = dict(payload.settings)
    applied_settings = registration.adapter.normalize_settings(requested_settings)

    run = repositories.create_generation_run(
        db,
        input_text=payload.text,
        model_key=payload.model_key,
        voice_key=payload.voice_key,
        speed=payload.speed,
        settings=requested_settings,
        requested_settings=requested_settings,
        applied_settings=applied_settings,
    )

    output_path = str(Path(config.output_dir) / "runs" / f"{run.id}.wav")

    try:
        result = registration.adapter.synthesize(
            text=payload.text,
            voice_key=payload.voice_key,
            speed=payload.speed,
            settings=requested_settings,
            output_path=output_path,
        )
    except Exception as exc:
        repositories.mark_run_failed(db, run=run, error_message=str(exc))
        raise HTTPException(status_code=503, detail=f"synthesis failed: {exc}") from exc

    repositories.mark_run_succeeded(
        db,
        run=run,
        audio_path=result.audio_path,
        latency_ms=result.latency_ms,
        requested_settings=requested_settings,
        applied_settings=result.applied_settings,
        normalized_voice_key=result.normalized_voice_key,
    )

    return SynthesizeResponse(
        run_id=run.id,
        audio_path=result.audio_path,
        audio_base64=None,
        latency_ms=result.latency_ms,
        metadata={
            "requested_settings": requested_settings,
            "applied_settings": result.applied_settings,
            "normalized_voice_key": result.normalized_voice_key,
        },
    )


@router.post("/v1/evaluations", status_code=201, response_model=EvaluationRecordResponse)
def create_evaluation(
    payload: EvaluationCreateRequest,
    db: Session = Depends(get_db_session),
) -> EvaluationRecordResponse:
    run = repositories.get_run(db, payload.run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="generation run not found")

    evaluation = repositories.create_evaluation(
        db,
        run_id=payload.run_id,
        latency_rating=payload.latency_rating,
        naturalness_rating=payload.naturalness_rating,
        tone_quality_rating=payload.tone_quality_rating,
        stability_rating=payload.stability_rating,
        reviewer_note=payload.reviewer_note,
    )

    return EvaluationRecordResponse(
        evaluation_id=evaluation.id,
        run_id=evaluation.generation_run_id,
        created_at=evaluation.created_at,
        latency_rating=evaluation.latency_rating,
        naturalness_rating=evaluation.naturalness_rating,
        tone_quality_rating=evaluation.tone_quality_rating,
        stability_rating=evaluation.stability_rating,
        reviewer_note=evaluation.reviewer_note,
    )


@router.get("/v1/evaluations/{evaluation_id}", response_model=EvaluationWithRunResponse)
def get_evaluation_with_run(
    evaluation_id: str,
    db: Session = Depends(get_db_session),
) -> EvaluationWithRunResponse:
    record = repositories.get_evaluation_with_run(db, evaluation_id)
    if record is None:
        raise HTTPException(status_code=404, detail="evaluation not found")

    run_settings = json.loads(record.generation_run.settings_json)
    requested = json.loads(record.generation_run.requested_settings_json)
    applied = json.loads(record.generation_run.applied_settings_json)

    return EvaluationWithRunResponse(
        evaluation={
            "evaluation_id": record.evaluation.id,
            "run_id": record.evaluation.generation_run_id,
            "created_at": record.evaluation.created_at,
            "latency_rating": record.evaluation.latency_rating,
            "naturalness_rating": record.evaluation.naturalness_rating,
            "tone_quality_rating": record.evaluation.tone_quality_rating,
            "stability_rating": record.evaluation.stability_rating,
            "reviewer_note": record.evaluation.reviewer_note,
        },
        generation_run=GenerationRunView(
            run_id=record.generation_run.id,
            input_text=record.generation_run.input_text,
            model_key=record.generation_run.model_key,
            voice_key=record.generation_run.voice_key,
            speed=record.generation_run.speed,
            settings=run_settings,
            metadata={
                "requested_settings": requested,
                "applied_settings": applied,
            },
            latency_ms=record.generation_run.latency_ms or 0,
            audio_path=record.generation_run.audio_path or "",
            created_at=record.generation_run.created_at,
        ),
    )
