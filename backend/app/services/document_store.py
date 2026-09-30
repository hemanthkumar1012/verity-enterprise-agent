from app.models.document import IngestedDocument


_documents: dict[str, IngestedDocument] = {}


def save_document(document: IngestedDocument) -> IngestedDocument:
    _documents[document.id] = document
    return document


def list_chunks() -> list:
    chunks = []
    for document in _documents.values():
        chunks.extend(document.chunks)
    return chunks


def clear_store() -> None:
    _documents.clear()
