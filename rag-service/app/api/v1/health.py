from fastapi import APIRouter, Depends
from app.core.config import Settings, get_settings

router = APIRouter()


@router.get("/health", tags=["System"])
async def check_health(settings: Settings = Depends(get_settings)):
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "service": settings.PROJECT_NAME,
        "debug": settings.DEBUG,
    }