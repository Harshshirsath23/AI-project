import React from 'react';
import { AIAgentStatus } from '../../types';
import { Cpu, Activity, RefreshCw } from 'lucide-react';

interface AIAgentStreamProps {
  agents: AIAgentStatus[];
}

export const AIAgentStream: React.FC<AIAgentStreamProps> = ({ agents }) => {
  return (
    <div className="p-5 rounded-2xl glass-card bg-neutral-950/80 dark:bg-neutral-950/80 light:bg-white border border-amber-500/20 dark:border-amber-500/20 light:border-amber-500/30 text-left space-y-4 shadow-xl">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20">
            <Cpu className="w-5 h-5 animate-pulse text-amber-400" />
          </div>
          <div>
            <h3 className="text-sm font-semibold dark:text-white light:text-slate-900 tracking-tight">
              Autonomous Agent Orchestrator
            </h3>
            <p className="text-[11px] dark:text-neutral-400 light:text-slate-500 font-medium">
              Multi-agent reasoning engine • Real-time pipeline monitoring
            </p>
          </div>
        </div>
        <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-medium flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
          4/4 Operational
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {agents.map((agent) => (
          <div
            key={agent.id}
            className="p-4 rounded-xl bg-black/60 dark:bg-black/60 light:bg-slate-50 border border-amber-500/20 dark:border-amber-500/20 light:border-slate-200 hover:border-amber-500/50 transition flex items-start justify-between gap-3"
          >
            <div className="space-y-1.5 flex-1">
              <div className="flex items-center gap-2">
                <span className="text-xs font-semibold dark:text-white light:text-slate-900">{agent.name}</span>
                <span
                  className={`text-[9px] font-mono font-medium uppercase tracking-wider px-2 py-0.5 rounded-full border ${
                    agent.status === 'active'
                      ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                      : agent.status === 'processing'
                      ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                      : 'bg-neutral-800 dark:bg-neutral-800 light:bg-slate-200 text-neutral-400 light:text-slate-600 border-neutral-700'
                  }`}
                >
                  {agent.status === 'processing' && <RefreshCw className="w-2.5 h-2.5 inline mr-1 animate-spin" />}
                  {agent.status}
                </span>
              </div>
              <p className="text-[11px] dark:text-neutral-400 light:text-slate-500 font-medium">{agent.category}</p>
              <p className="text-xs text-amber-400 light:text-amber-700 font-mono font-semibold">{agent.metric}</p>
            </div>
            <div className="text-right text-[10px] font-mono text-neutral-500 light:text-slate-400 shrink-0">
              Uptime {agent.uptime}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
