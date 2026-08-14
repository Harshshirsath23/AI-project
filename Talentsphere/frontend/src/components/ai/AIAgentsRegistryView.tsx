import React, { useState, useEffect } from 'react';
import {
  Cpu,
  Activity,
  Eye
} from 'lucide-react';
import { AIAgentDetail } from '../../types';
import { aiIntelligenceApi } from '../../api';

export const AIAgentsRegistryView: React.FC = () => {
  const [agents, setAgents] = useState<AIAgentDetail[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<AIAgentDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    aiIntelligenceApi.getAgents().then((data) => {
      setAgents(data);
      setLoading(false);
    });
  }, []);

  return (
    <div className="space-y-6 text-left animate-fade-in">
      {/* Header Banner */}
      <div className="p-6 rounded-2xl glass-card flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full glass-panel dark:text-zinc-300 light:text-zinc-700 text-xs font-mono font-medium mb-2">
            <Cpu className="w-3.5 h-3.5 text-zinc-400" /> AI Intelligence OS
          </div>
          <h1 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight">AI Agent Registry &amp; Capabilities</h1>
          <p className="text-xs dark:text-zinc-400 light:text-zinc-600 mt-1 font-normal">
            Governance control plane for autonomous recruitment agents, prompt versions, tool permissions, and risk levels.
          </p>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <span className="px-3 py-1.5 rounded-xl glass-panel text-xs font-mono dark:text-zinc-300 light:text-zinc-700 font-medium flex items-center gap-1.5">
            <Activity className="w-3.5 h-3.5 text-emerald-400" /> 3 Agents Operational
          </span>
        </div>
      </div>

      {/* Agent Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {agents.map((ag) => (
          <div key={ag.id} className="p-5 rounded-2xl glass-card flex flex-col justify-between space-y-4 group hover:border-zinc-400 dark:hover:border-zinc-600 transition">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-mono font-medium uppercase dark:text-zinc-500 light:text-zinc-400">{ag.category}</span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-medium uppercase border ${ag.riskLevel === 'LOW' ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-600 dark:text-emerald-400' : 'glass-panel text-zinc-700 dark:text-zinc-300'
                  }`}>
                  Risk: {ag.riskLevel}
                </span>
              </div>

              <div>
                <h3 className="text-sm font-medium dark:text-white light:text-zinc-900 flex items-center gap-2">
                  <Cpu className="w-4 h-4 text-zinc-400 shrink-0" /> {ag.name}
                </h3>
                <span className="text-[10px] font-mono dark:text-zinc-500 light:text-zinc-400 block">Version {ag.version}</span>
              </div>

              <p className="text-xs dark:text-zinc-400 light:text-zinc-600 leading-relaxed line-clamp-2 font-normal">{ag.description}</p>
            </div>

            <div className="space-y-3 pt-3 border-t border-zinc-200 dark:border-zinc-800">
              <div className="grid grid-cols-2 gap-2 text-[11px] font-mono">
                <div>
                  <span className="dark:text-zinc-500 light:text-zinc-400 text-[10px] block">Success Rate</span>
                  <span className="text-emerald-600 dark:text-emerald-400 font-medium">{ag.successRate}%</span>
                </div>
                <div>
                  <span className="dark:text-zinc-500 light:text-zinc-400 text-[10px] block">Avg Latency</span>
                  <span className="dark:text-zinc-300 light:text-zinc-700 font-medium">{ag.avgLatencyMs}ms</span>
                </div>
              </div>

              <button
                onClick={() => setSelectedAgent(ag)}
                className="w-full py-2 rounded-xl bg-zinc-900 dark:bg-zinc-900 light:bg-zinc-100 dark:text-white light:text-zinc-900 text-xs font-medium transition flex items-center justify-center gap-1.5 hover:bg-zinc-800 dark:hover:bg-zinc-800"
              >
                <Eye className="w-3.5 h-3.5 text-zinc-400" /> Inspect Agent Traces
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Agent Detail Modal Drawer */}
      {selectedAgent && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-md z-50 flex items-center justify-center p-4">
          <div className="glass-card rounded-2xl w-full max-w-2xl overflow-hidden shadow-2xl">
            <div className="p-5 border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between glass-panel">
              <div className="flex items-center gap-3">
                <Cpu className="w-5 h-5 text-zinc-400" />
                <div>
                  <h3 className="text-sm font-medium dark:text-white light:text-zinc-900">{selectedAgent.name}</h3>
                  <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-600">Version {selectedAgent.version}</span>
                </div>
              </div>
              <button onClick={() => setSelectedAgent(null)} className="dark:text-zinc-400 light:text-zinc-600 hover:text-zinc-900 dark:hover:text-white text-xs font-medium">
                Close
              </button>
            </div>

            <div className="p-6 space-y-4 max-h-[75vh] overflow-y-auto custom-scrollbar">
              <div className="p-3.5 rounded-xl glass-panel space-y-2">
                <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-600 uppercase font-medium block">System Prompt Spec</span>
                <p className="text-xs font-mono dark:text-zinc-300 light:text-zinc-700 leading-relaxed">{selectedAgent.prompt}</p>
              </div>

              <div className="space-y-2">
                <span className="text-xs font-medium dark:text-white light:text-zinc-900 font-mono uppercase block">Bound Tools</span>
                <div className="flex flex-wrap gap-2">
                  {selectedAgent.tools.map((t, idx) => (
                    <span key={idx} className="px-2.5 py-1 rounded-lg glass-panel text-xs font-mono dark:text-zinc-300 light:text-zinc-700">
                      🔧 {t}
                    </span>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <span className="text-xs font-medium dark:text-white light:text-zinc-900 font-mono uppercase block">RBAC Permissions Scope</span>
                <div className="flex flex-wrap gap-2">
                  {selectedAgent.permissions.map((p, idx) => (
                    <span key={idx} className="px-2.5 py-1 rounded-lg glass-panel text-xs font-mono dark:text-zinc-300 light:text-zinc-700">
                      🔒 {p}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
