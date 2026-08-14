import React, { useState, useEffect } from 'react';
import { 
  Users, 
  ShieldCheck, 
  UserPlus, 
  KeyRound, 
  Lock, 
  CheckCircle, 
  AlertCircle,
  Plus,
  Building,
  RefreshCw
} from 'lucide-react';
import { orgAdminApi } from '../../api/client';

export const OrgAdminUsersRolesView: React.FC = () => {
  const [users, setUsers] = useState<any[]>([]);
  const [roles, setRoles] = useState<any[]>([]);
  const [permissions, setPermissions] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState<'users' | 'roles' | 'permissions'>('users');
  const [isLoading, setIsLoading] = useState(true);

  // Modals
  const [isAddUserModalOpen, setIsAddUserModalOpen] = useState(false);
  const [isAddRoleModalOpen, setIsAddRoleModalOpen] = useState(false);

  // User Form
  const [userForm, setUserForm] = useState({
    email: '',
    first_name: '',
    last_name: '',
    account_type: 'RECRUITER',
    password: 'OrgUserPassword123!'
  });

  // Role Form
  const [roleForm, setRoleForm] = useState({
    role_code: '',
    role_name: '',
    description: '',
    selectedPermissions: [] as string[]
  });

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [uRes, rRes, pRes] = await Promise.all([
        orgAdminApi.getUsers(),
        orgAdminApi.getRoles(),
        orgAdminApi.getPermissions()
      ]);
      if (uRes && Array.isArray(uRes)) setUsers(uRes);
      if (rRes && Array.isArray(rRes)) setRoles(rRes);
      if (pRes && Array.isArray(pRes)) setPermissions(pRes);
    } catch (err) {
      console.error('[OrgAdmin] Error fetching tenant data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleAddUser = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await orgAdminApi.createUser({
        username: userForm.email,
        email: userForm.email,
        first_name: userForm.first_name,
        last_name: userForm.last_name,
        account_type: userForm.account_type,
        password: userForm.password
      });
      if (res && res.status === 'success') {
        alert(`User ${userForm.email} created successfully!`);
        setIsAddUserModalOpen(false);
        setUserForm({
          email: '',
          first_name: '',
          last_name: '',
          account_type: 'RECRUITER',
          password: 'OrgUserPassword123!'
        });
        loadData();
      }
    } catch (err) {
      alert('Failed to create user');
    }
  };

  const handleAddRole = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await orgAdminApi.createCustomRole({
        role_code: roleForm.role_code,
        role_name: roleForm.role_name,
        description: roleForm.description,
        permissions: roleForm.selectedPermissions
      });
      if (res && res.status === 'success') {
        alert(`Custom role ${roleForm.role_name} created!`);
        setIsAddRoleModalOpen(false);
        setRoleForm({ role_code: '', role_name: '', description: '', selectedPermissions: [] });
        loadData();
      }
    } catch (err) {
      alert('Failed to create custom role');
    }
  };

  const togglePermissionSelection = (code: string) => {
    setRoleForm(prev => {
      const exists = prev.selectedPermissions.includes(code);
      return {
        ...prev,
        selectedPermissions: exists
          ? prev.selectedPermissions.filter(c => c !== code)
          : [...prev.selectedPermissions, code]
      };
    });
  };

  return (
    <div className="w-full space-y-6 animate-fade-in text-left">
      {/* Top Banner - Executive Styling */}
      <div className="always-dark flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-red-950 via-slate-900 to-zinc-950 p-6 rounded-2xl border border-red-900/50 shadow-2xl backdrop-blur-md text-white">
        <div className="flex items-center space-x-4">
          <div className="p-3.5 rounded-2xl bg-red-600/30 text-red-400 border border-red-500/40 shadow-lg shadow-red-600/20">
            <Building className="w-8 h-8" />
          </div>
          <div>
            <div className="flex items-center space-x-3">
              <h1 className="text-2xl font-black text-white tracking-tight">Organization Admin Control Panel</h1>
            </div>
            <p className="text-xs text-slate-300 mt-1 font-mono">
              Tenant User Management • Custom RBAC Roles • Local Governance
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={loadData}
            className="flex items-center space-x-2 px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl border border-slate-700 text-xs font-bold transition shadow-lg"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Sync Data</span>
          </button>
          <button
            onClick={() => setIsAddUserModalOpen(true)}
            className="flex items-center space-x-2 px-4 py-2.5 bg-red-600 hover:bg-red-500 text-white rounded-xl font-bold text-xs transition shadow-lg shadow-red-600/30"
          >
            <UserPlus className="w-4 h-4" />
            <span>Add User</span>
          </button>
        </div>
      </div>

      {/* Unified Sub-Navigation Tabs */}
      <div className="flex items-center space-x-2 border-b border-slate-200 dark:border-slate-800 pb-3 overflow-x-auto">
        <button
          onClick={() => setActiveTab('users')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl text-xs font-bold transition whitespace-nowrap ${activeTab === 'users' ? 'bg-red-600 text-white shadow-md' : 'bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800'}`}
        >
          <Users className="w-4 h-4" />
          <span>Tenant Users ({users.length})</span>
        </button>
        <button
          onClick={() => setActiveTab('roles')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl text-xs font-bold transition whitespace-nowrap ${activeTab === 'roles' ? 'bg-red-600 text-white shadow-md' : 'bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800'}`}
        >
          <ShieldCheck className="w-4 h-4" />
          <span>Custom Roles ({roles.length})</span>
        </button>
        <button
          onClick={() => setActiveTab('permissions')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl text-xs font-bold transition whitespace-nowrap ${activeTab === 'permissions' ? 'bg-red-600 text-white shadow-md' : 'bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800'}`}
        >
          <KeyRound className="w-4 h-4" />
          <span>Assignable Permissions Catalog</span>
        </button>
      </div>

      {/* Users Tab */}
      {activeTab === 'users' && (
        <div className="bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden shadow-sm">
          <table className="w-full text-left text-sm text-slate-700 dark:text-slate-300">
            <thead className="bg-slate-50 dark:bg-slate-950/80 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase border-b border-slate-200 dark:border-slate-800 tracking-wider">
              <tr>
                <th className="px-6 py-4">User</th>
                <th className="px-6 py-4">Account Type</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4">Roles</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">
              {users.length === 0 ? (
                <tr>
                  <td colSpan={4} className="px-6 py-8 text-center text-slate-500 font-medium">
                    No tenant users loaded yet.
                  </td>
                </tr>
              ) : (
                users.map((u) => (
                  <tr key={u.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/30 transition">
                    <td className="px-6 py-4">
                      <div className="font-extrabold text-slate-900 dark:text-white">
                        {u.profile?.first_name ? `${u.profile.first_name} ${u.profile.last_name || ''}` : u.username}
                      </div>
                      <div className="text-xs text-slate-500 font-medium mt-0.5">{u.email}</div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="px-2.5 py-1 rounded bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 font-mono text-[10px] font-bold border border-slate-200 dark:border-slate-700">
                        {u.account_type}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-mono text-[10px] font-bold border border-emerald-500/30">
                        {u.account_status || 'Active'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-xs font-mono text-slate-500 dark:text-slate-400 font-bold">
                      {u.roles?.join(', ') || 'Standard Member'}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* Roles Tab */}
      {activeTab === 'roles' && (
        <div className="space-y-4">
          <div className="flex justify-end">
            <button
              onClick={() => setIsAddRoleModalOpen(true)}
              className="flex items-center space-x-2 px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-xl text-xs font-bold transition shadow-md"
            >
              <Plus className="w-4 h-4" />
              <span>Create Custom Role</span>
            </button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {roles.map((r) => (
              <div key={r.id || r.role_code} className="p-5 bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-2xl space-y-3 shadow-sm hover:shadow-md transition">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <ShieldCheck className="w-5 h-5 text-red-500" />
                    <h3 className="font-extrabold text-slate-900 dark:text-white text-base">{r.role_name}</h3>
                  </div>
                  <span className="px-2.5 py-1 rounded bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 font-mono text-[10px] font-bold border border-slate-200 dark:border-slate-700">
                    {r.role_code}
                  </span>
                </div>
                <p className="text-xs text-slate-600 dark:text-slate-400 font-medium">{r.description || 'Tenant operational role'}</p>
                <div className="flex items-center space-x-2 text-[11px] text-slate-500 font-bold border-t border-slate-100 dark:border-slate-800/80 pt-3">
                  <span>Scope: {r.scope || 'ORGANIZATION'}</span>
                  <span>•</span>
                  <span className={r.is_system_role ? "text-red-500" : ""}>System Role: {r.is_system_role ? 'Yes' : 'No'}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Permissions Tab */}
      {activeTab === 'permissions' && (
        <div className="bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 space-y-4 shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-4">
            <div>
              <h3 className="font-bold text-slate-900 dark:text-white text-base flex items-center space-x-2">
                 <KeyRound className="w-5 h-5 text-red-500" />
                 <span>Organization Permissions Catalog</span>
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 font-medium">Strictly tenant-scoped. Platform administration permissions cannot be assigned by Organization Super Admins.</p>
            </div>
            <div className="px-3 py-1.5 bg-emerald-500/10 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400 text-[10px] rounded font-mono font-bold flex items-center space-x-1.5">
              <Lock className="w-3 h-3" />
              <span>Escalation Protection Active</span>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {permissions.map((p) => (
              <div key={p.code} className="p-4 bg-slate-50 dark:bg-slate-950/80 border border-slate-200 dark:border-slate-800 rounded-xl space-y-1.5 shadow-sm">
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-red-600 dark:text-red-400">{p.code}</span>
                  <span className="text-[10px] uppercase font-bold text-slate-600 dark:text-slate-400 bg-slate-200 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 px-2 py-0.5 rounded">{p.module}</span>
                </div>
                <div className="text-sm font-extrabold text-slate-900 dark:text-white mt-2">{p.name}</div>
                <div className="text-xs text-slate-600 dark:text-slate-400 font-medium">{p.description}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Modal: Add User */}
      {isAddUserModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl w-full max-w-md p-6 space-y-4 shadow-2xl text-slate-900 dark:text-white">
            <h3 className="text-lg font-black">Add Organization Member</h3>
            <form onSubmit={handleAddUser} className="space-y-3 text-xs">
              <div>
                <label className="font-bold text-slate-700 dark:text-slate-300">Email Address</label>
                <input
                  required
                  type="email"
                  placeholder="user@organization.com"
                  value={userForm.email}
                  onChange={(e) => setUserForm({ ...userForm, email: e.target.value })}
                  className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-red-500"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-bold text-slate-700 dark:text-slate-300">First Name</label>
                  <input
                    required
                    type="text"
                    placeholder="Alex"
                    value={userForm.first_name}
                    onChange={(e) => setUserForm({ ...userForm, first_name: e.target.value })}
                    className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-red-500"
                  />
                </div>
                <div>
                  <label className="font-bold text-slate-700 dark:text-slate-300">Last Name</label>
                  <input
                    required
                    type="text"
                    placeholder="Smith"
                    value={userForm.last_name}
                    onChange={(e) => setUserForm({ ...userForm, last_name: e.target.value })}
                    className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-red-500"
                  />
                </div>
              </div>
              <div>
                <label className="font-bold text-slate-700 dark:text-slate-300">Role / Account Type</label>
                <select
                  value={userForm.account_type}
                  onChange={(e) => setUserForm({ ...userForm, account_type: e.target.value })}
                  className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-red-500"
                >
                  <option value="HR_ADMIN">HR Admin</option>
                  <option value="RECRUITER">Recruiter</option>
                  <option value="HIRING_MANAGER">Hiring Manager</option>
                  <option value="INTERVIEWER">Interviewer</option>
                </select>
              </div>
              <div className="flex justify-end space-x-3 pt-4 border-t border-slate-200 dark:border-slate-800">
                <button
                  type="button"
                  onClick={() => setIsAddUserModalOpen(false)}
                  className="px-4 py-2 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-xl font-bold transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-xl font-bold shadow-md transition"
                >
                  Create User
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal: Add Role */}
      {isAddRoleModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl w-full max-w-lg p-6 space-y-4 shadow-2xl text-slate-900 dark:text-white">
            <h3 className="text-lg font-black">Create Custom Role</h3>
            <form onSubmit={handleAddRole} className="space-y-3 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-bold text-slate-700 dark:text-slate-300">Role Code</label>
                  <input
                    required
                    type="text"
                    placeholder="SR_RECRUITER"
                    value={roleForm.role_code}
                    onChange={(e) => setRoleForm({ ...roleForm, role_code: e.target.value })}
                    className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-red-500"
                  />
                </div>
                <div>
                  <label className="font-bold text-slate-700 dark:text-slate-300">Role Name</label>
                  <input
                    required
                    type="text"
                    placeholder="Senior Recruiter"
                    value={roleForm.role_name}
                    onChange={(e) => setRoleForm({ ...roleForm, role_name: e.target.value })}
                    className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-red-500"
                  />
                </div>
              </div>
              <div>
                <label className="font-bold text-slate-700 dark:text-slate-300">Description</label>
                <input
                  type="text"
                  placeholder="Custom permissions for senior talent acquisition staff"
                  value={roleForm.description}
                  onChange={(e) => setRoleForm({ ...roleForm, description: e.target.value })}
                  className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-red-500"
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 dark:text-slate-300">Assign Tenant Permissions</label>
                <div className="mt-1 max-h-48 overflow-y-auto space-y-1.5 border border-slate-200 dark:border-slate-800 p-2 rounded-xl bg-slate-50 dark:bg-slate-950">
                  {permissions.map((p) => (
                    <label key={p.code} className="flex items-center space-x-2 text-xs text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white cursor-pointer p-1 rounded hover:bg-slate-200 dark:hover:bg-slate-900 transition">
                      <input
                        type="checkbox"
                        checked={roleForm.selectedPermissions.includes(p.code)}
                        onChange={() => togglePermissionSelection(p.code)}
                        className="rounded border-slate-300 dark:border-slate-700 text-red-600 focus:ring-0 bg-white dark:bg-slate-900"
                      />
                      <span className="font-mono font-bold text-red-600 dark:text-red-400">{p.code}</span>
                      <span className="font-medium">({p.name})</span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="flex justify-end space-x-3 pt-4 border-t border-slate-200 dark:border-slate-800">
                <button
                  type="button"
                  onClick={() => setIsAddRoleModalOpen(false)}
                  className="px-4 py-2 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-xl font-bold transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-xl font-bold shadow-md transition"
                >
                  Save Role
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
