from sentence_transformers import CrossEncoder
from typing import List


class CrossEncoderReranker:
    """
    Reranks retrieved documents using a cross-encoder model.
    """

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, documents: list):
        if not documents:
            return []

        # Extract text
        texts = [doc["page_content"] for doc in documents]

        # Create pairs
        pairs = [(query, text) for text in texts]

        # Get scores
        scores = self.model.predict(pairs)

        # Attach scores back to documents
        scored_docs = list(zip(documents, scores))

        # Sort by score descending
        ranked_docs = sorted(
            scored_docs,
            key=lambda x: x[1],
            reverse=True
        )

        # Return FULL documents (not jjust text)
        return [doc for doc, score in ranked_docs]