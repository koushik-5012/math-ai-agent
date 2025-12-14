import json
import faiss
import numpy as np
from pathlib import Path
from backend.app.services.embeddings import EmbeddingService


class VectorStore:
    def __init__(self, index_path="data/faiss.index", metadata_path="data/faiss_meta.json"):
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.embedder = EmbeddingService()
        self.index = None
        self.metadata = []

    def _build_text(self, q):
        return (
            f"Topic: {q['topic']}\n"
            f"Question: {q['question']}\n"
            f"Steps: {' '.join(q['steps'])}\n"
            f"Answer: {q['answer']}"
        )

    def build_from_json(self, json_path="data/questions.json"):
        with open(json_path, "r") as f:
            data = json.load(f)

        texts = []
        self.metadata = []

        for q in data["questions"]:
            text = self._build_text(q)
            texts.append(text)
            self.metadata.append(q)

        embeddings = self.embedder.embed_texts(texts)

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype("float32"))

        Path(self.index_path).parent.mkdir(parents=True, exist_ok=True)

        faiss.write_index(self.index, self.index_path)

        with open(self.metadata_path, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def load(self):
        self.index = faiss.read_index(self.index_path)
        with open(self.metadata_path, "r") as f:
            self.metadata = json.load(f)

    def search(self, query: str, top_k: int = 3):
        if self.index is None:
            self.load()

        query_vec = self.embedder.embed_texts([query]).astype("float32")
        distances, indices = self.index.search(query_vec, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results
