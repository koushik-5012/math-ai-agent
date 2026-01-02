from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    correct: bool
    comment: Optional[str] = None   # ✅ Python 3.9 compatible

@router.post("/feedback")
def save_feedback(payload: FeedbackRequest):
    print("Feedback received:", payload.dict())
    return {"status": "ok"}
