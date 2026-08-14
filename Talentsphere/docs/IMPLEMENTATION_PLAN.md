# TalentSphere — Phase-Wise Implementation Plan

**Version:** 1.0  
**Date:** August 14, 2026  
**Source:** [`new plan.md`](./new%20plan.md) + current codebase audit  
**Timeline:** ~52 weeks to production MVP | 18 months to enterprise-grade

---

## Where You Are Today

| Area | Status | Notes |
|------|--------|-------|
| FastAPI backend (auth, org, RBAC) | ✅ Done | Milestones 1–7 |
| Recruitment lifecycle (jobs → offers) | ✅ Done | Milestone 8 |
| Communication module | ✅ Done | Milestone 9 |
| AI foundation (registry, HITL, RAG schema) | ✅ Done | Milestone 10 |
| LangGraph runtime (partial) | 🟡 In progress | Copilot, sourcing, screening workflows exist |
| Nemotron + LangSmith | 🟡 Partial | Providers & observability scaffolded |
| ~60 domain agents | 🔴 Not started | Only ~10 agent stubs exist |
| Frontend (React) | 🟡 UI shell | Many views built; some still on mock data |
| Mobile app | 🔴 Not started | — |
| Production hardening / compliance | 🔴 Not started | — |

**You are entering Phase 1B → Phase 2.** The deterministic platform is built; the multi-agent AI layer is the main gap.

---

## How to Use This Plan

1. Work in **2-week sprints** aligned to phases below.
2. Each phase has a **gate checklist** — do not start the next phase until the gate passes.
3. Build **vertical slices** (one agent end-to-end) before scaling horizontally (all 60 agents).
4. Keep deterministic APIs as source of truth; agents call services, never bypass RBAC.

---

## Phase 0 — Foundation & DevOps (Weeks 1–3)

> **Status:** Mostly complete. Use this as a checklist, not greenfield work.

### Goals
- Every engineer runs the stack locally in < 30 minutes.
- CI/CD validates every PR.
- Architecture decisions are documented.

### Tasks

| # | Task | Owner | Done When |
|---|------|-------|-----------|
| 0.1 | Monorepo structure (`backend/`, `frontend/`, `docs/`, `scripts/`) | DevOps | Clone → `docker compose up` works |
| 0.2 | GitHub Actions: lint, type-check, pytest, frontend build | DevOps | PR checks green |
| 0.3 | Environments: `.env.example`, dev/staging/prod config | Backend | No secret leaks in repo |
| 0.4 | Docker Compose: Postgres 17 + pgvector, Redis, backend, frontend | DevOps | Full stack local |
| 0.5 | ADRs: multi-tenancy, state management, tool auth, HITL | Architecture | 4 ADRs in `docs/architecture/` |
| 0.6 | Apply DB schema (`talentsphere_schema.sql`) + Alembic migrations | Backend | Migrations reproducible |
| 0.7 | Sprint cadence + ownership matrix | PM | RACI doc exists |

### Gate ✅
- [ ] `pytest` passes locally and in CI
- [ ] Frontend connects to backend (not mock-only)
- [ ] LangSmith project configured (dev)
- [ ] Team aligned on phase order

---

## Phase 1 — Core AI Platform (Weeks 4–12)

> **Goal:** Production-ready agent runtime that all 60 agents plug into.

### 1A — Agent Runtime Hardening (Weeks 4–6)

| # | Task | Files / Area | Done When |
|---|------|--------------|-----------|
| 1.1 | Finalize `WorkflowState` + checkpoint schema | `app/modules/ai/engine/state.py` | State survives restart |
| 1.2 | PostgreSQL checkpointer (LangGraph PostgresSaver) | `app/modules/ai/engine/` | Resume paused workflow |
| 1.3 | Master Supervisor routes to 4 subgraphs | `app/modules/ai/copilot/agents/supervisor.py` | Stage routing tested |
| 1.4 | Wire `AgentRuntime.execute()` to LangGraph graphs | `app/modules/ai/engine/runtime.py` | API → graph → DB |
| 1.5 | HITL interrupt + resume API | `app/modules/ai/engine/hitl.py`, `api.py` | Pause/resume E2E test |
| 1.6 | Tool authorization framework | `app/modules/ai/engine/tools.py` | Unauthorized tool blocked |
| 1.7 | Cost + token tracking per execution | `AIUsage` model | Billing row per run |

