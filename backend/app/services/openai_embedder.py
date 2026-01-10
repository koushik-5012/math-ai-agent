from backend.app.services.vector_store import search
from backend.app.services.mcp import call_mcp
from backend.app.services.openai_embedder import embed_text


def rag_answer(query: str):
    """
    1. Embed user query
    2. Retrieve top-k relevant KB chunks
    3. Inject retrieved context into MCP prompt
    4. Return answer + retrieved sources
    """

    # Embed query
    q_vec = embed_text(query)

    # Retrieve KB matches
    matches = search(q_vec, k=3)

    if not matches:
        return {
            "detected_text": query,
            "answer": "No relevant knowledge found in KB.",
            "steps": [],
            "confidence": 0.3,
            "retrieved_context": []
        }

    # Build RAG context
    context = "\n".join([m["text"] for m in matches])

    # Call MCP with injected context
    mcp = call_mcp(query, context)

    return {
        "detected_text": query,
        "answer": mcp["final_answer"],
        "steps": mcp["steps"],
        "confidence": mcp["confidence"],
        "retrieved_context": matches
    }