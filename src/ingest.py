import os
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from vector_store import get_vector_store, validate_envs
    
def chunks_pdf(chunk_size=1000, chunk_overlap=150)-> list[Document]:
    PDF_PATH = os.getenv("PDF_PATH")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=False)

    chunks = splitter.split_documents(documents)
    if not chunks:
        raise ValueError("Nenhum chunk foi criado a partir do PDF. Verifique o conteúdo do PDF e os parâmetros de chunking.")
    
    return chunks

def enrich_documents(documents: list[Document]) -> list[Document]:
    enriched_documents = []
    
    for chunk in documents:
        enriched_document = Document(
            page_content=chunk.page_content,
            metadata={k: v for k, v in chunk.metadata.items() if v not in ["", None]},
        )
        enriched_documents.append(enriched_document)

    return enriched_documents

def embed_documents(documents: list[Document]):
    ids = [f"doc_{i}" for i in range(len(documents))]
    store = get_vector_store()
    store.add_documents(documents, ids=ids)

def ingest_pdf():
    chunks = chunks_pdf()
    enriched_documents = enrich_documents(chunks)
    embed_documents(enriched_documents)

    
load_dotenv()
validate_envs()

if __name__ == "__main__":
    ingest_pdf()