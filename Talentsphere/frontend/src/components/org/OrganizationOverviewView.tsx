import React, { useState } from 'react';
import { useOrganization } from '../../context/OrganizationContext';
import { useAuth } from '../../context/AuthContext';
import { useNotification } from '../../context/NotificationContext';
import { 
  Building2, 
  ShieldCheck, 
  Plus, 
  GitBranch, 
  Layers, 
  Award, 
  MapPin, 
  Settings, 
  Building,
  CheckCircle2,
  Lock,
  Globe,
  Sliders
} from 'lucide-react';
import { CreateOrganizationModal } from './CreateOrganizationModal';

export const OrganizationOverviewView: React.FC = () => {
  const { organization, branches, departments, designations, addBranch, addDepartment, addDesignation } = useOrganization();
  const { currentUser } = useAuth();
  const { showSuccess } = useNotification();

  const [activeSubTab, setActiveSubTab] = useState<'overview' | 'branches' | 'departments' | 'designations' | 'settings'>('overview');

  // Modals
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isAddBranchModalOpen, setIsAddBranchModalOpen] = useState(false);
  const [isAddDeptModalOpen, setIsAddDeptModalOpen] = useState(false);
  const [isAddDesgModalOpen, setIsAddDesgModalOpen] = useState(false);

  // Forms
  const [branchForm, setBranchForm] = useState({ name: '', code: '', city: '', country: 'United States' });
  const [deptForm, setDeptForm] = useState({ name: '', code: '', headName: 'Unassigned', budgetAllocation: '$100,000' });
  const [desgForm, setDesgForm] = useState({ title: '', level: 'L3', department: 'Engineering', salaryBand: '$120,000 - $160,000' });

  const isPlatformAdmin = currentUser?.is_platform_admin || currentUser?.scope === 'PLATFORM';

  const handleAddBranchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!branchForm.name || !branchForm.code) return;
    addBranch({
      name: branchForm.name,
      code: branchForm.code.toUpperCase(),
      city: branchForm.city || 'Headquarters',
      country: branchForm.country,
      address: 'Enterprise Office',
      headcount: 0,
      isHeadquarters: false
    });
    showSuccess('Branch Created!', `${branchForm.name} registered in tenant hierarchy.`);
    setBranchForm({ name: '', code: '', city: '', country: 'United States' });
    setIsAddBranchModalOpen(false);
  };

  const handleAddDeptSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!deptForm.name || !deptForm.code) return;
    addDepartment({
      name: deptForm.name,
      code: deptForm.code.toUpperCase(),
      headName: deptForm.headName,
      branchName: 'Headquarters',
      openPositions: 0,
      totalMembers: 0,
      budgetAllocation: deptForm.budgetAllocation
    } as any);
    showSuccess('Department Created!', `${deptForm.name} added to department hierarchy.`);
    setDeptForm({ name: '', code: '', headName: 'Unassigned', budgetAllocation: '$100,000' });
    setIsAddDeptModalOpen(false);
  };

  const handleAddDesgSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!desgForm.title) return;
    addDesignation({
      title: desgForm.title,
      level: desgForm.level,
      department: desgForm.department,
      payGrade: `Band ${desgForm.level}`,
      salaryBand: desgForm.salaryBand
    } as any);
    showSuccess('Designation Added!', `${desgForm.title} added to compensation catalog.`);
    setDesgForm({ title: '', level: 'L3', department: 'Engineering', salaryBand: '$120,000 - $160,000' });
    setIsAddDesgModalOpen(false);
  };

  return (
    <div className="w-full space-y-6 animate-fade-in text-left">
      {/* Top Banner - Executive Styling */}
      <div className="always-dark flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-red-950 via-slate-900 to-zinc-950 p-6 rounded-2xl border border-red-900/50 shadow-2xl backdrop-blur-md text-white">
        <div className="flex items-center space-x-4">
          <div className="p-3.5 rounded-2xl bg-red-600/30 text-red-400 border border-red-500/40 shadow-lg shadow-red-600/20">
            <Building2 className="w-8 h-8" />
          </div>
          <div>
            <div className="flex items-center space-x-3">
              <h1 className="text-2xl font-black text-white tracking-tight">{organization.name}</h1>
              <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 flex items-center space-x-1.5">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                <span>SOC 2 Type II Verified</span>
              </span>
            </div>
            <p className="text-xs text-slate-300 mt-1 font-mono">
              Domain: {organization.domain} • Tax ID: {organization.taxId} • Subscription: {organization.plan}
            </p>
          </div>
        </div>

        {isPlatformAdmin && (
          <button
            onClick={() => setIsCreateModalOpen(true)}
            className="flex items-center space-x-2 px-4 py-2.5 bg-red-600 hover:bg-red-500 text-white text-xs font-bold rounded-xl transition shadow-lg shadow-red-600/30"
          >
            <Plus className="w-4 h-4" />
            <span>Provision New Tenant</span>
          </button>
        )}
      </div>

      {/* Unified Sub-Navigation Tabs */}
      <div className="flex items-center space-x-2 border-b border-slate-200 dark:border-slate-800 pb-3 overflow-x-auto">
        <button
          onClick={() => setActiveSubTab('overview')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl text-xs font-bold transition ${activeSubTab === 'overview' ? 'bg-red-600 text-white shadow-md' : 'bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800'}`}
        >
          <Building className="w-4 h-4" />
          <span>Profile Overview</span>
        </button>

        <button
          onClick={() => setActiveSubTab('branches')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl text-xs font-bold transition ${activeSubTab === 'branches' ? 'bg-red-600 text-white shadow-md' : 'bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800'}`}
        >
          <GitBranch className="w-4 h-4" />
          <span>Branches ({branches.length})</span>
        </button>

        <button
          onClick={() => setActiveSubTab('departments')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl text-xs font-bold transition ${activeSubTab === 'departments' ? 'bg-red-600 text-white shadow-md' : 'bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800'}`}
        >
          <Layers className="w-4 h-4" />
          <span>Departments ({departments.length})</span>
        </button>

        <button
          onClick={() => setActiveSubTab('designations')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl text-xs font-bold transition ${activeSubTab === 'designations' ? 'bg-red-600 text-white shadow-md' : 'bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800'}`}
        >
          <Award className="w-4 h-4" />
          <span>Designations ({designations.length})</span>
        </button>

        <button
          onClick={() => setActiveSubTab('settings')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl text-xs font-bold transition ${activeSubTab === 'settings' ? 'bg-red-600 text-white shadow-md' : 'bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800'}`}
        >
          <Settings className="w-4 h-4" />
          <span>Settings</span>
        </button>
      </div>

      {/* SUB-TAB 1: Profile Overview */}
      {activeSubTab === 'overview' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div 
              onClick={() => setActiveSubTab('branches')}
              className="p-5 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition cursor-pointer group"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs text-slate-500 dark:text-slate-400 font-semibold uppercase tracking-wider">Global Office Branches</span>
                <GitBranch className="w-5 h-5 text-red-500 group-hover:scale-110 transition" />
              </div>
              <div className="mt-3 text-3xl font-black text-slate-900 dark:text-white">{branches.length}</div>
              <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">Silicon Valley, London, Singapore</p>
            </div>

            <div 
              onClick={() => setActiveSubTab('departments')}
              className="p-5 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition cursor-pointer group"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs text-slate-500 dark:text-slate-400 font-semibold uppercase tracking-wider">Departments</span>
                <Layers className="w-5 h-5 text-blue-500 group-hover:scale-110 transition" />
              </div>
              <div className="mt-3 text-3xl font-black text-slate-900 dark:text-white">{departments.length}</div>
              <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">Engineering, Product, Talent, Exec</p>
            </div>

            <div 
              onClick={() => setActiveSubTab('designations')}
              className="p-5 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition cursor-pointer group"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs text-slate-500 dark:text-slate-400 font-semibold uppercase tracking-wider">Active Designations</span>
                <Award className="w-5 h-5 text-emerald-500 group-hover:scale-110 transition" />
              </div>
              <div className="mt-3 text-3xl font-black text-slate-900 dark:text-white">{designations.length}</div>
              <p className="mt-2 text-xs text-emerald-600 dark:text-emerald-400 font-semibold">Standardized Compensation Bands</p>
            </div>
          </div>

          <div className="p-6 bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-2xl space-y-4 shadow-sm">
            <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
              <Lock className="w-5 h-5 text-red-500" />
              <span>Tenant Organization Entity Specification</span>
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
              <div className="p-4 bg-slate-50 dark:bg-slate-950/80 rounded-xl border border-slate-200 dark:border-slate-800">
                <span className="text-slate-500 font-semibold">Legal Entity Name</span>
                <div className="font-extrabold text-slate-900 dark:text-white text-sm mt-1">{organization.name}</div>
              </div>
              <div className="p-4 bg-slate-50 dark:bg-slate-950/80 rounded-xl border border-slate-200 dark:border-slate-800">
                <span className="text-slate-500 font-semibold">Registered Tax Identification</span>
                <div className="font-mono font-extrabold text-slate-900 dark:text-white text-sm mt-1">{organization.taxId}</div>
              </div>
              <div className="p-4 bg-slate-50 dark:bg-slate-950/80 rounded-xl border border-slate-200 dark:border-slate-800">
                <span className="text-slate-500 font-semibold">Subscription Plan</span>
                <div className="font-bold text-red-600 dark:text-red-400 text-sm mt-1">{organization.plan}</div>
              </div>
              <div className="p-4 bg-slate-50 dark:bg-slate-950/80 rounded-xl border border-slate-200 dark:border-slate-800">
                <span className="text-slate-500 font-semibold">Multi-Tenant Isolation</span>
                <div className="font-bold text-emerald-600 dark:text-emerald-400 text-sm mt-1">ENFORCED (Strict Boundary)</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* SUB-TAB 2: Branches Section */}
      {activeSubTab === 'branches' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                <GitBranch className="w-5 h-5 text-red-500" />
                <span>Global Office Branches</span>
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">Regional office locations & localized compliance bounds.</p>
            </div>
            <button
              onClick={() => setIsAddBranchModalOpen(true)}
              className="flex items-center space-x-2 px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-xl text-xs font-bold transition shadow-md"
            >
              <Plus className="w-4 h-4" />
              <span>Add Branch</span>
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {branches.map((br) => (
              <div key={br.id} className="p-5 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 space-y-3 shadow-sm hover:shadow-md transition">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono font-bold bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 px-2 py-0.5 rounded border border-slate-200 dark:border-slate-700">
                    {br.code || 'HQ'}
                  </span>
                  {br.isHeadquarters && (
                    <span className="text-[10px] font-mono font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/30">
                      Global HQ
                    </span>
                  )}
                </div>
                <h4 className="text-base font-extrabold text-slate-900 dark:text-white">{br.name}</h4>
                <p className="text-xs text-slate-600 dark:text-slate-400 flex items-center gap-1 font-medium">
                  <MapPin className="w-3.5 h-3.5 text-slate-400" /> {br.city}, {br.country}
                </p>
                <div className="pt-2 border-t border-slate-100 dark:border-slate-800 flex justify-between text-[11px] text-slate-500 font-medium">
                  <span>Headcount: <strong className="text-slate-900 dark:text-white">{br.headcount}</strong></span>
                  <span className="text-emerald-600 font-bold">Active</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* SUB-TAB 3: Departments Section */}
      {activeSubTab === 'departments' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                <Layers className="w-5 h-5 text-blue-500" />
                <span>Enterprise Departments</span>
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">Departmental budget allocations & headcount capacity tracking.</p>
            </div>
            <button
              onClick={() => setIsAddDeptModalOpen(true)}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-bold transition shadow-md"
            >
              <Plus className="w-4 h-4" />
              <span>Add Department</span>
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {departments.map((dept) => (
              <div key={dept.id} className="p-5 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 space-y-3 shadow-sm hover:shadow-md transition">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono font-bold bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 px-2 py-0.5 rounded border border-slate-200 dark:border-slate-700">
                    {dept.code || 'DEPT'}
                  </span>
                  <span className="text-xs font-mono font-bold text-emerald-600 dark:text-emerald-400">{dept.budgetAllocation}</span>
                </div>
                <h4 className="text-base font-extrabold text-slate-900 dark:text-white">{dept.name}</h4>
                <p className="text-xs text-slate-600 dark:text-slate-400 font-medium">Department Head: <span className="text-slate-900 dark:text-white font-bold">{dept.headName}</span></p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* SUB-TAB 4: Designations Section */}
      {activeSubTab === 'designations' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                <Award className="w-5 h-5 text-emerald-500" />
                <span>Standardized Designations Catalog</span>
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">Job level hierarchy, grade bands & salary benchmarking matrix.</p>
            </div>
            <button
              onClick={() => setIsAddDesgModalOpen(true)}
              className="flex items-center space-x-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold transition shadow-md"
            >
              <Plus className="w-4 h-4" />
              <span>Add Designation</span>
            </button>
          </div>

          <div className="space-y-3">
            {designations.map((desg) => (
              <div key={desg.id} className="p-4 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 flex items-center justify-between gap-4 shadow-sm hover:shadow-md transition">
                <div>
                  <div className="flex items-center space-x-2">
                    <h4 className="text-sm font-extrabold text-slate-900 dark:text-white">{desg.title}</h4>
                    <span className="px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 font-mono text-[10px] font-bold border border-slate-200 dark:border-slate-700">
                      Grade {desg.level}
                    </span>
                  </div>
                  <p className="text-xs text-slate-600 dark:text-slate-400 font-medium mt-0.5">Department: {desg.department}</p>
                </div>
                <span className="text-xs font-mono font-bold text-emerald-600 dark:text-emerald-400">{desg.salaryBand}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* SUB-TAB 5: Settings */}
      {activeSubTab === 'settings' && (
        <div className="p-6 bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-2xl space-y-4 shadow-sm">
          <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
            <Settings className="w-5 h-5 text-red-500" />
            <span>Tenant Security & Administrative Governance Settings</span>
          </h3>
          <div className="space-y-3 text-xs">
            <div className="flex items-center justify-between p-3.5 bg-slate-50 dark:bg-slate-950/80 rounded-xl border border-slate-200 dark:border-slate-800">
              <div>
                <div className="font-bold text-slate-900 dark:text-white">Strict Multi-Tenant Partitioning</div>
                <div className="text-slate-500">Cross-tenant data isolation strictly enforced by database foreign keys</div>
              </div>
              <span className="px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-bold border border-emerald-500/30">Active</span>
            </div>

            <div className="flex items-center justify-between p-3.5 bg-slate-50 dark:bg-slate-950/80 rounded-xl border border-slate-200 dark:border-slate-800">
              <div>
                <div className="font-bold text-slate-900 dark:text-white">Role-Based Access Control (RBAC)</div>
                <div className="text-slate-500">Tenant-scoped granular permissions for recruiters, interviewers & hiring managers</div>
              </div>
              <span className="px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-bold border border-emerald-500/30">Enforced</span>
            </div>
          </div>
        </div>
      )}

      {/* Modal: Add Branch */}
      {isAddBranchModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl w-full max-w-md p-6 space-y-4 shadow-2xl text-slate-900 dark:text-white">
            <h3 className="text-lg font-black">Add Office Branch</h3>
            <form onSubmit={handleAddBranchSubmit} className="space-y-3 text-xs">
              <div>
                <label className="font-bold text-slate-700 dark:text-slate-300">Branch Name</label>
                <input
                  required
                  type="text"
                  placeholder="e.g. London Office"
                  value={branchForm.name}
                  onChange={(e) => setBranchForm({ ...branchForm, name: e.target.value })}
                  className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-red-500"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-bold text-slate-700 dark:text-slate-300">Branch Code</label>
                  <input
                    required
                    type="text"
                    placeholder="LON"
                    value={branchForm.code}
                    onChange={(e) => setBranchForm({ ...branchForm, code: e.target.value })}
                    className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-red-500"
                  />
                </div>
                <div>
                  <label className="font-bold text-slate-700 dark:text-slate-300">City</label>
                  <input
                    required
                    type="text"
                    placeholder="London"
                    value={branchForm.city}
                    onChange={(e) => setBranchForm({ ...branchForm, city: e.target.value })}
                    className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-red-500"
                  />
                </div>
              </div>

              <div className="flex justify-end space-x-3 pt-4 border-t border-slate-200 dark:border-slate-800">
                <button
                  type="button"
                  onClick={() => setIsAddBranchModalOpen(false)}
                  className="px-4 py-2 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-xl font-bold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-red-600 text-white rounded-xl font-bold shadow-md"
                >
                  Save Branch
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal: Add Department */}
      {isAddDeptModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl w-full max-w-md p-6 space-y-4 shadow-2xl text-slate-900 dark:text-white">
            <h3 className="text-lg font-black">Add Department</h3>
            <form onSubmit={handleAddDeptSubmit} className="space-y-3 text-xs">
              <div>
                <label className="font-bold text-slate-700 dark:text-slate-300">Department Name</label>
                <input
                  required
                  type="text"
                  placeholder="e.g. Artificial Intelligence"
                  value={deptForm.name}
                  onChange={(e) => setDeptForm({ ...deptForm, name: e.target.value })}
                  className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-blue-500"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-bold text-slate-700 dark:text-slate-300">Code</label>
                  <input
                    required
                    type="text"
                    placeholder="AI"
                    value={deptForm.code}
                    onChange={(e) => setDeptForm({ ...deptForm, code: e.target.value })}
                    className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="font-bold text-slate-700 dark:text-slate-300">Budget Allocation</label>
                  <input
                    required
                    type="text"
                    placeholder="$250,000"
                    value={deptForm.budgetAllocation}
                    onChange={(e) => setDeptForm({ ...deptForm, budgetAllocation: e.target.value })}
                    className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-blue-500"
                  />
                </div>
              </div>

              <div className="flex justify-end space-x-3 pt-4 border-t border-slate-200 dark:border-slate-800">
                <button
                  type="button"
                  onClick={() => setIsAddDeptModalOpen(false)}
                  className="px-4 py-2 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-xl font-bold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-xl font-bold shadow-md"
                >
                  Save Department
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal: Add Designation */}
      {isAddDesgModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl w-full max-w-md p-6 space-y-4 shadow-2xl text-slate-900 dark:text-white">
            <h3 className="text-lg font-black">Add Designation</h3>
            <form onSubmit={handleAddDesgSubmit} className="space-y-3 text-xs">
              <div>
                <label className="font-bold text-slate-700 dark:text-slate-300">Designation Title</label>
                <input
                  required
                  type="text"
                  placeholder="e.g. Senior AI Engineer"
                  value={desgForm.title}
                  onChange={(e) => setDesgForm({ ...desgForm, title: e.target.value })}
                  className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-emerald-500"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-bold text-slate-700 dark:text-slate-300">Grade Level</label>
                  <input
                    required
                    type="text"
                    placeholder="L5"
                    value={desgForm.level}
                    onChange={(e) => setDesgForm({ ...desgForm, level: e.target.value })}
                    className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-emerald-500"
                  />
                </div>
                <div>
                  <label className="font-bold text-slate-700 dark:text-slate-300">Salary Band</label>
                  <input
                    required
                    type="text"
                    placeholder="$140,000 - $180,000"
                    value={desgForm.salaryBand}
                    onChange={(e) => setDesgForm({ ...desgForm, salaryBand: e.target.value })}
                    className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-emerald-500"
                  />
                </div>
              </div>

              <div className="flex justify-end space-x-3 pt-4 border-t border-slate-200 dark:border-slate-800">
                <button
                  type="button"
                  onClick={() => setIsAddDesgModalOpen(false)}
                  className="px-4 py-2 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-xl font-bold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-emerald-600 text-white rounded-xl font-bold shadow-md"
                >
                  Save Designation
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal: Create Organization (Platform Admin) */}
      <CreateOrganizationModal 
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
      />
    </div>
  );
};
