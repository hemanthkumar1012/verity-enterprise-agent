# Verity Deployment

Verity is designed as two independently deployable surfaces:

- Frontend: Vercel
- Backend: FastAPI on Render
- Database: managed PostgreSQL with pgvector when persistence is enabled

## Frontend

Deploy the frontend directory as a Vercel project.

Set frontend/config.js to the public Render API URL:

    window.VERITY_CONFIG = {
      apiUrl: "https://YOUR-RENDER-SERVICE.onrender.com",
    };

The frontend remains accessible if the API is unavailable. Upload and search actions show an offline state instead of breaking the workspace.

## Backend

Create a Render Web Service from the repository.

- Runtime: Python
- Build command: pip install -e ".[dev]"
- Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
- Health check: /health

Set these environment variables:

    ALLOWED_ORIGINS=https://YOUR-VERCEL-APP.vercel.app
    DATABASE_URL=YOUR_POSTGRES_CONNECTION_STRING

When DATABASE_URL is not configured, Verity uses the simple in-memory store for local development.

## Database

Use a PostgreSQL service with the pgvector extension enabled.

The repository includes the baseline schema in infra/postgres/schema.sql. The API also creates its required tables and text-search index automatically on startup when DATABASE_URL is configured.

The current persistent retrieval path uses PostgreSQL full-text search. pgvector is enabled in the schema so semantic embeddings can be added without replacing the document model.

## Deployment order

1. Create the PostgreSQL/pgvector database.
2. Configure DATABASE_URL on Render.
3. Deploy the Render API and verify /health.
4. Put the Render URL into frontend/config.js.
5. Deploy frontend/ to Vercel.
6. Upload a test document and verify evidence search.

## Failure behavior

- Frontend unavailable: backend remains independently deployable.
- Backend unavailable: frontend remains viewable and shows an offline state.
- Database unavailable during startup: the API will fail startup rather than silently pretending that persistent storage is available.
