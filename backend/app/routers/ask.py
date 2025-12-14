from fastapi import APIRouter
from backend.app.services.vector_store import VectorStore
from backend.app.services.guardrails import check_math_guardrails
from backend.app.services.llm import LLMService
from backend.app.models.request import AskRequest
from backend.app.models.response import AskResponse

router = APIRouter()

vector_store = VectorStore()
llm = LLMService()

def build_context(results):
    context_blocks = []
    for r in results:
        block = f"""
Topic: {r['topic']}
Question: {r['question']}
Steps: {' '.join(r['steps'])}
Answer: {r['answer']}
"""
        context_blocks.append(block)

    return "\n---\n".join(context_blocks)

@router.post("/ask", response_model=AskResponse)
def ask_question(req: AskRequest):
    # 1. Guardrails
    if not check_math_guardrails(req.question):
        return AskResponse(
            answer="I can only answer math-related questions.",
            sources=[]
        )

    # 2. Vector search
    results = vector_store.search(req.question, top_k=3)
    if not results:
        return AskResponse(
            answer="I couldn't find a relevant math problem.",
            sources=[]
        )

    # 3. Build RAG context
    context = build_context(results)

    # 4. LLM reasoning
    answer = llm.generate_answer(req.question, context)

    return AskResponse(
        answer=answer,
        sources=[r["id"] for r in results]
    )
