from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.document import IngestedDocument
from app.services.ingestion import ingest_document


router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.get("/formats")
def supported_formats() -> dict[str, list[str]]:
    return {
        "extensions": [".pdf", ".txt", ".md", ".csv", ".json", ".html"],
        "max_file_size_mb": 10,
    }


@router.post("/ingest", response_model=IngestedDocument)
async def ingest(
    file: Annotated[UploadFile, File(description="Document to ingest")],
) -> IngestedDocument:
    try:
        content = await file.read()
        return ingest_document(file.filename or "", file.content_type, content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        await file.close()
