from pydantic import BaseModel


class DocumentChunk(BaseModel):
    id: str
    document_id: str
    text: str
    chunk_index: int
    source: str


class IngestedDocument(BaseModel):
    id: str
    filename: str
    content_type: str | None
    size_bytes: int
    character_count: int
    chunk_count: int
    status: str
    chunks: list[DocumentChunk]
