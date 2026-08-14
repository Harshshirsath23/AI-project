import React, { useState, useEffect } from 'react';
import { Wrench, AlertTriangle } from 'lucide-react';
import { AIToolItem } from '../../types';
import { aiIntelligenceApi } from '../../api';

export const AIToolsRegistryView: React.FC = () => {
  const [tools, setTools] = useState<AIToolItem[]>([]);

  useEffect(() => {
    aiIntelligenceApi.getTools().then(setTools);
  }, []);

  return (
    <div className="space-y-6 text-left animate-fade-in">
      <div className="p-6 rounded-2xl glass-card flex items-center justify-between">
        <div>
          <h1 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight flex items-center gap-2">
            <Wrench className="w-5 h-5 dark:text-zinc-300 light:text-zinc-700" /> AI Tool Registry &amp; Risk Classifications
          </h1>
          <p className="text-xs dark:text-zinc-400 light:text-zinc-600 mt-1 font-normal">
            Registered tools accessible by AI Agents with explicit risk boundary classifications and mandatory HITL enforcement.
          </p>
        </div>
      </div>

      <div className="p-6 rounded-2xl glass-card">
        <div className="overflow-x-auto custom-scrollbar">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-zinc-200 dark:border-zinc-800 dark:text-zinc-400 light:text-zinc-600 font-mono uppercase text-[10px]">
                <th className="py-3 px-4 font-medium">Tool Name</th>
                <th className="py-3 px-4 font-medium">Category</th>
                <th className="py-3 px-4 font-medium">Risk Level</th>
                <th className="py-3 px-4 font-medium">HITL Mandatory</th>
                <th className="py-3 px-4 font-medium">Permissions Required</th>
                <th className="py-3 px-4 font-medium">Executions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-200 dark:divide-zinc-800">
              {tools.map((tl) => (
                <tr key={tl.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-900/50 transition">
                  <td className="py-3 px-4 font-mono font-medium dark:text-white light:text-zinc-900">{tl.name}</td>
                  <td className="py-3 px-4 dark:text-zinc-300 light:text-zinc-700 font-normal">{tl.category}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2.5 py-1 rounded-lg text-[10px] font-mono font-medium uppercase border ${tl.riskLevel === 'LOW'
                        ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-600 dark:text-emerald-400'
                        : 'glass-panel text-zinc-700 dark:text-zinc-300'
                      }`}>
                      {tl.riskLevel}
                    </span>
                  </td>
                  <td className="py-3 px-4 font-mono">
                    {tl.hitlRequired ? (
                      <span className="dark:text-zinc-200 light:text-zinc-800 font-medium inline-flex items-center gap-1">
                        <AlertTriangle className="w-3.5 h-3.5 text-zinc-400" /> Enforced
                      </span>
                    ) : (
                      <span className="text-emerald-600 dark:text-emerald-400 font-medium">Autonomous</span>
                    )}
                  </td>
                  <td className="py-3 px-4 font-mono text-[11px] dark:text-zinc-400 light:text-zinc-600">
                    {tl.requiredPermissions.join(', ')}
                  </td>
                  <td className="py-3 px-4 font-mono dark:text-white light:text-zinc-900 font-medium">
                    {tl.usageCount.toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
