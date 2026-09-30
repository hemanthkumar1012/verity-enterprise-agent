from app.models.document import DocumentChunk, IngestedDocument
from app.retrieval.search import SearchResult
from app.storage.database import connection, database_enabled


_documents: dict[str, IngestedDocument] = {}


def save_document(document: IngestedDocument) -> IngestedDocument:
    if not database_enabled():
        _documents[document.id] = document
        return document

    with connection() as conn:
        conn.execute(
            """
            INSERT INTO documents
                (id, filename, content_type, size_bytes, character_count, chunk_count, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """,
            (
                document.id,
                document.filename,
                document.content_type,
                document.size_bytes,
                document.character_count,
                document.chunk_count,
                document.status,
            ),
        )
        conn.executemany(
            """
            INSERT INTO document_chunks (id, document_id, chunk_index, source, text)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """,
            [
                (chunk.id, chunk.document_id, chunk.chunk_index, chunk.source, chunk.text)
                for chunk in document.chunks
            ],
        )
        conn.commit()

    return document


def list_chunks() -> list[DocumentChunk]:
    if not database_enabled():
        chunks: list[DocumentChunk] = []
        for document in _documents.values():
            chunks.extend(document.chunks)
        return chunks

    with connection() as conn:
        rows = conn.execute(
            """
            SELECT id, document_id, text, chunk_index, source
            FROM document_chunks
            ORDER BY document_id, chunk_index
            """
        ).fetchall()

    return [
        DocumentChunk(
            id=row[0],
            document_id=row[1],
            text=row[2],
            chunk_index=row[3],
            source=row[4],
        )
        for row in rows
    ]


def search_chunks(query: str, limit: int) -> list[SearchResult]:
    if not database_enabled():
        from app.retrieval.search import search_chunks as memory_search

        return memory_search(query, list_chunks(), limit)

    with connection() as conn:
        rows = conn.execute(
            """
            SELECT id, document_id, text, chunk_index, source,
                   ts_rank_cd(to_tsvector('english', text), plainto_tsquery('english', %s)) AS score
            FROM document_chunks
            WHERE to_tsvector('english', text) @@ plainto_tsquery('english', %s)
            ORDER BY score DESC, source, chunk_index
            LIMIT %s
            """,
            (query, query, limit),
        ).fetchall()

    return [
        SearchResult(
            document_id=row[1],
            chunk_id=row[0],
            source=row[4],
            chunk_index=row[3],
            text=row[2],
            score=round(float(row[5]), 4),
        )
        for row in rows
    ]


def clear_store() -> None:
    if database_enabled():
        with connection() as conn:
            conn.execute("TRUNCATE TABLE document_chunks, documents")
            conn.commit()
        return
    _documents.clear()
