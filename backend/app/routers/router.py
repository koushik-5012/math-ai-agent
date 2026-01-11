from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import pytesseract
from PIL import Image
import io, os, tempfile, subprocess, speech_recognition as sr

from backend.app.services.rag import rag_answer

router = APIRouter()


@router.post("/ask")
async def ask_question(
    question: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    audio: Optional[UploadFile] = File(None),
):
    if not question and not image and not audio:
        raise HTTPException(status_code=400, detail="At least one input is required")

    extracted_text = ""

    # -------- TEXT INPUT --------
    if question:
        extracted_text = question.strip()

    # -------- IMAGE OCR --------
    elif image:
        try:
            content = await image.read()
            img = Image.open(io.BytesIO(content)).convert("L")
            extracted_text = pytesseract.image_to_string(img).strip()
        except Exception:
            raise HTTPException(400, "Unable to extract text from image")

    # -------- AUDIO SPEECH --------
    elif audio:
        raw_path = None
        pcm_path = None
        try:
            content = await audio.read()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as raw:
                raw.write(content)
                raw_path = raw.name

            pcm_path = raw_path.replace(".wav", "_pcm.wav")

            subprocess.run(
                ["ffmpeg", "-y", "-i", raw_path, "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", pcm_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            r = sr.Recognizer()
            with sr.AudioFile(pcm_path) as source:
                audio_data = r.record(source)
                extracted_text = r.recognize_google(audio_data)

        except Exception:
            raise HTTPException(400, "Unable to extract text from audio")

        finally:
            if raw_path and os.path.exists(raw_path):
                os.remove(raw_path)
            if pcm_path and os.path.exists(pcm_path):
                os.remove(pcm_path)

    if not extracted_text:
        raise HTTPException(400, "No text extracted")

    # -------- RAG PIPELINE --------
    result = rag_answer(extracted_text)
#-------------Answer output structure----------------
    return {
        "detected_text": extracted_text,
        "answer": result.get("answer"),
        "steps": result.get("steps"),
        "confidence": result.get("confidence"),
        "retrieved_context": result.get("retrieved_context"),
    }