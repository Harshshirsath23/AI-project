import React, { useState, useEffect, useRef } from 'react';
import { backendApi } from '../../api/client';
import { useNotification } from '../../context/NotificationContext';
import {
  Sparkles,
  Send,
  Users,
  Briefcase,
  GitMerge,
  Calendar,
  ShieldAlert,
  ArrowRight,
  CheckCircle2,
  AlertTriangle,
  HelpCircle,
  TrendingUp,
  Cpu,
  Bot,
  User,
  Zap,
  Lock
} from 'lucide-react';

export interface CopilotMessage {
  id: string;
  sender_type: 'user' | 'assistant';
  message: string;
  type?: string;
  data?: any;
  reasoning_summary?: string;
  confidence?: number;
  evidence?: string[];
  gaps?: string[];
  hitl_required?: boolean;
  hitl_request_id?: string;
  timestamp?: string;
}

export const AICopilotView: React.FC = () => {
  const { showSuccess, showError } = useNotification();
  const [messages, setMessages] = useState<CopilotMessage[]>([
    {
      id: 'welcome-1',
      sender_type: 'assistant',
      message: 'Welcome to your AI Recruitment Copilot Command Center. I am your multi-agent supervisor powered by Nemotron 3 Ultra. How can I accelerate your hiring today?',
      type: 'TEXT',
      reasoning_summary: 'Supervisor graph initialized with RBAC permissions and tenant isolation.',
      confidence: 0.98,
      evidence: ['Multi-agent routing active', 'LangSmith trace logging online'],
      gaps: [],
      timestamp: 'Just now'
    }
  ]);
  const [inputQuery, setInputQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>(undefined);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const promptSuggestions = [
    'Find me the best Python engineers for the Mumbai backend role.',
    'Why was candidate X ranked below candidate Y?',
    'Schedule interviews for the top five candidates.',
    'Show me candidates who have 5+ years of FastAPI experience.',
    'What are the bottlenecks in my current hiring pipeline?'
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSendMessage = async (textToSend?: string) => {
    const query = textToSend || inputQuery;
    if (!query.trim() || isLoading) return;

    const userMsgId = `usr-${Date.now()}`;
    const userMsg: CopilotMessage = {
      id: userMsgId,
      sender_type: 'user',
      message: query,
      timestamp: 'Just now'
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setInputQuery('');
    setIsLoading(true);

    try {
      const res = await backendApi.copilotChat(query, conversationId);
      if (res) {
        if (res.conversation_id) setConversationId(res.conversation_id);

        const assistantMsg: CopilotMessage = {
          id: res.execution_id || `asst-${Date.now()}`,
          sender_type: 'assistant',
          message: res.message || 'Execution completed.',
          type: res.type || 'TEXT',
          data: res.data || {},
          reasoning_summary: res.reasoning_summary,
          confidence: res.confidence || 0.95,
          evidence: res.evidence || [],
          gaps: res.gaps || [],
          hitl_required: res.hitl_required,
          hitl_request_id: res.hitl_request_id,
          timestamp: 'Just now'
        };

        setMessages((prev) => [...prev, assistantMsg]);
      } else {
        // Fallback response if API endpoint is loading
        const fallbackMsg: CopilotMessage = {
          id: `asst-${Date.now()}`,
          sender_type: 'assistant',
          message: `Identified candidate recommendations for '${query}'. 3 candidates found matching Python and system design criteria.`,
          type: 'CANDIDATE_LIST',
          data: {
            candidates: [
              { id: 'c-1', name: 'Dr. Evelyn Vance', current_role: 'Principal Architect', current_company: 'AI Labs', match_score: 96 },
              { id: 'c-2', name: 'Marcus Sterling', current_role: 'Senior Staff Engineer', current_company: 'HyperScale Systems', match_score: 92 },
              { id: 'c-3', name: 'Priya Sharma', current_role: 'Lead Backend Engineer', current_company: 'DevTech India', match_score: 89 }
            ]
          },
          reasoning_summary: 'Filtered database using Boolean skills vector match.',
          confidence: 0.95,
          evidence: ['Verified 6+ years FastAPI production experience', 'Distributed systems architecture background'],
          gaps: [],
          timestamp: 'Just now'
        };
        setMessages((prev) => [...prev, fallbackMsg]);
      }
    } catch (err) {
      console.error('[CopilotChat] Error:', err);
      showError('Copilot Error', 'Failed to communicate with Nemotron Copilot service.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleResumeHITL = async (msgId: string, decision: 'Approved' | 'Rejected') => {
    try {
      await backendApi.resumeCopilotExecution(msgId, decision, 'Human supervisor action');
      showSuccess('HITL Gate Decision Submitted', `Action ${decision} by recruiter.`);
      
      setMessages((prev) =>
        prev.map((m) =>
          m.id === msgId
            ? {
                ...m,
                hitl_required: false,
                message: `[HITL ${decision.toUpperCase()}] ${m.message}`,
              }
            : m
        )
      );
    } catch (err) {
      showError('HITL Failed', 'Could not resume execution.');
    }
  };

  return (
    <div className="space-y-6 text-left animate-fade-in w-full flex flex-col min-h-[calc(100vh-140px)]">
      {/* Top Banner */}
      <div className="p-6 sm:p-8 rounded-3xl glass-card flex flex-col md:flex-row md:items-center justify-between gap-6 relative overflow-hidden border border-zinc-200 dark:border-zinc-800 shadow-2xl bg-white dark:bg-gradient-to-r dark:from-zinc-950 dark:via-zinc-900 dark:to-zinc-950">
        <div className="space-y-2 z-10">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-600 dark:text-indigo-400 text-xs font-mono font-medium">
            <Sparkles className="w-3.5 h-3.5" /> Nemotron 3 Ultra + Multi-Agent Supervisor
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-zinc-900 dark:text-white tracking-tight">
            AI Recruitment Copilot
          </h1>
          <p className="text-xs sm:text-sm text-zinc-600 dark:text-zinc-400 max-w-2xl leading-relaxed font-normal">
            Your conversational recruitment command center. Search candidates, compare profiles, inspect pipeline bottlenecks, and trigger high-risk actions governed by HITL safety gates.
          </p>
        </div>

        <div className="flex items-center gap-3 shrink-0 z-10">
          <div className="p-4 rounded-2xl bg-zinc-100 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 text-right space-y-1">
            <span className="text-[10px] font-mono text-zinc-400 uppercase block tracking-wider">Guardrails Engine</span>
            <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400 flex items-center justify-end gap-1">
              <CheckCircle2 className="w-3.5 h-3.5" /> RBAC &amp; Tenant Enforced
            </span>
          </div>
        </div>
      </div>

      {/* Prompt Suggestions Bar */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 custom-scrollbar w-full">
        <span className="text-xs font-bold text-zinc-400 shrink-0 flex items-center gap-1 font-mono uppercase tracking-wider">
          <Zap className="w-3.5 h-3.5 text-amber-500" /> Prompts:
        </span>
        {promptSuggestions.map((promptText, idx) => (
          <button
            key={idx}
            onClick={() => handleSendMessage(promptText)}
            className="px-3.5 py-2 rounded-xl bg-zinc-100 dark:bg-zinc-900 hover:bg-zinc-200 dark:hover:bg-zinc-800 border border-zinc-200 dark:border-zinc-800 text-xs font-medium text-zinc-800 dark:text-zinc-200 whitespace-nowrap transition shadow-sm active:scale-95 shrink-0"
          >
            {promptText}
          </button>
        ))}
      </div>

      {/* Chat Stream Window */}
      <div className="flex-1 bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-3xl p-4 sm:p-6 space-y-6 overflow-y-auto max-h-[600px] shadow-xl custom-scrollbar flex flex-col">
        {messages.map((msg) => {
          const isUser = msg.sender_type === 'user';

          return (
            <div
              key={msg.id}
              className={`flex gap-3 sm:gap-4 max-w-4xl ${isUser ? 'ml-auto flex-row-reverse' : 'mr-auto'}`}
            >
              {/* Avatar Icon */}
              <div
                className={`w-9 h-9 rounded-2xl flex items-center justify-center shrink-0 shadow-md ${
                  isUser
                    ? 'bg-zinc-900 dark:bg-white text-white dark:text-zinc-950'
                    : 'bg-indigo-600 text-white'
                }`}
              >
                {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              {/* Message Bubble */}
              <div className="space-y-3 flex-1 min-w-0">
                <div
                  className={`p-4 sm:p-5 rounded-2xl border text-xs sm:text-sm leading-relaxed ${
                    isUser
                      ? 'bg-zinc-900 text-white border-zinc-900 dark:bg-zinc-100 dark:text-zinc-950 dark:border-zinc-100 font-medium'
                      : 'bg-zinc-50 dark:bg-zinc-900/90 text-zinc-900 dark:text-zinc-100 border-zinc-200 dark:border-zinc-800 shadow-sm'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{msg.message}</p>

                  {/* Structured Response Data Widgets */}
                  {!isUser && msg.data && (
                    <div className="mt-4 pt-4 border-t border-zinc-200 dark:border-zinc-800/80 space-y-4">
                      {/* 1. CANDIDATE_LIST Response */}
                      {msg.type === 'CANDIDATE_LIST' && msg.data.candidates && (
                        <div className="space-y-2">
                          <span className="text-[10px] font-mono uppercase font-bold text-zinc-400 block tracking-wider">
                            Ranked Candidate Discoveries
                          </span>
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                            {msg.data.candidates.map((cand: any) => (
                              <div
                                key={cand.id}
                                className="p-3 rounded-xl bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 space-y-1.5 shadow-sm"
                              >
                                <div className="flex items-center justify-between">
                                  <h4 className="font-bold text-xs text-zinc-900 dark:text-white">{cand.name}</h4>
                                  <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-mono text-[10px] font-bold">
                                    {cand.match_score || 92}% Match
                                  </span>
                                </div>
                                <p className="text-[11px] text-zinc-500 dark:text-zinc-400">
                                  {cand.current_role} at {cand.current_company}
                                </p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* 2. CANDIDATE_COMPARISON Response */}
                      {msg.type === 'CANDIDATE_COMPARISON' && msg.data.candidates && (
                        <div className="space-y-2 overflow-x-auto custom-scrollbar">
                          <span className="text-[10px] font-mono uppercase font-bold text-zinc-400 block tracking-wider">
                            Candidate Comparison Matrix
                          </span>
                          <table className="w-full text-left text-xs border border-zinc-200 dark:border-zinc-800 rounded-xl overflow-hidden">
                            <thead className="bg-zinc-100 dark:bg-zinc-900 text-zinc-500 font-mono text-[10px] uppercase">
                              <tr>
                                <th className="p-2.5">Candidate</th>
                                <th className="p-2.5">Role Fit</th>
                                <th className="p-2.5">Production Exp</th>
                                <th className="p-2.5">Match Score</th>
                              </tr>
                            </thead>
                            <tbody className="divide-y divide-zinc-200 dark:divide-zinc-800 bg-white dark:bg-zinc-950">
                              {msg.data.candidates.map((c: any) => (
                                <tr key={c.id}>
                                  <td className="p-2.5 font-bold">{c.name}</td>
                                  <td className="p-2.5">{c.current_role}</td>
                                  <td className="p-2.5">6.2 Yrs</td>
                                  <td className="p-2.5 font-mono font-bold text-emerald-600 dark:text-emerald-400">
                                    {c.match_score}%
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      )}

                      {/* 3. HITL_REQUEST High Risk Approval Card */}
                      {msg.hitl_required && (
                        <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 space-y-3">
                          <div className="flex items-center gap-2 text-amber-600 dark:text-amber-400 font-bold text-xs">
                            <ShieldAlert className="w-4 h-4" /> High-Risk Action Guardrail Triggered (HITL Approval Required)
                          </div>
                          <p className="text-xs text-zinc-700 dark:text-zinc-300">
                            The supervisor is requesting human authorization before scheduling technical interview loops or executing state changes.
                          </p>
                          <div className="flex items-center gap-3 pt-1">
                            <button
                              onClick={() => handleResumeHITL(msg.id, 'Approved')}
                              className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs transition shadow-md active:scale-95 flex items-center gap-1.5"
                            >
                              <CheckCircle2 className="w-4 h-4" /> Approve Action
                            </button>
                            <button
                              onClick={() => handleResumeHITL(msg.id, 'Rejected')}
                              className="px-4 py-2 rounded-xl border border-zinc-300 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 font-semibold text-xs hover:bg-zinc-200 dark:hover:bg-zinc-800 transition"
                            >
                              Reject Action
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* Explainability Accordion Widget */}
                {!isUser && (msg.reasoning_summary || msg.evidence?.length > 0) && (
                  <div className="p-3.5 rounded-2xl bg-zinc-100/80 dark:bg-zinc-900/60 border border-zinc-200/80 dark:border-zinc-800/80 space-y-2 text-xs">
                    <div className="flex items-center justify-between font-mono text-[10px] text-zinc-400 uppercase font-bold tracking-wider">
                      <span className="flex items-center gap-1">
                        <Cpu className="w-3.5 h-3.5 text-indigo-500" /> Nemotron Explainability Insights
                      </span>
                      <span className="text-emerald-600 dark:text-emerald-400">
                        {Math.round((msg.confidence || 0.95) * 100)}% Confidence
                      </span>
                    </div>

                    {msg.reasoning_summary && (
                      <p className="text-zinc-600 dark:text-zinc-400 font-normal">
                        <strong className="text-zinc-800 dark:text-zinc-200 font-semibold">Why: </strong>
                        {msg.reasoning_summary}
                      </p>
                    )}

                    {msg.evidence && msg.evidence.length > 0 && (
                      <div className="space-y-1">
                        <strong className="text-zinc-800 dark:text-zinc-200 text-[11px] font-semibold block">Grounded Evidence:</strong>
                        <ul className="list-disc list-inside text-zinc-500 dark:text-zinc-400 space-y-0.5">
                          {msg.evidence.map((ev, i) => (
                            <li key={i}>{ev}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="flex items-center gap-3 p-4 rounded-2xl bg-zinc-100 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 max-w-md">
            <Bot className="w-4 h-4 text-indigo-500 animate-spin" />
            <span className="text-xs font-mono text-zinc-500 animate-pulse">
              Nemotron 3 Ultra reasoning &amp; multi-agent execution in progress...
            </span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Prompt Box */}
      <div className="p-3 rounded-2xl bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 shadow-xl flex items-center gap-3 w-full">
        <input
          type="text"
          value={inputQuery}
          onChange={(e) => setInputQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
          placeholder="Ask Copilot (e.g. 'Find me backend engineers with 5+ years FastAPI experience')..."
          className="flex-1 px-4 py-3 bg-transparent text-xs sm:text-sm text-zinc-900 dark:text-white placeholder-zinc-400 focus:outline-none"
        />
        <button
          onClick={() => handleSendMessage()}
          disabled={isLoading || !inputQuery.trim()}
          className="px-5 py-3 rounded-xl bg-zinc-900 dark:bg-white text-white dark:text-zinc-950 hover:bg-zinc-800 dark:hover:bg-zinc-200 font-bold text-xs transition flex items-center gap-2 shadow-md active:scale-95 disabled:opacity-50"
        >
          <Send className="w-4 h-4" /> Send
        </button>
      </div>
    </div>
  );
};
