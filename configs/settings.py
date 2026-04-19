from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 🔐 API Keys
    OPENAI_API_KEY: str

    # 🤖 Models
    LLM_MODEL: str = "gpt-4o-mini"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    RERANKER_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    # 📊 Retrieval Config
    TOP_K: int = 5
    BM25_WEIGHT: float = 0.5

    # 📦 Qdrant Config
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    COLLECTION_NAME: str = "rag_documents"

    # 🧪 Evaluation Config (NEW)
    EVAL_THRESHOLD: float = 0.6

    class Config:
        env_file = ".env"


settings = Settings()