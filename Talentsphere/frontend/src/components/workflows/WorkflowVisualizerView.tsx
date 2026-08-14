import React, { useState } from 'react';
import {
  Workflow,
  CheckCircle2,
  Clock,
  Sparkles,
  ShieldCheck,
  Cpu,
  ArrowRight,
  Database,
  FileCheck,
  UserCheck,
  AlertTriangle
} from 'lucide-react';

export const WorkflowVisualizerView: React.FC = () => {
  const [activeNode, setActiveNode] = useState<string>('node-matching');

  const nodes = [
    { id: 'node-trigger', label: '1. Candidate Upload Trigger', type: 'trigger', status: 'completed', duration: '80ms', details: 'Ingests PDF/DOCX file stream via HTTPS POST.' },
    { id: 'node-ocr', label: '2. OCR & Skill Extraction', type: 'agent', status: 'completed', duration: '240ms', details: 'Parses experience, education, and technical keyphrases.' },
    { id: 'node-rag', label: '3. Knowledge Base RAG Lookup', type: 'rag', status: 'completed', duration: '190ms', details: 'Retrieves engineering level benchmarks & compensation bands.' },
    { id: 'node-matching', label: '4. Nemotron Vector Match', type: 'agent', status: 'running', duration: '410ms', details: 'Calculates multi-dimensional cosine match score across 12 dimensions.' },
    { id: 'node-compliance', label: '5. EEOC Bias Shield', type: 'condition', status: 'idle', duration: '45ms', details: 'Audits criteria for protected attribute neutral evaluation.' },
    { id: 'node-hitl', label: '6. HITL Approval Trigger', type: 'hitl', status: 'idle', duration: 'Pending', details: 'Dispatches high-confidence candidate to recruiter review queue.' }
  ];

  const activeNodeData = nodes.find((n) => n.id === activeNode) || nodes[3];

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="p-6 rounded-2xl bg-neutral-950 border border-neutral-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-500/30 text-sky-400 text-xs font-mono font-medium mb-2">
            <Workflow className="w-3.5 h-3.5 text-sky-300" /> LangGraph Orchestration Canvas
          </div>
          <h1 className="text-xl font-bold text-white tracking-tight">Recruitment Agent Workflow Visualizer</h1>
          <p className="text-xs text-neutral-400 mt-1">
            Visual control plane for candidate evaluation graph execution, agent node statuses, and HITL boundaries.
          </p>
        </div>

        <div className="px-3 py-1.5 rounded-xl bg-neutral-900 border border-neutral-800 text-xs font-mono text-sky-400 font-semibold flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-sky-400 animate-ping" /> Live Graph Execution
        </div>
      </div>

      {/* Node Canvas Flow View */}
      <div className="p-6 rounded-2xl bg-neutral-950 border border-neutral-800 space-y-6">
        <h3 className="text-sm font-semibold text-white flex items-center gap-2">
          <Workflow className="w-4 h-4 text-sky-400" /> LangGraph Pipeline Topology
        </h3>

        {/* Visual Node Flow Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-3 relative">
          {nodes.map((node) => {
            const isSelected = activeNode === node.id;

            return (
              <button
                key={node.id}
                onClick={() => setActiveNode(node.id)}
                className={`p-4 rounded-xl text-left border transition flex flex-col justify-between space-y-3 relative group ${
                  isSelected
                    ? 'bg-neutral-900 border-sky-500/80 shadow-lg ring-1 ring-sky-500/30'
                    : 'bg-neutral-900/40 border-neutral-800 hover:border-neutral-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span
                    className={`w-2 h-2 rounded-full ${
                      node.status === 'completed'
                        ? 'bg-emerald-400'
                        : node.status === 'running'
                        ? 'bg-sky-400 animate-pulse'
                        : 'bg-neutral-600'
                    }`}
                  />
                  <span className="text-[10px] font-mono text-neutral-500">{node.duration}</span>
                </div>

                <div>
                  <h4 className="text-xs font-semibold text-white group-hover:text-sky-300 transition">{node.label}</h4>
                  <span className="text-[10px] font-mono text-neutral-500 capitalize">{node.type}</span>
                </div>

                <div className="pt-2 border-t border-neutral-800/60 flex items-center justify-between text-[9px] font-mono">
                  <span className={`${
                    node.status === 'completed' ? 'text-emerald-400' : node.status === 'running' ? 'text-sky-400' : 'text-neutral-500'
                  }`}>
                    {node.status}
                  </span>
                  <ArrowRight className="w-3 h-3 text-neutral-600 group-hover:text-sky-400 transition" />
                </div>
              </button>
            );
          })}
        </div>

        {/* Selected Node Inspector Details */}
        <div className="p-5 rounded-xl bg-neutral-900/80 border border-neutral-800 space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-semibold text-white font-mono flex items-center gap-2">
              <Cpu className="w-4 h-4 text-sky-400" /> Selected Node Spec: {activeNodeData.label}
            </h4>
            <span className="text-xs font-mono text-sky-400">Duration: {activeNodeData.duration}</span>
          </div>
          <p className="text-xs text-neutral-300 font-mono leading-relaxed">{activeNodeData.details}</p>
        </div>
      </div>
    </div>
  );
};
