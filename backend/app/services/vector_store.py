import os
import json
import faiss
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

INDEX_PATH = os.path.join(DATA_DIR, "kb.index")
META_PATH = os.path.join(DATA_DIR, "kb_meta.json")

DIM = 1536  # text-embedding-3-small dimension


def init_collection():
    if not os.path.exists(INDEX_PATH):
        index = faiss.IndexFlatL2(DIM)
        faiss.write_index(index, INDEX_PATH)
        with open(META_PATH, "w") as f:
            json.dump([], f)


def upsert(vectors, docs):
    index = faiss.read_index(INDEX_PATH)

    vecs = np.array(vectors).astype("float32")
    index.add(vecs)
    faiss.write_index(index, INDEX_PATH)

    if os.path.exists(META_PATH):
        with open(META_PATH) as f:
            meta = json.load(f)
    else:
        meta = []

    for d in docs:
        meta.append(d)

    with open(META_PATH, "w") as f:
        json.dump(meta, f)


def search(query_vector, k=3):
    if not os.path.exists(INDEX_PATH):
        return []

    index = faiss.read_index(INDEX_PATH)

    q = np.array([query_vector]).astype("float32")
    scores, ids = index.search(q, k)

    with open(META_PATH) as f:
        meta = json.load(f)

    results = []
    for idx in ids[0]:
        if idx < len(meta):
            results.append(meta[idx])

    return results