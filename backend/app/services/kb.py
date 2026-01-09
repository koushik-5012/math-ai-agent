from backend.app.services.vector_store import VectorStore
from backend.app.services.mcp import call_mcp
from backend.app.services.guardrails import check_math_guardrails
from backend.app.agents.verifier import verify_answer

store = VectorStore()

def answer_math_question(raw_text: str):

    trace = []
    context = []

    if not check_math_guardrails(raw_text):
        return {
            "detected_text": raw_text,
            "answer": "Only math related questions are allowed.",
            "steps": [],
            "confidence": 0.0,
            "trace": ["guardrails_block"],
            "context": [],
            "verification": {"is_correct": False, "confidence": 0.0}
        }

    trace.append("guardrails_pass")

    results = store.search(raw_text, k=3)

    if results:
        trace.append("vector_retrieval")
        top = results[0]
        context = results

        answer = top.get("answer", "")
        steps = top.get("steps", [])
        confidence = min(0.95, float(top.get("score", 0.75)))

    else:
        trace.append("mcp_fallback")
        mcp = call_mcp(raw_text)

        answer = mcp.get("final_answer", "")
        steps = mcp.get("steps", [])
        confidence = float(mcp.get("confidence", 0.6))

    trace.append("verifier_agent")
    verification = verify_answer(answer)

    if verification.get("is_correct"):
        confidence = min(1.0, confidence + 0.05)
    else:
        confidence = max(0.2, confidence - 0.1)

    return {
        "detected_text": raw_text,
        "answer": answer,
        "steps": steps,
        "confidence": round(confidence, 2),
        "trace": trace,
        "context": context,
        "verification": verification
    }