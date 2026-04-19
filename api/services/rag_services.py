from app.ingestion.loader import load_documents
from app.ingestion.chunker import split_documents
from app.vectorstore.qdrant_store import QdrantVectorStore
from app.retrieval.bm25_retriever import BM25Retriever
from app.retrieval.hybrid_retriever import HybridRetriever
from app.reranker.cross_encoder import CrossEncoderReranker
from app.generation.generator import RAGGenerator
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self):
        self.vectorstore = QdrantVectorStore()
        self.reranker = CrossEncoderReranker()
        self.generator = RAGGenerator()
        self.bm25_corpus = []
        self.bm25 = None
        self.hybrid = None

    def _ensure_hybrid_from_vectorstore(self) -> bool:
        """Restore BM25 + hybrid from Qdrant after process restart (or cold start)."""
        if self.hybrid is not None:
            return True
        chunks = self.vectorstore.fetch_chunks_for_bm25()
        if not chunks:
            return False
        self.bm25_corpus = chunks
        self.bm25 = BM25Retriever(self.bm25_corpus)
        self.hybrid = HybridRetriever(self.bm25, self.vectorstore)
        logger.info("Rebuilt hybrid retriever from Qdrant (%s chunks).", len(chunks))
        return True

    def ingest_document(self, file_path, user_id, thread_id, document_id, source):
        docs = load_documents(file_path)
        chunks = split_documents(docs)
        texts = [chunk.page_content for chunk in chunks]

        if not texts:
            logger.warning("No text extracted from the document.")
            return

        metadata_list = [
            {
                "user_id": user_id,
                "thread_id": thread_id,
                "document_id": document_id,
                "source": source,
                "chunk_id": i,
                "timestamp": datetime.utcnow().isoformat(),
            }
            for i in range(len(texts))
        ]

        # Store in Qdrant
        self.vectorstore.add_documents(texts, metadata_list)

        # BM25 corpus: BM25Retriever expects {"text", "metadata"} per chunk
        bm25_docs = [
            {"text": text, "metadata": meta}
            for text, meta in zip(texts, metadata_list)
        ]
        self.bm25_corpus.extend(bm25_docs)

        self.bm25 = BM25Retriever(self.bm25_corpus)
        self.hybrid = HybridRetriever(self.bm25, self.vectorstore)

        logger.info(f"Document {document_id} ingested successfully.")

    def query(self, user_query: str, thread_id: str):
        logger.info(f"Received query: {user_query}")

        if not self._ensure_hybrid_from_vectorstore():
            return {
                "answer": "No documents available. Please upload first.",
                "sources": []
            }

        retrieved_docs = self.hybrid.search(
            query=user_query,
            thread_id=thread_id,
            top_k=5
        )

        if not retrieved_docs:
            return {
                "answer": "I don't know.",
                "sources": []
            }

        # ✅ Pass FULL docs to reranker
        reranked_docs = self.reranker.rerank(user_query, retrieved_docs)

        # ✅ Generator returns structured output
        result = self.generator.generate(user_query, reranked_docs)

        return result