# Architecture

## System Context

Workforce IQ has two user experiences:

1. Microsoft 365 Copilot Chat declarative agent for conversational workforce intelligence.
2. Web dashboard for HR analysts and operators.

The Copilot agent does not store Microsoft 365 content. It uses Microsoft 365 Copilot work context available to the signed-in user and calls the HR Workforce Intelligence API for structured aggregate analytics.

## Runtime Components

- Microsoft 365 app package: Defines the app and Copilot agent.
- Declarative agent: Defines instructions, safety boundaries, conversation starters, and actions.
- API plugin: Exposes OpenAPI actions to Microsoft 365 Copilot.
- FastAPI backend: Hosts workforce analytics, prediction, report, and monitoring endpoints.
- PostgreSQL: Stores workforce records, analytics snapshots, predictions, reports, and audit events.
- Redis: Reserved for caching, queue coordination, and session workflows.
- Next.js dashboard: Presents operational KPIs and recommendations.
- Prometheus and Grafana: Collect and visualize API telemetry.

## Data Flow

1. User asks Workforce IQ a question in Microsoft 365 Copilot Chat.
2. Copilot uses user-permitted Microsoft 365 work context when relevant.
3. Copilot invokes an API plugin operation from `openapi.yaml`.
4. FastAPI validates the request and applies authentication policy.
5. Repository and service layers compute aggregate workforce intelligence.
6. The API returns concise, citation-friendly JSON.
7. Copilot composes the final answer with safety constraints from the agent manifest.

## Domain Boundaries

- Workforce domain: employees, attendance, performance, retention, department KPIs.
- Prediction domain: attrition risk and productivity forecasts.
- Reporting domain: auditable report request workflow.
- Governance domain: authentication, authorization, audit events, data handling policy.
- Observability domain: health and Prometheus metrics.

## Security Architecture

- Microsoft Entra ID is the intended production identity provider.
- OAuth placeholders are included in the plugin and OpenAPI manifests.
- Local development can disable plugin auth through `REQUIRE_PLUGIN_AUTH=false`.
- Production should enable `REQUIRE_PLUGIN_AUTH=true` and validate Entra-issued access tokens.
- Secrets are excluded from source control.

## Scalability Notes

- API is stateless and can scale horizontally.
- PostgreSQL is the system of record.
- Redis supports cache and queue workloads.
- Report generation is modeled as asynchronous.
- Prometheus metrics track latency and request counts.

## Known Gaps

- Alembic migrations are not yet generated.
- Celery worker implementation is not yet wired to report generation.
- Entra token validation currently uses local JWT validation in code and requires production hardening.
- MCP Apps bonus capability is not yet implemented.
- Direct Work IQ APIs are not implemented because the GA date is after the hackathon deadline.
