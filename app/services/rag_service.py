from app.services.loader import KnowledgeLoader
from app.services.chunker import DocumentChunker
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.retriever import Retriever
from app.services.ai_service import AIService


class RAGService:

    def __init__(self):

        self.loader = KnowledgeLoader()

        self.chunker = DocumentChunker()

        self.embedder = EmbeddingService()

        self.vector_store = VectorStore()

        self.retriever = Retriever(
            self.embedder,
            self.vector_store,
        )

        self.ai = AIService()

    def ingest(self):

        print("\nLoading documents...")

        docs = self.loader.load_documents()

        print(f"Loaded {len(docs)} documents")

        chunks = self.chunker.chunk_documents(
            docs
        )

        print(f"Created {len(chunks)} chunks")

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = self.embedder.embed(
            texts
        )

        ids = [
            chunk["id"]
            for chunk in chunks
        ]

        metadatas = [
            {
                "source": chunk["source"],
                "chunk": chunk["chunk_index"],
            }
            for chunk in chunks
        ]

        self.vector_store.add_documents(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        print("Knowledge Base Ready!")

    def ask(
        self,
        question,
    ):

        retrieved = self.retriever.retrieve(
            question
        )

        context = "\n\n".join(
            [
                r["document"]
                for r in retrieved
            ]
        )

        answer = self.ai.rag(
            question,
            context,
        )

        return {
            "answer": answer,
            "retrieved": retrieved,
        }