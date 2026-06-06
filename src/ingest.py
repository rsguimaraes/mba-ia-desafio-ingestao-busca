import os
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from dotenv import load_dotenv

def validate_envs():
    required_envs = ["PDF_PATH"]
    missing_envs = [env for env in required_envs if env not in os.environ]
    if missing_envs:
        raise EnvironmentError(f"Variaveis de ambiente obrigatórias não definidas: {', '.join(missing_envs)}")
    
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

def embed_documents(documents: list[Document]) -> list[Document]:
    ids = [f"doc_{i}" for i in range(len(documents))]
    embedding_model = GoogleGenerativeAIEmbeddings(
        model=os.getenv("GOOGLE_EMBEDDING_MODEL"),
        requests_per_minute=10,
    )
    
    store = PGVector(
        embeddings=embedding_model,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True
    )

    store.add_documents(documents, ids=ids)

def ingest_pdf():
    chunks = chunks_pdf()
    enriched_documents = enrich_documents(chunks)
    embed_documents(enriched_documents)

    
load_dotenv()
validate_envs()

if __name__ == "__main__":
    ingest_pdf()