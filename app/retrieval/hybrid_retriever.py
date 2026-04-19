from typing import List, Dict


class HybridRetriever:
    def __init__(self, bm25_retriever, vectorstore):
        self.bm25_retriever = bm25_retriever
        self.vectorstore = vectorstore

    def search(self, query: str, thread_id: str, top_k: int = 5) -> List[Dict]:

        # 🔹 Vector search (already correct format)
        vector_results = self.vectorstore.similarity_search(
            query=query,
            thread_id=thread_id,
            k=top_k
        )

        # BM25 returns same shape as vector hits: page_content, metadata, score
        bm25_results = []
        if self.bm25_retriever:
            bm25_results = self.bm25_retriever.search(
                query=query,
                thread_id=thread_id,
                top_k=top_k,
            )

        # 🔹 Merge + deduplicate
        merged = {}

        for doc in vector_results + bm25_results:
            key = doc["page_content"]

            if key not in merged:
                merged[key] = doc
            else:
                if doc.get("score", 0) > merged[key].get("score", 0):
                    merged[key] = doc

        # 🔹 Sort by score
        sorted_docs = sorted(
            merged.values(),
            key=lambda x: x.get("score", 0),
            reverse=True
        )

        return sorted_docs[:top_k]