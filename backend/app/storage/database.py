import os
from contextlib import contextmanager
from typing import Iterator

import psycopg


DATABASE_URL = os.getenv("DATABASE_URL", "").strip()


@contextmanager
def connection() -> Iterator[psycopg.Connection]:
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured.")
    with psycopg.connect(DATABASE_URL) as conn:
        yield conn


def database_enabled() -> bool:
    return bool(DATABASE_URL)


def initialize_database() -> None:
    if not DATABASE_URL:
        return

    with connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                content_type TEXT,
                size_bytes BIGINT NOT NULL,
                character_count INTEGER NOT NULL,
                chunk_count INTEGER NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS document_chunks (
                id TEXT PRIMARY KEY,
                document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
                chunk_index INTEGER NOT NULL,
                source TEXT NOT NULL,
                text TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS document_chunks_document_id_idx
                ON document_chunks(document_id);

            CREATE INDEX IF NOT EXISTS document_chunks_search_idx
                ON document_chunks
                USING GIN (to_tsvector('english', text));
            """
        )
        conn.commit()
