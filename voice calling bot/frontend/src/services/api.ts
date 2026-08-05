const API_BASE = "http://localhost:8000/api/v1";

export async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        "Content-Type": "application/json",
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

// Agents API
export const api = {
  getAgents: () => fetchApi<any[]>("/agents"),
  getAgentDetail: (id: string) => fetchApi<any>(`/agents/${id}`),
  createAgent: (data: any) => fetchApi<any>("/agents", { method: "POST", body: JSON.stringify(data) }),
  updateAgent: (id: string, data: any) => fetchApi<any>(`/agents/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteAgent: (id: string) => fetchApi<any>(`/agents/${id}`, { method: "DELETE" }),


  // Phone Numbers API
  getPhoneNumbers: () => fetchApi<any[]>("/phone-numbers"),
  createPhoneNumber: (data: any) => fetchApi<any>("/phone-numbers", { method: "POST", body: JSON.stringify(data) }),

  // Leads API
  getLeads: () => fetchApi<any[]>("/leads"),
  createLead: (data: any) => fetchApi<any>("/leads", { method: "POST", body: JSON.stringify(data) }),
  
  // Knowledge Base API
  getKnowledgeBases: () => fetchApi<any[]>("/knowledge-base"),
  getAllKnowledgeDocuments: () => fetchApi<any[]>("/knowledge-base/documents/all"),
  createKnowledgeBase: (data: any) => fetchApi<any>("/knowledge-base", { method: "POST", body: JSON.stringify(data) }),


  // Voices API
  getVoices: () => fetchApi<any[]>("/voices"),

  // Analytics API
  getAnalytics: () => fetchApi<any>("/analytics/overview"),

  // Campaigns API
  getCampaigns: () => fetchApi<any[]>("/campaigns"),
  createCampaign: (data: any) => fetchApi<any>("/campaigns", { method: "POST", body: JSON.stringify(data) }),

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
  testChat: (data: { agent_id: string; message: string; voice_id: string; llm_provider: string }) =>
    fetchApi<any>("/playground/chat", { method: "POST", body: JSON.stringify(data) }),
};


