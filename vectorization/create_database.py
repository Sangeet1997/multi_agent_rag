import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def create_collection(pdf_path):

    chroma_client = chromadb.Client()

    try:
        collection = chroma_client.create_collection(name="basic_rag")
    except ValueError:  # Collection already exists
        collection = chroma_client.get_collection(name="basic_rag")

    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(pages)

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk.page_content],
            metadatas=[{"source": pdf_path, "page": chunk.metadata["page"]}],
            ids=[f"doc_{i}"]
        )
    
    return f"Added {len(chunks)} chunks from {pdf_path} to the collection"
    
