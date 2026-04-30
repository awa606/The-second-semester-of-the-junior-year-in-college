from fastapi import APIRouter

from app.schemas import HealthResponse
from app.version import APP_VERSION

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", version=APP_VERSION)
