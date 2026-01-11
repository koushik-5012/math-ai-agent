from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.routers.router import router as ask_router
from app.routers.feedback import router as feedback_router

app = FastAPI(title="Math Professor AI")

# ----------- API ROUTERS -----------
app.include_router(ask_router)
app.include_router(feedback_router)

# ----------- SERVE FRONTEND -----------
app.mount("/ui", StaticFiles(directory="frontend", html=True), name="frontend")

# ----------- ROOT -----------
@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
      <head><title>Math Professor AI</title></head>
      <body style="font-family:Arial;padding:40px">
        <h1>🧮 Math Professor AI — Multimodal RAG System</h1>
        <p>Backend running successfully.</p>
        <p>Open the UI at: <a href="/ui">/ui</a></p>
        <p>API endpoint: <code>POST /ask</code></p>
      </body>
    </html>
    """