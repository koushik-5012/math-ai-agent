from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import pytesseract
from PIL import Image
import io
import os
import tempfile
import subprocess
import speech_recognition as sr

from app.services.rag import rag_answer
from app.services.guardrails import check_math_guardrails


router = APIRouter()


@router.post("/ask")
async def ask_question(
    question: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    audio: Optional[UploadFile] = File(None),
):
    """
    Unified multimodal endpoint

    Flow:
    Text / Image / Audio
        ↓
    Extract text
        ↓
    Guardrails (math only)
        ↓
    RAG + LLM
        ↓
    Response
    """

    extracted_text = ""

    # --------------------------------------------------
    # CLEAN EMPTY MULTIPART BUGS (very important)
    # --------------------------------------------------
    if question is not None and question.strip() == "":
        question = None

    if image and image.filename == "":
        image = None

    if audio and audio.filename == "":
        audio = None

    if not question and not image and not audio:
        raise HTTPException(
            status_code=400,
            detail="At least one input is required"
        )

    # ==================================================
    # TEXT INPUT
    # ==================================================
    if question:
        extracted_text = question.strip()

    # ==================================================
    # IMAGE OCR
    # ==================================================
    elif image:
        try:
            content = await image.read()
            if not content:
                raise ValueError("Empty image file")

            img = Image.open(io.BytesIO(content)).convert("L")
            extracted_text = pytesseract.image_to_string(img).strip()

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Image OCR failed: {str(e)}"
            )

    # ==================================================
    # AUDIO SPEECH → TEXT
    # ==================================================
    elif audio:
        raw_path = None
        pcm_path = None

        try:
            content = await audio.read()
            if not content:
                raise ValueError("Empty audio file")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as raw:
                raw.write(content)
                raw_path = raw.name

            pcm_path = raw_path.replace(".wav", "_pcm.wav")

            subprocess.run(
                [
                    "ffmpeg", "-y",
                    "-i", raw_path,
                    "-acodec", "pcm_s16le",
                    "-ac", "1",
                    "-ar", "16000",
                    pcm_path
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            r = sr.Recognizer()
            with sr.AudioFile(pcm_path) as source:
                audio_data = r.record(source)
                extracted_text = r.recognize_google(audio_data)

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Audio processing failed: {str(e)}"
            )

        finally:
            if raw_path and os.path.exists(raw_path):
                os.remove(raw_path)
            if pcm_path and os.path.exists(pcm_path):
                os.remove(pcm_path)

    # ==================================================
    # VALIDATION
    # ==================================================
    if not extracted_text:
        raise HTTPException(
            status_code=400,
            detail="No text extracted"
        )

    # ==================================================
    # 🚨 GUARDRAILS (STRICT MATH FILTER)
    # ==================================================
    if not check_math_guardrails(extracted_text):
        raise HTTPException(
            status_code=400,
            detail="Only math-related questions are supported."
        )

    # ==================================================
    # RAG PIPELINE
    # ==================================================
    try:
        result = rag_answer(extracted_text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"RAG failure: {str(e)}"
        )

    # ==================================================
    # RESPONSE
    # ==================================================
    return {
        "detected_text": extracted_text,
        "answer": result.get("answer", ""),
        "steps": result.get("steps", []),
        "confidence": result.get("confidence", 0.0),
        "agent_trace": result.get("agent_trace", []),
        "retrieved_context": result.get("retrieved_context", [])
    }