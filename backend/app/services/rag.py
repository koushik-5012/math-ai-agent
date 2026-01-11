from app.services.vector_store import search
from app.services.mcp import call_mcp
from app.services.openai_embedder import embed_text


def rag_answer(query: str):
    """
    End-to-end RAG pipeline:
    1. Embed query
    2. Search vector DB
    3. Inject context into MCP
    4. Return answer + trace
    """

    # -------- EMBED QUERY --------
    q_vec = embed_text(query)

    # -------- SEARCH VECTOR DB --------
    matches = search(q_vec, k=3)

    if not matches:
        return {
            "detected_text": query,
            "answer": "No relevant knowledge found.",
            "steps": [],
            "confidence": 0.3,
            "agent_trace": [],
            "retrieved_context": []
        }

    # -------- BUILD CONTEXT --------
    context = [m["text"] for m in matches]

    # -------- CALL MCP --------
    mcp = call_mcp(query, context)

    # -------- FINAL RESPONSE --------
    return {
        "detected_text": query,
        "answer": mcp.get("final_answer"),
        "steps": mcp.get("steps", []),
        "confidence": mcp.get("confidence", 0.0),
        "agent_trace": mcp.get("agent_trace", []),
        "retrieved_context": matches
    }