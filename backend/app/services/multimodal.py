from fastapi import UploadFile, HTTPException
import pytesseract
from PIL import Image
import io
import speech_recognition as sr

from backend.app.agents.parser import parse_problem
from backend.app.agents.router_agent import route_intent
from backend.app.services.kb import answer_math_question


# ----------------------------------------------------
# IMAGE PROCESSING
# ----------------------------------------------------
async def process_image(file: UploadFile):
    try:
        content = await file.read()
        image = Image.open(io.BytesIO(content))
        text = pytesseract.image_to_string(image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")

    return await run_agent_pipeline(text)


# ----------------------------------------------------
# AUDIO PROCESSING
# ----------------------------------------------------
async def process_audio(file: UploadFile):
    try:
        content = await file.read()
        recognizer = sr.Recognizer()

        with sr.AudioFile(io.BytesIO(content)) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech recognition failed: {str(e)}")

    return await run_agent_pipeline(text)


# ----------------------------------------------------
# SHARED AGENT PIPELINE
# ----------------------------------------------------
async def run_agent_pipeline(text: str):
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="No text detected in input")

    parsed = parse_problem(text)
    intent = route_intent(parsed)
    result = answer_math_question(parsed["problem_text"])

    return {
        "detected_text": result.get("detected_text", text),
        "answer": result.get("answer", ""),
        "steps": result.get("steps", []),
        "confidence": result.get("confidence", 0),
        "trace": result.get("trace", []),
        "context": result.get("context", []),
        "parsed": parsed,
        "intent": intent,
        "verification": result.get("verification", {})
    }
