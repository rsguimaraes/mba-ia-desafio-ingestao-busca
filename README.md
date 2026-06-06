# Desafio MBA Engenharia de Software com IA - Full Cycle

Pipeline RAG (Retrieval-Augmented Generation) com ingestão de PDFs, busca semântica e geração de respostas via Google Gemini, usando PostgreSQL com pgvector como vector store.

## Visão geral

| Módulo | Arquivo | Responsabilidade |
| --- | --- | --- |
| Ingestão | `src/ingest.py` | Carrega PDF, divide em chunks, gera embeddings e armazena no pgvector |
| Vector store | `src/vector_store.py` | Inicializa o `PGVector` e valida variáveis de ambiente |
| Busca + LLM | `src/search.py` | Busca semântica no pgvector e geração de resposta via Gemini |
| Interface | `src/chat.py` | Loop interativo no terminal (pergunta → busca → resposta) |

## Fluxo

```text
PDF → chunks → embeddings (Gemini) → pgvector
                                          ↓
pergunta → embedding → busca semântica → contexto → LLM (Gemini) → resposta
```

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
| `GOOGLE_EMBEDDING_MODEL` | Modelo de embedding (ex: `models/gemini-embedding-001`) |
| `GOOGLE_LLM_MODEL` | Modelo de geração de texto (padrão: `gemini-2.5-flash`) |
| `DATABASE_URL` | URL de conexão com o PostgreSQL |
| `PG_VECTOR_COLLECTION_NAME` | Nome da coleção no pgvector |
| `PDF_PATH` | Caminho relativo ao PDF a ser ingerido |

> **Atenção:** o `PDF_PATH` usa caminho relativo. Execute os scripts sempre a partir da raiz do projeto.

Exemplo de `.env`:

```env
GOOGLE_API_KEY=sua_chave_aqui
GOOGLE_EMBEDDING_MODEL=models/gemini-embedding-001
GOOGLE_LLM_MODEL=gemini-2.5-flash
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=documentos
PDF_PATH=document.pdf
```

### 4. Subir o banco de dados

```bash
docker compose up -d
```

Isso sobe o container `postgres_rag` na porta `5432` (banco `rag`, usuário `postgres`, senha `postgres`) com a extensão `vector` habilitada automaticamente.

## Execução

### Etapa 1 — Ingestão do PDF

```bash
python src/ingest.py
```

O script irá:

1. Carregar e dividir o PDF em chunks (tamanho 1000, overlap 150)
2. Remover metadados vazios dos documentos
3. Gerar embeddings via `gemini-embedding-001`
4. Armazenar os vetores no PostgreSQL

> **Nota:** o parâmetro `requests_per_minute=10` é aplicado automaticamente para evitar erros de rate limit na tier gratuita da API do Google.

### Etapa 2 — Interface de chat

```bash
python src/chat.py
```

Digite sua pergunta quando solicitado. Para cada pergunta o sistema:

1. Realiza busca semântica no pgvector (top-10 chunks mais similares)
2. Monta o contexto e envia ao LLM Gemini com um prompt restritivo
3. Exibe a resposta gerada com base exclusivamente no conteúdo do PDF

Para encerrar, digite `SAIR`.

## Observações técnicas

- As dependências foram atualizadas para versões recentes (LangChain 1.x, `google-genai` 2.x) para compatibilidade com os modelos mais recentes do Google. As versões originais do desafio não são compatíveis com esses modelos.
- O LLM responde **somente** com base no contexto recuperado — nunca usa conhecimento externo.
- O modelo de LLM pode ser sobrescrito pela variável `GOOGLE_LLM_MODEL`; o padrão é `gemini-2.5-flash`.
