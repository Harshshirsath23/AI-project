import React, { useState } from 'react';
import { useOrganization } from '../../context/OrganizationContext';
import { useNotification } from '../../context/NotificationContext';
import { GitBranch, Plus, MapPin } from 'lucide-react';

export const BranchesView: React.FC = () => {
  const { branches, addBranch } = useOrganization();
  const { showSuccess } = useNotification();

  const [name, setName] = useState('');
  const [code, setCode] = useState('');
  const [city, setCity] = useState('');

  const handleAddBranch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !code) return;

    addBranch({
      name,
      code,
      city,
      country: 'United States',
      address: 'Enterprise Tech Center',
      headcount: 0,
      isHeadquarters: false,
    });

    showSuccess('Branch Added!', `${name} registered in global organization hierarchy.`);
    setName('');
    setCode('');
    setCity('');
  };

  return (
    <div className="space-y-6 text-left animate-fade-in">
      <div>
        <h2 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight flex items-center gap-2">
          <GitBranch className="w-5 h-5 dark:text-zinc-300 light:text-zinc-700" /> Global Enterprise Branches
        </h2>
        <p className="text-xs dark:text-zinc-400 light:text-zinc-600 font-normal mt-0.5">
          Regional office locations &amp; localized recruitment compliance bounds
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {branches.map((br) => (
          <div key={br.id} className="p-5 rounded-2xl glass-card space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-mono font-medium glass-panel px-2 py-0.5 rounded dark:text-zinc-300 light:text-zinc-700">
                {br.code}
              </span>
              {br.isHeadquarters && (
                <span className="text-[10px] font-mono font-medium text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/30">
                  Global HQ
                </span>
              )}
            </div>
            <h3 className="text-base font-medium dark:text-white light:text-zinc-900">{br.name}</h3>
            <p className="text-xs dark:text-zinc-400 light:text-zinc-600 flex items-center gap-1 font-normal">
              <MapPin className="w-3.5 h-3.5 text-zinc-400" /> {br.city}, {br.country}
            </p>
            <div className="pt-2 border-t border-zinc-200 dark:border-zinc-800 text-xs font-mono dark:text-zinc-400 light:text-zinc-600 flex justify-between">
              <span>Active Headcount:</span>
              <span className="dark:text-white light:text-zinc-900 font-medium">{br.headcount} Team Members</span>
            </div>
          </div>
        ))}
      </div>

      {/* Add Branch Form */}
      <div className="p-5 rounded-2xl glass-card space-y-4">
        <h3 className="text-sm font-medium dark:text-white light:text-zinc-900">Register New Regional Branch</h3>
        <form onSubmit={handleAddBranch} className="grid grid-cols-1 sm:grid-cols-4 gap-3 text-xs">
          <input
            type="text"
            required
            placeholder="Branch Name (e.g. Tokyo Hub)"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="px-3 py-2 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 dark:text-white light:text-zinc-900 focus:outline-none"
          />
          <input
            type="text"
            required
            placeholder="Branch Code (e.g. TYO-01)"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="px-3 py-2 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 dark:text-white light:text-zinc-900 font-mono uppercase focus:outline-none"
          />
          <input
            type="text"
            placeholder="City"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            className="px-3 py-2 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 dark:text-white light:text-zinc-900 focus:outline-none"
          />
          <button
            type="submit"
            className="px-4 py-2 rounded-xl bg-zinc-900 text-white font-medium transition flex items-center justify-center gap-2 shadow-sm hover:bg-zinc-800"
          >
            <Plus className="w-4 h-4" /> Add Branch
          </button>
        </form>
      </div>
    </div>
  );
};
