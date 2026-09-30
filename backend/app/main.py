from pathlib import Path
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes.documents import router as documents_router
from app.api.routes.search import router as search_router
from app.settings import settings
from app.storage.database import initialize_database


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIR = PROJECT_ROOT / "frontend"

app = FastAPI(
    title=settings.app_name,
    description="Enterprise Multimodal Research & Action Agent",
    version="0.1.0",
)

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://localhost:5500",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_database()

app.include_router(documents_router)
app.include_router(search_router)

if FRONTEND_DIR.exists():
    app.mount("/workspace", StaticFiles(directory=FRONTEND_DIR, html=True), name="workspace")


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "message": "Enterprise Multimodal Research & Action Agent",
        "workspace": "/workspace",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "verity",
        "version": "0.1.0",
    }


@app.get("/api/status")
def api_status() -> dict[str, str]:
    return {
        "service": "verity-api",
        "status": "online",
        "message": "Research API is ready.",
    }
