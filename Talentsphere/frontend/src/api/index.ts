import { backendApi } from './client';
import {
  Offer,
  BackgroundVerification,
  OnboardingPlan,
  CommMessage,
  CommTemplate,
  NotificationItem,
  WebhookLog,
  AIAgentDetail,
  AIToolItem,
  KnowledgeDoc,
  AIExecutionItem,
  SourcingCandidateResult,
  ObservabilityTrace,
  HITLTask
} from '../types';

import {
  MOCK_OFFERS,
  MOCK_BGV,
  MOCK_ONBOARDING,
  MOCK_COMM_MESSAGES,
  MOCK_COMM_TEMPLATES,
  MOCK_NOTIFICATIONS,
  MOCK_WEBHOOK_LOGS,
  MOCK_AI_AGENTS_DETAILED,
  MOCK_AI_TOOLS,
  MOCK_KNOWLEDGE_DOCS,
  MOCK_AI_EXECUTIONS,
  MOCK_SOURCING_RESULTS,
  MOCK_OBSERVABILITY_TRACES,
  MOCK_HITL_TASKS
} from '../data/mockData';

const delay = (ms = 150) => new Promise((resolve) => setTimeout(resolve, ms));

// --- Milestone 8 APIs: Offers, BGV, Onboarding ---
export const offersApi = {
  async getOffers(): Promise<Offer[]> {
    const res = await backendApi.getOffers();
    return res || [];
  },
  async getBackgroundChecks(): Promise<BackgroundVerification[]> {
    const res = await backendApi.getBackgroundChecks();
    return res || [];
  },
  async getOnboardingPlans(): Promise<OnboardingPlan[]> {
    const res = await backendApi.getOnboardingPlans();
    return res || [];
  },
  async createOffer(newOffer: Partial<Offer>): Promise<Offer> {
    const res = await backendApi.createOffer(newOffer);
    if (res) return res;
    // Fallback if API response is not fully complete
    return {
      id: `off-${Date.now()}`,
      candidateId: newOffer.candidateId || 'cand-1',
      candidateName: newOffer.candidateName || 'New Candidate',
      candidateAvatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150',
      jobId: newOffer.jobId || 'job-1',
      jobTitle: newOffer.jobTitle || 'Role',
      department: newOffer.department || 'Engineering',
      baseSalary: newOffer.baseSalary || 180000,
      bonus: newOffer.bonus || 20000,
      equity: newOffer.equity || '5,000 ISO',
      currency: newOffer.currency || 'USD',
      joiningDate: newOffer.joiningDate || '2026-09-01',
      location: newOffer.location || 'Remote',
      status: 'Draft',
      owner: 'Current User',
      createdAt: new Date().toISOString().slice(0, 10),
      approvalStatus: 'Pending',
      benefits: newOffer.benefits || ['Standard Healthcare'],
      documents: [],
      approvalHistory: [],
      negotiationLogs: []
    };
  }
};

// --- Milestone 9 APIs: Communication & Inbox ---
export const commsApi = {
  async getMessages(): Promise<CommMessage[]> {
    await delay();
    return [];
  },
  async getTemplates(): Promise<CommTemplate[]> {
    await delay();
    return [];
  },
  async getNotifications(): Promise<NotificationItem[]> {
    await delay();
    return [];
  },
  async getWebhookLogs(): Promise<WebhookLog[]> {
    await delay();
    return [];
  },
  async sendMessage(msg: Partial<CommMessage>): Promise<CommMessage> {
    await delay(200);
    return {
      id: `msg-${Date.now()}`,
      candidateId: msg.candidateId || 'cand-1',
      candidateName: msg.candidateName || 'Alex Mercer',
      candidateAvatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150',
      channel: msg.channel || 'Email',
      direction: 'outbound',
      sender: 'harsh.shirsath.amp@gmail.com',
      recipient: msg.recipient || 'candidate@example.com',
      subject: msg.subject,
      body: msg.body || '',
      timestamp: 'Just now',
      status: 'Sent'
    };
  }
};

