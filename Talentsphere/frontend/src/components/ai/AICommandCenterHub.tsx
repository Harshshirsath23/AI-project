import React from 'react';
import { useOrganization } from '../../context/OrganizationContext';
import { useNotification } from '../../context/NotificationContext';
import { AI3DCoreCanvas } from './AI3DCoreCanvas';
import { AIAgentStream } from './AIAgentStream';
import { HITLApprovalCard } from './HITLApprovalCard';
import { MOCK_AI_AGENTS_STATUS } from '../../data/mockData';
import { Sparkles, ShieldAlert } from 'lucide-react';

export const AICommandCenterHub: React.FC = () => {
  const { hitlTasks, resolveHITLTask } = useOrganization();
  const { showSuccess, showInfo } = useNotification();

  const handleApprove = (id: string) => {
    resolveHITLTask(id, 'Approved');
    showSuccess('HITL Decision Executed!', 'Human approval recorded and agent action triggered.');
  };

  const handleReject = (id: string) => {
    resolveHITLTask(id, 'Rejected');
    showInfo('HITL Decision Rejected', 'Agent recommendation dismissed by human reviewer.');
  };

  return (
    <div className="space-y-6 text-left animate-fade-in">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-6 rounded-2xl glass-card relative overflow-hidden">
        <div className="space-y-1 z-10">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full glass-panel text-xs font-mono font-medium dark:text-zinc-300 light:text-zinc-700">
            <Sparkles className="w-3.5 h-3.5 text-zinc-400" /> AI Executive Command Hub
          </div>
          <h2 className="text-2xl font-medium dark:text-white light:text-zinc-900 tracking-tight">Autonomous Recruitment Intelligence</h2>
          <p className="text-xs dark:text-zinc-400 light:text-zinc-600 max-w-xl font-normal">
            Real-time multi-agent reasoning engine monitoring candidate vectors, interview sentiment, and human-in-the-loop approvals.
          </p>
        </div>

        {/* 3D Core Canvas */}
        <div className="w-full md:w-72 h-44 shrink-0 rounded-2xl glass-panel relative overflow-hidden">
          <AI3DCoreCanvas className="w-full h-full" activeAgentCount={4} />
        </div>
      </div>

      {/* Autonomous Agent Status */}
      <AIAgentStream agents={MOCK_AI_AGENTS_STATUS} />

      {/* Human-In-The-Loop Approval Queue */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-medium dark:text-white light:text-zinc-900 flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-zinc-400" /> Human-in-the-Loop Decision Queue
            </h3>
            <p className="text-xs dark:text-zinc-400 light:text-zinc-600 font-normal">
              High-impact AI agent actions requiring explicit human verification before execution
            </p>
          </div>
          <span className="px-3 py-1 rounded-full glass-panel text-xs font-mono font-medium dark:text-zinc-300 light:text-zinc-700">
            {hitlTasks.filter((t) => t.status === 'Pending').length} Pending Human Review
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {hitlTasks.map((task) => (
            <HITLApprovalCard
              key={task.id}
              task={task}
              onApprove={handleApprove}
              onReject={handleReject}
            />
          ))}
        </div>
      </div>
    </div>
  );
};
