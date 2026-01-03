from fastapi import APIRouter, HTTPException

from backend.app.services.logger import log_event
from backend.app.services.vector_store import VectorStore
from backend.app.services.guardrails import check_math_guardrails
from backend.app.services.llm import LLMService
from backend.app.services.mcp import call_mcp

from backend.app.models.request import AskRequest
from backend.app.models.response import AskResponse

router = APIRouter()

vector_store = VectorStore()
llm = LLMService()

# ✅ Correct cosine similarity threshold for FAISS IP
SIMILARITY_THRESHOLD = 0.28


def build_context(results):
    blocks = []
    for r in results:
        blocks.append(
            f"""
Topic: {r.get('topic')}
Question: {r.get('question')}
Steps: {' '.join(r.get('steps', []))}
Answer: {r.get('answer')}
"""
        )
    return "\n---\n".join(blocks)


@router.post("/ask", response_model=AskResponse)
def ask_question(req: AskRequest):

    # 1️⃣ Hard math guardrail
    if not check_math_guardrails(req.question):
        raise HTTPException(
            status_code=400,
            detail="Only math-related questions are allowed."
        )

    # 2️⃣ Always search vector DB
    results = vector_store.search(req.question, k=3)

    # ✅ Debug print – real cosine scores
    print("🔍 VECTOR SCORES:", [r["score"] for r in results])

    # 3️⃣ RAG path when similarity is high
    if results and results[0]["score"] >= SIMILARITY_THRESHOLD:
        print("🧠 RAG HIT:", results[0]["score"])
        context = build_context(results)
        answer = llm.generate_answer(req.question, context)

        return AskResponse(
            answer=answer,
            sources=["vector_db"]
        )

    # 4️⃣ MCP fallback ONLY when KB confidence is low
    print("🌐 MCP FALLBACK:", results[0]["score"] if results else None)
    answer = call_mcp(req.question)

    return AskResponse(
        answer=answer,
        sources=["web_mcp"]
    )
