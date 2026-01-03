from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers.router import router as ask_router
from backend.app.services.multimodal import process_image, process_audio
from backend.app.routers.feedback import router as feedback_router

app = FastAPI(title="Math AI Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ask_router)
app.include_router(feedback_router)
