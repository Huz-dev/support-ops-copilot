import os

os.environ["ANONYMIZED_TELEMETRY"] = "False"
import chromadb

from app.config import settings


class VectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PATH
        )

        try:
            self.client.delete_collection("support_ops")
        except:
            pass

        self.collection = self.client.create_collection(
            name="support_ops"
        )

    def add_documents(
        self,
        ids,
        documents,
        embeddings,
        metadatas,
    ):

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        embedding,
        top_k=3,
    ):

        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )