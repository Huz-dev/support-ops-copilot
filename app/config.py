import os

os.environ["ANONYMIZED_TELEMETRY"] = "FALSE"
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    MODEL_NAME = "llama-3.3-70b-versatile"

    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    CHROMA_PATH = "chroma_db"

    KNOWLEDGE_PATH = "app/knowledge"


settings = Settings()