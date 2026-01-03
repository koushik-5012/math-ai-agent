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
            "answer": "❌ Only math-related questions are allowed.",
            "steps": [],
            "confidence": 0.0,
            "trace": ["guardrails_block"],
            "context": [],
            "verification": {"is_correct": False, "confidence": 0.0}
        }

    trace.append("guardrails_pass")

    results = store.search(raw_text, k=3)

    if results and float(results[0].get("score", 0)) > 0.85:
        top = results[0]
        trace.append("vector_used")
        context = results

        answer = top["answer"]
        steps = top.get("steps", [])
        confidence = float(top["score"])

    else:
        trace.append("mcp_fallback")
        mcp = call_mcp(raw_text)
        answer = mcp["final_answer"]
        steps = mcp["steps"]
        confidence = mcp["confidence"]

    trace.append("verifier_agent")
    verification = verify_answer(answer)

    return {
        "detected_text": raw_text,
        "answer": answer,
        "steps": steps,
        "confidence": confidence,
        "trace": trace,
        "context": context,
        "verification": verification
    }