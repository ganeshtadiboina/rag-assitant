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

        # Update BM25 corpus
        self.bm25_corpus.extend(texts)
        self.bm25 = BM25Retriever(self.bm25_corpus)

        # Initialize Hybrid Retriever
        self.hybrid = HybridRetriever(self.bm25, self.vectorstore)

        logger.info(f"Document {document_id} ingested successfully.")

    def query(self, user_query: str, thread_id: str) -> str:
        logger.info(f"Received query: {user_query}")

        # Ensure hybrid retriever is initialized
        if not self.hybrid:
            logger.warning("Hybrid retriever not initialized.")
            return "No documents available. Please upload documents first."

        # Hybrid retrieval
        retrieved_docs = self.hybrid.search(
            query=user_query,
            thread_id=thread_id,
            top_k=5
        )

        if not retrieved_docs:
            return "I don't know."

        # Extract text
        texts = [doc["page_content"] for doc in retrieved_docs]

        # Rerank
        reranked_docs = self.reranker.rerank(user_query, texts)

        # Generate answer with citations
        answer = self.generator.generate(user_query, reranked_docs)

        return answer