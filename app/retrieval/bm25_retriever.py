from rank_bm25 import BM25Okapi
from typing import List


class BM25Retriever:
    """
    Lexical retriever using BM25 for keyword-based search.
    """

    def __init__(self, texts: List[str]):
        self.texts = texts
        self.tokenized_corpus = [text.lower().split() for text in texts]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def search(self, query: str, top_k: int = 5) -> List[str]:
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)

        # Rank documents by score
        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        return [self.texts[i] for i in ranked_indices]