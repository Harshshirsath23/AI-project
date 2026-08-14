import React from 'react';
import { HITLTask } from '../../types';
import { Sparkles, CheckCircle2, XCircle, ShieldAlert, Cpu } from 'lucide-react';

interface HITLApprovalCardProps {
  task: HITLTask;
  onApprove: (id: string) => void;
  onReject: (id: string) => void;
}

export const HITLApprovalCard: React.FC<HITLApprovalCardProps> = ({
  task,
  onApprove,
  onReject,
}) => {
  return (
    <div className="p-5 rounded-2xl glass-card relative overflow-hidden transition-all duration-200">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
        <div className="flex items-center gap-2">
          <span className="p-1.5 rounded-lg glass-panel">
            <ShieldAlert className="w-4 h-4 text-zinc-400" />
          </span>
          <div>
            <span className="text-[10px] font-medium uppercase tracking-widest dark:text-zinc-400 light:text-zinc-600 block">
              Human-in-the-Loop Verification
            </span>
            <h4 className="text-sm font-medium dark:text-white light:text-zinc-900">{task.title}</h4>
          </div>
        </div>
        <span className="px-2.5 py-1 rounded-full glass-panel text-[10px] font-mono font-medium flex items-center gap-1 dark:text-zinc-300 light:text-zinc-700">
          <Cpu className="w-3 h-3 text-zinc-400" />
          {task.agentName}
        </span>
      </div>

      {/* Candidate / Job Summary */}
      <div className="p-3 rounded-xl glass-panel mb-3 text-xs flex flex-wrap items-center justify-between gap-2 font-normal">
        <div>
          <span className="dark:text-zinc-400 light:text-zinc-600 font-normal">Candidate: </span>
          <span className="dark:text-white light:text-zinc-900 font-medium">{task.candidateName}</span>
        </div>
        <div>
          <span className="dark:text-zinc-400 light:text-zinc-600 font-normal">Position: </span>
          <span className="dark:text-zinc-200 light:text-zinc-800 font-medium">{task.jobTitle}</span>
        </div>
        <div className="dark:text-zinc-400 light:text-zinc-600 font-mono text-[11px]">
          Confidence: <span className="text-emerald-600 dark:text-emerald-400 font-medium">{Math.round(task.confidenceScore * 100)}%</span>
        </div>
      </div>

      {/* Recommendation */}
      <div className="mb-3 space-y-1">
        <div className="text-[11px] font-medium dark:text-zinc-400 light:text-zinc-600 flex items-center gap-1 uppercase tracking-wider">
          <Sparkles className="w-3 h-3 text-zinc-400" /> AI Agent Recommendation
        </div>
        <p className="text-xs dark:text-zinc-300 light:text-zinc-700 leading-relaxed glass-panel p-3 rounded-xl font-normal">
          {task.recommendation}
        </p>
      </div>

      {/* Evidence checklist */}
      <div className="mb-4 space-y-1.5">
        <span className="text-[10px] font-medium dark:text-zinc-400 light:text-zinc-600 uppercase tracking-wider block">
          Agent Evidence Log
        </span>
        <ul className="space-y-1 text-xs dark:text-zinc-300 light:text-zinc-700 font-mono">
          {task.evidence.map((ev, i) => (
            <li key={i} className="flex items-start gap-2">
              <span className="text-emerald-600 dark:text-emerald-400 mt-0.5">✓</span>
              <span>{ev}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Action Buttons or Resolved Badge */}
      {task.status === 'Pending' ? (
        <div className="flex items-center justify-end gap-3 pt-3 border-t border-zinc-200 dark:border-zinc-800">
          <button
            onClick={() => onReject(task.id)}
            className="px-4 py-2 rounded-xl glass-panel text-red-600 dark:text-red-400 text-xs font-medium transition flex items-center gap-1.5 hover:bg-red-50 dark:hover:bg-red-950/20"
          >
            <XCircle className="w-3.5 h-3.5" /> Reject Recommendation
          </button>
          <button
            onClick={() => onApprove(task.id)}
            className="px-4 py-2 rounded-xl bg-zinc-900 text-white text-xs font-medium transition flex items-center gap-1.5 shadow-sm hover:bg-zinc-800"
          >
            <CheckCircle2 className="w-3.5 h-3.5" /> Human Approve &amp; Execute
          </button>
        </div>
      ) : (
        <div className="pt-2 border-t border-zinc-200 dark:border-zinc-800 text-right">
          <span
            className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium uppercase tracking-wider border ${
              task.status === 'Approved'
                ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/30'
                : 'bg-red-500/10 text-red-600 dark:text-red-400 border-red-500/30'
            }`}
          >
            {task.status === 'Approved' ? <CheckCircle2 className="w-3.5 h-3.5" /> : <XCircle className="w-3.5 h-3.5" />}
            Human Decision: {task.status}
          </span>
        </div>
      )}
    </div>
  );
};
