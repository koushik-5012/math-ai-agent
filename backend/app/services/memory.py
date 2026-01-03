import json
from pathlib import Path

MEMORY_FILE = Path("data/memory.json")

def save_memory(entry):
    MEMORY_FILE.parent.mkdir(exist_ok=True)
    data = []
    if MEMORY_FILE.exists():
        data = json.load(open(MEMORY_FILE))
    data.append(entry)
    json.dump(data, open(MEMORY_FILE, "w"), indent=2)
