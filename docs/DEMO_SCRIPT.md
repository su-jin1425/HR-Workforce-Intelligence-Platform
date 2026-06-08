# Demo Script

## Setup

1. Start the stack with `docker compose up --build`.
2. Open the dashboard at `http://localhost:3000`.
3. Seed data by calling `/api/v1/analytics/overview?seed_demo_data=true`.
4. Package and sideload the Microsoft 365 app package after replacing placeholders.

## Demo Flow

1. Show the Microsoft 365 app package files.
2. Open Microsoft 365 Copilot Chat and select Workforce IQ.
3. Ask: `Show the current workforce health overview and explain the highest-risk department.`
4. Show the backend API action response in Swagger.
5. Open the dashboard and show department risk bands.
6. Ask: `Based on my recent HR planning meetings and workforce analytics, draft a follow-up plan.`
7. Explain that Copilot supplies user-permitted Microsoft 365 work context while the API supplies HR analytics.
8. Show the security/disclaimer docs and confirm no confidential information is included.

## Key Message

Workforce IQ is a business-ready Microsoft 365 Copilot agent that brings governed HR analytics into the flow of work while preserving safety, auditability, and human review.
