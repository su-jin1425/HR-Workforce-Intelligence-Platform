from fastapi import APIRouter

from app.api.routes import analytics, employees, health, m365_plugin, predictions, reports

api_router = APIRouter()
api_router.include_router(health.router, tags=["monitoring"])
api_router.include_router(employees.router, prefix="/employees", tags=["employees"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["predictions"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(m365_plugin.router, prefix="/copilot", tags=["microsoft-365-copilot"])
