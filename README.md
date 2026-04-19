# Production RAG App

A full-stack Retrieval-Augmented Generation (RAG) application where users upload documents and ask grounded questions.  
The system retrieves relevant chunks using hybrid search (BM25 + vector search), reranks them, and generates answers with citations.

## What It Does

- Upload PDF/text documents and index them into Qdrant
- Query documents by `thread_id` for scoped retrieval
- Hybrid retrieval with BM25 + dense embeddings
- Cross-encoder reranking before generation
- LLM answer generation with source tags (`[Doc1]`, `[Doc2]`, ...)
- React frontend for upload, query, and answer display

## Architecture

```text
User (React UI)
   -> FastAPI (/upload, /query)
      -> Ingestion (load + chunk)
      -> Qdrant (vector index + metadata payload)
      -> HybridRetriever (BM25 + vector)
      -> CrossEncoderReranker
      -> OpenAI Generator
      -> Answer + Sources
```

## Tech Stack

- **Backend:** FastAPI
- **Frontend:** React + Vite + Material UI
- **Vector DB:** Qdrant
- **Embeddings:** sentence-transformers/all-MiniLM-L6-v2
- **Retrieval:** BM25 + vector similarity search
- **Reranker:** cross-encoder/ms-marco-MiniLM-L-6-v2
- **LLM:** OpenAI chat models (configurable via `.env`)
- **Infra:** Docker Compose (Qdrant)

## Project Structure

```text
production-rag-app/
├── api/
│   ├── routes/            # FastAPI routes
│   ├── schemas/           # Request/response models
│   ├── services/          # RAG orchestration service
│   └── evals/             # Evaluation scripts/dataset
├── app/
│   ├── ingestion/         # Document loading/chunking
│   ├── retrieval/         # BM25 + hybrid retrievers
│   ├── reranker/          # Cross-encoder reranker
│   ├── generation/        # LLM generation
│   └── vectorstore/       # Qdrant integration
├── rag-frontend/          # React app
├── data/uploads/          # Uploaded files (runtime/local)
├── docker-compose.yml
└── README.md
```

## Setup

### 1) Clone

```bash
git clone https://github.com/ganeshtadiboina/rag-assitant.git
cd rag-assitant
```

### 2) Backend

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `.env` in project root:

```env
OPENAI_API_KEY=your_openai_api_key
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2
TOP_K=5
BM25_WEIGHT=0.5
QDRANT_HOST=localhost
QDRANT_PORT=6333
COLLECTION_NAME=rag_documents
EVAL_THRESHOLD=0.6
```

### 3) Start Qdrant

```bash
docker compose up -d
```

### 4) Run API

```bash
uvicorn api.main:app --reload --port 8001
```

API docs: `http://localhost:8001/docs`

### 5) Frontend

```bash
cd rag-frontend
npm install
npm run dev
```

Set frontend env (`rag-frontend/.env`):

```env
VITE_API_URL=http://127.0.0.1:8001
```

## API Endpoints

### `POST /upload`

`multipart/form-data` fields:

- `file`: document file
- `user_id`: user identifier
- `thread_id`: conversation/thread identifier

### `POST /query`

Request:

```json
{
  "query": "What are user account rules?",
  "thread_id": "your-thread-id"
}
```

Response:

```json
{
  "answer": ".... [Doc1] ...",
  "sources": [
    {
      "tag": "[Doc1]",
      "source": "terms_conditions.pdf",
      "document_id": "..."
    }
  ]
}
```

## Notes on Reliability

- The query path rebuilds in-memory BM25/hybrid state from Qdrant when needed (helpful after backend restarts)
- Retrieval is metadata-aware (`thread_id`) to avoid cross-thread leakage
- Generation prompt is constrained to answer from retrieved context and cite sources

## Evaluation (Optional)

Run local eval:

```bash
PYTHONPATH=. python api/evals/run_eval.py
```

GitHub Actions workflow: `.github/workflows/eval.yml` (requires `OPENAI_API_KEY` secret).

## Security

- Keep `.env` out of version control
- Do not commit local uploaded documents (`data/uploads/*.pdf` is ignored)
- Rotate API keys if exposed

## License

MIT