import chromadb


class VectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(path="./chroma_db")

        self.collection = self.client.get_or_create_collection(
            name="msa_contract"
        )

    def reset(self):
        try:
            self.client.delete_collection("msa_contract")
        except:
            pass

        self.collection = self.client.get_or_create_collection(
            name="msa_contract"
        )

    def add_chunks(self, chunks, embeddings, metadatas):

        self.collection.add(
            documents=chunks,
            embeddings=embeddings.tolist(),
            ids=[f"chunk_{i}" for i in range(len(chunks))],
            metadatas=metadatas
        )

    def search(self, query_embedding, k=5):

        return self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=k,
            include=["documents", "distances", "metadatas"]
        )