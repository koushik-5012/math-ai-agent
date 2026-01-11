import os
import sys
import json
from dotenv import load_dotenv
from openai import OpenAI

# Fix python path so "backend" imports work
sys.path.append(os.path.abspath("."))

from app.services.vector_store import init_collection, upsert

# Load env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not found in .env file")

client = OpenAI(api_key=OPENAI_API_KEY)

# Load KB docs
KB_PATH = "backend/app/data/kb_docs.json"
if not os.path.exists(KB_PATH):
    raise RuntimeError("kb_docs.json not found at backend/app/data/kb_docs.json")

with open(KB_PATH) as f:
    docs = json.load(f)

texts = [d["text"] for d in docs]

print(f"Embedding {len(texts)} KB documents...")

# Create embeddings
embeds = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts
).data

vectors = [e.embedding for e in embeds]

# Initialize FAISS + store
init_collection()
upsert(vectors, docs)
# output success message
print("KB ingestion complete.")