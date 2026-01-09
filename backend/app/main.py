from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from backend.app.routers.router import router

app = FastAPI(title="Math Professor AI")

app.include_router(router)

app.mount("/ui", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
      <body style="font-family:Arial;padding:40px">
        <h2>Math Professor AI is running 🚀</h2>
        <p>Open UI at <a href="/ui">/ui</a></p>
      </body>
    </html>
    """