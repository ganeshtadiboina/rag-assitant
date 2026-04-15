from app.ingestion.loader import load_documents
from app.ingestion.chunker import split_documents
from app.embeddings.embedder import EmbeddingModel
from app.vectorstore.faiss_store import FAISSVectorStore
from app.retrieval.bm25_retriever import BM25Retriever
from app.retrieval.hybrid_retriever import HybridRetriever
from app.reranker.cross_encoder import CrossEncoderReranker
from app.generation.generator import RAGGenerator

def test_rag():
    # Load + chunk
    docs = load_documents("data/raw/sample.txt")
    chunks = split_documents(docs)
    texts = [chunk.page_content for chunk in chunks]

    # Embeddings + vector DB
    embedder = EmbeddingModel()
    embeddings = embedder.embed_documents(texts)

    vectorstore = FAISSVectorStore(dimension=len(embeddings[0]))
    vectorstore.add_documents(embeddings, texts)

    # BM25 + Hybrid
    bm25 = BM25Retriever(texts)
    hybrid = HybridRetriever(bm25, vectorstore, embedder)

    # Query
    query = "what is deep learning?"
    retrieved_docs = hybrid.search(query)

    # Rerank
    reranker = CrossEncoderReranker()
    reranked_docs = reranker.rerank(query, retrieved_docs)

    # Generate Answer
    generator = RAGGenerator()
    answer = generator.generate(query, retrieved_docs)

    print("\n Query:", query)
    print("\n Answer:\n", answer)

if __name__ == "__main__":
    test_rag()
