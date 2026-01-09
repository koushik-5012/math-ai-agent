import json
import faiss
import numpy as np
from pathlib import Path
from backend.app.services.embeddings import EmbeddingService

class VectorStore:
    def __init__(self):
        self.index_path = "data/faiss.index"
        self.meta_path = "data/faiss_meta.json"
        self.embedder = EmbeddingService()
        self.index = None
        self.metadata = []
        self.load()

    def load(self):
        if not Path(self.index_path).exists():
            print("⚠️ No vector index found. Running without KB retrieval.")
            self.index = None
            self.metadata = []
            return

        self.index = faiss.read_index(self.index_path)

        if Path(self.meta_path).exists():
            with open(self.meta_path) as f:
                self.metadata = json.load(f)
        else:
            self.metadata = []

        print(f"✅ Vector index loaded with {len(self.metadata)} records")

    def search(self, query: str, k: int = 3):
        try:
            if self.index is None or not self.metadata:
                return []

            q_emb = self.embedder.embed_texts([query]).astype("float32")
            faiss.normalize_L2(q_emb)

            scores, indices = self.index.search(q_emb, k)

            results = []
            for idx, score in zip(indices[0], scores[0]):
                if idx < 0 or idx >= len(self.metadata):
                    continue
                item = self.metadata[idx].copy()
                item["score"] = float(score)
                results.append(item)

            return results

        except Exception as e:
            print("❌ Vector search error:", e)
            return []