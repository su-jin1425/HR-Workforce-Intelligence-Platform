from app.models.hr import Employee
from app.schemas.hr import AgentContextResponse
from app.services.analytics import WorkforceAnalyticsService


class AgentContextService:
    def __init__(self, analytics: WorkforceAnalyticsService):
        self.analytics = analytics

    def build_context_response(
        self,
        user_prompt: str,
        employees: list[Employee],
        include_actions: bool,
    ) -> AgentContextResponse:
        overview = self.analytics.build_overview(employees)
        if not include_actions:
            overview.recommended_actions = []

        answer = (
            f"{overview.employee_count} employees are represented across "
            f"{len(overview.departments)} departments. Retention is "
            f"{overview.retention_rate}% and attendance health is "
            f"{overview.attendance_rate}%."
        )
        citations = [
            "HR Workforce Intelligence API: /api/v1/analytics/overview",
            "HR Workforce Intelligence API: /api/v1/predictions/attrition",
        ]
        safety_notes = [
            "Only synthetic sample data or tenant-owned HR data should be used.",
            "Do not upload confidential employee records into the public repository or demo video.",
            "Human HR review is required before employment-impacting decisions.",
        ]
        return AgentContextResponse(
            answer_brief=answer,
            overview=overview,
            citations=citations,
            safety_notes=safety_notes,
        )
