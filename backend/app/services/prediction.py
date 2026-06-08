from app.models.hr import Employee
from app.schemas.hr import PredictionRead


class PredictionService:
    def score_employees(self, employees: list[Employee]) -> list[PredictionRead]:
        return [self.score_employee(employee) for employee in employees]

    def score_employee(self, employee: Employee) -> PredictionRead:
        attendance_rate = self._attendance_rate(employee)
        productivity = self._latest_productivity(employee)
        tenure_months = self._tenure_months(employee)

        risk = 0.15
        evidence: list[str] = []
        if attendance_rate < 85:
            risk += 0.28
            evidence.append("Attendance is below the 85 percent review threshold.")
        if productivity < 72:
            risk += 0.25
            evidence.append("Productivity trend is below the department intervention threshold.")
        if tenure_months < 9:
            risk += 0.12
            evidence.append("Early-tenure employees require manager check-ins.")
        if not evidence:
            evidence.append("No material risk indicator crossed an alert threshold.")

        risk = min(round(risk, 2), 0.95)
        risk_band = "high" if risk >= 0.7 else "medium" if risk >= 0.4 else "low"
        productivity_prediction = round((productivity * 0.72) + (attendance_rate * 0.28), 2)

        return PredictionRead(
            employee_id=employee.id,
            employee_name=employee.employee_name,
            department=employee.department,
            attrition_risk_score=risk,
            productivity_prediction=productivity_prediction,
            risk_band=risk_band,
            evidence=evidence,
        )

    def _attendance_rate(self, employee: Employee) -> float:
        if not employee.attendance_records:
            return 100.0
        healthy = [
            record
            for record in employee.attendance_records
            if record.attendance_status.value in {"present", "remote"}
        ]
        return round((len(healthy) / len(employee.attendance_records)) * 100, 2)

    def _latest_productivity(self, employee: Employee) -> float:
        if not employee.performance_metrics:
            return 75.0
        return employee.performance_metrics[-1].productivity_score

    def _tenure_months(self, employee: Employee) -> int:
        from datetime import date

        delta_days = (date.today() - employee.joining_date).days
        return max(delta_days // 30, 0)
