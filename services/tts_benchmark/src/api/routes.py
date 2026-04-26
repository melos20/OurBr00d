from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy.orm import Session
import io
import scipy.io.wavfile as wavfile

from src.core.database import get_db
from src.models.evaluation import Evaluation
from src.inference import generate_audio, get_available_models

router = APIRouter(prefix="/api/v1", tags=["tts"])

class GenerationRequest(BaseModel):
    text: str
    model_id: str

class EvaluationCreate(BaseModel):
    text_input: str
    model_id: str
    score_speed: int
    score_human_like: int
    score_warmth: int
    score_no_hiccups: int
    persist_audio: bool = False

@router.post("/generate")
def create_generation(request: GenerationRequest):
    if request.model_id not in get_available_models():
        raise HTTPException(status_code=400, detail="Invalid model_id or unsupported model")
    
    try:
        sample_rate, audio_array = generate_audio(request.model_id, request.text)
        # Convert numpy array to WAV bytes
        byte_io = io.BytesIO()
        wavfile.write(byte_io, sample_rate, (audio_array * 32767).astype('int16'))
        byte_io.seek(0)
        return Response(content=byte_io.getvalue(), media_type="audio/wav")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evaluations", status_code=201)
def create_evaluation(eval_data: EvaluationCreate, db: Session = Depends(get_db)):
    audio_path = None
    if eval_data.persist_audio:
        import os
        from src.core.config import settings
        import uuid
        try:
            # Re-generate or pull from some cache? Here we assume either it was meant for future usage or we recreate merely for saving to disk.
            # Real implementation would probably upload file here or fetch from cache.
            # MOCK saving functionality.
            filename = f"{uuid.uuid4()}.wav"
            audio_path = os.path.join(settings.AUDIO_OUTPUT_DIR, filename)
            # Dummy saving
            with open(audio_path, 'wb') as f:
                f.write(b"RIFF dummy...")
        except Exception:
            pass

    eval_record = Evaluation(
        text_input=eval_data.text_input,
        model_id=eval_data.model_id,
        score_speed=eval_data.score_speed,
        score_human_like=eval_data.score_human_like,
        score_warmth=eval_data.score_warmth,
        score_no_hiccups=eval_data.score_no_hiccups,
        audio_persisted=eval_data.persist_audio,
        audio_file_path=audio_path
    )
    db.add(eval_record)
    db.commit()
    db.refresh(eval_record)
    return {"status": "success", "id": eval_record.id}

@router.get("/evaluations")
def list_evaluations(db: Session = Depends(get_db)):
    records = db.query(Evaluation).all()
    return records
