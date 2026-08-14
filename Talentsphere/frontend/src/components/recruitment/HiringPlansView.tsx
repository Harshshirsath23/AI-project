import React, { useState } from 'react';
import { useOrganization } from '../../context/OrganizationContext';
import { useNotification } from '../../context/NotificationContext';
import { TrendingUp, Plus } from 'lucide-react';

export const HiringPlansView: React.FC = () => {
  const { hiringPlans, addHiringPlan } = useOrganization();
  const { showSuccess } = useNotification();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [title, setTitle] = useState('');
  const [department, setDepartment] = useState('AI & Core Engineering');
  const [targetQuarter, setTargetQuarter] = useState('2026-Q4');
  const [positionsCount, setPositionsCount] = useState(6);
  const [allocatedBudget, setAllocatedBudget] = useState('$2,100,000');

  const handleCreatePlan = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title) return;

    addHiringPlan({
      title,
      department,
      targetQuarter,
      positionsCount: Number(positionsCount),
      allocatedBudget,
      status: 'Pending Approval',
      owner: 'Recruitment Lead',
    });

    showSuccess('Hiring Plan Created!', `${title} submitted for executive approval.`);
    setIsModalOpen(false);
    setTitle('');
  };

  return (
    <div className="space-y-6 text-left animate-fade-in">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight flex items-center gap-2">
            <TrendingUp className="w-5 h-5 dark:text-zinc-300 light:text-zinc-700" /> Strategic Hiring Plans
          </h2>
          <p className="text-xs dark:text-zinc-400 light:text-zinc-600 font-normal mt-0.5">
            Headcount planning, quarter budget allocations &amp; executive approval workflows
          </p>
        </div>

        <button
          onClick={() => setIsModalOpen(true)}
          className="px-4 py-2 rounded-xl bg-zinc-900 text-white text-xs font-medium transition flex items-center gap-2 shadow-sm hover:bg-zinc-800"
        >
          <Plus className="w-4 h-4" /> Create Hiring Plan
        </button>
      </div>

      <div className="space-y-3">
        {hiringPlans.map((plan) => (
          <div
            key={plan.id}
            className="p-5 rounded-2xl glass-card flex flex-col md:flex-row md:items-center justify-between gap-4"
          >
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <h3 className="text-base font-medium dark:text-white light:text-zinc-900">{plan.title}</h3>
                <span
                  className={`px-2.5 py-0.5 rounded-full text-[10px] font-mono font-medium uppercase ${plan.status === 'Approved'
                      ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30'
                      : 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/30'
                    }`}
                >
                  {plan.status}
                </span>
              </div>
              <p className="text-xs dark:text-zinc-400 light:text-zinc-600 font-normal">
                {plan.department} • Quarter: <span className="dark:text-zinc-200 light:text-zinc-800 font-mono font-medium">{plan.targetQuarter}</span>
              </p>
            </div>

            <div className="flex items-center gap-6 shrink-0">
              <div className="text-right">
                <span className="text-[10px] font-mono dark:text-zinc-500 light:text-zinc-400 block uppercase">Headcount</span>
                <span className="text-sm font-medium dark:text-white light:text-zinc-900 font-mono">{plan.positionsCount} Roles</span>
              </div>
              <div className="text-right">
                <span className="text-[10px] font-mono dark:text-zinc-500 light:text-zinc-400 block uppercase">Allocated Budget</span>
                <span className="text-sm font-medium text-emerald-600 dark:text-emerald-400 font-mono">{plan.allocatedBudget}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
