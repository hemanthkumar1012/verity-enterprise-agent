from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.settings import settings

app = FastAPI(
    title=settings.app_name,
    description="Enterprise Multimodal Research & Action Agent",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "message": "Enterprise Multimodal Research & Action Agent",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "verity",
        "version": "0.1.0",
    }
