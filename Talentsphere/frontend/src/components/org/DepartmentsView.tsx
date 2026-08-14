import React from 'react';
import { useOrganization } from '../../context/OrganizationContext';
import { Layers } from 'lucide-react';

export const DepartmentsView: React.FC = () => {
  const { departments } = useOrganization();

  return (
    <div className="space-y-6 text-left animate-fade-in">
      <div>
        <h2 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight flex items-center gap-2">
          <Layers className="w-5 h-5 dark:text-zinc-300 light:text-zinc-700" /> Enterprise Departments
        </h2>
        <p className="text-xs dark:text-zinc-400 light:text-zinc-600 font-normal mt-0.5">
          Departmental budget allocations &amp; headcount capacity tracking
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {departments.map((dept) => (
          <div key={dept.id} className="p-5 rounded-2xl glass-card space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-mono font-medium glass-panel px-2 py-0.5 rounded dark:text-zinc-300 light:text-zinc-700">
                {dept.code}
              </span>
              <span className="text-xs font-mono font-medium text-emerald-600 dark:text-emerald-400">{dept.budgetAllocation}</span>
            </div>
            <h3 className="text-base font-medium dark:text-white light:text-zinc-900">{dept.name}</h3>
            <p className="text-xs dark:text-zinc-400 light:text-zinc-600 font-normal">Department Head: <span className="dark:text-white light:text-zinc-900 font-medium">{dept.headName}</span></p>
          </div>
        ))}
      </div>
    </div>
  );
};
