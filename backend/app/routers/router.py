from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from backend.app.services.kb import answer_math_question
from backend.app.services.multimodal import process_image, process_audio

router = APIRouter()

@router.post("/ask")
async def ask_question(
    mode: str = Form("text"),
    question: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
):
    if mode == "text":
        if not question:
            raise HTTPException(400, "Question is required")
        return answer_math_question(question)

    elif mode == "image":
        if not file:
            raise HTTPException(400, "Image file required")
        extracted = await process_image(file)
        return answer_math_question(extracted["text"])

    elif mode == "audio":
        if not file:
            raise HTTPException(400, "Audio file required")
        extracted = await process_audio(file)
        return answer_math_question(extracted["text"])

    else:
        raise HTTPException(400, "Invalid mode")
