from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import pytesseract
from PIL import Image
import io, os, tempfile, subprocess, speech_recognition as sr

from backend.app.services.mcp import call_mcp

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

    if question:
        extracted_text = question.strip()

    elif image:
        content = await image.read()
        img = Image.open(io.BytesIO(content)).convert("L")
        extracted_text = pytesseract.image_to_string(img).strip()

    elif audio:
        raw_path = None
        pcm_path = None
        try:
            content = await audio.read()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as raw:
                raw.write(content)
                raw_path = raw.name

            pcm_path = raw_path.replace(".wav", "_pcm.wav")

            subprocess.run([
                "ffmpeg","-y","-i",raw_path,"-acodec","pcm_s16le","-ac","1","-ar","16000",pcm_path
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            r = sr.Recognizer()
            with sr.AudioFile(pcm_path) as source:
                audio_data = r.record(source)
                extracted_text = r.recognize_google(audio_data)
        finally:
            if raw_path and os.path.exists(raw_path): os.remove(raw_path)
            if pcm_path and os.path.exists(pcm_path): os.remove(pcm_path)

    if not extracted_text:
        raise HTTPException(400, "No text extracted")

    result = call_mcp(extracted_text)

    return {
        "detected_text": extracted_text,
        "answer": result.get("final_answer"),
        "steps": result.get("steps"),
        "confidence": result.get("confidence")
    }