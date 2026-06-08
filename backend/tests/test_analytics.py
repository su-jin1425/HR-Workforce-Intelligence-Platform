from datetime import date, timedelta

from app.models.hr import AttendanceRecord, AttendanceStatus, Employee, PerformanceMetric
from app.services.analytics import WorkforceAnalyticsService
from app.services.prediction import PredictionService


def test_overview_computes_core_kpis() -> None:
    employee = Employee(
        id="emp-1",
        employee_name="Test User",
        department="Engineering",
        designation="Engineer",
        joining_date=date.today() - timedelta(days=400),
        employment_status="active",
    )
    employee.attendance_records = [
        AttendanceRecord(attendance_status=AttendanceStatus.PRESENT, attendance_date=date.today()),
        AttendanceRecord(attendance_status=AttendanceStatus.ABSENT, attendance_date=date.today()),
    ]
    employee.performance_metrics = [
        PerformanceMetric(productivity_score=88, performance_rating=4.2, review_period="2026-Q2")
    ]

    overview = WorkforceAnalyticsService().build_overview([employee])

    assert overview.employee_count == 1
    assert overview.attendance_rate == 50.0
    assert overview.average_productivity == 88.0


def test_prediction_explains_high_absence_risk() -> None:
    employee = Employee(
        id="emp-1",
        employee_name="Test User",
        department="Support",
        designation="Manager",
        joining_date=date.today() - timedelta(days=90),
        employment_status="active",
    )
    employee.attendance_records = [
        AttendanceRecord(attendance_status=AttendanceStatus.ABSENT, attendance_date=date.today())
    ]
    employee.performance_metrics = [
        PerformanceMetric(productivity_score=65, performance_rating=3.1, review_period="2026-Q2")
    ]

    prediction = PredictionService().score_employee(employee)

    assert prediction.risk_band in {"medium", "high"}
    assert prediction.evidence
