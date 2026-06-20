from sentence_transformers import SentenceTransformer


class Embedder:

    def __init__(self):
        self.model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    def embed_text(self, text):
        return self.model.encode(text, normalize_embeddings=True)

    def embed_chunks(self, chunks):
        return self.model.encode(chunks, normalize_embeddings=True)