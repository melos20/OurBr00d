from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from tts_benchmark.models.db_models import EvaluationRecord, GenerationRun


@dataclass(frozen=True)
class EvaluationWithRun:
    evaluation: EvaluationRecord
    generation_run: GenerationRun


def create_generation_run(
    db: Session,
    *,
    input_text: str,
    model_key: str,
    voice_key: str | None,
    speed: float,
    settings: dict,
    requested_settings: dict,
    applied_settings: dict,
) -> GenerationRun:
    run = GenerationRun(
        id=str(uuid4()),
        created_at=datetime.now(timezone.utc),
        input_text=input_text,
        model_key=model_key,
        voice_key=voice_key,
        speed=speed,
        settings_json=json.dumps(settings),
        requested_settings_json=json.dumps(requested_settings),
        applied_settings_json=json.dumps(applied_settings),
        status="pending",
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def mark_run_succeeded(
    db: Session,
    *,
    run: GenerationRun,
    audio_path: str,
    latency_ms: int,
    audio_duration_ms: int | None = None,
    requested_settings: dict,
    applied_settings: dict,
    normalized_voice_key: str | None,
) -> GenerationRun:
    run.audio_path = audio_path
    run.latency_ms = latency_ms
    run.audio_duration_ms = audio_duration_ms
    run.requested_settings_json = json.dumps(requested_settings)
    payload = dict(applied_settings)
    payload["normalized_voice_key"] = normalized_voice_key
    run.applied_settings_json = json.dumps(payload)
    run.settings_json = json.dumps(requested_settings)
    run.status = "succeeded"
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def mark_run_failed(db: Session, *, run: GenerationRun, error_message: str) -> GenerationRun:
    run.status = "failed"
    run.error_message = error_message
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def create_evaluation(
    db: Session,
    *,
    run_id: str,
    latency_rating: int,
    naturalness_rating: int,
    tone_quality_rating: int,
    stability_rating: int,
    reviewer_note: str | None,
) -> EvaluationRecord:
    evaluation = EvaluationRecord(
        id=str(uuid4()),
        generation_run_id=run_id,
        created_at=datetime.now(timezone.utc),
        latency_rating=latency_rating,
        naturalness_rating=naturalness_rating,
        tone_quality_rating=tone_quality_rating,
        stability_rating=stability_rating,
        reviewer_note=reviewer_note,
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return evaluation


def get_run(db: Session, run_id: str) -> GenerationRun | None:
    return db.get(GenerationRun, run_id)


def get_evaluation(db: Session, evaluation_id: str) -> EvaluationRecord | None:
    return db.get(EvaluationRecord, evaluation_id)


def get_evaluation_with_run(db: Session, evaluation_id: str) -> EvaluationWithRun | None:
    evaluation = get_evaluation(db, evaluation_id)
    if evaluation is None:
        return None
    run = get_run(db, evaluation.generation_run_id)
    if run is None:
        return None
    return EvaluationWithRun(evaluation=evaluation, generation_run=run)
