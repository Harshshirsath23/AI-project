import React from 'react';
import { MOCK_ROLES } from '../../data/mockData';
import { Shield } from 'lucide-react';

export const RolesManagementView: React.FC = () => {
  return (
    <div className="space-y-6 text-left animate-fade-in">
      <div>
        <h2 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight flex items-center gap-2">
          <Shield className="w-5 h-5 dark:text-zinc-300 light:text-zinc-700" /> RBAC Roles &amp; Permission Matrices
        </h2>
        <p className="text-xs dark:text-zinc-400 light:text-zinc-600 font-normal mt-0.5">
          Granular privilege management across recruitment, AI agents, IAM, and audit controls
        </p>
      </div>

      <div className="space-y-4">
        {MOCK_ROLES.map((role) => (
          <div key={role.id} className="p-5 rounded-2xl glass-card space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-medium dark:text-white light:text-zinc-900">{role.name}</h3>
              <span className="text-xs font-mono dark:text-zinc-300 light:text-zinc-700 font-medium">{role.permissions.length} Permissions Granted</span>
            </div>
            <p className="text-xs dark:text-zinc-400 light:text-zinc-600 font-normal">{role.description}</p>

            <div className="flex flex-wrap gap-1.5 pt-2">
              {role.permissions.map((perm, i) => (
                <span key={i} className="px-2 py-0.5 rounded glass-panel dark:text-zinc-300 light:text-zinc-700 font-mono text-[10px]">
                  {perm}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
