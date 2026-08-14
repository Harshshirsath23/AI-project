/**
 * TalentSphere API Client
 * Primary Gateway connecting Frontend to FastAPI Backend (http://localhost:8000/api/v1)
 * Includes automatic Bearer Token auth, JSON parsing, error handling, and robust fallback to structured mock data.
 */

const API_BASE_URL = (import.meta as any).env?.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T | null> {
  const token = localStorage.getItem('talentsphere_session_token');
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      console.warn(`[API Call] ${endpoint} returned status ${response.status}`);
      return null;
    }

    return (await response.json()) as T;
  } catch (err) {
    console.warn(`[API Call Failed] Endpoint ${endpoint} unreachable. Using fallback context.`, err);
    return null;
  }
}

export const backendApi = {
  // Auth
  async login(email: string, pass: string) {
    return request<{ access_token: string; refresh_token: string; token_type: string; user_id: string; organization_id: string; account_type: string }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email: email, password: pass }),
    });
  },

  async getMe() {
    return request<any>('/auth/me');
  },

  // Candidates
  async getCandidates() {
    return request<any[]>('/candidates');
  },

  async getCandidateProfile(candidateId: string) {
    return request<any>(`/candidates/${candidateId}`);
  },

  async createCandidate(candidateData: any) {
    return request<any>('/candidates', {
      method: 'POST',
      body: JSON.stringify(candidateData),
    });
  },

  async createCandidateFromStaged(payload: any) {
    return request<any>('/candidates/from-staged', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  async parseCandidateResume(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    
    const token = localStorage.getItem('talentsphere_session_token');
    const headers: Record<string, string> = {};
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/candidates/parse`, {
        method: 'POST',
        headers,
        body: formData,
      });

      if (!response.ok) {
        return null;
      }
      return await response.json();
    } catch (err) {
      console.warn('[parseCandidateResume] Failed:', err);
      return null;
    }
  },

  async uploadCandidateResume(candidateId: string, file: File) {
    const formData = new FormData();
    formData.append('file', file);
    
    const token = localStorage.getItem('talentsphere_session_token');
    const headers: Record<string, string> = {};
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/candidates/${candidateId}/resume`, {
        method: 'POST',
        headers,
        body: formData,
      });

      if (!response.ok) return null;
      return await response.json();
    } catch (err) {
      console.warn('[uploadCandidateResume] Failed:', err);
      return null;
    }
  },

  async deleteCandidate(candidateId: string) {
    return request<any>(`/candidates/${candidateId}`, {
      method: 'DELETE',
    });
  },

  // Jobs & Recruitment
  async getJobs() {
    return request<any[]>('/recruitment/jobs');
  },

  async createJob(jobData: any) {
    return request<any>('/recruitment/jobs', {
      method: 'POST',
      body: JSON.stringify(jobData),
    });
  },

  async getApplications() {
    return request<any[]>('/recruitment/applications');
  },

  // AI Intelligence & Agents
  async getAgents() {
    return request<any[]>('/ai/agents');
  },

  async getTools() {
    return request<any[]>('/ai/tools');
  },

  async getKnowledgeDocs() {
    return request<any[]>('/ai/knowledge');
  },

  async getExecutions() {
    return request<any[]>('/ai/executions');
  },

  // Milestone 11 & Nemotron AgentRuntime
  async executeAgent(agentId: string, inputData: any, workflowId?: string) {
    return request<any>('/ai/execute', {
      method: 'POST',
      body: JSON.stringify({
        agent_id: agentId,
        input_data: inputData,
        workflow_id: workflowId,
      }),
    });
  },

  async resumeExecution(executionId: string, decision: string, reason?: string) {
    return request<any>(`/ai/executions/${executionId}/resume`, {
      method: 'POST',
      body: JSON.stringify({
        decision,
        decision_reason: reason,
      }),
    });
  },

  async getExecutionEvents(executionId: string) {
    return request<any>(`/ai/executions/${executionId}/events`);
  },

  // Milestone 12 Intelligent Sourcing & Candidate Discovery
  async executeSourcing(jobId: string, weights?: any) {
    return request<any>('/ai/sourcing/execute', {
      method: 'POST',
      body: JSON.stringify({
        job_id: jobId,
        weights,
      }),
    });
  },

  async getSourcingExecution(executionId: string) {
    return request<any>(`/ai/sourcing/executions/${executionId}`);
  },

  async getSourcingRecommendations(executionId: string) {
    return request<any>(`/ai/sourcing/executions/${executionId}/recommendations`);
  },

  async resumeSourcing(executionId: string, decision: string, reason?: string) {
    return request<any>(`/ai/sourcing/executions/${executionId}/resume`, {
      method: 'POST',
      body: JSON.stringify({
        decision,
        decision_reason: reason,
      }),
    });
  },

  // Organization
  async getOrganizations() {
    return request<any[]>('/organizations/');
  },

  async createOrganization(orgData: any) {
    return request<any>('/organizations/', {
      method: 'POST',
      body: JSON.stringify(orgData),
    });
  },

  async getOrganization() {
    try {
      return await request<any>('/organizations/me');
    } catch (e) {
      console.warn('Current org not found, likely Super Admin');
      return null;
    }
  },

  async getBranches() {
    return request<any>('/organizations/branches');
  },

  async getDepartments() {
    return request<any>('/organizations/departments');
  },

  async getDesignations() {
    return request<any>('/organizations/designations');
  },

  // Hiring Plans
  async getHiringPlans() {
    return request<any[]>('/recruitment/hiring-plans');
  },

  async createHiringPlan(planData: any) {
    return request<any>('/recruitment/hiring-plans', {
      method: 'POST',
      body: JSON.stringify(planData),
    });
  },

  // Offers
  async getOffers() {
    return request<any[]>('/offers/');
  },

  async createOffer(offerData: any) {
    return request<any>('/offers/', {
      method: 'POST',
      body: JSON.stringify(offerData),
    });
  },

  // Background Verifications
  async getBackgroundChecks() {
    return request<any[]>('/offers/background-verifications');
  },

  async initiateBGV(bgvData: any) {
    return request<any>('/offers/background-verifications', {
      method: 'POST',
      body: JSON.stringify(bgvData),
    });
  },

  // Onboarding
  async getOnboardingPlans() {
    return request<any[]>('/offers/onboarding/plans');
  },

  async createOnboardingPlan(planData: any) {
    return request<any>('/offers/onboarding/plans', {
      method: 'POST',
      body: JSON.stringify(planData),
    });
  },

  // Interviews
  async getInterviews() {
    return request<any[]>('/interviews/');
  },

  async createInterview(interviewData: any) {
    return request<any>('/interviews/', {
      method: 'POST',
      body: JSON.stringify(interviewData),
    });
  },

  // Milestone 13 — AI Recruitment Copilot
  async copilotChat(message: string, conversationId?: string, context?: any) {
    return request<any>('/ai/copilot/chat', {
      method: 'POST',
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
        context: context || {},
      }),
    });
  },

  async getCopilotConversations() {
    return request<any[]>('/ai/copilot/conversations');
  },

  async getCopilotMessages(conversationId: string) {
    return request<any[]>(`/ai/copilot/conversations/${conversationId}/messages`);
  },

  async resumeCopilotExecution(executionId: string, decision: string, reason?: string) {
    return request<any>(`/ai/copilot/executions/${executionId}/resume`, {
      method: 'POST',
      body: JSON.stringify({
        decision,
        decision_reason: reason,
      }),
    });
  },
};

