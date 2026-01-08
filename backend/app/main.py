from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.app.routers.router import router as ask_router
from backend.app.routers.feedback import router as feedback_router

app = FastAPI()

# API Routers
app.include_router(ask_router)
app.include_router(feedback_router)

# Serve UI
app.mount(
    "/ui",
    StaticFiles(directory="frontend", html=True),
    name="frontend"
)

@app.get("/")
def root():
    return {
        "message": "Backend running successfully on HuggingFace Spaces",
        "ui": "/ui",
        "ask_endpoint": "/ask"
    }