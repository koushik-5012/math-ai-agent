from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from backend.app.routers.router import router as ask_router
from backend.app.routers.feedback import router as feedback_router

app = FastAPI(title="Math Professor AI")

# API routers
app.include_router(ask_router)
app.include_router(feedback_router)

# ---- Root endpoint for HuggingFace readiness ----
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Math Professor AI</title>
        </head>
        <body style="font-family: Arial; padding: 40px;">
            <h1>Math Professor AI – Multimodal LLM Agent</h1>
            <p>Backend is running successfully on HuggingFace Spaces.</p>
            <p>Open the UI at <a href="/ui">/ui</a></p>
            <p>Use POST <code>/ask</code> to interact with the API.</p>
        </body>
    </html>
    """

# ---- Frontend mounted at /ui ----
app.mount("/ui", StaticFiles(directory="frontend", html=True), name="frontend")