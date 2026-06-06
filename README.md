# Desafio MBA Engenharia de Software com IA - Full Cycle

Pipeline de ingestão de documentos PDF com vetorização no PostgreSQL, utilizando modelos do Google Gemini.

## Visão geral

O projeto contempla atualmente a etapa de ingestão:

- **Ingestão** (`src/ingest.py`): carrega um PDF, divide em chunks, gera embeddings via Google Gemini e armazena os vetores no PostgreSQL com a extensão pgvector.
- **Interface interativa** (`src/main.py`): loop de entrada de perguntas via terminal (busca semântica em desenvolvimento).

## Pré-requisitos

- Python 3.11+
- Docker e Docker Compose
- Chave de API do Google (Google AI Studio)

## Configuração do ambiente

### 1. Criar e ativar o ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar as variáveis de ambiente

Copie o arquivo de exemplo e preencha os valores:

```bash
cp .env.example .env
```

| Variável | Descrição |
| --- | --- |
| `GOOGLE_API_KEY` | Chave de API do Google AI Studio |
| `GOOGLE_EMBEDDING_MODEL` | Modelo de embedding (padrão: `models/gemini-embedding-001`) |
| `DATABASE_URL` | URL de conexão com o PostgreSQL |
| `PG_VECTOR_COLLECTION_NAME` | Nome da coleção no pgvector |
| `PDF_PATH` | Caminho relativo ao PDF a ser ingerido |

> **Atenção:** o `PDF_PATH` usa caminho relativo sem concatenar o diretório atual. Execute os scripts sempre a partir da raiz do projeto.

Exemplo de `.env`:

```env
GOOGLE_API_KEY=sua_chave_aqui
GOOGLE_EMBEDDING_MODEL=models/gemini-embedding-001
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=documentos
PDF_PATH=document.pdf
```

### 4. Subir o banco de dados

O Docker Compose sobe o PostgreSQL com a extensão pgvector já habilitada:

```bash
docker compose up -d
```

Isso cria o container `postgres_rag` na porta `5432` com banco `rag`, usuário `postgres` e senha `postgres`.

## Execução

### Etapa 1 — Ingestão do PDF

Execute a partir da raiz do projeto:

```bash
python .\src\ingest.py
```

O script irá:

- Carregar e dividir o PDF em chunks (tamanho 1000, overlap 150)
- Enriquecer os metadados dos documentos
- Gerar embeddings via `gemini-embedding-001`
- Armazenar os vetores no PostgreSQL

> **Nota sobre o modelo gratuito do Google:** o parâmetro `requests_per_minute=10` é aplicado automaticamente para evitar erros de rate limit ao usar a tier gratuita da API.

### Etapa 2 — Interface interativa (em desenvolvimento)

```bash
python .\src\main.py
```

Digite sua pergunta quando solicitado. Para encerrar, digite `SAIR`. A integração com busca semântica ainda está em desenvolvimento.

## Observações técnicas

- As bibliotecas do projeto foram atualizadas para versões mais recentes (LangChain 1.x, google-genai 2.x, openai 2.x) para compatibilidade com os modelos mais recentes do Google. As versões originais do desafio não são compatíveis com esses modelos.
- O modelo utilizado para embeddings é o `gemini-embedding-001` do Google.
