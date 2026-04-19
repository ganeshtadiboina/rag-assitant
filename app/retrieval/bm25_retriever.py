from rank_bm25 import BM25Okapi
from typing import List, Dict, Optional


class BM25Retriever:
    def __init__(self, corpus: List[Dict]):
        """
        corpus = [
            {"text": "...", "metadata": {...}}
        ]
        """
        self.corpus = corpus

    def search(
        self,
        query: str,
        thread_id: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict]:

        # 🔹 Filter by thread_id
        filtered = [
            doc for doc in self.corpus
            if doc["metadata"]["thread_id"] == thread_id
        ] if thread_id else self.corpus

        if not filtered:
            return []

        texts = [doc["text"] for doc in filtered]

        tokenized_corpus = [text.lower().split() for text in texts]
        bm25 = BM25Okapi(tokenized_corpus)

        tokenized_query = query.lower().split()
        scores = bm25.get_scores(tokenized_query)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        return [
            {
                "page_content": filtered[i]["text"],
                "metadata": filtered[i]["metadata"],
                "score": scores[i],
                "retriever": "bm25"
            }
            for i in ranked_indices
        ]