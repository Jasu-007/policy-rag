from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.health import router as health_router
from app.core.config import get_settings
from app.api.v1.ingest import router as ingest_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Vector DB initialization / embedding warmup hooks go here
    print(f"Starting {settings.PROJECT_NAME} [{settings.ENVIRONMENT}]")
    yield
    # Teardown: Disconnect DB clients and clear in-memory caches
    print("Shutting down service gracefully")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json" if settings.DEBUG else None,
    docs_url=f"{settings.API_V1_PREFIX}/docs" if settings.DEBUG else None,
    lifespan=lifespan,
)

# Mount versioned API routes
app.include_router(health_router, prefix=settings.API_V1_PREFIX)
app.include_router(ingest_router, prefix=settings.API_V1_PREFIX)