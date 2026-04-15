from typing import List, Dict


class HybridRetriever:
    """
    Combines BM25 and vector search results.
    """

    def __init__(self, bm25_retriever, vectorstore, bm25_weight: float = 0.5):
        self.bm25_retriever = bm25_retriever
        self.vectorstore = vectorstore
        self.bm25_weight = bm25_weight

    def search(self, query: str, thread_id: str, top_k: int = 5) -> List[Dict]:
        # Vector search results
        vector_results = self.vectorstore.similarity_search(
            query=query,
            thread_id=thread_id,
            k=top_k
        )

        # BM25 results (text only)
        bm25_texts = []
        if self.bm25_retriever:
            bm25_texts = self.bm25_retriever.search(query, top_k=top_k)

        # Convert BM25 results to document format
        bm25_results = [
            {
                "page_content": text,
                "metadata": {"source": "bm25"}
            }
            for text in bm25_texts
        ]

        # Combine and deduplicate results
        combined = vector_results + bm25_results
        unique_docs = {}
        for doc in combined:
            content = doc["page_content"]
            if content not in unique_docs:
                unique_docs[content] = doc

        return list(unique_docs.values())[:top_k]