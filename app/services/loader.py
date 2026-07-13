from pathlib import Path

from app.config import settings


class KnowledgeLoader:
    """
    Loads all knowledge documents from the knowledge folder.
    """

    def __init__(self):
        self.knowledge_path = Path(settings.KNOWLEDGE_PATH)

    def load_documents(self):

        documents = []

        if not self.knowledge_path.exists():
            raise FileNotFoundError(
                f"Knowledge folder not found: {self.knowledge_path}"
            )

        files = sorted(self.knowledge_path.glob("*.txt"))

        if not files:
            raise Exception("No .txt files found inside knowledge folder.")

        for file in files:

            text = file.read_text(encoding="utf-8").strip()

            if not text:
                print(f"Skipping empty file: {file.name}")
                continue

            documents.append(
                {
                    "source": file.name,
                    "text": text,
                }
            )

        if not documents:
            raise Exception("All knowledge files are empty.")

        return documents