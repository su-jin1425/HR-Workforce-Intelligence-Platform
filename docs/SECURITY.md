# Security

## Confidential Information Policy

Do not commit or upload:

- Microsoft 365 credentials
- Azure API keys
- Tenant IDs
- Access tokens
- Connection strings
- Employee PII
- Customer data
- Confidential company documents
- Internal HR processes

The repository uses synthetic seed data only.

## Authentication and Authorization

The production design uses Microsoft Entra ID with OAuth 2.0 authorization code flow for the Microsoft 365 Copilot API plugin.

Current implementation:

- `appPackage/apiSpecificationFile/openapi.yaml` defines OAuth 2.0.
- `appPackage/hr-workforce-plugin.json` uses an OAuth plugin vault placeholder.
- `backend/app/security/auth.py` has a local development auth bypass and JWT validation path.

Required production hardening:

- Validate Entra-issued JWTs against tenant signing keys.
- Enforce audience and issuer checks.
- Map Entra groups or app roles to HR roles.
- Add per-endpoint authorization policies.
- Enable `REQUIRE_PLUGIN_AUTH=true`.

## AI Safety Controls

The declarative agent instructions require:

- Aggregate analysis by default.
- No confidential employee data exposure.
- No employment-impacting decisions without human HR review.
- Refusal for protected-class, legal, medical, or unsafe individual decision requests.
- Clear distinction between synthetic, tenant-owned, and unavailable data.

## Auditability

The data model includes `AuditEvent` and `ReportingLog`. Report requests are persisted with request parameters and requester identity. Future work should add audit events for every read/write plugin invocation.

## Dependency and Secret Scanning

Recommended CI gates:

- Dependency vulnerability scan
- Secret scan
- Static analysis
- Manifest validation
- API contract validation
- Unit and integration tests
