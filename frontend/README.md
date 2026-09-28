# Verity Research Workspace

The frontend is intentionally simple for the first version: plain HTML, CSS, and JavaScript.

It is served by the FastAPI application at:

**http://localhost:8000/workspace/**

## Local development

From the repository root:

```bash
python -m pip install -e ".[dev]"
python -m uvicorn app.main:app --reload
```

Then open the workspace URL above.

The first UI supports:

- Document upload
- PDF, TXT, Markdown, CSV, JSON, and HTML ingestion
- Extracted document metadata
- Evidence chunk preview
- Clean responsive research workspace

The UI will grow as retrieval, citations, agent workflows, approvals, and evaluation features are added.
