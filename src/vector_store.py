import os
from langchain_postgres import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def validate_envs():
    required_envs = ["PDF_PATH", "GOOGLE_API_KEY", "GOOGLE_EMBEDDING_MODEL", "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME"]
    missing_envs = [env for env in required_envs if env not in os.environ]
    if missing_envs:
        raise EnvironmentError(f"Variaveis de ambiente obrigatórias não definidas: {', '.join(missing_envs)}")


def get_vector_store() -> PGVector:
    embedding_model = GoogleGenerativeAIEmbeddings(
        model=os.getenv("GOOGLE_EMBEDDING_MODEL"),
        requests_per_minute=10,
    )
    return PGVector(
        embeddings=embedding_model,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )
