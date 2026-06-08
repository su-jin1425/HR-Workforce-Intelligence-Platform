from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.repositories.workforce_repository import WorkforceRepository
from app.schemas.hr import PredictionRead
from app.security.auth import require_api_principal
from app.services.prediction import PredictionService

router = APIRouter(dependencies=[Depends(require_api_principal)])


@router.get("/attrition", response_model=list[PredictionRead])
async def attrition_predictions(
    department: str | None = None,
    session: AsyncSession = Depends(get_session),
) -> list[PredictionRead]:
    employees = await WorkforceRepository(session).list_employees(department)
    return PredictionService().score_employees(employees)


@router.get("/productivity", response_model=list[PredictionRead])
async def productivity_predictions(
    department: str | None = None,
    session: AsyncSession = Depends(get_session),
) -> list[PredictionRead]:
    employees = await WorkforceRepository(session).list_employees(department)
    return PredictionService().score_employees(employees)
