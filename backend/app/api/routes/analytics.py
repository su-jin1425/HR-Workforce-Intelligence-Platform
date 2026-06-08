from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.repositories.workforce_repository import WorkforceRepository
from app.schemas.hr import WorkforceOverview
from app.security.auth import require_api_principal
from app.services.analytics import WorkforceAnalyticsService

router = APIRouter(dependencies=[Depends(require_api_principal)])


@router.get("/overview", response_model=WorkforceOverview)
async def workforce_overview(
    department: str | None = None,
    seed_demo_data: bool = False,
    session: AsyncSession = Depends(get_session),
) -> WorkforceOverview:
    repository = WorkforceRepository(session)
    if seed_demo_data:
        await repository.seed_demo_data()
    employees = await repository.list_employees(department)
    return WorkforceAnalyticsService().build_overview(employees)


@router.get("/workforce")
async def workforce_trends(
    session: AsyncSession = Depends(get_session),
) -> dict[str, dict[str, float]]:
    employees = await WorkforceRepository(session).list_employees()
    return WorkforceAnalyticsService().build_department_trends(employees)
