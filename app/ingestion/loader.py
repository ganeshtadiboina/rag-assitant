from langchain_community.document_loaders import PyPDFLoader, TextLoader


from typing import List

def load_documents(file_path: str) -> List:
    """
    Load Documents from file (PDF or TXT)

    """
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)
    else:
        raise ValueError("Unsupported file format")
    
    documents = loader.load()
    return documents