from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.repositories.workforce_repository import WorkforceRepository
from app.schemas.hr import AttendanceCreate, EmployeeCreate, EmployeeRead, PerformanceCreate
from app.security.auth import require_api_principal

router = APIRouter(dependencies=[Depends(require_api_principal)])


@router.post("", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
async def create_employee(
    payload: EmployeeCreate,
    session: AsyncSession = Depends(get_session),
) -> EmployeeRead:
    employee = await WorkforceRepository(session).create_employee(payload)
    return EmployeeRead.model_validate(employee)


@router.get("", response_model=list[EmployeeRead])
async def list_employees(
    department: str | None = None,
    session: AsyncSession = Depends(get_session),
) -> list[EmployeeRead]:
    employees = await WorkforceRepository(session).list_employees(department)
    return [EmployeeRead.model_validate(employee) for employee in employees]


@router.get("/{employee_id}", response_model=EmployeeRead)
async def get_employee(
    employee_id: str,
    session: AsyncSession = Depends(get_session),
) -> EmployeeRead:
    employee = await WorkforceRepository(session).get_employee(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return EmployeeRead.model_validate(employee)


@router.post("/attendance", status_code=status.HTTP_201_CREATED)
async def record_attendance(
    payload: AttendanceCreate,
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    await WorkforceRepository(session).record_attendance(payload)
    return {"status": "created"}


@router.post("/performance", status_code=status.HTTP_201_CREATED)
async def record_performance(
    payload: PerformanceCreate,
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    await WorkforceRepository(session).record_performance(payload)
    return {"status": "created"}
