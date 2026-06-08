from uuid import uuid4

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.hr import ReportingLog
from app.schemas.hr import ReportJob, ReportRequest
from app.security.auth import require_api_principal

router = APIRouter(dependencies=[Depends(require_api_principal)])


@router.post("/generate", response_model=ReportJob, status_code=status.HTTP_202_ACCEPTED)
async def generate_report(
    payload: ReportRequest,
    session: AsyncSession = Depends(get_session),
) -> ReportJob:
    report_id = str(uuid4())
    session.add(
        ReportingLog(
            id=report_id,
            report_type=payload.report_type,
            generated_by=str(payload.requested_by),
            parameters=payload.model_dump_json(),
        )
    )
    await session.commit()
    return ReportJob(
        report_id=report_id,
        status="queued",
        message="Report generation request accepted for asynchronous processing.",
    )


@router.get("")
async def list_reports() -> dict[str, str]:
    return {"status": "report listing endpoint reserved for paginated audit-safe report metadata"}
