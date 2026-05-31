from contextlib import asynccontextmanager

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import API_PREFIX
from app.core.dependencies import get_container
from app.routers import dataset_router, exploration_router, models_router, prediction_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_container().load()
    yield


app = FastAPI(
    title="FraudShield API",
    description="Backend API for credit card fraud analysis and prediction.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dataset_router.router, prefix=API_PREFIX)
app.include_router(exploration_router.router, prefix=API_PREFIX)
app.include_router(prediction_router.router, prefix=API_PREFIX)
app.include_router(models_router.router, prefix=API_PREFIX)


@app.get(f"{API_PREFIX}/health", tags=["health"])
def health(response: Response) -> dict:
    status_payload = get_container().health()
    if status_payload["status"] != "healthy":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return status_payload


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {"message": "FraudShield API", "docs": "/docs"}

