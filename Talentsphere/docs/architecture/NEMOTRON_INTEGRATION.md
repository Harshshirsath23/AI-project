# NVIDIA Nemotron 3 Ultra Integration Architecture — TalentSphere AI Enterprise Platform

## 1. Architectural Overview

NVIDIA Nemotron 3 Ultra is integrated into TalentSphere as the **high-reasoning decision intelligence model**.

It operates strictly within TalentSphere's established layered architecture:

```text
FastAPI Endpoints
       │
       ▼
  AgentRuntime
(Central Execution Gateway)
       │
       ▼
   LangGraph
(Orchestrator & State Machine)
       │
       ▼
   LLMService
(Provider Abstraction)
       │
       ▼
NemotronProvider ────► NVIDIA NIM API (https://integrate.api.nvidia.com/v1)
       │                 └─► Fallback: MockLLM (Offline / Tests)
       ▼
Structured Reasoning & Evidence Synthesis
       │
       ▼
Guardrails & Schema Validation
       │
       ▼
Tool Authorization & Permission Validator
       │
       ▼
  HITL Gate Manager (Pauses WAITING_HITL if High Risk)
       │
       ▼
Authorized Tool Execution & Database State Update
       │
       ▼
PostgreSQL (System of Record) ◄──────► LangSmith (Telemetry Tracing)
```

---

## 2. Responsibilities Matrix

| Architectural Layer | Responsible Component | Responsibilities |
| :--- | :--- | :--- |
| **Workflow State Machine** | LangGraph (`StateGraph`) | Orchestrates graph nodes, handles execution state transitions, conditional routing, and retries. |
| **Execution Gateway** | `AgentRuntime` | Agent/version resolution, tool authorization checks, execution persistence in PostgreSQL, correlation IDs. |
| **LLM Provider Abstraction** | `LLMService` & `NemotronProvider` | Formats prompts, invokes NVIDIA NIM endpoints, manages max tokens, retries, and structured Pydantic outputs. |
| **Reasoning Engine** | NVIDIA Nemotron 3 Ultra | High-reasoning tasks: requirement extraction, resume evidence synthesis, qualitative fit analysis, candidate recommendation generation. |
| **Deterministic Calculations** | Python Matching Engine | Skill match %, experience %, role %, education %, semantic similarity score calculations. |
| **Security & HITL Boundary** | `ToolExecutionFramework` & `HITLGateManager` | Enforces `organization_id` multi-tenancy, RBAC permissions, risk level checks, and recruiter approval interruptions. |
| **System of Record** | PostgreSQL 17 + pgvector | Persistent storage of executions, candidates, jobs, tools, and HITL states. |
| **AI Observability** | LangSmith & `TraceContext` | Tracing, latency monitoring, cost/token tracking, and PII scrubbing. |

---

## 3. Configuration & Fallback Architecture

Configured via environment variables in `app/core/config.py`:

```env
NEMOTRON_ENABLED=true
NEMOTRON_MODEL=nvidia/nemotron-3-ultra
NEMOTRON_API_KEY=your_nvidia_api_key
NEMOTRON_BASE_URL=https://integrate.api.nvidia.com/v1
NEMOTRON_TIMEOUT_SECONDS=30
NEMOTRON_MAX_RETRIES=3
NEMOTRON_TEMPERATURE=0.2
NEMOTRON_MAX_TOKENS=4096
NEMOTRON_FALLBACK_ENABLED=true
```

### Local Development & Offline Resiliency
If `NEMOTRON_API_KEY` is not configured or an external network failure occurs, `NemotronProvider` automatically degrades gracefully to `MockLLM` for local testing and offline development without breaking pipeline execution.

---

## 4. Security, Tenant Isolation & Observability

1. **Multi-Tenant Isolation**: Row-level tenancy enforced via `organization_id` on all vector searches and database queries.
2. **Privacy Scrubbing**: `app/core/observability/privacy.py` scrubs emails, phone numbers, JWTs, API keys, and passwords before transmitting telemetry.
3. **LangSmith Correlation**: `AIExecution.langsmith_trace_id` correlates PostgreSQL database execution records with LangSmith traces.
