from fastapi import FastAPI
from backend.app.routers.ask import router as ask_router

app = FastAPI(title="Math AI Agent")

app.include_router(ask_router)

@app.get("/health")
def health():
    return {"status": "ok"}