export const platformApi = {
  async getMetrics() {
    return request<any>('/platform/metrics');
  },
  async getOrganizations() {
    return request<any[]>('/platform/organizations');
  },
  async createOrganization(data: any) {
    return request<any>('/platform/organizations', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
  async activateOrganization(orgId: string) {
    return request<any>(`/platform/organizations/${orgId}/activate`, { method: 'POST' });
  },
  async suspendOrganization(orgId: string) {
    return request<any>(`/platform/organizations/${orgId}/suspend`, { method: 'POST' });
  },
  async provisionOrgAdmin(orgId: string, adminData: any) {
    return request<any>(`/platform/organizations/${orgId}/admin`, {
      method: 'POST',
      body: JSON.stringify(adminData),
    });
  },
  async getRoles() {
    return request<any[]>('/platform/roles');
  },
  async getPermissions() {
    return request<any>('/platform/permissions');
  },
  async getAuditLogs() {
    return request<any[]>('/platform/audit');
  },
};

export const orgAdminApi = {
  async getUsers() {
    return request<any[]>('/organization/users');
  },
  async createUser(userData: any) {
    return request<any>('/organization/users', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  },
  async getRoles() {
    return request<any[]>('/organization/roles');
  },
  async createCustomRole(roleData: any) {
    return request<any>('/organization/roles', {
      method: 'POST',
      body: JSON.stringify(roleData),
    });
  },
  async getPermissions() {
    return request<any[]>('/organization/permissions');
  },
  async getSettings() {
    return request<any[]>('/organization/settings');
  },
};
