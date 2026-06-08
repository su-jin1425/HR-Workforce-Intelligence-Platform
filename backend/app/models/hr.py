from datetime import UTC, date, datetime
from enum import StrEnum
from uuid import uuid4

from sqlalchemy import Date, DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Role(StrEnum):
    HR_ADMIN = "hr_admin"
    MANAGER = "manager"
    ANALYST = "analyst"
    VIEWER = "viewer"


class AttendanceStatus(StrEnum):
    PRESENT = "present"
    ABSENT = "absent"
    LEAVE = "leave"
    REMOTE = "remote"


def new_id() -> str:
    return str(uuid4())


def utc_now() -> datetime:
    return datetime.now(UTC)


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.VIEWER, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    employee_name: Mapped[str] = mapped_column(String(180), nullable=False)
    department: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    designation: Mapped[str] = mapped_column(String(140), nullable=False)
    joining_date: Mapped[date] = mapped_column(Date, nullable=False)
    employment_status: Mapped[str] = mapped_column(String(40), default="active", index=True)

    attendance_records: Mapped[list["AttendanceRecord"]] = relationship(back_populates="employee")
    performance_metrics: Mapped[list["PerformanceMetric"]] = relationship(back_populates="employee")
    predictive_scores: Mapped[list["PredictiveScore"]] = relationship(back_populates="employee")


class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    employee_id: Mapped[str] = mapped_column(ForeignKey("employees.id"), nullable=False, index=True)
    attendance_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    check_in_time: Mapped[str | None] = mapped_column(String(8))
    check_out_time: Mapped[str | None] = mapped_column(String(8))
    attendance_status: Mapped[AttendanceStatus] = mapped_column(Enum(AttendanceStatus), nullable=False)

    employee: Mapped[Employee] = relationship(back_populates="attendance_records")


class PerformanceMetric(Base):
    __tablename__ = "performance_metrics"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    employee_id: Mapped[str] = mapped_column(ForeignKey("employees.id"), nullable=False, index=True)
    productivity_score: Mapped[float] = mapped_column(Float, nullable=False)
    performance_rating: Mapped[float] = mapped_column(Float, nullable=False)
    review_period: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    employee: Mapped[Employee] = relationship(back_populates="performance_metrics")


class WorkforceAnalyticsSnapshot(Base):
    __tablename__ = "workforce_analytics"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    department: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    employee_count: Mapped[int] = mapped_column(nullable=False)
    retention_rate: Mapped[float] = mapped_column(Float, nullable=False)
    engagement_score: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class PredictiveScore(Base):
    __tablename__ = "predictive_scores"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    employee_id: Mapped[str] = mapped_column(ForeignKey("employees.id"), nullable=False, index=True)
    attrition_risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    productivity_prediction: Mapped[float] = mapped_column(Float, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    employee: Mapped[Employee] = relationship(back_populates="predictive_scores")


class ReportingLog(Base):
    __tablename__ = "reporting_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    report_type: Mapped[str] = mapped_column(String(80), nullable=False)
    generated_by: Mapped[str] = mapped_column(String(255), nullable=False)
    parameters: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    actor_id: Mapped[str] = mapped_column(String(255), nullable=False)
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(120), nullable=False)
    resource_id: Mapped[str | None] = mapped_column(String(255))
    metadata_json: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
