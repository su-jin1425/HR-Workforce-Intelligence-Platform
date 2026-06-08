from datetime import date, timedelta

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.hr import AttendanceRecord, Employee, PerformanceMetric, PredictiveScore
from app.schemas.hr import AttendanceCreate, EmployeeCreate, PerformanceCreate


class WorkforceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_employee(self, payload: EmployeeCreate) -> Employee:
        employee = Employee(**payload.model_dump())
        self.session.add(employee)
        await self.session.commit()
        await self.session.refresh(employee)
        return employee

    async def list_employees(self, department: str | None = None) -> list[Employee]:
        query: Select[tuple[Employee]] = select(Employee).options(
            selectinload(Employee.attendance_records),
            selectinload(Employee.performance_metrics),
            selectinload(Employee.predictive_scores),
        )
        if department:
            query = query.where(Employee.department == department)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_employee(self, employee_id: str) -> Employee | None:
        result = await self.session.execute(
            select(Employee)
            .options(
                selectinload(Employee.attendance_records),
                selectinload(Employee.performance_metrics),
                selectinload(Employee.predictive_scores),
            )
            .where(Employee.id == employee_id)
        )
        return result.scalar_one_or_none()

    async def record_attendance(self, payload: AttendanceCreate) -> AttendanceRecord:
        record = AttendanceRecord(**payload.model_dump())
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def record_performance(self, payload: PerformanceCreate) -> PerformanceMetric:
        metric = PerformanceMetric(**payload.model_dump())
        self.session.add(metric)
        await self.session.commit()
        await self.session.refresh(metric)
        return metric

    async def upsert_prediction(
        self,
        employee_id: str,
        attrition_risk_score: float,
        productivity_prediction: float,
    ) -> PredictiveScore:
        score = PredictiveScore(
            employee_id=employee_id,
            attrition_risk_score=attrition_risk_score,
            productivity_prediction=productivity_prediction,
        )
        self.session.add(score)
        await self.session.commit()
        await self.session.refresh(score)
        return score

    async def seed_demo_data(self) -> None:
        existing = await self.list_employees()
        if existing:
            return

        employees = [
            EmployeeCreate(
                employee_name="Avery Patel",
                department="People Operations",
                designation="HR Business Partner",
                joining_date=date.today() - timedelta(days=760),
            ),
            EmployeeCreate(
                employee_name="Jordan Kim",
                department="Sales",
                designation="Enterprise Account Executive",
                joining_date=date.today() - timedelta(days=420),
            ),
            EmployeeCreate(
                employee_name="Mira Shah",
                department="Engineering",
                designation="Senior Platform Engineer",
                joining_date=date.today() - timedelta(days=1120),
            ),
            EmployeeCreate(
                employee_name="Noah Williams",
                department="Support",
                designation="Customer Success Manager",
                joining_date=date.today() - timedelta(days=240),
            ),
        ]
        created = [await self.create_employee(employee) for employee in employees]

        for index, employee in enumerate(created):
            for day in range(0, 20):
                status = "present"
                if employee.department == "Support" and day in {3, 9, 14}:
                    status = "absent"
                if employee.department == "Sales" and day in {7, 15}:
                    status = "remote"
                await self.record_attendance(
                    AttendanceCreate(
                        employee_id=employee.id,
                        attendance_date=date.today() - timedelta(days=day),
                        check_in_time="09:00" if status != "absent" else None,
                        check_out_time="17:30" if status != "absent" else None,
                        attendance_status=status,
                    )
                )
            await self.record_performance(
                PerformanceCreate(
                    employee_id=employee.id,
                    productivity_score=78 + (index * 4),
                    performance_rating=3.6 + (index * 0.2),
                    review_period="2026-Q2",
                )
            )
