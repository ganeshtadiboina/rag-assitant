from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_score(expected, actual):
    emb1 = model.encode([expected])
    emb2 = model.encode([actual])
    return cosine_similarity(emb1, emb2)[0][0]


def keyword_score(keywords: list, actual: str) -> float:
    if not keywords:
        return 1.0
    text = (actual or "").lower()
    hits = sum(1 for k in keywords if k and str(k).lower() in text)
    return hits / len(keywords)