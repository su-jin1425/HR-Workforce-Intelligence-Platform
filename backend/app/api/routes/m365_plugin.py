from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.repositories.workforce_repository import WorkforceRepository
from app.schemas.hr import AgentContextRequest, AgentContextResponse, WorkforceOverview
from app.security.auth import require_api_principal
from app.services.agent_context import AgentContextService
from app.services.analytics import WorkforceAnalyticsService

router = APIRouter(dependencies=[Depends(require_api_principal)])


@router.get("/workforce-overview", response_model=WorkforceOverview, operation_id="getWorkforceOverview")
async def get_workforce_overview(
    department: str | None = None,
    session: AsyncSession = Depends(get_session),
) -> WorkforceOverview:
    employees = await WorkforceRepository(session).list_employees(department)
    return WorkforceAnalyticsService().build_overview(employees)


@router.post("/agent-context", response_model=AgentContextResponse, operation_id="getAgentWorkforceContext")
async def get_agent_workforce_context(
    payload: AgentContextRequest,
    session: AsyncSession = Depends(get_session),
) -> AgentContextResponse:
    employees = await WorkforceRepository(session).list_employees(payload.department)
    service = AgentContextService(WorkforceAnalyticsService())
    return service.build_context_response(
        user_prompt=payload.user_prompt,
        employees=employees,
        include_actions=payload.include_recommended_actions,
    )