### 1B — LLM & Observability (Weeks 6–9)

| # | Task | Reference | Done When |
|---|------|-----------|-----------|
| 1.8 | Nemotron provider (primary) | `docs/architecture/NEMOTRON_INTEGRATION.md` | Structured JSON output works |
| 1.9 | Fallback chain: Nemotron → GPT-4 → Claude | `app/modules/ai/engine/providers/` | Failover test passes |
| 1.10 | LangSmith tracing + PII scrubber | `docs/architecture/LANGSMITH_OBSERVABILITY.md` | Traces correlate to `ai_executions` |
| 1.11 | Embedding service (1536-dim, pgvector) | `app/core/embeddings.py` | Store + query embeddings |
| 1.12 | RAG retrieval pipeline | `KnowledgeService` | Top-k chunks returned |

### 1C — API & Testing (Weeks 9–12)

| # | Task | Done When |
|---|------|-----------|
| 1.13 | REST: `/workflows`, `/agents`, `/executions`, `/tools` | OpenAPI docs complete |
| 1.14 | WebSocket hub for live execution status | Frontend receives status events |
| 1.15 | Tenant isolation tests (cross-org access denied) | Security test suite |
| 1.16 | Integration tests: auth → execute → checkpoint → HITL | >80% coverage on AI module |
| 1.17 | Rate limiting per org (100 req/min default) | 429 on overflow |

### Phase 1 Deliverables
- Agent runtime with checkpointing, HITL, tool auth
- Nemotron + fallback LLMs
- LangSmith + cost tracking
- pgvector embeddings live

### Gate ✅
- [ ] Start workflow via API → completes or pauses at HITL
- [ ] Resume after HITL approval
- [ ] LangSmith trace ID stored in `ai_executions`
- [ ] P95 API latency < 500ms (non-LLM endpoints)
- [ ] >80% test coverage on `app/modules/ai/`

---

## Phase 2 — Domain Subgraphs & 60 Agents (Weeks 13–30)

> **Goal:** End-to-end AI recruitment: JD → screen → interview → offer.

Build **one vertical slice first**, then parallelize subgraphs.

### Recommended Build Order

```
Week 13–14: Vertical slice (JD Generator → Resume Parser → Ranker)
Week 15–18: Sourcing subgraph (8 agents)
Week 19–24: Screening subgraph (12 agents) ← core differentiator
Week 25–28: Interview subgraph (10 agents)
Week 29–30: Offer subgraph (6 agents) + E2E orchestration
```

---

### 2A — Sourcing & JD Subgraph (Weeks 13–18)

**Path:** `app/modules/ai/sourcing/` + `workflows/sourcing_workflow.py`

| Agent | Input | Output | Priority |
|-------|-------|--------|----------|
| JD Generator | title, skills, seniority | structured JD | P0 |
| JD Optimizer | JD draft | SEO-optimized JD | P1 |
| Keyword Extractor | JD | keywords, skills tags | P1 |
| Salary Band Agent | role, location | comp range | P2 |
| Location Analyzer | JD | geo/market insights | P2 |
| Role Classifier | JD | job family, level | P2 |
| Compliance Checker | JD | EEO/legal flags | P1 |
| Job Board Publisher | JD | published URLs | P1 |

**Implementation pattern (repeat for every agent):**
1. Pydantic input/output schemas
2. Prompt template in `PromptTemplate` table
3. LangGraph node function
4. Register in agent registry + tool permissions
5. Unit test + LangSmith eval dataset
6. Wire to deterministic `recruitment` APIs

