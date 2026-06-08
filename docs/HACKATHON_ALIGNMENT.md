# Hackathon Alignment

This document maps the submission to the Agents League Enterprise Agents requirements.

## Required Items

| Requirement | Evidence in repository | Status |
| --- | --- | --- |
| Microsoft 365 Copilot Chat agent | `appPackage/manifest.json`, `appPackage/declarativeAgent.json` | Implemented as declarative agent package |
| Microsoft IQ integration | `appPackage/declarativeAgent.json` instructions use Microsoft 365 Copilot work context; README documents Work IQ deadline constraint | Implemented through Copilot Chat Work IQ context |
| Business-ready enterprise scenario | HR workforce intelligence workflows in backend and dashboard | Implemented |
| Public repository with README | `README.md` | Implemented |
| No confidential information | `.gitignore`, synthetic data only, security docs | Implemented |

## Enterprise Agents Track Fit

Workforce IQ is built for Microsoft 365 Copilot Chat, not as a standalone chatbot. The declarative agent connects Copilot to a workforce analytics API through an API plugin. Users can ask HR planning questions in Copilot Chat and the agent can retrieve aggregate HR KPIs, risk explanations, and report job status.

## Microsoft IQ Position

The project uses Work IQ through Microsoft 365 Copilot Chat. The agent instructions require the model to use user-permitted Microsoft 365 work context for meeting, document, conversation, and stakeholder-aware workforce planning. The HR API plugin supplies structured workforce analytics.

Direct Work IQ API calls are intentionally not implemented for the hackathon deadline because Microsoft announced Work IQ APIs as generally available on June 16, 2026, two days after the June 14, 2026 submission deadline.

## Optional Higher-Rating Items

| Optional criterion | Current status | Evidence |
| --- | --- | --- |
| External REST action plugin | Implemented | `appPackage/hr-workforce-plugin.json`, `openapi.yaml` |
| OAuth security for plugin | Designed with placeholders | OAuth scheme in OpenAPI and plugin manifest |
| MCP Apps | Not implemented in this initial build | Can be added after core Copilot package validates |
| External MCP server | Not implemented in this initial build | Not claimed |

## Judging Rubric Evidence

| Rubric area | Repository evidence |
| --- | --- |
| Accuracy and relevance | M365 app package, declarative agent, API plugin, HR business domain |
| Reasoning and multi-step thinking | Agent context endpoint returns analytics, citations, safety notes, and recommended actions |
| Creativity and originality | Workforce intelligence combines Copilot work context with aggregate HR analytics |
| User experience and presentation | Next.js operational dashboard and Copilot conversation starters |
| Reliability and safety | Health checks, Prometheus metrics, guarded AI instructions, synthetic data policy |
| Community vote readiness | README gives demo setup and concise project narrative |