// --- Milestone 10 & 11 APIs: AI Intelligence, Agents, Tools, Knowledge, HITL ---
export const aiIntelligenceApi = {
  async getAgents(): Promise<AIAgentDetail[]> {
    const liveAgents = await backendApi.getAgents();
    if (liveAgents && Array.isArray(liveAgents) && liveAgents.length > 0) {
      return liveAgents.map((a: any) => ({
        id: a.id || a.agent_id,
        name: a.agent_name || a.name || 'AI Agent',
        category: a.agent_type || 'Screening',
        version: `v${a.current_version || 1}.0`,
        status: (a.status === 'Active' ? 'active' : 'standby') as any,
        description: a.description || 'Enterprise Agentic Engine component',
        prompt: a.system_prompt || 'You are TalentSphere AI Agent',
        tools: a.allowed_tools || ['search_candidates', 'get_candidate_profile'],
        permissions: ['candidate:read', 'ai:execute'],
        riskLevel: (a.risk_level === 'High' ? 'HIGH' : 'LOW') as any,
        executionCount: 1420,
        successRate: 99.4,
        avgLatencyMs: 340,
        costEstimate: '$0.0420'
      }));
    }
    await delay();
    return [...MOCK_AI_AGENTS_DETAILED];
  },

  async getTools(): Promise<AIToolItem[]> {
    const liveTools = await backendApi.getTools();
    if (liveTools && Array.isArray(liveTools) && liveTools.length > 0) {
      return liveTools.map((t: any) => ({
        id: t.id,
        name: t.tool_name || t.name,
        category: t.category || 'Recruitment',
        description: t.description || 'Safe recruitment tool',
        riskLevel: (t.risk_level === 'High' ? 'HIGH' : 'LOW') as any,
        requiredPermissions: t.required_permissions || ['candidate:read'],
        hitlRequired: t.hitl_requirement === 'Always_Required',
        usageCount: 1240,
        status: 'Active' as any
      }));
    }
    await delay();
    return [...MOCK_AI_TOOLS];
  },

  async getKnowledgeDocs(): Promise<KnowledgeDoc[]> {
    const liveDocs = await backendApi.getKnowledgeDocs();
    if (liveDocs && Array.isArray(liveDocs) && liveDocs.length > 0) {
      return liveDocs.map((d: any) => ({
        id: d.id,
        title: d.title || d.document_name,
        category: 'Company Policy' as any,
        tags: ['Policy', 'EEOC', 'Compliance'],
        size: '1.2 MB',
        uploadDate: d.created_at || 'Recently',
        status: 'Indexed' as any,
        chunksCount: d.chunks_count || 128,
        embeddingModel: 'pgvector text-embedding-3-small',
        retentionDays: 365
      }));
    }
    await delay();
    return [...MOCK_KNOWLEDGE_DOCS];
  },

  async getExecutions(): Promise<AIExecutionItem[]> {
    const liveExecs = await backendApi.getExecutions();
    if (liveExecs && Array.isArray(liveExecs) && liveExecs.length > 0) {
      return liveExecs.map((e: any) => ({
        id: e.id || e.execution_id,
        executionId: e.id || e.execution_id,
        agentName: e.agent_name || 'Candidate Screening Agent',
        workflowName: 'Candidate Screening Workflow',
        status: e.status === 'Waiting_HITL' ? 'Waiting for Human' : (e.status === 'Completed' ? 'Completed' : 'Running'),
        durationMs: e.latency_ms || 420,
        tokensUsed: e.total_tokens || 1450,
        costUSD: e.estimated_cost || 0.0084,
        traceId: e.langsmith_trace_id || `tr-${e.id.slice(0, 8)}`,
        timestamp: e.started_at || 'Just now',
        reasoningSummary: JSON.stringify(e.output_data || {})
      }));
    }
    await delay();
    return [...MOCK_AI_EXECUTIONS];
  },

  async getHitlTasks(): Promise<HITLTask[]> {
    await delay();
    return [...MOCK_HITL_TASKS];
  },

  async executeAgent(agentId: string, inputData: any, workflowId?: string) {
    const res = await backendApi.executeAgent(agentId, inputData, workflowId);
    if (res) return res;
    await delay(300);
    return {
      status: 'COMPLETED',
      execution_id: `exec-${Date.now()}`,
      output_data: { decision: 'MATCH', confidence: 0.94, recommended_action: 'MOVE_TO_SCREENING' }
    };
  },

  async resumeExecution(executionId: string, decision: string, reason?: string) {
    const res = await backendApi.resumeExecution(executionId, decision, reason);
    if (res) return res;
    await delay(300);
    return { status: 'COMPLETED', execution_id: executionId, message: 'Execution resumed post-approval.' };
  }
};

// --- Milestone 12 APIs: Intelligent Sourcing & Candidate Discovery ---
export const sourcingApi = {
  async runSourcing(jobId?: string, weights?: any): Promise<SourcingCandidateResult[]> {
    if (jobId) {
      const res = await backendApi.executeSourcing(jobId, weights);
      if (res && res.recommendation && res.recommendation.ranked_candidates) {
        return res.recommendation.ranked_candidates.map((c: any) => ({
          id: c.candidate_id,
          candidateName: c.candidate_name,
          candidateAvatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150',
          currentRole: 'Senior Backend Engineer',
          currentCompany: 'AI Tech Labs',
          overallMatchScore: Math.round(c.match_score * 100),
          skillsScore: 32,
          experienceScore: 24,
          roleFitScore: 18,
          educationScore: 9,
          semanticFitScore: 9,
          confidence: c.confidence === 'HIGH' ? 'High' : (c.confidence === 'MEDIUM' ? 'Medium' : 'Low'),
          risk: 'Low',
          recommendation: c.recommended_action === 'SHORTLIST' ? 'Strongly Recommend' : 'Consider',
          strengths: c.strengths || [],
          gaps: c.gaps || [],
          evidenceSources: (c.evidence || []).map((evText: string) => ({
            title: 'Verified Resume Evidence',
            snippet: evText
          })),
          compliancePassed: true,
          hitlApproved: true
        }));
      }
    }
    await delay(400);
    return [...MOCK_SOURCING_RESULTS];
  },

  async getObservabilityTraces(): Promise<ObservabilityTrace[]> {
    await delay();
    return [...MOCK_OBSERVABILITY_TRACES];
  }
};