### 2B — Screening & Match Subgraph (Weeks 19–24) ⭐

**Path:** `app/modules/ai/workflows/candidate_screening.py` + `app/modules/candidates/`

| Agent | Depends On | Priority |
|-------|------------|----------|
| Resume Parser | PDF/DOCX extract tool | P0 |
| PDF Extractor | S3/file storage | P0 |
| Vector Embedding Agent | embeddings service | P0 |
| Hybrid Search Agent | pgvector + FTS | P0 |
| Candidate Ranker | search results + JD | P0 |
| Skill Matcher | parsed resume + JD skills | P0 |
| Experience Matcher | parsed resume + JD level | P1 |
| Education Matcher | parsed resume + requirements | P1 |
| Bias Detector | ranked list | P0 — HITL gate |
| Red Flag Detector | resume + history | P1 |
| Culture Fit Agent | JD culture + profile | P2 |
| Summary Generator | full profile | P1 |

**Hybrid search formula (from plan):**
- 30% full-text search
- 50% vector similarity
- 20% deterministic skill match

**HITL gates:** Bias Detector, Red Flag Detector → require human approval before advancing candidate.

### 2C — Interview & Assessment Subgraph (Weeks 25–28)

**Path:** `app/modules/interviews/` + new `app/modules/ai/interviews/`

| Agent | Integration | Priority |
|-------|-------------|----------|
| Question Generator | JD + candidate profile | P0 |
| Interview Scheduler | Google/Outlook calendar | P1 |
| Transcript Analyzer | audio/text transcript | P0 |
| Technical Scorer | rubric from questions | P0 |
| Communication Scorer | transcript sentiment | P1 |
| Behavior Scorer | behavioral answers | P1 |
| Coding Test Evaluator | external assessment API | P2 |
| Take-Home Evaluator | submission review | P2 |
| Sentiment Analyzer | transcript | P1 |
| Interview Recommendation | all scores → hire/no | P0 — HITL gate |

### 2D — Offer & Onboarding Subgraph (Weeks 29–30)

**Path:** `app/modules/offers/` + new `app/modules/ai/offers/`

| Agent | Integration | Priority |
|-------|-------------|----------|
| Offer Letter Generator | PDF tool + templates | P0 |
| Salary Negotiator | comp benchmarks | P1 |
| Background Check Agent | Checkr/Verified API | P2 |
| Document Verification Agent | ID/doc upload | P2 |
| Onboarding Task Agent | task checklist | P1 |
| Offer Acceptance Tracker | candidate portal | P1 |

### 2E — Master Orchestration (Week 30)

Wire supervisor to run full pipeline:

```
Sourcing → Screening → Interview → Offer → Communication
                ↓           ↓          ↓
              HITL        HITL       HITL
```

**E2E test:** `scripts/test_recruitment_flow.py` runs full AI pipeline with mocked external APIs.

### Phase 2 Deliverables
- 4 domain subgraphs in LangGraph
- ~60 agents registered and tested
- Full recruitment AI pipeline with HITL
- Bias detection + fairness reporting

### Gate ✅
- [ ] JD → publish → parse resume → rank → interview → offer (E2E)
- [ ] Resume parsing success >95% on test corpus
- [ ] Hybrid search returns relevant top-50 in <2s
- [ ] Bias detector triggers HITL on flagged rankings
- [ ] Agent success rate >95% (LangSmith evals)
- [ ] Avg agent latency <2s (excluding LLM cold start)

---

## Phase 3 — Frontend & UX (Weeks 31–40)

> **Goal:** Connect existing UI to live backend; ship recruiter + candidate experiences.

### Current Frontend Assets (already built)
- Recruiter: `JobManagementView`, `RecruitmentPipelineView`, `CandidateCommandCenter`
- AI: `AICommandCenterHub`, `HITLCenterView`, `AgentRuntimeView`, `WorkflowVisualizerView`
- Interviews: `InterviewDashboardView`, `InterviewCalendarView`
- Offers: `OffersDashboardView`
- Org/IAM: `OrgAdminUsersRolesView`, `RolesManagementView`

