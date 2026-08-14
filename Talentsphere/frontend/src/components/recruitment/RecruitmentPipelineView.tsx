import React from 'react';
import { useOrganization } from '../../context/OrganizationContext';
import { useNotification } from '../../context/NotificationContext';
import { GitMerge, Sparkles, ChevronRight } from 'lucide-react';

export const RecruitmentPipelineView: React.FC = () => {
  const { applications, updateApplicationStage } = useOrganization();
  const { showSuccess } = useNotification();

  const stages = [
    { id: 'stg-1', name: 'Application Received' },
    { id: 'stg-2', name: 'Screening' },
    { id: 'stg-3', name: 'Technical Interview' },
    { id: 'stg-4', name: 'Managerial' },
    { id: 'stg-5', name: 'Offer' },
  ];

  const handleAdvanceStage = (appId: string, currentStageId: string) => {
    const currentIdx = stages.findIndex((s) => s.id === currentStageId);
    if (currentIdx < stages.length - 1) {
      const nextStage = stages[currentIdx + 1];
      updateApplicationStage(appId, nextStage.id, nextStage.name);
      showSuccess('Pipeline Stage Advanced!', `Application moved to ${nextStage.name}.`);
    }
  };

  return (
    <div className="space-y-6 text-left animate-fade-in">
      {/* Header */}
      <div>
        <h2 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight flex items-center gap-2">
          <GitMerge className="w-5 h-5 dark:text-zinc-300 light:text-zinc-700" /> Interactive Recruitment Pipeline (Kanban)
        </h2>
        <p className="text-xs dark:text-zinc-400 light:text-zinc-600 font-normal mt-0.5">
          Visual candidate pipeline • One-click stage advancement &amp; AI recommendation signals
        </p>
      </div>

      {/* Kanban Board Columns */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 overflow-x-auto pb-4 custom-scrollbar">
        {stages.map((stage) => {
          const stageApps = applications.filter((app) => app.stageId === stage.id || app.stageName === stage.name);

          return (
            <div key={stage.id} className="p-4 rounded-2xl glass-panel space-y-3 min-w-[240px]">
              <div className="flex items-center justify-between border-b border-zinc-200 dark:border-zinc-800 pb-2">
                <h3 className="text-xs font-medium dark:text-white light:text-zinc-900 uppercase tracking-wider font-mono">{stage.name}</h3>
                <span className="px-2 py-0.5 rounded-full bg-zinc-100 dark:bg-zinc-900 dark:text-zinc-300 light:text-zinc-700 border border-zinc-200 dark:border-zinc-800 text-[10px] font-mono font-medium">
                  {stageApps.length}
                </span>
              </div>

              <div className="space-y-3">
                {stageApps.map((app) => (
                  <div
                    key={app.id}
                    className="p-3.5 rounded-xl glass-card space-y-2 shadow-sm"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-medium dark:text-white light:text-zinc-900">{app.candidateName}</span>
                      <span className="text-[10px] font-mono text-emerald-600 dark:text-emerald-400 font-medium">{app.matchScore}%</span>
                    </div>

                    <p className="text-[11px] dark:text-zinc-400 light:text-zinc-600 font-medium">{app.jobTitle}</p>

                    <div className="p-2 rounded-lg glass-panel text-[10px] dark:text-zinc-300 light:text-zinc-700 font-normal">
                      <span className="text-amber-600 dark:text-amber-400 font-medium inline-flex items-center gap-1">
                        <Sparkles className="w-2.5 h-2.5" /> AI Signal:
                      </span>{' '}
                      {app.aiRecommendation}
                    </div>

                    <div className="pt-2 border-t border-zinc-200 dark:border-zinc-800 flex items-center justify-between">
                      <span className="text-[10px] dark:text-zinc-500 light:text-zinc-400 font-mono">{app.appliedDate}</span>
                      <button
                        onClick={() => handleAdvanceStage(app.id, app.stageId)}
                        className="px-2 py-1 rounded-lg bg-zinc-900 dark:bg-zinc-900 light:bg-zinc-900 text-white text-[10px] font-medium transition flex items-center gap-1 hover:bg-zinc-800"
                      >
                        Advance <ChevronRight className="w-3 h-3" />
                      </button>
                    </div>
                  </div>
                ))}

                {stageApps.length === 0 && (
                  <div className="p-6 text-center text-[11px] dark:text-zinc-600 light:text-zinc-400 font-mono">
                    No candidates in stage
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
