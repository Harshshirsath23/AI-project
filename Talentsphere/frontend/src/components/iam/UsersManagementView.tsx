import React, { useState } from 'react';
import { MOCK_ROLES } from '../../data/mockData';
import { DEMO_PRESETS } from '../../data/presets';
import { useNotification } from '../../context/NotificationContext';
import { Users, Lock, Search } from 'lucide-react';

export const UsersManagementView: React.FC = () => {
  const { showSuccess } = useNotification();
  const [usersList, setUsersList] = useState(
    DEMO_PRESETS.map((p) => ({ ...p, status: 'Active', mfaEnabled: true }))
  );
  const [searchQuery, setSearchQuery] = useState('');

  const handleRoleChange = (userId: string, newRole: string) => {
    setUsersList((prev) =>
      prev.map((u) => (u.id === userId ? { ...u, role: newRole } : u))
    );
    showSuccess('User Role Updated', `Role changed to ${newRole}.`);
  };

  const handleToggleMfa = (userId: string) => {
    setUsersList((prev) =>
      prev.map((u) => (u.id === userId ? { ...u, mfaEnabled: !u.mfaEnabled } : u))
    );
    showSuccess('MFA Policy Enforced', 'User multi-factor security setting saved.');
  };

  const filteredUsers = usersList.filter((u) =>
    u.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    u.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
    u.role.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6 text-left animate-fade-in">
      <div>
        <h2 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight flex items-center gap-2">
          <Users className="w-5 h-5 dark:text-zinc-300 light:text-zinc-700" /> Identity &amp; Access Management (Users)
        </h2>
        <p className="text-xs dark:text-zinc-400 light:text-zinc-600 font-normal mt-0.5">
          Enterprise user accounts, MFA enforcement, and RBAC role assignments
        </p>
      </div>

      <div className="p-4 rounded-2xl glass-card flex items-center justify-between gap-4">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search users by name, email, or role..."
            className="w-full pl-10 pr-4 py-2 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 text-xs dark:text-white light:text-zinc-900 placeholder-zinc-500 focus:outline-none"
          />
        </div>
      </div>

      <div className="space-y-3">
        {filteredUsers.map((usr) => (
          <div
            key={usr.id}
            className="p-4 rounded-2xl glass-card flex flex-col md:flex-row md:items-center justify-between gap-4"
          >
            <div className="flex items-center gap-3">
              <img
                src={usr.avatar}
                alt={usr.name}
                className="w-10 h-10 rounded-full object-cover border border-zinc-300 dark:border-zinc-700 shrink-0"
              />
              <div>
                <h4 className="text-sm font-medium dark:text-white light:text-zinc-900 flex items-center gap-2">
                  {usr.name}
                  <span
                    className={`text-[9px] font-mono px-2 py-0.5 rounded-full border uppercase ${usr.status === 'Active'
                        ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/30'
                        : 'glass-panel text-zinc-500'
                      }`}
                  >
                    {usr.status}
                  </span>
                </h4>
                <p className="text-xs dark:text-zinc-400 light:text-zinc-600 font-normal">{usr.email}</p>
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-4 text-xs">
              <div>
                <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-500 block">Assigned Role</span>
                <select
                  value={usr.role}
                  onChange={(e) => handleRoleChange(usr.id, e.target.value)}
                  className="px-2.5 py-1 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 dark:text-white light:text-zinc-900 font-medium"
                >
                  {MOCK_ROLES.map((r) => (
                    <option key={r.id} value={r.name}>
                      {r.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-500 block">Hardware MFA</span>
                <button
                  onClick={() => handleToggleMfa(usr.id)}
                  className={`px-3 py-1 rounded-xl font-mono text-xs font-medium transition flex items-center gap-1 ${usr.mfaEnabled
                      ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30'
                      : 'glass-panel text-zinc-500'
                    }`}
                >
                  <Lock className="w-3 h-3" />
                  {usr.mfaEnabled ? 'Enforced' : 'Disabled'}
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
