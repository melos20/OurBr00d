import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from src.core.database import Base

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    text_input = Column(String, nullable=False)
    model_id = Column(String, nullable=False)
    score_speed = Column(Integer, nullable=False)
    score_human_like = Column(Integer, nullable=False)
    score_warmth = Column(Integer, nullable=False)
    score_no_hiccups = Column(Integer, nullable=False)
    audio_persisted = Column(Boolean, default=False)
    audio_file_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)