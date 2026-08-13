const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const token = localStorage.getItem("auth_token");
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...options?.headers,
      },
      ...options,
    });
    if (!res.ok) {
      throw new Error(`API Error ${res.status}: ${res.statusText}`);
    }
    return await res.json();
  } catch (err) {
    console.warn(`Fetch error for ${endpoint}:`, err);
    throw err;
  }
}

export const api = {
  // Auth API
  login: (data: { email: string; password: string; organization_slug?: string }) =>
    fetchApi<any>("/auth/login", { method: "POST", body: JSON.stringify(data) }),

  requestPasswordReset: (email: string) =>
    fetchApi<any>("/auth/reset-password", { method: "POST", body: JSON.stringify({ email }) }),
  getCurrentUser: () => fetchApi<any>("/auth/me"),
  logout: () => fetchApi<any>("/auth/logout", { method: "POST" }),

  // Agents API
  getAgents: () => fetchApi<any[]>("/agents"),
  getAgentDetail: (id: string) => fetchApi<any>(`/agents/${id}`),
  createAgent: (data: any) => fetchApi<any>("/agents", { method: "POST", body: JSON.stringify(data) }),
  updateAgent: (id: string, data: any) => fetchApi<any>(`/agents/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteAgent: (id: string) => fetchApi<any>(`/agents/${id}`, { method: "DELETE" }),

  // Phone Numbers API
  getPhoneNumbers: () => fetchApi<any[]>("/phone-numbers"),
  syncTwilioPhoneNumbers: () => fetchApi<any[]>("/phone-numbers/sync-twilio", { method: "POST" }),
  createPhoneNumber: (data: any) => fetchApi<any>("/phone-numbers", { method: "POST", body: JSON.stringify(data) }),


  // Leads API
  getLeads: () => fetchApi<any[]>("/leads"),
  createLead: (data: any) => fetchApi<any>("/leads", { method: "POST", body: JSON.stringify(data) }),
  createLeadsBulk: (leads: any[]) => fetchApi<any>("/leads/bulk", { method: "POST", body: JSON.stringify(leads) }),
  uploadLeadsCsv: async (file: File) => {
    const token = localStorage.getItem("auth_token");
    const formData = new FormData();
    formData.append("file", file);
    const res = await fetch(`${API_BASE}/leads/upload-csv`, {
      method: "POST",
      headers: {
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: formData,
    });
    if (!res.ok) {
      throw new Error(`CSV Upload Error ${res.status}: ${res.statusText}`);
    }
    return await res.json();
  },
  updateLead: (id: string, data: any) => fetchApi<any>(`/leads/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteLead: (id: string) => fetchApi<any>(`/leads/${id}`, { method: "DELETE" }),

  // Knowledge Base API
  getKnowledgeBases: () => fetchApi<any[]>("/knowledge-base"),
  getAllKnowledgeDocuments: () => fetchApi<any[]>("/knowledge-base/documents/all"),
  getKbDocuments: (kbId: string) => fetchApi<any[]>(`/knowledge-base/${kbId}/documents`),
  createKnowledgeBase: (data: any) => fetchApi<any>("/knowledge-base", { method: "POST", body: JSON.stringify(data) }),
  createKbTextDocument: (kbId: string, data: { title: string; script_text: string }) =>
    fetchApi<any>(`/knowledge-base/${kbId}/documents/text`, { method: "POST", body: JSON.stringify(data) }),
  updateKbDocument: (docId: string, data: { title: string; content: string }) =>
    fetchApi<any>(`/knowledge-base/documents/${docId}`, { method: "PUT", body: JSON.stringify(data) }),

  // Voices API
  getVoices: () => fetchApi<any[]>("/voices"),

  // Analytics API
  getAnalytics: () => fetchApi<any>("/analytics/overview"),

  // Campaigns API
  getCampaigns: () => fetchApi<any[]>("/campaigns"),
  getCampaignDetail: (id: string) => fetchApi<any>(`/campaigns/${id}`),
  createCampaign: (data: any) => fetchApi<any>("/campaigns", { method: "POST", body: JSON.stringify(data) }),
  updateCampaign: (id: string, data: any) => fetchApi<any>(`/campaigns/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteCampaign: (id: string) => fetchApi<any>(`/campaigns/${id}`, { method: "DELETE" }),
  startCampaign: (id: string) => fetchApi<any>(`/campaigns/${id}/start`, { method: "POST" }),
  pauseCampaign: (id: string) => fetchApi<any>(`/campaigns/${id}/pause`, { method: "POST" }),
  stopCampaign: (id: string) => fetchApi<any>(`/campaigns/${id}/stop`, { method: "POST" }),

  // Calls API
  getCalls: () => fetchApi<any[]>("/calls"),
  getLiveCalls: () => fetchApi<any[]>("/calls/live"),
  startCall: (data: { agent_id: string; from_number: string; to_number: string; lead_id?: string }) =>
    fetchApi<any>("/calls/start", { method: "POST", body: JSON.stringify(data) }),
  terminateCall: (callId: string) =>
    fetchApi<any>(`/calls/${callId}/terminate`, { method: "POST" }),

  // Settings API
  getSettings: () => fetchApi<any>("/settings"),
  updateSettings: (data: any) => fetchApi<any>("/settings", { method: "PUT", body: JSON.stringify(data) }),

  // Playground Chat API
  testChat: (data: any) =>
    fetchApi<any>("/playground/chat", { method: "POST", body: JSON.stringify(data) }),
};
