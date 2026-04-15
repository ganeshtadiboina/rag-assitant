from langchain_text_splitters import RecursiveCharacterTextSplitter
def split_documents(documents):
    """
    Split documents into chunks
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=80,
        chunk_overlap=10
    )

    chunks = splitter.split_documents(documents)
    return chunks