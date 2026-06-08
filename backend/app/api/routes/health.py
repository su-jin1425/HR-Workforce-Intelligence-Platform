from fastapi import APIRouter

from app.monitoring.metrics import metrics_response

router = APIRouter()


@router.get("/monitoring/health")
async def health() -> dict[str, str]:
    return {"status": "healthy", "service": "hr-workforce-intelligence-api"}


@router.get("/monitoring/metrics")
async def metrics():
    return metrics_response()
