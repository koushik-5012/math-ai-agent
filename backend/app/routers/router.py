from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import pytesseract
from PIL import Image
import io
import tempfile
import subprocess
import os
import speech_recognition as sr

from backend.app.services.kb import answer_math_question
from backend.app.agents.parser import parse_problem
from backend.app.agents.router_agent import route_intent

router = APIRouter()


@router.post("/ask")
async def ask_question(
    question: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    audio: Optional[UploadFile] = File(None),
):
    if not question and not image and not audio:
        raise HTTPException(400, "At least one input is required")

    extracted_text = ""

    # -------- TEXT --------
    if question:
        extracted_text = question.strip()

    # -------- IMAGE --------
    elif image:
        content = await image.read()
        img = Image.open(io.BytesIO(content)).convert("L")
        extracted_text = pytesseract.image_to_string(img).strip()
        if not extracted_text:
            raise HTTPException(400, "No text detected in image")

    # -------- AUDIO --------
    elif audio:
        raw_path = None
        pcm_path = None

        try:
            content = await audio.read()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as raw:
                raw.write(content)
                raw_path = raw.name

            pcm_path = raw_path.replace(".wav", "_pcm.wav")

            # Convert ANY audio to PCM WAV
            subprocess.run([
                "ffmpeg", "-y", "-i", raw_path,
                "-acodec", "pcm_s16le",
                "-ac", "1",
                "-ar", "16000",
                pcm_path
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            recognizer = sr.Recognizer()
            with sr.AudioFile(pcm_path) as source:
                audio_data = recognizer.record(source)
                extracted_text = recognizer.recognize_google(audio_data)

        except sr.UnknownValueError:
            raise HTTPException(400, "Could not understand audio")
        except Exception as e:
            raise HTTPException(500, f"Audio processing failed: {str(e)}")
        finally:
            if raw_path and os.path.exists(raw_path):
                os.remove(raw_path)
            if pcm_path and os.path.exists(pcm_path):
                os.remove(pcm_path)

    if not extracted_text:
        raise HTTPException(400, "No text extracted")

    parsed = parse_problem(extracted_text)
    intent = route_intent(parsed)
    result = answer_math_question(extracted_text)

    return {
        "detected_text": extracted_text,
        "answer": result.get("answer"),
        "steps": result.get("steps"),
        "confidence": result.get("confidence"),
        "agent_trace": result.get("trace"),
        "retrieved_context": result.get("context"),
        "parsed": parsed,
        "intent": intent,
        "verification": result.get("verification"),
    }
