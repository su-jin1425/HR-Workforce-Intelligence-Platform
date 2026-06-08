# HR Workforce Intelligence Platform

Workforce IQ is an Enterprise Agents project for the Agents League Hackathon. It is designed as a Microsoft 365 Copilot Chat declarative agent backed by an enterprise HR analytics platform.

The agent helps HR leaders, managers, and analysts ask workforce questions in Microsoft 365 Copilot Chat while using tenant-owned workforce data from a governed API. The implementation avoids confidential sample data and uses synthetic development data only.

## Hackathon Track

- Track: Enterprise Agents
- Required host: Microsoft 365 Copilot Chat
- Required IQ layer: Work IQ through the Microsoft 365 Copilot Chat agent experience, with the agent instructed to combine user-permitted Microsoft 365 work context with HR analytics actions
- Required agent artifact: `appPackage/manifest.json`
- Declarative agent artifact: `appPackage/declarativeAgent.json`
- API plugin artifact: `appPackage/hr-workforce-plugin.json`
- OpenAPI action contract: `appPackage/apiSpecificationFile/openapi.yaml`

Microsoft announced that Work IQ APIs are generally available on June 16, 2026, after the June 14, 2026 hackathon deadline. This project therefore integrates Work IQ through the Microsoft 365 Copilot Chat declarative agent context and keeps direct Work IQ API calls out of the deadline submission.

## What Is Implemented

- Microsoft 365 app package with declarative agent and API plugin manifests
- FastAPI backend with workforce overview, employee, attendance, prediction, report, and Copilot action endpoints
- SQLAlchemy data model for employees, attendance, performance, predictive scores, reports, and audit events
- Explainable attrition and productivity scoring service
- Next.js dashboard for operational workforce intelligence
- Docker Compose environment with PostgreSQL, Redis, Prometheus, Grafana, backend, and frontend
- Synthetic demo data seeding through the analytics endpoint
- Manifest validation script and unit tests for analytics logic

## Local Development

Copy environment defaults:

```bash
cp .env.example .env
```

Start the stack:

```bash
docker compose up --build
```

Open services:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- OpenAPI docs: http://localhost:8000/docs
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001

Seed demo data by opening:

```text
http://localhost:8000/api/v1/analytics/overview?seed_demo_data=true
```

## Validation

Run backend tests from the backend directory:

```bash
pytest
```

Run manifest structure checks from the repository root:

```bash
python scripts/validate_manifests.py
```

Run the baseline ML pipeline:

```bash
python ml/pipelines/attrition_baseline.py
```

## Microsoft 365 Copilot Sideloading Notes

1. Replace placeholders in `appPackage/manifest.json`, `appPackage/hr-workforce-plugin.json`, and `appPackage/apiSpecificationFile/openapi.yaml`.
2. Expose the backend over HTTPS with a development tunnel or deployed host.
3. Register the API in Microsoft Entra ID and configure the OAuth reference through Microsoft 365 Agents Toolkit.
4. Package and provision with Microsoft 365 Agents Toolkit.
5. Test in Microsoft 365 Copilot Chat at `https://m365.cloud.microsoft/chat`.

## Security Posture

- No credentials, tenant IDs, access tokens, employee PII, or real organizational data are included.
- `.gitignore` blocks common secret and local configuration files.
- API plugin OAuth placeholders are present for Microsoft Entra ID integration.
- The agent instructions require human HR review before employment-impacting decisions.
- Predictive outputs are explainable and treated as advisory decision support.

## Repository Map

```text
appPackage/                     Microsoft 365 app package files
backend/                        FastAPI workforce intelligence API
frontend/                       Next.js dashboard
infra/                          Prometheus and Grafana configuration
ml/                             Baseline ML pipeline code
scripts/                        Validation and packaging helpers
docs/                           Architecture, security, and hackathon evidence
```
