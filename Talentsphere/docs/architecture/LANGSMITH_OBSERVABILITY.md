# TalentSphere AI Observability, Tracing, Debugging & Evaluation Architecture (LangSmith Integration)

## 1. Why LangSmith Exists
In TalentSphere's multi-tenant AI recruitment platform, AI agents perform complex, multi-step workflows (candidate sourcing, resume parsing, candidate matching via RAG, compliance verification, and human-in-the-loop approvals).

Traditional application logging and database records capture final execution states but fail to reveal:
- Detailed inner execution steps of multi-agent graphs.
- Sub-node latency breakdowns (LLM vs tool vs database search).
- Granular token consumption per agent/chain.
- Agent decision branches, retries, and tool invocation parameters.
- Regression testing and evaluation metrics across model and prompt versions.

LangSmith fills this gap as a dedicated **AI observability, tracing, evaluation, and debugging nervous system** operating non-blockingly around the core application.

---

## 2. What LangSmith Does
LangSmith is responsible for:
- **Trace Visualization**: Visualizing full execution trees for LangGraph workflows, LangChain chains, LLM calls, and tools.
- **Latency & Cost Profiling**: Emitting high-resolution timing and token metrics per step.
- **Debug & Root-Cause Analysis**: Inspecting failed agent steps, retry loops, and parameter payloads.
- **HITL Observability**: Instrumenting workflow pauses for human approval and recording decision outcomes.
- **Evaluation & Feedback**: Running qualitative evaluators (`Correctness`, `Relevance`, `Groundedness`, `Safety`, `StructuredOutputValidity`, `RetrievalQuality`) and posting scores/feedback.

---

## 3. What PostgreSQL Does (Source of Truth Separation)
PostgreSQL remains the single authoritative source of truth for:
- **Tenant Isolation & Security**: Organization data, user accounts, JWT security, RBAC.
- **Business Records**: Candidates, jobs, applications, interview schedules, offer letters.
- **AI State & Accounting**: `ai_executions`, `ai_agents`, `ai_agent_versions`, `ai_workflows`, `ai_tools`, `hitl_states`, `ai_usage` cost and token billing records.
- **Audit Logs**: Compliance and audit events.

> **Principle**: PostgreSQL handles business state, security, and financial accounting. LangSmith handles observability, debugging, performance tracing, and AI evaluation.

---

## 4. Trace Architecture & Hierarchy
Executions follow a hierarchical tree model:

```text
TalentSphere AI Execution (Workflow Root Run)
│
├── LangGraph Workflow Run
│   │
│   ├── Supervisor Agent Run
│   │   ├── LLM Call Run (GPT-4 / Claude 3.5)
│   │   └── Routing Decision Run
│   │
│   ├── Resume Parser Agent Run
│   │   ├── Document Parsing Tool Run
│   │   └── Structured Output LLM Run
│   │
│   ├── Candidate Matcher Agent Run
│   │   ├── Embedding Run
│   │   ├── pgvector RAG Retrieval Run
│   │   ├── Reranking Run
│   │   └── Recommendation LLM Run
│   │
│   ├── Compliance Agent Run
│   │   └── Compliance Evaluation LLM Run
│   │
│   └── HITL Interruption Event Run
│       └── Human Decision State (Approved / Rejected / Modified)
│
└── Final Output
```

---

## 5. Metadata Standards
Every trace span includes standardized metadata attributes:
- `organization_id`: Multi-tenant organization UUID.
- `user_id`: Triggering user UUID.
- `agent_id`: DB registered agent UUID.
- `agent_version`: Active agent prompt/config version integer.
- `workflow_id`: AI workflow UUID.
- `workflow_version`: Workflow graph version integer.
- `execution_id`: Database `AIExecution` UUID.
- `hitl_id`: Database `HITLState` UUID (when human intervention occurs).
- `environment`: Runtime environment (`development`, `staging`, `production`).
- `feature_name`: Specific platform feature module (e.g. `candidate_screening`).

---

## 6. Privacy Rules & PII Protection
TalentSphere processes sensitive recruitment data. Telemetry payloads pass through `app.core.observability.privacy`:

