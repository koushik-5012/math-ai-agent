from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import pytesseract
from PIL import Image
import io, os, tempfile, subprocess, speech_recognition as sr

from app.services.rag import rag_answer

router = APIRouter()


@router.post("/ask")
async def ask_question(
    question: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    audio: Optional[UploadFile] = File(None),
):
    extracted_text = ""

    # ---------- CLEAN EMPTY MULTIPART ----------
    if question is not None and question.strip() == "":
        question = None
    if image and image.filename == "":
        image = None
    if audio and audio.filename == "":
        audio = None

    if not question and not image and not audio:
        raise HTTPException(status_code=400, detail="At least one input is required")

    # ---------- TEXT ----------
    if question:
        extracted_text = question.strip()

    # ---------- IMAGE ----------
    elif image:
        try:
            content = await image.read()
            if not content:
                raise ValueError("Empty image file")

            img = Image.open(io.BytesIO(content)).convert("L")
            extracted_text = pytesseract.image_to_string(img).strip()

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Image OCR failed: {str(e)}")

    # ---------- AUDIO ----------
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
                ["ffmpeg", "-y", "-i", raw_path, "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", pcm_path],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            r = sr.Recognizer()
            with sr.AudioFile(pcm_path) as source:
                audio_data = r.record(source)
                extracted_text = r.recognize_google(audio_data)

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Audio processing failed: {str(e)}")

        finally:
            if raw_path and os.path.exists(raw_path):
                os.remove(raw_path)
            if pcm_path and os.path.exists(pcm_path):
                os.remove(pcm_path)

    if not extracted_text:
        raise HTTPException(status_code=400, detail="No text extracted")

    try:
        result = rag_answer(extracted_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG failure: {str(e)}")

    return {
        "detected_text": extracted_text,
        "answer": result.get("answer", ""),
        "steps": result.get("steps", []),
        "confidence": result.get("confidence", 0.0),
        "retrieved_context": result.get("retrieved_context", []),
    }