### 3A — Backend Integration (Weeks 31–33)

| # | Task | Component |
|---|------|-----------|
| 3.1 | Replace mock data with TanStack Query hooks | All views |
| 3.2 | Auth flow: JWT refresh, org context | `AuthContext`, `OrganizationContext` |
| 3.3 | Real-time execution status (WebSocket) | `AgentRuntimeView`, `WorkflowVisualizerView` |
| 3.4 | HITL approval UI wired to API | `HITLCenterView`, `HITLApprovalCard` |
| 3.5 | Resume upload → trigger screening workflow | `ResumeUploadModal` |
| 3.6 | AI Copilot chat wired to copilot API | `AICopilotView` |

### 3B — Recruiter Dashboard (Weeks 33–35)

| Feature | View | API |
|---------|------|-----|
| Job CRUD + AI JD generation | `JobManagementView` | `/recruitment`, `/ai/workflows` |
| Kanban pipeline | `RecruitmentPipelineView` | `/recruitment/applications` |
| Candidate search (hybrid) | `CandidateCommandCenter` | `/candidates/search` |
| Workflow builder | `WorkflowBuilderView` | `/ai/workflows` |
| Analytics | `DashboardOverview` | `/ai/usage`, recruitment metrics |

### 3C — Candidate Portal (Weeks 35–38)

| Feature | Build |
|---------|-------|
| Job browsing + apply | New routes in `App.tsx` |
| Application status tracker | Candidate-facing pipeline view |
| Interview self-scheduling | Calendar integration |
| Document upload | Reuse resume upload flow |
| Offer accept/decline | Offer portal page |

### 3D — Mobile App (Weeks 38–40)

| Feature | Stack |
|---------|-------|
| Recruiter: candidate search, HITL approvals | React Native |
| Candidate: status, interview reminders | React Native |
| Push notifications | FCM / APNs |

### Phase 3 Deliverables
- Recruiter dashboard on live APIs
- Candidate portal
- Mobile MVP (iOS + Android)
- WebSocket live updates

### Gate ✅
- [ ] Zero mock data in production views
- [ ] Recruiter completes full hire flow from UI
- [ ] Candidate can apply and track status
- [ ] Page load <3s (Lighthouse)
- [ ] HITL approval from mobile works

---

## Phase 4 — Production, Scale & GTM (Weeks 41–52+)

### 4A — Production Hardening (Weeks 41–45)

| # | Task | Target |
|---|------|--------|
| 4.1 | Load test: 1,000 concurrent users | k6 / Locust |
| 4.2 | OWASP + penetration test | Third-party audit |
| 4.3 | SOC 2 Type II prep | Policies + evidence |
| 4.4 | GDPR: data export, deletion, consent | API + UI |
| 4.5 | DR: backup, restore, RTO <4h | Runbooks |
| 4.6 | Monitoring: Prometheus + Grafana + alerts | 99.9% uptime SLA |
| 4.7 | LLM cost caps per org | Usage limits in `AIUsage` |

### 4B — Go-to-Market (Weeks 41–52+)

| # | Task |
|---|------|
| 4.8 | Marketing site + pricing page |
| 4.9 | Enterprise pilot program (first 10 customers) |
| 4.10 | Case studies + onboarding playbooks |
| 4.11 | Customer success + support tooling |

### 4C — Continuous Improvement (Ongoing)

| Area | Action |
|------|--------|
| Matching quality | A/B test ranking weights |
| Agent quality | LangSmith eval datasets per agent |
| Cost | Prompt compression, caching, batching |
| Features | Customer feedback → sprint backlog |

### Gate ✅
- [ ] 99.9% uptime over 30 days (staging → prod)
- [ ] Security audit passed
- [ ] 10+ pilot customers onboarded
- [ ] AI cost per execution < $0.50

