class TextChunker:

    def chunk_text(self, paragraphs):

        chunks = []
        metadatas = []

        for item in paragraphs:

            chunks.append(item["text"])

            metadatas.append({
                "page": item["page"],
                "para": item["para"]
            })

        return chunks, metadatas