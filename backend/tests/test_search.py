from app.models.document import DocumentChunk
from app.retrieval.search import search_chunks, score_chunk


def make_chunk(text: str, index: int = 0) -> DocumentChunk:
    return DocumentChunk(
        id=f"chunk-{index}",
        document_id="doc-1",
        text=text,
        chunk_index=index,
        source="research.txt",
    )


def test_score_chunk_rewards_query_overlap():
    chunk = make_chunk("Verity uses evidence retrieval for grounded research.")
    assert score_chunk("evidence retrieval", chunk) == 1.0


def test_search_returns_best_matching_chunk_first():
    chunks = [
        make_chunk("The platform stores customer invoices.", 0),
        make_chunk("Verity retrieves evidence for grounded research answers.", 1),
    ]
    results = search_chunks("evidence research", chunks)

    assert len(results) == 1
    assert results[0].chunk_index == 1
    assert results[0].score == 1.0


def test_search_returns_empty_for_blank_query():
    assert search_chunks("   ", [make_chunk("anything")]) == []