---

## Sprint Backlog — Start Here (Next 4 Weeks)

Since Milestone 10 is done, **start Phase 1B + first vertical slice:**

### Sprint 1 (Weeks 1–2)
- [ ] PostgreSQL LangGraph checkpointer (resume workflows)
- [ ] Wire Supervisor → sourcing subgraph
- [ ] Nemotron provider E2E test with structured output
- [ ] LangSmith trace ID → `ai_executions.langsmith_trace_id`

### Sprint 2 (Weeks 3–4)
- [ ] JD Generator agent (full: schema, prompt, node, test)
- [ ] Resume Parser agent (PDF + DOCX + LLM extraction)
- [ ] Frontend: `ResumeUploadModal` triggers screening workflow
- [ ] Frontend: `HITLCenterView` wired to real API

### Sprint 3 (Weeks 5–6)
- [ ] Vector Embedding + Hybrid Search agents
- [ ] Candidate Ranker + Bias Detector (with HITL)
- [ ] E2E test: upload resume → ranked list → HITL gate

### Sprint 4 (Weeks 7–8)
- [ ] Interview Question Generator + Transcript Analyzer
- [ ] Offer Letter Generator
- [ ] Full pipeline E2E: JD → hire decision (script + UI)

---

## Team & Ownership

| Role | Count | Owns |
|------|-------|------|
| Architecture / AI Lead | 1 | LangGraph, supervisor, agent design |
| Backend Engineers | 2 | Subgraphs, APIs, DB |
| AI/ML Engineer | 1 | Prompts, evals, embeddings |
| DevOps | 1 | CI/CD, K8s, monitoring |
| Frontend Engineers | 2 | Dashboard, portal, API integration |
| Mobile Engineer | 1 | React Native (Phase 3) |
| QA | 1 | E2E, load, security tests |
| PM | 1 | Roadmap, customer feedback |

---

## Success Metrics by Phase

| Phase | Key Metric | Target |
|-------|------------|--------|
| 0 | Local setup time | < 30 min |
| 1 | Test coverage (AI module) | > 80% |
| 1 | API P95 latency | < 500ms |
| 2 | Agent success rate | > 95% |
| 2 | Resume parse accuracy | > 95% |
| 2 | E2E pipeline | JD → offer works |
| 3 | Page load | < 3s |
| 3 | Mock data in UI | 0% |
| 4 | Uptime | 99.9% |
| 4 | Pilot customers | 10+ |

---

## Risk Register (Top 5)

| Risk | Mitigation |
|------|------------|
| LLM cost blowup | Per-org caps, caching, smaller models for simple tasks |
| 60 agents = scope creep | P0/P1/P2 priority; ship vertical slice first |
| Agent coordination bugs | LangGraph state machine + extensive E2E tests |
| Frontend/backend drift | OpenAPI-generated TypeScript types |
| Compliance (bias, GDPR) | HITL gates, audit logs, PII scrubbing in traces |

---

## Document Map

| Doc | Purpose |
|-----|---------|
| [`new plan.md`](./new%20plan.md) | Full vision, code examples, 60-agent catalog |
| [`hierarchical_tree_flowchart.md`](./hierarchical_tree_flowchart.md) | System hierarchy diagram |
| [`talentsphere_schema.sql`](./talentsphere_schema.sql) | Full DB schema (291 tables) |
| [`architecture/NEMOTRON_INTEGRATION.md`](./architecture/NEMOTRON_INTEGRATION.md) | LLM provider setup |
| [`architecture/LANGSMITH_OBSERVABILITY.md`](./architecture/LANGSMITH_OBSERVABILITY.md) | Tracing & evals |
| `backend/MILESTONE_*_REPORT.md` | Completed milestone audit trail |

---

**Next action:** Execute Sprint 1 — PostgreSQL checkpointer + Supervisor routing + Nemotron E2E.
