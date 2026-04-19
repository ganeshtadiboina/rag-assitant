from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    Filter,
    FieldCondition,
    MatchValue,
    PointStruct,
)
from sentence_transformers import SentenceTransformer
from uuid import uuid4
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class QdrantVectorStore:
    def __init__(self, collection_name: str = "rag_documents"):
        self.client = QdrantClient(host="localhost", port=6333)
        self.collection_name = collection_name

        # Embedding model
        self.embedding_model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )
        self.embedding_dim = (
            self.embedding_model.get_sentence_embedding_dimension()
        )

        self._create_collection()

    def _create_collection(self):
        collections = [
            c.name for c in self.client.get_collections().collections
        ]
        if self.collection_name not in collections:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedding_dim,
                    distance=Distance.COSINE,
                ),
            )
            logger.info(f"Created collection: {self.collection_name}")

    def add_documents(
        self, texts: List[str], metadata_list: List[Dict]
    ) -> List[str]:
        if not texts:
            logger.warning("No texts provided for insertion.")
            return []

        embeddings = self.embedding_model.encode(
            texts,
            batch_size=32,
            show_progress_bar=False,
            normalize_embeddings=True,
        )

        point_ids = [str(uuid4()) for _ in texts]

        points = [
            PointStruct(
                id=pid,
                vector=embedding.tolist(),
                payload={"text": text, **metadata},
            )
            for pid, text, embedding, metadata in zip(
                point_ids, texts, embeddings, metadata_list
            )
        ]

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=True,
        )

        logger.info(f"Inserted {len(points)} documents into Qdrant.")
        return point_ids

    def similarity_search(
        self,
        query: str,
        thread_id: Optional[str] = None,
        user_id: Optional[str] = None,
        k: int = 5,
    ) -> List[Dict]:
        query_embedding = self.embedding_model.encode(
            query,
            normalize_embeddings=True,
        ).tolist()

        conditions = []

        if user_id:
            conditions.append(
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=user_id)
                )
            )

        # Apply metadata filter
        if thread_id:
            conditions.append(
                FieldCondition(
                    key="thread_id",
                    match=MatchValue(value=thread_id)
                )
            )
        
        query_filter = Filter(must=conditions) if conditions else None

        logger.info(f"Query: {query}")
        logger.info(f"Thread ID: {thread_id}")
        logger.info(f"User ID: {user_id}")
        logger.info(f"Filter applied: {query_filter}")

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=k,
            query_filter=query_filter,
        )

        points = getattr(results, "points", [])

        documents = []
        MIN_SCORE = 0.2

        for point in results:
            if point.score < MIN_SCORE:
                continue

            payload = point.payload or {}

            documents.append(
                {
                    "page_content": payload.get("text", ""),
                    "metadata": payload,
                    "score": point.score,
                }
            )

        logger.info(f"Retrieved {len(documents)} filter documents.")

        return documents

    def fetch_chunks_for_bm25(self) -> List[Dict]:
        """
        Rebuild BM25 corpus from all stored points. Used after API restart when
        in-memory BM25 state is empty but Qdrant still has indexed chunks.
        """
        offset = None
        out: List[Dict] = []
        while True:
            points, next_offset = self.client.scroll(
                collection_name=self.collection_name,
                limit=256,
                offset=offset,
                with_payload=True,
                with_vectors=False,
            )
            for point in points:
                payload = point.payload or {}
                text = payload.get("text") or ""
                if not str(text).strip():
                    continue
                meta = {k: v for k, v in payload.items() if k != "text"}
                out.append({"text": str(text), "metadata": meta})
            offset = next_offset
            if offset is None or not points:
                break
        logger.info(f"Loaded {len(out)} chunks from Qdrant for BM25 corpus.")
        return out
