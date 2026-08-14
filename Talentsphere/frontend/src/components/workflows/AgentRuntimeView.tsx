import React, { useState, useEffect } from 'react';
import {
  Activity,
  Terminal,
  Cpu,
  Eye
} from 'lucide-react';
import { AIExecutionItem } from '../../types';
import { aiIntelligenceApi } from '../../api';

export const AgentRuntimeView: React.FC = () => {
  const [executions, setExecutions] = useState<AIExecutionItem[]>([]);
  const [selectedExecution, setSelectedExecution] = useState<AIExecutionItem | null>(null);

  useEffect(() => {
    aiIntelligenceApi.getExecutions().then(setExecutions);
  }, []);

  return (
    <div className="space-y-6 text-left animate-fade-in">
      {/* Header Banner */}
      <div className="p-6 rounded-2xl glass-card flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full glass-panel text-xs font-mono font-medium mb-2 dark:text-zinc-300 light:text-zinc-700">
            <Cpu className="w-3.5 h-3.5 text-zinc-400" /> Milestone 11: AgentRuntime &amp; Orchestration
          </div>
          <h1 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight">Agent Runtime Execution &amp; Traces</h1>
          <p className="text-xs dark:text-zinc-400 light:text-zinc-600 mt-1 font-normal">
            Real-time execution telemetry, LangGraph runtime loops, execution timelines, token usage, and latency tracking.
          </p>
        </div>

        <div className="flex items-center gap-3 shrink-0 font-mono text-xs text-emerald-600 dark:text-emerald-400 font-medium">
          <Activity className="w-4 h-4 text-emerald-400" /> Runtime Operational
        </div>
      </div>

      {/* KPI Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl glass-card space-y-1">
          <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-500 uppercase font-medium">Executions Today</span>
          <p className="text-2xl font-medium dark:text-white light:text-zinc-900 font-mono">1,420</p>
        </div>
        <div className="p-4 rounded-xl glass-card space-y-1">
          <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-500 uppercase font-medium">Avg Execution Time</span>
          <p className="text-2xl font-medium dark:text-zinc-200 light:text-zinc-800 font-mono">1.24s</p>
        </div>
        <div className="p-4 rounded-xl glass-card space-y-1">
          <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-500 uppercase font-medium">Tokens Processed</span>
          <p className="text-2xl font-medium dark:text-zinc-200 light:text-zinc-800 font-mono">1.28M</p>
        </div>
        <div className="p-4 rounded-xl glass-card space-y-1">
          <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-500 uppercase font-medium">Success Rate</span>
          <p className="text-2xl font-medium text-emerald-600 dark:text-emerald-400 font-mono">99.8%</p>
        </div>
      </div>

      {/* Executions Table */}
      <div className="p-6 rounded-2xl glass-card space-y-4">
        <h3 className="text-sm font-medium dark:text-white light:text-zinc-900 flex items-center gap-2">
          <Terminal className="w-4 h-4 text-zinc-400" /> Agent Execution Log &amp; Traces
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-zinc-200 dark:border-zinc-800 dark:text-zinc-400 light:text-zinc-600 font-mono uppercase text-[10px]">
                <th className="py-3 px-4 font-medium">Execution ID</th>
                <th className="py-3 px-4 font-medium">Agent Name</th>
                <th className="py-3 px-4 font-medium">Workflow</th>
                <th className="py-3 px-4 font-medium">Duration</th>
                <th className="py-3 px-4 font-medium">Tokens</th>
                <th className="py-3 px-4 font-medium">Status</th>
                <th className="py-3 px-4 text-right font-medium">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-200 dark:divide-zinc-800">
              {executions.map((ex) => (
                <tr key={ex.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-900/50 transition">
                  <td className="py-3 px-4 font-mono dark:text-zinc-300 light:text-zinc-700 font-medium">{ex.executionId}</td>
                  <td className="py-3 px-4 font-medium dark:text-white light:text-zinc-900">{ex.agentName}</td>
                  <td className="py-3 px-4 dark:text-zinc-300 light:text-zinc-700 font-normal">{ex.workflowName}</td>
                  <td className="py-3 px-4 font-mono dark:text-zinc-400 light:text-zinc-600">{ex.durationMs}ms</td>
                  <td className="py-3 px-4 font-mono dark:text-zinc-300 light:text-zinc-700 font-medium">{ex.tokensUsed.toLocaleString()}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2.5 py-1 rounded-lg text-[10px] font-mono font-medium ${ex.status === 'Completed' ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30' : 'glass-panel text-zinc-700 dark:text-zinc-300'
                      }`}>
                      {ex.status}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-right">
                    <button
                      onClick={() => setSelectedExecution(ex)}
                      className="px-3 py-1.5 rounded-lg glass-panel dark:text-zinc-200 light:text-zinc-800 font-medium transition inline-flex items-center gap-1 hover:bg-zinc-100 dark:hover:bg-zinc-800"
                    >
                      <Eye className="w-3.5 h-3.5 text-zinc-400" /> Execution Timeline
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Execution Timeline Modal */}
      {selectedExecution && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-md z-50 flex items-center justify-center p-4">
          <div className="glass-card rounded-2xl w-full max-w-xl overflow-hidden shadow-2xl">
            <div className="p-5 border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between glass-panel">
              <h3 className="text-sm font-medium dark:text-white light:text-zinc-900 font-mono">Trace Timeline: {selectedExecution.executionId}</h3>
              <button onClick={() => setSelectedExecution(null)} className="dark:text-zinc-400 light:text-zinc-600 hover:text-zinc-900 dark:hover:text-white text-xs font-medium">
                Close
              </button>
            </div>
            <div className="p-6 space-y-4 font-mono text-xs">
              <div className="p-3.5 rounded-xl glass-panel space-y-1">
                <span className="dark:text-zinc-400 light:text-zinc-600 text-[10px] block">Safe AI Reasoning Summary</span>
                <p className="leading-relaxed dark:text-zinc-200 light:text-zinc-800">{selectedExecution.reasoningSummary}</p>
              </div>

              <div className="space-y-2">
                <span className="text-[10px] dark:text-zinc-400 light:text-zinc-600 uppercase block font-medium">Execution Steps Timeline</span>
                <div className="p-3 rounded-lg glass-panel text-[11px] dark:text-zinc-300 light:text-zinc-700 space-y-2">
                  <div className="flex justify-between border-b border-zinc-200 dark:border-zinc-800 pb-1">
                    <span>09:41:12 PST</span>
                    <span className="text-emerald-600 dark:text-emerald-400 font-medium">Request Received &amp; Validated</span>
                  </div>
                  <div className="flex justify-between border-b border-zinc-200 dark:border-zinc-800 pb-1">
                    <span>09:41:13 PST</span>
                    <span className="text-emerald-600 dark:text-emerald-400 font-medium">Nemotron 3 Ultra Decision Engine Initialized</span>
                  </div>
                  <div className="flex justify-between border-b border-zinc-200 dark:border-zinc-800 pb-1">
                    <span>09:41:14 PST</span>
                    <span className="text-emerald-600 dark:text-emerald-400 font-medium">Vector Search pgvector Cosine Traversal</span>
                  </div>
                  <div className="flex justify-between">
                    <span>09:41:15 PST</span>
                    <span className="dark:text-white light:text-zinc-900 font-medium">Execution Completed Successfully</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
