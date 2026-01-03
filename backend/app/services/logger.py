import json
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("logs")
LOG_PATH.mkdir(exist_ok=True)

LOG_FILE = LOG_PATH / "agent_logs.jsonl"


def log_event(
    question: str,
    route: str,
    similarity_scores=None,
    sources=None
):
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "route": route,  # "rag" or "mcp"
        "similarity_scores": similarity_scores,
        "sources": sources,
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")
