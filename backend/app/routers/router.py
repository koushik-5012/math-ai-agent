from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import pytesseract
from PIL import Image
import io, os, tempfile, subprocess, speech_recognition as sr

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
        raise HTTPException(status_code=400, detail="At least one input is required")

    extracted_text = ""

    # ---------- TEXT ----------
    if question:
        extracted_text = question.strip()

    # ---------- IMAGE ----------
    elif image:
        try:
            content = await image.read()
            img = Image.open(io.BytesIO(content)).convert("L")
            extracted_text = pytesseract.image_to_string(img).strip()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid image file")

    # ---------- AUDIO ----------
    elif audio:
        raw_path = None
        pcm_path = None
        try:
            content = await audio.read()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as raw:
                raw.write(content)
                raw_path = raw.name

            pcm_path = raw_path.replace(".wav", "_pcm.wav")

            process = subprocess.run(
                ["ffmpeg", "-y", "-i", raw_path, "-ac", "1", "-ar", "16000", pcm_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            if process.returncode != 0:
                raise HTTPException(status_code=400, detail="Unsupported audio format")

            recognizer = sr.Recognizer()
            with sr.AudioFile(pcm_path) as source:
                audio_data = recognizer.record(source)
                extracted_text = recognizer.recognize_google(audio_data)

        except sr.UnknownValueError:
            raise HTTPException(status_code=400, detail="Could not understand audio")
        except Exception:
            raise HTTPException(status_code=500, detail="Audio processing failed")
        finally:
            if raw_path and os.path.exists(raw_path):
                os.remove(raw_path)
            if pcm_path and os.path.exists(pcm_path):
                os.remove(pcm_path)

    if not extracted_text:
        raise HTTPException(status_code=400, detail="No text extracted")

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