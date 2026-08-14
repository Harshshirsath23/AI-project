import React, { useState, useEffect } from 'react';
import {
  ShieldAlert,
  CheckCircle,
  Check,
  X
} from 'lucide-react';
import { HITLTask } from '../../types';
import { aiIntelligenceApi } from '../../api';

export const HITLCenterView: React.FC = () => {
  const [tasks, setTasks] = useState<HITLTask[]>([]);

  useEffect(() => {
    aiIntelligenceApi.getHitlTasks().then(setTasks);
  }, []);

  const handleAction = (id: string, action: 'Approved' | 'Rejected') => {
    setTasks(tasks.map((t) => (t.id === id ? { ...t, status: action } : t)));
  };

  return (
    <div className="space-y-6 text-left animate-fade-in">
      {/* Header Banner */}
      <div className="p-6 rounded-2xl glass-card flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full glass-panel dark:text-zinc-300 light:text-zinc-700 text-xs font-mono font-medium mb-2">
            <ShieldAlert className="w-3.5 h-3.5 text-zinc-400" /> Human-in-the-Loop Governance
          </div>
          <h1 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight">HITL Approval &amp; Accountability Center</h1>
          <p className="text-xs dark:text-zinc-400 light:text-zinc-600 mt-1 font-normal">
            Mandatory review control plane for high-risk AI recommendations, offer exceptions, and automated candidate shortlist dispatches.
          </p>
        </div>

        <div className="p-3 rounded-xl glass-panel text-xs font-mono font-medium shrink-0 text-center dark:text-zinc-300 light:text-zinc-700">
          AI Assists. Humans Remain Accountable.
        </div>
      </div>

      {/* HITL Tasks Grid */}
      <div className="space-y-4">
        {tasks.map((task) => (
          <div
            key={task.id}
            className="p-6 rounded-2xl glass-card space-y-4"
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-zinc-200 dark:border-zinc-800 pb-3">
              <div className="flex items-center gap-2">
                <span className="px-2.5 py-0.5 rounded glass-panel text-[10px] font-mono font-medium uppercase dark:text-zinc-300 light:text-zinc-700">
                  Agent: {task.agentName}
                </span>
                <span className="text-xs dark:text-zinc-400 light:text-zinc-500 font-mono">• {task.timestamp}</span>
              </div>
              <span
                className={`px-3 py-1 rounded-full text-xs font-mono font-medium ${task.status === 'Pending'
                    ? 'glass-panel dark:text-zinc-200 light:text-zinc-800 font-semibold'
                    : task.status === 'Approved'
                      ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30'
                      : 'bg-red-500/10 text-red-600 dark:text-red-400 border border-red-500/30'
                  }`}
              >
                {task.status === 'Pending' ? 'Action Required' : task.status}
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="md:col-span-2 space-y-3">
                <h3 className="text-sm font-medium dark:text-white light:text-zinc-900">{task.title}</h3>
                <p className="text-xs dark:text-zinc-300 light:text-zinc-700 leading-relaxed font-mono glass-panel p-3 rounded-xl">
                  <span className="dark:text-zinc-400 light:text-zinc-600 font-medium block mb-1">Proposed AI Action:</span>
                  {task.recommendation}
                </p>

                <div className="space-y-1">
                  <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-500 uppercase font-medium">Verified Evidence &amp; Signals</span>
                  <div className="space-y-1">
                    {task.evidence.map((ev, idx) => (
                      <div key={idx} className="flex items-center gap-2 text-xs dark:text-zinc-300 light:text-zinc-700">
                        <CheckCircle className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400 shrink-0" />
                        <span>{ev}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="p-4 rounded-xl glass-panel flex flex-col justify-between space-y-4">
                <div className="space-y-3">
                  <div className="flex justify-between items-center text-xs">
                    <span className="dark:text-zinc-400 light:text-zinc-500">Confidence:</span>
                    <span className="font-mono text-emerald-600 dark:text-emerald-400 font-medium">{Math.round(task.confidenceScore * 100)}%</span>
                  </div>
                  <div className="flex justify-between items-center text-xs">
                    <span className="dark:text-zinc-400 light:text-zinc-500">Risk Level:</span>
                    <span className="font-mono dark:text-zinc-200 light:text-zinc-800 font-medium">{task.riskLevel || 'HIGH'}</span>
                  </div>
                  <div className="flex justify-between items-center text-xs border-t border-zinc-200 dark:border-zinc-800 pt-2">
                    <span className="dark:text-zinc-400 light:text-zinc-500">Impact:</span>
                    <span className="text-xs dark:text-zinc-200 light:text-zinc-800 font-medium">{task.impact || 'High Executive Impact'}</span>
                  </div>
                </div>

                {task.status === 'Pending' && (
                  <div className="grid grid-cols-2 gap-2 pt-2">
                    <button
                      onClick={() => handleAction(task.id, 'Approved')}
                      className="py-2 rounded-xl bg-zinc-900 text-white text-xs font-medium transition flex items-center justify-center gap-1 hover:bg-zinc-800"
                    >
                      <Check className="w-3.5 h-3.5" /> Approve
                    </button>
                    <button
                      onClick={() => handleAction(task.id, 'Rejected')}
                      className="py-2 rounded-xl glass-panel text-zinc-700 dark:text-zinc-300 text-xs font-medium transition flex items-center justify-center gap-1 hover:bg-zinc-100 dark:hover:bg-zinc-800"
                    >
                      <X className="w-3.5 h-3.5" /> Reject
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
