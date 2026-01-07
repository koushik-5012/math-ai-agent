from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.app.routers.router import router as ask_router
from backend.app.routers.feedback import router as feedback_router

app = FastAPI()

app.include_router(ask_router)
app.include_router(feedback_router)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
