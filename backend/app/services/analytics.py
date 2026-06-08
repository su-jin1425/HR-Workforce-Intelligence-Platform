from collections import defaultdict
from datetime import UTC, datetime

from app.models.hr import Employee
from app.schemas.hr import DepartmentKpi, WorkforceOverview


class WorkforceAnalyticsService:
    def build_overview(self, employees: list[Employee]) -> WorkforceOverview:
        active = [employee for employee in employees if employee.employment_status == "active"]
        departments = sorted({employee.department for employee in employees})
        department_kpis = [self._department_kpi(department, employees) for department in departments]

        attendance_rate = self._attendance_rate(employees)
        average_productivity = self._average_productivity(employees)
        retention_rate = round((len(active) / len(employees)) * 100, 2) if employees else 0.0
        high_risk_count = sum(1 for employee in employees if self._latest_attrition(employee) >= 0.7)

        return WorkforceOverview(
            as_of=datetime.now(UTC),
            employee_count=len(employees),
            active_employee_count=len(active),
            retention_rate=retention_rate,
            average_productivity=average_productivity,
            attendance_rate=attendance_rate,
            high_risk_employee_count=high_risk_count,
            departments=department_kpis,
            recommended_actions=self._recommend_actions(department_kpis, high_risk_count),
        )

    def _department_kpi(self, department: str, employees: list[Employee]) -> DepartmentKpi:
        scoped = [employee for employee in employees if employee.department == department]
        active = [employee for employee in scoped if employee.employment_status == "active"]
        retention_rate = round((len(active) / len(scoped)) * 100, 2) if scoped else 0.0
        productivity = self._average_productivity(scoped)
        attendance = self._attendance_rate(scoped)
        engagement = round((productivity * 0.55) + (attendance * 0.45), 2)
        risk_band = "high" if engagement < 70 else "medium" if engagement < 82 else "low"
        return DepartmentKpi(
            department=department,
            employee_count=len(scoped),
            active_count=len(active),
            retention_rate=retention_rate,
            average_productivity=productivity,
            attendance_rate=attendance,
            engagement_score=engagement,
            risk_band=risk_band,
        )

    def _average_productivity(self, employees: list[Employee]) -> float:
        scores: list[float] = []
        for employee in employees:
            if employee.performance_metrics:
                scores.append(employee.performance_metrics[-1].productivity_score)
        return round(sum(scores) / len(scores), 2) if scores else 0.0

    def _attendance_rate(self, employees: list[Employee]) -> float:
        total = present = 0
        for employee in employees:
            for record in employee.attendance_records:
                total += 1
                if record.attendance_status.value in {"present", "remote"}:
                    present += 1
        return round((present / total) * 100, 2) if total else 0.0

    def _latest_attrition(self, employee: Employee) -> float:
        if not employee.predictive_scores:
            return 0.0
        return employee.predictive_scores[-1].attrition_risk_score

    def _recommend_actions(self, departments: list[DepartmentKpi], high_risk_count: int) -> list[str]:
        actions: list[str] = []
        weak_departments = [dept.department for dept in departments if dept.risk_band == "high"]
        if weak_departments:
            actions.append(
                "Schedule manager review for departments below workforce health threshold: "
                + ", ".join(weak_departments)
            )
        if high_risk_count:
            actions.append(f"Review retention plans for {high_risk_count} high-risk employee profiles.")
        if not actions:
            actions.append("Maintain current cadence and monitor weekly trend changes.")
        return actions

    def build_department_trends(self, employees: list[Employee]) -> dict[str, dict[str, float]]:
        grouped: dict[str, list[Employee]] = defaultdict(list)
        for employee in employees:
            grouped[employee.department].append(employee)
        return {
            department: {
                "average_productivity": self._average_productivity(scoped),
                "attendance_rate": self._attendance_rate(scoped),
            }
            for department, scoped in grouped.items()
        }
