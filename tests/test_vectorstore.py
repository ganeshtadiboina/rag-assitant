from app.ingestion.loader import load_documents
from app.ingestion.chunker import split_documents
from app.embeddings.embedder import EmbeddingModel
from app.vectorstore.faiss_store import FAISSVectorStore

def test_vectorstore():
    # load + chunk
    docs = load_documents("data/raw/sample.txt")
    chunks = split_documents(docs)

    texts = [chunk.page_content for chunk in chunks]

    # Embeddings
    embedder = EmbeddingModel()
    embeddings = embedder.embed_documents(texts)

    # Vector DB 
    vectorstore = FAISSVectorStore(dimension=len(embeddings[0]))
    vectorstore.add_documents(embeddings, texts)

    # Query
    query = "what is machine learning?"
    query_embedding = embedder.embed_query(query)

    results = vectorstore.search(query_embedding)

    print("\n Query:", query)
    print("\n Results:")
    for res in results:
        print("-", res)

if __name__ == "__main__":
    test_vectorstore()



