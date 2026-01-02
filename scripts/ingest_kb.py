import json
from pathlib import Path
import faiss
from sentence_transformers import SentenceTransformer

print("🚀 Starting KB ingestion...")

# 🔥 THIS IS MANDATORY
BASE_DIR = Path(__file__).resolve().parent.parent   # math-ai-agent/

DATA_DIR = BASE_DIR / "data"                       # source questions.json
BACKEND_DATA_DIR = BASE_DIR / "backend" / "data"   # runtime vector DB

DATA_DIR.mkdir(exist_ok=True)
BACKEND_DATA_DIR.mkdir(exist_ok=True)

QUESTIONS_FILE = DATA_DIR / "questions.json"
INDEX_FILE = BACKEND_DATA_DIR / "faiss.index"
META_FILE = BACKEND_DATA_DIR / "faiss_meta.json"

with open(QUESTIONS_FILE, "r") as f:
    data = json.load(f)

questions = data["questions"]
texts = []
metadata = []

# 🔥 embed only question text (not steps / answers)
for q in questions:
    texts.append(q["question"])
    metadata.append(q)

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts, convert_to_numpy=True).astype("float32")

faiss.normalize_L2(embeddings)

dim = embeddings.shape[1]
index = faiss.IndexFlatIP(dim)
index.add(embeddings)

faiss.write_index(index, str(INDEX_FILE))

with open(META_FILE, "w") as f:
    json.dump(metadata, f, indent=2)

print("📦 FAISS index size:", index.ntotal)
print("✅ KB INGESTED INTO backend/data/")
