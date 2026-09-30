from typing import Annotated

from fastapi import APIRouter, Query

from app.retrieval.search import SearchResult
from app.services.document_store import search_chunks


router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("")
def search(
    q: Annotated[str, Query(min_length=1, max_length=200, description="Evidence search query")],
    limit: Annotated[int, Query(ge=1, le=20)] = 5,
) -> dict[str, object]:
    results = search_chunks(q, limit)
    return {
        "query": q,
        "count": len(results),
        "results": [_serialize_result(result) for result in results],
    }


def _serialize_result(result: SearchResult) -> dict[str, object]:
    return {
        "document_id": result.document_id,
        "chunk_id": result.chunk_id,
        "source": result.source,
        "chunk_index": result.chunk_index,
        "text": result.text,
        "score": result.score,
        "citation": f"{result.source} · chunk {result.chunk_index + 1}",
    }
