import React, { useState, useEffect } from 'react';
import { Activity } from 'lucide-react';
import { ObservabilityTrace, TraceNode } from '../../types';
import { sourcingApi } from '../../api';

export const AIObservabilityView: React.FC = () => {
  const [traces, setTraces] = useState<ObservabilityTrace[]>([]);

  useEffect(() => {
    sourcingApi.getObservabilityTraces().then(setTraces);
  }, []);

  const renderTraceNode = (node: TraceNode) => {
    return (
      <div key={node.id} className="pl-4 border-l border-zinc-200 dark:border-zinc-800 space-y-2 py-1">
        <div className="p-3 rounded-xl glass-panel flex items-center justify-between text-xs">
          <div className="flex items-center gap-2 font-mono">
            <span className="px-2 py-0.5 rounded glass-panel text-[10px] uppercase font-medium dark:text-zinc-300 light:text-zinc-700">
              {node.type}
            </span>
            <span className="dark:text-white light:text-zinc-900 font-medium">{node.name}</span>
            {node.model && <span className="dark:text-zinc-500 light:text-zinc-400 text-[10px]">({node.model})</span>}
          </div>
          <div className="flex items-center gap-3 font-mono text-[11px]">
            {node.tokens && <span className="dark:text-zinc-300 light:text-zinc-700 font-medium">{node.tokens} Tokens</span>}
            <span className="dark:text-zinc-400 light:text-zinc-600">{node.durationMs}ms</span>
          </div>
        </div>

        {node.children && node.children.length > 0 && (
          <div className="space-y-1">
            {node.children.map((child) => renderTraceNode(child))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="space-y-6 text-left animate-fade-in">
      {/* Header Banner */}
      <div className="p-6 rounded-2xl glass-card flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full glass-panel dark:text-zinc-300 light:text-zinc-700 text-xs font-mono font-medium mb-2">
            <Activity className="w-3.5 h-3.5 text-zinc-400" /> AI Observability Engine
          </div>
          <h1 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight">AI Observability &amp; Trace Tree Explorer</h1>
          <p className="text-xs dark:text-zinc-400 light:text-zinc-600 mt-1 font-normal">
            Execution traces across AI models, vector database queries, tool invocations, and RAG retrievers.
          </p>
        </div>

        <span className="px-3 py-1.5 rounded-xl glass-panel text-xs font-mono dark:text-zinc-300 light:text-zinc-700 font-medium">
          Trace Telemetry Active
        </span>
      </div>

      {/* KPI Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl glass-card space-y-1">
          <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-500 uppercase font-medium">Trace Count Today</span>
          <p className="text-2xl font-medium dark:text-white light:text-zinc-900 font-mono">1,420</p>
        </div>
        <div className="p-4 rounded-xl glass-card space-y-1">
          <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-500 uppercase font-medium">Avg Trace Latency</span>
          <p className="text-2xl font-medium dark:text-zinc-200 light:text-zinc-800 font-mono">1,240ms</p>
        </div>
        <div className="p-4 rounded-xl glass-card space-y-1">
          <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-500 uppercase font-medium">Total AI Cost (Est)</span>
          <p className="text-2xl font-medium text-emerald-600 dark:text-emerald-400 font-mono">$12.42</p>
        </div>
        <div className="p-4 rounded-xl glass-card space-y-1">
          <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-500 uppercase font-medium">Error Rate</span>
          <p className="text-2xl font-medium text-emerald-600 dark:text-emerald-400 font-mono">0.00%</p>
        </div>
      </div>

      {/* Visual Trace Tree Inspector */}
      {traces.map((tr) => (
        <div key={tr.id} className="p-6 rounded-2xl glass-card space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-zinc-200 dark:border-zinc-800 pb-3">
            <div>
              <span className="text-xs font-mono font-medium dark:text-white light:text-zinc-900">{tr.traceName}</span>
              <span className="text-[10px] font-mono dark:text-zinc-500 light:text-zinc-400 block">{tr.timestamp}</span>
            </div>
            <div className="flex items-center gap-3 text-xs font-mono">
              <span className="dark:text-zinc-300 light:text-zinc-700 font-medium">{tr.totalTokens.toLocaleString()} Tokens</span>
              <span className="text-emerald-600 dark:text-emerald-400 font-medium">${tr.totalCostUSD}</span>
              <span className="dark:text-zinc-400 light:text-zinc-600 font-medium">{tr.totalDurationMs}ms</span>
            </div>
          </div>

          <div className="space-y-2">
            <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-500 uppercase font-medium block">Execution Trace Tree Topology</span>
            {renderTraceNode(tr.rootNode)}
          </div>
        </div>
      ))}
    </div>
  );
};
