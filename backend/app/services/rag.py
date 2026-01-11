from app.services.vector_store import search
from app.services.mcp import call_mcp
from app.services.openai_embedder import embed_text


def rag_answer(query: str):

    q_vec = embed_text(query)

    matches = search(q_vec, k=3)

    if not matches:
        return {
            "answer": "No relevant knowledge found.",
            "steps": [],
            "confidence": 0.3,
            "retrieved_context": []
        }

    context = "\n".join([m["text"] for m in matches])

    mcp = call_mcp(query, context)

    return {
        "answer": mcp.get("final_answer"),
        "steps": mcp.get("steps", []),
        "confidence": mcp.get("confidence", 0.5),
        "retrieved_context": matches
    }