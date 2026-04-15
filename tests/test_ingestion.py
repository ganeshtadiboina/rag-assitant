from app.ingestion.loader import load_documents
from app.ingestion.chunker import split_documents

def test_ingestion():
    docs = load_documents("data/raw/sample.txt")
    chunks = split_documents(docs)

    print(f"Loaded {len(docs)} documents")
    print(f"Created {len(chunks)} chunks")

    if len(chunks) > 0:    
        print("\nSample chunk:")
        print(chunks[0].page_content)
    else:
        print("\n No Chunks created. Check your input file.")

if __name__ == "__main__":
    test_ingestion()