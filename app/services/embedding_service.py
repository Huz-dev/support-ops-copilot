import os
import warnings

os.environ["TOKENIZERS_PARALLELISM"] = "false"

warnings.filterwarnings("ignore", category=FutureWarning)

from sentence_transformers import SentenceTransformer

from app.config import settings


class EmbeddingService:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

        print("Embedding model loaded.")

    def embed(self, texts):

        return self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
        ).tolist()