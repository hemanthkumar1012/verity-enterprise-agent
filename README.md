# Verity — Enterprise Multimodal Research & Action Agent

Verity is an enterprise-oriented AI research and action platform designed around evidence, controlled tool use, human approval, security, and reproducible evaluation.

## Core capabilities

- Hybrid retrieval (keyword + vector)
- Multimodal document ingestion
- Tables and images as first-class evidence
- Agentic research workflows
- MCP-based tool integration
- SQL tools with safety controls
- Human-in-the-loop approval gates
- Source-level citations and provenance
- Evaluation datasets and regression tests
- Security and auditability
- Containerized deployment

## Repository layout

```
backend/   Python/FastAPI application
frontend/  Web application
docs/      Architecture, security and product documentation
evals/     Evaluation datasets and evaluation code
infra/     Deployment and infrastructure configuration
tests/     Cross-component tests
```

## Development status

Verity is being built incrementally. The first milestone establishes the repository, backend API, testing, configuration, and deployment foundations before adding retrieval, multimodal processing, agents, MCP, SQL, approvals, and evaluations.

## Local development

The backend virtual environment can live inside `backend/.venv`. From the repository root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
cd ..
python -m pip install -e ".[dev]"
python -m uvicorn app.main:app --reload
```

API documentation:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

## Security

Never commit real API keys, passwords, database credentials, tokens, or private documents. Use `.env` locally and keep secrets out of Git.

## License

MIT

## Research Workspace

Verity now includes a simple browser workspace for the ingestion pipeline.

Start the API:

```bash
python -m pip install -e ".[dev]"
python -m uvicorn app.main:app --reload
```

Open:

**http://localhost:8000/workspace/**

You can upload a PDF, TXT, Markdown, CSV, JSON, or HTML document and immediately inspect its extracted metadata and evidence chunks.

FastAPI's `UploadFile` is used for file uploads because it provides a file-like interface and avoids loading every upload into a plain bytes parameter. citeturn0search0turn0search1
