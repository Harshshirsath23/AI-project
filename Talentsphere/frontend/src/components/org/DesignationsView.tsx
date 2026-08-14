import React from 'react';
import { useOrganization } from '../../context/OrganizationContext';
import { Award } from 'lucide-react';

export const DesignationsView: React.FC = () => {
  const { designations } = useOrganization();

  return (
    <div className="space-y-6 text-left animate-fade-in">
      <div>
        <h2 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight flex items-center gap-2">
          <Award className="w-5 h-5 dark:text-zinc-300 light:text-zinc-700" /> Standardized Designations Catalog
        </h2>
        <p className="text-xs dark:text-zinc-400 light:text-zinc-600 font-normal mt-0.5">
          Job level hierarchy, grade bands &amp; salary benchmarking matrix
        </p>
      </div>

      <div className="space-y-3">
        {designations.map((desg) => (
          <div key={desg.id} className="p-4 rounded-2xl glass-card flex items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-medium dark:text-white light:text-zinc-900">{desg.title}</h3>
                <span className="px-2 py-0.5 rounded glass-panel dark:text-zinc-300 light:text-zinc-700 font-mono text-[10px] font-medium">
                  Grade {desg.level}
                </span>
              </div>
              <p className="text-xs dark:text-zinc-400 light:text-zinc-600 font-normal">Department: {desg.department}</p>
            </div>
            <span className="text-xs font-mono font-medium text-emerald-600 dark:text-emerald-400">{desg.salaryBand}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
