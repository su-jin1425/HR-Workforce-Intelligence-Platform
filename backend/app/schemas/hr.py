from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmployeeCreate(BaseModel):
    employee_name: str = Field(min_length=2, max_length=180)
    department: str = Field(min_length=2, max_length=120)
    designation: str = Field(min_length=2, max_length=140)
    joining_date: date
    employment_status: str = "active"


class EmployeeRead(EmployeeCreate):
    model_config = ConfigDict(from_attributes=True)

    id: str


class AttendanceCreate(BaseModel):
    employee_id: str
    attendance_date: date
    check_in_time: str | None = None
    check_out_time: str | None = None
    attendance_status: Literal["present", "absent", "leave", "remote"]


class PerformanceCreate(BaseModel):
    employee_id: str
    productivity_score: float = Field(ge=0, le=100)
    performance_rating: float = Field(ge=0, le=5)
    review_period: str


class DepartmentKpi(BaseModel):
    department: str
    employee_count: int
    active_count: int
    retention_rate: float
    average_productivity: float
    attendance_rate: float
    engagement_score: float
    risk_band: Literal["low", "medium", "high"]


class WorkforceOverview(BaseModel):
    summary_title: str = "Workforce intelligence overview"
    as_of: datetime
    employee_count: int
    active_employee_count: int
    retention_rate: float
    average_productivity: float
    attendance_rate: float
    high_risk_employee_count: int
    departments: list[DepartmentKpi]
    recommended_actions: list[str]
    data_classification: str = "Synthetic or tenant-owned HR data only"


class PredictionRead(BaseModel):
    employee_id: str
    employee_name: str
    department: str
    attrition_risk_score: float
    productivity_prediction: float
    risk_band: Literal["low", "medium", "high"]
    evidence: list[str]


class ReportRequest(BaseModel):
    report_type: Literal["executive_summary", "department_health", "attrition_risk"]
    department: str | None = None
    requested_by: EmailStr


class ReportJob(BaseModel):
    report_id: str
    status: Literal["queued", "running", "complete", "failed"]
    message: str


class AgentContextRequest(BaseModel):
    user_prompt: str = Field(min_length=3)
    department: str | None = None
    include_recommended_actions: bool = True


class AgentContextResponse(BaseModel):
    answer_brief: str
    overview: WorkforceOverview
    citations: list[str]
    safety_notes: list[str]
