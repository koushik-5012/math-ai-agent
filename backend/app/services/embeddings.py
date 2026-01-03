from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self):
        # Load model once (important for performance)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_texts(self, texts: list[str]):
        """
        Convert a list of texts into embedding vectors.
        """
        return self.model.encode(texts, convert_to_numpy=True)
