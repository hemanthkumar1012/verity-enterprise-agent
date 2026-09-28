from app.services.ingestion import chunk_text, extract_text, ingest_document


def test_extract_text_from_markdown():
    content = b"# Verity\n\nEvidence first."
    assert extract_text("notes.md", content) == "# Verity\nEvidence first."


def test_chunk_text_returns_small_input_as_one_chunk():
    chunks = chunk_text("hello world")
    assert chunks == ["hello world"]


def test_ingest_document_creates_metadata_and_chunks():
    document = ingest_document(
        "research.txt",
        "text/plain",
        b"Verity helps researchers work with evidence.",
    )

    assert document.filename == "research.txt"
    assert document.status == "ready"
    assert document.chunk_count == 1
    assert document.chunks[0].document_id == document.id


def test_document_ingest_api():
    from fastapi.testclient import TestClient

    from app.main import app

    client = TestClient(app)
    response = client.post(
        "/api/documents/ingest",
        files={"file": ("notes.txt", b"API evidence test.", "text/plain")},
    )

    assert response.status_code == 200
    assert response.json()["filename"] == "notes.txt"
    assert response.json()["chunk_count"] == 1
