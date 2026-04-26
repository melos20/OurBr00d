from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tts_benchmark.core.database import Base


class GenerationRun(Base):
    __tablename__ = "generation_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    input_text: Mapped[str] = mapped_column(Text, nullable=False)
    model_key: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    voice_key: Mapped[str | None] = mapped_column(String(128), nullable=True)
    speed: Mapped[float] = mapped_column(Float, nullable=False)
    settings_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    requested_settings_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    applied_settings_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    audio_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    audio_duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="pending")
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    evaluations: Mapped[list[EvaluationRecord]] = relationship(
        "EvaluationRecord", back_populates="generation_run"
    )


class EvaluationRecord(Base):
    __tablename__ = "evaluation_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    generation_run_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("generation_runs.id"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    latency_rating: Mapped[int] = mapped_column(Integer, nullable=False)
    naturalness_rating: Mapped[int] = mapped_column(Integer, nullable=False)
    tone_quality_rating: Mapped[int] = mapped_column(Integer, nullable=False)
    stability_rating: Mapped[int] = mapped_column(Integer, nullable=False)
    reviewer_note: Mapped[str | None] = mapped_column(Text, nullable=True)

    generation_run: Mapped[GenerationRun] = relationship(
        "GenerationRun", back_populates="evaluations"
    )
