import json
import faiss
from pathlib import Path
from backend.app.services.embeddings import EmbeddingService

class VectorStore:
    def __init__(self):
        self.index_path = "data/faiss.index"
        self.meta_path = "data/faiss_meta.json"
        self.embedder = EmbeddingService()
        self.index = None
        self.metadata = []

    def load(self):
        if not Path(self.index_path).exists():
            print("⚠️ Vector index not found. Skipping vector search.")
            self.index = None
            self.metadata = []
            return

        self.index = faiss.read_index(self.index_path)

        if Path(self.meta_path).exists():
            with open(self.meta_path) as f:
                self.metadata = json.load(f)
        else:
            self.metadata = []

        print(f" Vector index loaded: {len(self.metadata)} entries")

    def search(self, query: str, k: int = 3):
        try:
            if self.index is None:
                self.load()

            if self.index is None or len(self.metadata) == 0:
                return []

            q_emb = self.embedder.embed_texts([query]).astype("float32")
            faiss.normalize_L2(q_emb)

            scores, indices = self.index.search(q_emb, k)

            results = []
            for idx, score in zip(indices[0], scores[0]):
                if idx == -1:
                    continue
                if idx >= len(self.metadata):
                    continue
                item = self.metadata[idx].copy()
                item["score"] = float(score)
                results.append(item)

            return results

        except Exception as e:
            print(" Vector search failed:", str(e))
            return []
