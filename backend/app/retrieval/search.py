import re
from dataclasses import dataclass

from app.models.document import DocumentChunk

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "in", "is", "it", "of", "on", "or", "that", "the", "to", "was", "with",
}


@dataclass(frozen=True)
class SearchResult:
    document_id: str
    chunk_id: str
    source: str
    chunk_index: int
    text: str
    score: float


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in TOKEN_PATTERN.findall(text.lower())
        if token not in STOP_WORDS
    }


def score_chunk(query: str, chunk: DocumentChunk) -> float:
    query_tokens = _tokens(query)
    chunk_tokens = _tokens(chunk.text)
    if not query_tokens or not chunk_tokens:
        return 0.0
    return len(query_tokens & chunk_tokens) / len(query_tokens)


def search_chunks(query: str, chunks: list[DocumentChunk], limit: int = 5) -> list[SearchResult]:
    if not query.strip():
        return []

    ranked = []
    for chunk in chunks:
        score = score_chunk(query, chunk)
        if score > 0:
            ranked.append(
                SearchResult(
                    document_id=chunk.document_id,
                    chunk_id=chunk.id,
                    source=chunk.source,
                    chunk_index=chunk.chunk_index,
                    text=chunk.text,
                    score=round(score, 4),
                )
            )

    ranked.sort(key=lambda result: (-result.score, result.source, result.chunk_index))
    return ranked[:limit]
