import React, { useState } from 'react';
import { useOrganization } from '../../context/OrganizationContext';
import { useNotification } from '../../context/NotificationContext';
import { WorkflowStage, RecruitmentWorkflow } from '../../types';
import {
  Workflow,
  Plus,
  Trash2,
  MoveRight,
  Save
} from 'lucide-react';

export const WorkflowBuilderView: React.FC = () => {
  const { workflows, updateWorkflow } = useOrganization();
  const { showSuccess } = useNotification();

  const [activeWorkflow, setActiveWorkflow] = useState<RecruitmentWorkflow>(workflows[0]);
  const [newStageName, setNewStageName] = useState('');
  const [newSlaHours, setNewSlaHours] = useState(48);

  const handleAddStage = () => {
    if (!newStageName) return;
    const newStage: WorkflowStage = {
      id: `stg-custom-${Date.now()}`,
      name: newStageName,
      type: 'interview',
      slaHours: Number(newSlaHours),
      requireScorecard: true,
      color: '#38bdf8',
    };

    const updated = {
      ...activeWorkflow,
      stages: [...activeWorkflow.stages, newStage],
    };

    setActiveWorkflow(updated);
    updateWorkflow(updated);
    setNewStageName('');
    showSuccess('Stage Added!', `Added "${newStageName}" stage to workflow.`);
  };

  const handleRemoveStage = (stageId: string) => {
    const updated = {
      ...activeWorkflow,
      stages: activeWorkflow.stages.filter((s) => s.id !== stageId),
    };
    setActiveWorkflow(updated);
    updateWorkflow(updated);
    showSuccess('Stage Removed', 'Workflow configuration updated.');
  };

  const handleSaveWorkflow = () => {
    updateWorkflow(activeWorkflow);
    showSuccess('Workflow Published!', `${activeWorkflow.name} is now live across recruitment pipelines.`);
  };

  return (
    <div className="space-y-6 text-left animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight flex items-center gap-2">
            <Workflow className="w-5 h-5 dark:text-zinc-300 light:text-zinc-700" /> Visual Recruitment Workflow Builder
          </h2>
          <p className="text-xs dark:text-zinc-400 light:text-zinc-600 font-normal mt-0.5">
            Configure recruitment stages, SLAs, automated agent triggers, and scorecard requirements
          </p>
        </div>

        <button
          onClick={handleSaveWorkflow}
          className="px-4 py-2 rounded-xl bg-zinc-900 text-white text-xs font-medium transition flex items-center gap-2 shadow-sm hover:bg-zinc-800"
        >
          <Save className="w-4 h-4" /> Publish Workflow Changes
        </button>
      </div>

      {/* Interactive Workflow Node Chain */}
      <div className="p-6 rounded-2xl glass-card space-y-6">
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <h3 className="text-base font-medium dark:text-white light:text-zinc-900">{activeWorkflow.name}</h3>
            <p className="text-xs dark:text-zinc-400 light:text-zinc-600 font-normal">{activeWorkflow.description}</p>
          </div>
          <span className="px-3 py-1 rounded-full glass-panel text-xs font-mono font-medium dark:text-zinc-300 light:text-zinc-700">
            {activeWorkflow.stages.length} Configured Stages
          </span>
        </div>

        {/* Graph Node Flow Layout */}
        <div className="p-6 rounded-2xl glass-panel overflow-x-auto custom-scrollbar">
          <div className="flex items-center gap-4 min-w-max">
            {activeWorkflow.stages.map((stage, idx) => (
              <React.Fragment key={stage.id}>
                {/* Stage Node Box */}
                <div className="w-64 p-4 rounded-2xl glass-card space-y-3 relative group hover:border-zinc-400 dark:hover:border-zinc-600 transition">
                  <div className="flex items-center justify-between">
                    <span className="px-2 py-0.5 rounded glass-panel dark:text-zinc-400 light:text-zinc-600 text-[10px] font-mono font-medium">
                      Step 0{idx + 1}
                    </span>
                    <button
                      onClick={() => handleRemoveStage(stage.id)}
                      className="text-zinc-400 hover:text-red-500 transition"
                      title="Delete Stage"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>

                  <div>
                    <h4 className="text-sm font-medium dark:text-white light:text-zinc-900">{stage.name}</h4>
                    <span className="text-[10px] dark:text-zinc-400 light:text-zinc-600 font-mono">Type: {stage.type}</span>
                  </div>

                  <div className="pt-2 border-t border-zinc-200 dark:border-zinc-800 text-[11px] space-y-1 dark:text-zinc-400 light:text-zinc-600 font-mono font-normal">
                    <div className="flex items-center justify-between">
                      <span>SLA Window:</span>
                      <span className="dark:text-zinc-200 light:text-zinc-800 font-medium">{stage.slaHours}h</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Require Scorecard:</span>
                      <span className={stage.requireScorecard ? 'text-emerald-600 dark:text-emerald-400 font-medium' : 'dark:text-zinc-500 light:text-zinc-400'}>
                        {stage.requireScorecard ? 'Yes' : 'No'}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Arrow Connector */}
                {idx < activeWorkflow.stages.length - 1 && (
                  <MoveRight className="w-6 h-6 text-zinc-400 shrink-0" />
                )}
              </React.Fragment>
            ))}
          </div>
        </div>

        {/* Add Stage Controls */}
        <div className="p-4 rounded-2xl glass-panel flex flex-col md:flex-row items-center gap-3">
          <input
            type="text"
            value={newStageName}
            onChange={(e) => setNewStageName(e.target.value)}
            placeholder="New Stage Name (e.g. Executive Culture Screen)..."
            className="flex-1 w-full px-3.5 py-2 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 text-xs dark:text-white light:text-zinc-900 placeholder-zinc-500 focus:outline-none"
          />
          <div className="flex items-center gap-2 w-full md:w-auto">
            <span className="text-xs dark:text-zinc-400 light:text-zinc-600 shrink-0">SLA Hours:</span>
            <input
              type="number"
              value={newSlaHours}
              onChange={(e) => setNewSlaHours(Number(e.target.value))}
              className="w-20 px-2 py-2 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 text-xs dark:text-white light:text-zinc-900 font-mono focus:outline-none"
            />
            <button
              onClick={handleAddStage}
              className="px-4 py-2 rounded-xl bg-zinc-900 text-white text-xs font-medium transition flex items-center gap-1.5 shrink-0 hover:bg-zinc-800"
            >
              <Plus className="w-3.5 h-3.5" /> Add Stage
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
