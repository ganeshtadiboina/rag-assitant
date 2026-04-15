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
        k: int = 5,
    ) -> List[Dict]:
        query_embedding = self.embedding_model.encode(
            query,
            normalize_embeddings=True,
        ).tolist()

        # Apply metadata filter
        conditions = []
        if thread_id:
            conditions.append(
                FieldCondition(
                    key="thread_id",
                    match=MatchValue(value=thread_id),
                )
            )

        query_filter = Filter(must=conditions) if conditions else None

        # Updated API call for newer Qdrant versions
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=k,
            query_filter=query_filter,
        )

        documents = []
        for point in results.points:
            payload = point.payload or {}
            documents.append(
                {
                    "page_content": payload.get("text", ""),
                    "metadata": payload,
                    "score": point.score,
                }
            )

        logger.info(f"Retrieved {len(documents)} documents for query.")
        return documents