class Retriever:

    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(self, query_embedding, k=8):

        results = self.vector_store.search(query_embedding, k)

        docs = results["documents"][0]
        dists = results["distances"][0]
        metas = results["metadatas"][0]

        query_text = ""  # optional later if needed

        formatted = []

        for i in range(len(docs)):

            text = docs[i].lower()

            base_score = 1 - dists[i]

            # 🔥 BOOST 1: keyword matching (VERY IMPORTANT)
            keyword_boost = 0
            keywords = ["invoice", "payment", "fee", "tax", "liability", "termination", "agreement"]

            for kw in keywords:
                if kw in text:
                    keyword_boost += 0.03

            # 🔥 BOOST 2: clause density (longer legal clause = more relevant)
            length_boost = min(len(text) / 1000, 0.05)

            final_score = base_score + keyword_boost + length_boost

            formatted.append({
                "rank": i + 1,
                "chunk": docs[i],
                "similarity": round(min(final_score, 1.0), 3),
                "page": metas[i]["page"],
                "para": metas[i]["para"]
            })

        # 🔥 FINAL rerank
        formatted = sorted(
            formatted,
            key=lambda x: x["similarity"],
            reverse=True
        )

        return formatted[:5]