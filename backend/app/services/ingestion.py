from io import BytesIO
from pathlib import Path
from uuid import uuid4

from pypdf import PdfReader

from app.models.document import DocumentChunk, IngestedDocument


MAX_FILE_SIZE = 10 * 1024 * 1024
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 150
SUPPORTED_EXTENSIONS = {".txt", ".md", ".csv", ".json", ".html"}


def _clean_text(text: str) -> str:
    lines = [line.strip() for line in text.replace("\r\n", "\n").split("\n")]
    return "\n".join(line for line in lines if line).strip()


def extract_text(filename: str, content: bytes) -> str:
    extension = Path(filename).suffix.lower()

    if extension == ".pdf":
        reader = PdfReader(BytesIO(content))
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        return _clean_text("\n".join(pages))

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            "Unsupported file type. Use PDF, TXT, Markdown, CSV, JSON, or HTML."
        )

    return _clean_text(content.decode("utf-8", errors="replace"))


def chunk_text(text: str) -> list[str]:
    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = max(end - CHUNK_OVERLAP, start + 1)

    return chunks


def ingest_document(
    filename: str,
    content_type: str | None,
    content: bytes,
) -> IngestedDocument:
    if not filename:
        raise ValueError("A filename is required.")

    if len(content) > MAX_FILE_SIZE:
        raise ValueError("File is too large. The maximum size is 10 MB.")

    text = extract_text(filename, content)
    document_id = str(uuid4())
    raw_chunks = chunk_text(text)

    chunks = [
        DocumentChunk(
            id=str(uuid4()),
            document_id=document_id,
            text=chunk,
            chunk_index=index,
            source=filename,
        )
        for index, chunk in enumerate(raw_chunks)
    ]

    return IngestedDocument(
        id=document_id,
        filename=filename,
        content_type=content_type,
        size_bytes=len(content),
        character_count=len(text),
        chunk_count=len(chunks),
        status="ready",
        chunks=chunks,
    )
