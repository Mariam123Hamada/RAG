# RAG Application

A Retrieval-Augmented Generation (RAG) service built with FastAPI, PostgreSQL, and pgvector.

The application lets users upload documents, split them into vectorized text chunks, store them in PostgreSQL with pgvector, and answer questions by retrieving relevant chunks from the vector store.

## Key Features

- FastAPI REST API for upload and question answering
- File upload with document splitting into chunks
- Vector storage using PostgreSQL + pgvector
- Embedding provider abstraction for Cohere and Gemini
- Metrics support via Prometheus-compatible middleware
- Docker compose configuration for PostgreSQL/pgvector

## Repository Structure

- `src/Routes/main.py` — FastAPI app initialization
- `src/Routes/DataRoute.py` — upload and retrieval endpoints
- `src/servicies` — task orchestration, embedding, and project services
- `src/stores/providers/PGVECTOR.py` — pgvector database adapter
- `docker/docker-compose.yaml` — PostgreSQL + pgvector service
- `src/requirements.txt` — Python dependencies

## Prerequisites

- Python 3.11+ recommended
- Docker and Docker Compose
- PostgreSQL-compatible database with pgvector support

## Setup

1. Clone the repository

```bash
git clone https://github.com/Mariam123Hamada/RAG.git
cd RAG
```

2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r src/requirements.txt
```

4. Configure environment variables

Copy the example env file into a local `.env` file and populate your secrets.

```bash
cp .env.example .env
```

Your `.env` file should include values for:

- `DATABASE_URL`
- `POSTGRES_PASSWORD`
- `COHERE_KEY`
- `GEMMNI_KEY`
- `EMBEDDING_PROVIDER`
- `EMBEDDING_MODEL_COHER`
- `EMBEDDING_MODEL_GEMMNI`
- `GENERTION_MODEL`
- `GROK_KEY`

> If `.env.example` is not present, create `.env` manually using the same variable names.

## Running with Docker

The project includes a Docker Compose service for PostgreSQL with pgvector.

```bash
cd docker
docker compose up -d
```

This starts a `pgvector` database container and exposes port `54329` on the host.

## Running the API

From the project root, run:

```bash
uvicorn src.Routes.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Upload a file

`POST /API/Upload/FileUpload`

Form parameters:

- `project_id` (int)
- `file` (UploadFile)

Response:

- `status`: success
- `data`: upload result with project metadata

### Ask a question

`POST /API/Upload/AsnwerQuestions`

JSON or form parameters:

- `project_id` (int)
- `text` (string)

Response:

- `answer`: generated answer text

### Retrieve chunks

`POST /API/Upload/Reterivechunks`

JSON or form parameters:

- `project_id` (int)
- `text` (string)

Response:

- `res`: list of retrieved chunk data related to the query

## Notes

- The current implementation uses `NLPTask` and `ProjectServices` for file processing and retrieval.
- Embedding provider selection is handled in `src/servicies/embedding/EmbeddingFactory.py`.
- The Docker Compose setup uses `docker/env/.env.postgres` for database credentials.

## Future Improvements

- Add automated tests for API and database flows
- Improve file format support and document parser coverage
- Add authentication and role-based access control
- Support additional embedding providers and generation backends