1. **Automatic Redaction of Credentials**: Dict keys containing `password`, `secret`, `jwt`, `token`, `access_token`, `api_key`, `authorization`, `credit_card`, `ssn`, `private_key` are scrubbed to `[REDACTED]`.
2. **Regex Scrubbing**: Emails and phone numbers are scrubbed to `[REDACTED_EMAIL]` and `[REDACTED_PHONE]`.
3. **Payload Capture Control**:
   - `LANGSMITH_CAPTURE_INPUTS=false`: Replaces raw inputs with `[REDACTED_PAYLOAD]` or summary length placeholders.
   - `LANGSMITH_CAPTURE_OUTPUTS=false`: Replaces raw outputs with `[REDACTED_PAYLOAD]`.

---

## 7. Agent Tracing
Agents registered in the `AI Agent Registry` are traced with `@traceable_agent` or `trace_agent(...)`. Every run records `agent_id` and `agent_version` so performance regressions between v1, v2, v3 of an agent can be pinpointed.

---

## 8. LangGraph Tracing
LangGraph graphs are automatically traced by registering `get_langchain_tracer()` callbacks in graph compilation/execution configs. Nodes, edges, state transitions, and conditional branches render natively in LangSmith.

---

## 9. LangChain Tracing
LangChain models, chains, prompt templates, and output parsers use standard LangChain callbacks. The central tracer (`get_langchain_tracer()`) propagates trace context seamlessly.

---

## 10. RAG Tracing
Document retrieval operations (`KnowledgeService.retrieve_knowledge`) are instrumented with `trace_rag(...)`, recording:
- `query` (sanitized)
- `retrieval_strategy` (e.g. `pgvector_hybrid`)
- `top_k` requested
- `documents_retrieved` count
- `similarity_scores`

---

## 11. Tool Tracing
Tools registered in the `AI Tool Registry` use `@traceable_tool` or `trace_tool(...)`, recording tool name, risk level (`Low`, `Medium`, `High`, `Critical`), required permissions, and execution time.

---

## 12. HITL Tracing
When an agent reaches `WAITING_HITL`, `trace_hitl(...)` records:
- `hitl_required`: `true`
- `hitl_triggered`: `true`
- `hitl_reason`: Description of high-risk action requiring approval.
- `hitl_decision`: Decision recorded upon user response (`Approved`, `Rejected`, `Modified`).

---

## 13. Evaluation Strategy
The evaluation framework in `app.core.observability.evaluation` provides:
- Evaluation dimensions: `Correctness`, `Relevance`, `Groundedness`, `Safety`, `PolicyCompliance`, `StructuredOutputValidity`, `ToolSelection`, `DecisionQuality`, `RetrievalQuality`.
- Evaluators for deterministic schema validity and document retrieval quality.
- `EvaluationManager.record_feedback(...)` to submit normalized scores (0.0 to 1.0) and comments directly to LangSmith runs.

---

## 14. Failure Handling & Graceful Degradation
**Non-Blocking & Resilient**:
- LangSmith calls run asynchronously.
- Any network timeout, rate limit, invalid credential error, or LangSmith API outage is caught and logged silently.
- **Application operations and API responses will NEVER fail due to a LangSmith issue.**

---

## 15. Performance Considerations
- Telemetry emission does not block FastAPI response threads.
- Payload sanitization uses fast regex and single-pass dict traversal.
- Sampling rate control via `LANGSMITH_SAMPLING_RATE`.

---

## 16. Environment Configuration
Configuration is managed via Pydantic settings in `app/core/config.py`:

```env
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=ls__your_api_key_here
LANGSMITH_PROJECT=talentsphere-development
LANGSMITH_ENVIRONMENT=development
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_SAMPLING_RATE=1.0
LANGSMITH_CAPTURE_INPUTS=false
LANGSMITH_CAPTURE_OUTPUTS=false
```

---

## 17. Development Usage
Set `LANGSMITH_TRACING=true` and supply your `LANGSMITH_API_KEY` in `.env`. Traces will stream to project `talentsphere-development`.

---

## 18. Production Usage
In production:
- Set `LANGSMITH_ENVIRONMENT=production` and `LANGSMITH_PROJECT=talentsphere-production`.
- Keep `LANGSMITH_CAPTURE_INPUTS=false` and `LANGSMITH_CAPTURE_OUTPUTS=false` to enforce PII security.
- Monitor evaluation metrics and latency histograms in the LangSmith dashboard.
