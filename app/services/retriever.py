class Retriever:

    def __init__(
        self,
        embedder,
        vector_store,
    ):
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(
        self,
        question,
        top_k=3,
    ):

        query_embedding = self.embedder.embed(
            [question]
        )[0]

        results = self.vector_store.search(
            query_embedding,
            top_k,
        )

        retrieved = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        distances = results["distances"][0]

        for doc, meta, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            

            retrieved.append(
                {
                    "document": doc,
                    "source": meta["source"],
                    "chunk": meta["chunk"],
                    "score": round(1 - distance, 3),
                }
            )

        return retrieved