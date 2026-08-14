import React, { useState, useEffect } from 'react';
import { 
  Building2, 
  ShieldAlert, 
  Users, 
  Plus, 
  CheckCircle2, 
  XCircle, 
  Key, 
  Search, 
  Activity, 
  Lock, 
  Globe, 
  BarChart3,
  RefreshCw,
  Shield,
  Eye,
  Sliders,
  Filter,
  ArrowUpRight,
  Server,
  Layers
} from 'lucide-react';
import { platformApi } from '../../api/client';
import { PlatformMetrics } from '../../types';

interface PlatformAdminDashboardViewProps {
  activeTab?: string;
  onNavigate?: (tabId: string) => void;
}

export const PlatformAdminDashboardView: React.FC<PlatformAdminDashboardViewProps> = ({ 
  activeTab = 'platform-dashboard',
  onNavigate 
}) => {
  const [metrics, setMetrics] = useState<PlatformMetrics | null>(null);
  const [organizations, setOrganizations] = useState<any[]>([]);
  const [auditLogs, setAuditLogs] = useState<any[]>([]);
  const [roles, setRoles] = useState<any[]>([]);
  const [permissionsCatalog, setPermissionsCatalog] = useState<{ platform_permissions: any[]; organization_permissions: any[]; catalog: any[] }>({
    platform_permissions: [],
    organization_permissions: [],
    catalog: []
  });
  
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<'ALL' | 'Active' | 'Suspended'>('ALL');
  const [severityFilter, setSeverityFilter] = useState<string>('ALL');
  const [isLoading, setIsLoading] = useState(true);

  // Modals
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isResetAdminModalOpen, setIsResetAdminModalOpen] = useState(false);
  const [isOrgDetailModalOpen, setIsOrgDetailModalOpen] = useState(false);
  const [isEventDetailModalOpen, setIsEventDetailModalOpen] = useState(false);
  
  const [selectedOrg, setSelectedOrg] = useState<any | null>(null);
  const [selectedEvent, setSelectedEvent] = useState<any | null>(null);

  // Forms
  const [createForm, setCreateForm] = useState({
    organization_code: '',
    legal_name: '',
    display_name: '',
    subscription_plan: 'Enterprise Tier 1',
    admin_email: '',
    admin_first_name: '',
    admin_last_name: '',
    admin_password: 'Password123!'
  });

  const [adminForm, setAdminForm] = useState({
    email: '',
    first_name: '',
    last_name: '',
    password: 'Password123!'
  });

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [mRes, orgsRes, auditRes, rolesRes, permsRes] = await Promise.all([
        platformApi.getMetrics(),
        platformApi.getOrganizations(),
        platformApi.getAuditLogs(),
        platformApi.getRoles(),
        platformApi.getPermissions()
      ]);
      if (mRes) setMetrics(mRes);
      if (orgsRes && Array.isArray(orgsRes)) setOrganizations(orgsRes);
      if (auditRes && Array.isArray(auditRes)) setAuditLogs(auditRes);
      if (rolesRes && Array.isArray(rolesRes)) setRoles(rolesRes);
      if (permsRes) setPermissionsCatalog(permsRes);
    } catch (err) {
      console.error('[PlatformAdmin] Error fetching platform data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateOrg = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = {
        ...createForm,
        industry_id: '00000000-0000-0000-0000-000000000000',
        subscription_status: 'Active'
      };
      const res = await platformApi.createOrganization(payload);
      if (res && res.status === 'success') {
        const adminEmail = res.admin_user?.email || createForm.admin_email || `admin@${createForm.organization_code.toLowerCase()}.com`;
        const adminPwd = res.admin_user?.temporary_password || createForm.admin_password || 'Password123!';
        alert(`Organization "${createForm.display_name}" created successfully!\n\nProvisioned Org Super Admin Credentials:\nEmail: ${adminEmail}\nPassword: ${adminPwd}`);
        setIsCreateModalOpen(false);
        setCreateForm({
          organization_code: '',
          legal_name: '',
          display_name: '',
          subscription_plan: 'Enterprise Tier 1',
          admin_email: '',
          admin_first_name: '',
          admin_last_name: '',
          admin_password: 'Password123!'
        });
        loadData();
      }
    } catch (err: any) {
      alert(`Failed to create organization: ${err?.message || 'Unknown error'}`);
    }
  };

  const handleToggleOrgStatus = async (orgId: string, currentStatus: string) => {
    try {
      if (currentStatus === 'Active') {
        await platformApi.suspendOrganization(orgId);
      } else {
        await platformApi.activateOrganization(orgId);
      }
      loadData();
    } catch (err) {
      alert('Action failed');
    }
  };

  const handleProvisionAdmin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedOrg) return;
    try {
      const res = await platformApi.provisionOrgAdmin(selectedOrg.id, {
        email: adminForm.email,
        first_name: adminForm.first_name || 'Org',
        last_name: adminForm.last_name || 'Admin',
        password: adminForm.password || 'Password123!'
      });
      if (res && res.status === 'success') {
        alert(`Org Super Admin Provisioned for ${selectedOrg.display_name}!\n\nCredentials:\nEmail: ${res.email}\nPassword: ${res.temporary_password}`);
        setIsResetAdminModalOpen(false);
        loadData();
      }
    } catch (err: any) {
      alert(`Failed to provision admin: ${err?.message || 'Unknown error'}`);
    }
  };

  const filteredOrgs = organizations.filter(o => {
    const matchesSearch = o.display_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          o.organization_code?.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === 'ALL' || o.subscription_status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const filteredAuditLogs = auditLogs.filter(e => {
    const matchesSearch = e.event_type?.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          e.description?.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesSev = severityFilter === 'ALL' || e.severity === severityFilter;
    return matchesSearch && matchesSev;
  });

  const currentTab = activeTab;

  return (
    <div className="w-full space-y-6">
      {/* Platform Header Banner - Always Dark Theme Styled for Executive Punch */}
      <div className="always-dark flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-red-950 via-slate-900 to-zinc-950 p-6 rounded-2xl border border-red-900/50 shadow-2xl backdrop-blur-md text-white">
        <div>
          <div className="flex items-center space-x-3">
            <div className="p-3 rounded-2xl bg-red-600/30 text-red-400 border border-red-500/40 shadow-lg shadow-red-600/20">
              <Globe className="w-7 h-7" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h1 className="text-2xl font-extrabold text-white tracking-tight">Platform Super Admin Control Center</h1>
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-red-500/30 text-red-300 border border-red-500/40 uppercase tracking-widest">Global Scope</span>
              </div>
              <p className="text-xs text-slate-300 mt-1">Multi-Tenant Platform Governance, Organization Provisioning & Global Security</p>
            </div>
          </div>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={loadData}
            className="flex items-center space-x-2 px-4 py-2.5 bg-slate-800/90 hover:bg-slate-700 text-white rounded-xl border border-slate-700 text-xs font-semibold transition shadow-md"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Sync System</span>
          </button>
          <button
            onClick={() => setIsCreateModalOpen(true)}
            className="flex items-center space-x-2 px-4 py-2.5 bg-red-600 hover:bg-red-500 text-white rounded-xl font-bold text-xs transition shadow-lg shadow-red-600/30"
          >
            <Plus className="w-4 h-4" />
            <span>Provision New Tenant</span>
          </button>
        </div>
      </div>

      {/* Top Metrics Cards - Theme Adaptive */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-500 dark:text-slate-400 font-semibold uppercase tracking-wider">Total Enrolled Tenants</span>
            <div className="p-2 rounded-xl bg-red-500/10 text-red-500 dark:text-red-400">
              <Building2 className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3 text-3xl font-black text-slate-900 dark:text-white">{metrics?.total_organizations ?? organizations.length}</div>
          <div className="mt-2 flex items-center space-x-1.5 text-xs text-emerald-600 dark:text-emerald-400 font-semibold">
            <ArrowUpRight className="w-3.5 h-3.5" />
            <span>Active Tenant Partitioning</span>
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-500 dark:text-slate-400 font-semibold uppercase tracking-wider">Active Organizations</span>
            <div className="p-2 rounded-xl bg-emerald-500/10 text-emerald-500 dark:text-emerald-400">
              <CheckCircle2 className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3 text-3xl font-black text-slate-900 dark:text-white">
            {metrics?.active_organizations ?? organizations.filter(o => o.subscription_status === 'Active').length}
          </div>
          <div className="mt-2 flex items-center space-x-1 text-xs text-slate-500 dark:text-slate-400 font-medium">
            <span>Operational & Healthy</span>
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-500 dark:text-slate-400 font-semibold uppercase tracking-wider">Suspended Tenants</span>
            <div className="p-2 rounded-xl bg-amber-500/10 text-amber-500 dark:text-amber-400">
              <XCircle className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3 text-3xl font-black text-slate-900 dark:text-white">
            {metrics?.suspended_organizations ?? organizations.filter(o => o.subscription_status === 'Suspended').length}
          </div>
          <div className="mt-2 flex items-center space-x-1 text-xs text-amber-600 dark:text-amber-400 font-semibold">
            <span>Tenant Lock Enforced</span>
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-500 dark:text-slate-400 font-semibold uppercase tracking-wider">Total Platform Users</span>
            <div className="p-2 rounded-xl bg-blue-500/10 text-blue-500 dark:text-blue-400">
              <Users className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3 text-3xl font-black text-slate-900 dark:text-white">{metrics?.total_users ?? 12}</div>
          <div className="mt-2 flex items-center space-x-1 text-xs text-blue-600 dark:text-blue-400 font-semibold">
            <span>Across All Tenants</span>
          </div>
        </div>
      </div>

      {/* VIEW SECTION 1: Control Center Dashboard Overview */}
      {(currentTab === 'platform-dashboard' || currentTab === 'dashboard') && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Quick Actions Panel */}
            <div className="lg:col-span-1 p-6 bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-2xl space-y-4 shadow-sm">
              <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                <Sliders className="w-5 h-5 text-red-500 dark:text-red-400" />
                <span>Platform Quick Governance</span>
              </h2>
              <div className="space-y-2.5">
                <button
                  onClick={() => setIsCreateModalOpen(true)}
                  className="w-full flex items-center justify-between p-3.5 bg-slate-50 hover:bg-slate-100 dark:bg-slate-950/80 dark:hover:bg-slate-800/80 border border-slate-200 dark:border-slate-800 rounded-xl text-left transition group"
                >
                  <div>
                    <div className="font-bold text-slate-900 dark:text-white text-xs group-hover:text-red-600 dark:group-hover:text-red-400 transition">Provision New Tenant</div>
                    <div className="text-[11px] text-slate-500 dark:text-slate-400">Create organization & initial Org Super Admin</div>
                  </div>
                  <Plus className="w-4 h-4 text-slate-400 group-hover:text-red-500" />
                </button>

                <button
                  onClick={() => onNavigate && onNavigate('platform-orgs')}
                  className="w-full flex items-center justify-between p-3.5 bg-slate-50 hover:bg-slate-100 dark:bg-slate-950/80 dark:hover:bg-slate-800/80 border border-slate-200 dark:border-slate-800 rounded-xl text-left transition group"
                >
                  <div>
                    <div className="font-bold text-slate-900 dark:text-white text-xs group-hover:text-red-600 dark:group-hover:text-red-400 transition">Manage Tenant Access</div>
                    <div className="text-[11px] text-slate-500 dark:text-slate-400">Activate or suspend tenant organizations</div>
                  </div>
                  <Building2 className="w-4 h-4 text-slate-400 group-hover:text-red-500" />
                </button>

                <button
                  onClick={() => onNavigate && onNavigate('platform-roles')}
                  className="w-full flex items-center justify-between p-3.5 bg-slate-50 hover:bg-slate-100 dark:bg-slate-950/80 dark:hover:bg-slate-800/80 border border-slate-200 dark:border-slate-800 rounded-xl text-left transition group"
                >
                  <div>
                    <div className="font-bold text-slate-900 dark:text-white text-xs group-hover:text-red-600 dark:group-hover:text-red-400 transition">Inspect System Permissions</div>
                    <div className="text-[11px] text-slate-500 dark:text-slate-400">Global vs Organization scope permissions</div>
                  </div>
                  <Shield className="w-4 h-4 text-slate-400 group-hover:text-red-500" />
                </button>
              </div>
            </div>

            {/* Platform Tenant Health Overview */}
            <div className="lg:col-span-2 p-6 bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-2xl space-y-4 shadow-sm">
              <div className="flex items-center justify-between">
                <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                  <Activity className="w-5 h-5 text-emerald-500 dark:text-emerald-400" />
                  <span>Tenant Partitioning Health</span>
                </h2>
                <span className="text-xs font-mono text-slate-500 dark:text-slate-400 font-semibold">Platform Isolation: ENFORCED</span>
              </div>

              <div className="p-4 bg-slate-50 dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800/80 rounded-xl space-y-3">
                <div className="flex justify-between text-xs font-bold">
                  <span className="text-slate-700 dark:text-slate-300">Active vs Suspended Distribution</span>
                  <span className="text-emerald-600 dark:text-emerald-400 font-mono">
                    {organizations.length > 0 ? Math.round((organizations.filter(o => o.subscription_status === 'Active').length / organizations.length) * 100) : 100}% Active
                  </span>
                </div>
                <div className="w-full h-3 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden flex">
                  <div 
                    className="bg-emerald-500 h-full transition-all duration-500" 
                    style={{ width: `${organizations.length > 0 ? (organizations.filter(o => o.subscription_status === 'Active').length / organizations.length) * 100 : 100}%` }}
                  />
                  <div 
                    className="bg-amber-500 h-full transition-all duration-500" 
                    style={{ width: `${organizations.length > 0 ? (organizations.filter(o => o.subscription_status === 'Suspended').length / organizations.length) * 100 : 0}%` }}
                  />
                </div>
                <div className="flex items-center justify-between text-[11px] font-semibold text-slate-600 dark:text-slate-400 pt-1">
                  <div className="flex items-center space-x-1.5">
                    <div className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                    <span>Active ({organizations.filter(o => o.subscription_status === 'Active').length})</span>
                  </div>
                  <div className="flex items-center space-x-1.5">
                    <div className="w-2.5 h-2.5 rounded-full bg-amber-500" />
                    <span>Suspended ({organizations.filter(o => o.subscription_status === 'Suspended').length})</span>
                  </div>
                </div>
              </div>

              {/* Recent Security Logs Preview */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider">Live Security Audit Feed</span>
                  <button 
                    onClick={() => onNavigate && onNavigate('platform-audit')}
                    className="text-xs text-red-600 dark:text-red-400 hover:underline font-bold"
                  >
                    View All Logs →
                  </button>
                </div>
                <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
                  {auditLogs.slice(0, 4).map((log) => (
                    <div key={log.id} className="p-3 bg-slate-50 dark:bg-slate-950/60 rounded-xl border border-slate-200 dark:border-slate-800/80 flex items-center justify-between text-xs">
                      <div className="flex items-center space-x-2">
                        <ShieldAlert className={`w-4 h-4 ${log.severity === 'WARNING' ? 'text-amber-500' : 'text-emerald-500'}`} />
                        <div>
                          <span className="font-bold text-slate-900 dark:text-white">{log.event_type}</span>
                          <span className="text-slate-600 dark:text-slate-400 ml-2 font-medium">{log.description}</span>
                        </div>
                      </div>
                      <span className="text-slate-500 font-mono text-[11px] font-medium">{new Date(log.event_time).toLocaleTimeString()}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* VIEW SECTION 2: Organizations Directory */}
      {(currentTab === 'platform-orgs' || currentTab === 'overview') && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="relative flex-1 w-full max-w-md">
              <Search className="w-4 h-4 absolute left-3.5 top-3 text-slate-400" />
              <input
                type="text"
                placeholder="Search organizations by name or code..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-xs text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:border-red-500"
              />
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-xs text-slate-500 dark:text-slate-400 font-semibold">Filter Status:</span>
              <button
                onClick={() => setStatusFilter('ALL')}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${statusFilter === 'ALL' ? 'bg-red-600 text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'}`}
              >
                All ({organizations.length})
              </button>
              <button
                onClick={() => setStatusFilter('Active')}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${statusFilter === 'Active' ? 'bg-emerald-600 text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'}`}
              >
                Active
              </button>
              <button
                onClick={() => setStatusFilter('Suspended')}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${statusFilter === 'Suspended' ? 'bg-amber-600 text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'}`}
              >
                Suspended
              </button>
            </div>
          </div>

          <div className="bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden shadow-xl">
            <table className="w-full text-left text-xs text-slate-700 dark:text-slate-300">
              <thead className="bg-slate-50 dark:bg-slate-950/90 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider border-b border-slate-200 dark:border-slate-800">
                <tr>
                  <th className="px-6 py-4">Organization</th>
                  <th className="px-6 py-4">Code</th>
                  <th className="px-6 py-4">Plan</th>
                  <th className="px-6 py-4">Status</th>
                  <th className="px-6 py-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">
                {filteredOrgs.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-6 py-12 text-center text-slate-500 font-medium">
                      No matching organization tenants found.
                    </td>
                  </tr>
                ) : (
                  filteredOrgs.map((org) => (
                    <tr key={org.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/40 transition">
                      <td className="px-6 py-4">
                        <div className="font-extrabold text-slate-900 dark:text-white text-sm">{org.display_name}</div>
                        <div className="text-xs text-slate-500 dark:text-slate-400 font-medium">{org.legal_name}</div>
                      </td>
                      <td className="px-6 py-4 font-mono text-xs font-bold text-red-600 dark:text-red-400">{org.organization_code}</td>
                      <td className="px-6 py-4">
                        <span className="px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-700">
                          {org.subscription_plan}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <span className={`px-3 py-1 rounded-full text-xs font-bold ${org.subscription_status === 'Active' ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20' : 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20'}`}>
                          {org.subscription_status}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right space-x-2">
                        <button
                          onClick={() => {
                            setSelectedOrg(org);
                            setIsOrgDetailModalOpen(true);
                          }}
                          className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg text-xs font-bold transition inline-flex items-center space-x-1"
                        >
                          <Eye className="w-3.5 h-3.5" />
                          <span>Details</span>
                        </button>
                        <button
                          onClick={() => {
                            setSelectedOrg(org);
                            setIsResetAdminModalOpen(true);
                          }}
                          className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg text-xs font-bold transition inline-flex items-center space-x-1"
                        >
                          <Key className="w-3.5 h-3.5" />
                          <span>Provision Admin</span>
                        </button>
                        <button
                          onClick={() => handleToggleOrgStatus(org.id, org.subscription_status)}
                          className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${org.subscription_status === 'Active' ? 'bg-amber-100 text-amber-700 border border-amber-300 dark:bg-amber-950/40 dark:text-amber-400 dark:border-amber-800/40' : 'bg-emerald-100 text-emerald-700 border border-emerald-300 dark:bg-emerald-950/40 dark:text-emerald-400 dark:border-emerald-800/40'}`}
                        >
                          {org.subscription_status === 'Active' ? 'Suspend' : 'Activate'}
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* VIEW SECTION 3: Global Roles & Permissions */}
      {currentTab === 'platform-roles' && (
        <div className="space-y-6">
          <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
            <div>
              <h2 className="text-lg font-extrabold text-slate-900 dark:text-white flex items-center space-x-2">
                <Shield className="w-5 h-5 text-red-500 dark:text-red-400" />
                <span>Global System Roles & Permission Catalog</span>
              </h2>
              <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">Categorized system permissions by PLATFORM vs ORGANIZATION authorization scopes.</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Platform Scope Permissions */}
            <div className="p-6 bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-2xl space-y-4 shadow-sm">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Globe className="w-5 h-5 text-red-500 dark:text-red-400" />
                  <h3 className="font-extrabold text-slate-900 dark:text-white text-base">Platform Scope Permissions</h3>
                </div>
                <span className="px-2.5 py-1 rounded-full text-xs font-mono font-bold bg-red-100 text-red-700 dark:bg-red-950/40 dark:text-red-400 border border-red-200 dark:border-red-900/40">
                  {permissionsCatalog.platform_permissions.length} System Rules
                </span>
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">Strictly reserved for Platform Super Admins. Organization Super Admins cannot possess or assign these permissions.</p>

              <div className="space-y-2 max-h-96 overflow-y-auto pr-1">
                {permissionsCatalog.platform_permissions.map((p) => (
                  <div key={p.code} className="p-3 bg-slate-50 dark:bg-slate-950/80 border border-slate-200 dark:border-slate-800/80 rounded-xl space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-xs font-bold text-red-600 dark:text-red-400">{p.code}</span>
                      <span className="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase bg-slate-200 dark:bg-slate-900 px-2 py-0.5 rounded-full">{p.module}</span>
                    </div>
                    <div className="text-xs font-bold text-slate-900 dark:text-white">{p.name}</div>
                    <div className="text-xs text-slate-600 dark:text-slate-400 font-medium">{p.description}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Organization Scope Permissions */}
            <div className="p-6 bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-2xl space-y-4 shadow-sm">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Building2 className="w-5 h-5 text-emerald-500 dark:text-emerald-400" />
                  <h3 className="font-extrabold text-slate-900 dark:text-white text-base">Organization Scope Permissions</h3>
                </div>
                <span className="px-2.5 py-1 rounded-full text-xs font-mono font-bold bg-emerald-100 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-900/40">
                  {permissionsCatalog.organization_permissions.length} Tenant Rules
                </span>
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">Assignable by Organization Super Admins to tenant users within their organization partition.</p>

              <div className="space-y-2 max-h-96 overflow-y-auto pr-1">
                {permissionsCatalog.organization_permissions.map((p) => (
                  <div key={p.code} className="p-3 bg-slate-50 dark:bg-slate-950/80 border border-slate-200 dark:border-slate-800/80 rounded-xl space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-xs font-bold text-emerald-600 dark:text-emerald-400">{p.code}</span>
                      <span className="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase bg-slate-200 dark:bg-slate-900 px-2 py-0.5 rounded-full">{p.module}</span>
                    </div>
                    <div className="text-xs font-bold text-slate-900 dark:text-white">{p.name}</div>
                    <div className="text-xs text-slate-600 dark:text-slate-400 font-medium">{p.description}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* VIEW SECTION 4: Platform Security & Audit Logs */}
      {currentTab === 'platform-audit' && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="relative flex-1 w-full max-w-md">
              <Search className="w-4 h-4 absolute left-3.5 top-3 text-slate-400" />
              <input
                type="text"
                placeholder="Search audit events by description or type..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-xs text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:border-red-500"
              />
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-xs text-slate-500 dark:text-slate-400 font-semibold">Severity:</span>
              <button
                onClick={() => setSeverityFilter('ALL')}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${severityFilter === 'ALL' ? 'bg-red-600 text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'}`}
              >
                All
              </button>
              <button
                onClick={() => setSeverityFilter('INFO')}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${severityFilter === 'INFO' ? 'bg-blue-600 text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'}`}
              >
                Info
              </button>
              <button
                onClick={() => setSeverityFilter('WARNING')}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${severityFilter === 'WARNING' ? 'bg-amber-600 text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'}`}
              >
                Warning
              </button>
            </div>
          </div>

          <div className="bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
            <h2 className="text-lg font-extrabold text-slate-900 dark:text-white flex items-center space-x-2">
              <ShieldAlert className="w-5 h-5 text-red-500 dark:text-red-400" />
              <span>Platform Security Audit Stream</span>
            </h2>

            <div className="space-y-2 max-h-[500px] overflow-y-auto pr-1">
              {filteredAuditLogs.length === 0 ? (
                <div className="py-12 text-center text-slate-500 text-xs font-medium">No audit events found matching filters.</div>
              ) : (
                filteredAuditLogs.map((log) => (
                  <div 
                    key={log.id} 
                    onClick={() => {
                      setSelectedEvent(log);
                      setIsEventDetailModalOpen(true);
                    }}
                    className="p-4 bg-slate-50 dark:bg-slate-950/80 hover:bg-slate-100 dark:hover:bg-slate-800/50 border border-slate-200 dark:border-slate-800/80 rounded-xl flex items-center justify-between text-xs transition cursor-pointer group"
                  >
                    <div className="flex items-center space-x-3">
                      <div className={`p-2 rounded-lg ${log.severity === 'WARNING' ? 'bg-amber-500/10 text-amber-500' : 'bg-blue-500/10 text-blue-500'}`}>
                        <ShieldAlert className="w-4 h-4" />
                      </div>
                      <div>
                        <div className="flex items-center space-x-2">
                          <span className="font-extrabold text-slate-900 dark:text-white group-hover:text-red-600 dark:group-hover:text-red-400 transition">{log.event_type}</span>
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${log.severity === 'WARNING' ? 'bg-amber-100 text-amber-700 dark:bg-amber-500/20 dark:text-amber-400' : 'bg-blue-100 text-blue-700 dark:bg-blue-500/20 dark:text-blue-400'}`}>
                            {log.severity}
                          </span>
                        </div>
                        <p className="text-slate-600 dark:text-slate-400 font-medium mt-0.5">{log.description}</p>
                      </div>
                    </div>
                    <div className="text-right font-mono">
                      <div className="text-slate-600 dark:text-slate-400 font-semibold">{new Date(log.event_time).toLocaleDateString()}</div>
                      <div className="text-[10px] text-slate-500">{new Date(log.event_time).toLocaleTimeString()}</div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}

      {/* Modal: Create Organization */}
      {isCreateModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl w-full max-w-lg p-6 space-y-4 shadow-2xl text-slate-900 dark:text-white">
            <h3 className="text-xl font-black">Provision Tenant & Org Super Admin</h3>
            <form onSubmit={handleCreateOrg} className="space-y-4 text-xs">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-slate-700 dark:text-slate-400 font-bold">Org Code</label>
                  <input
                    required
                    type="text"
                    placeholder="e.g. ACME"
                    value={createForm.organization_code}
                    onChange={(e) => setCreateForm({ ...createForm, organization_code: e.target.value })}
                    className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:border-red-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="text-slate-700 dark:text-slate-400 font-bold">Display Name</label>
                  <input
                    required
                    type="text"
                    placeholder="e.g. Acme Corp"
                    value={createForm.display_name}
                    onChange={(e) => setCreateForm({ ...createForm, display_name: e.target.value })}
                    className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:border-red-500 focus:outline-none"
                  />
                </div>
              </div>
              <div>
                <label className="text-slate-700 dark:text-slate-400 font-bold">Legal Registered Name</label>
                <input
                  required
                  type="text"
                  placeholder="e.g. Acme Corporation Inc."
                  value={createForm.legal_name}
                  onChange={(e) => setCreateForm({ ...createForm, legal_name: e.target.value })}
                  className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:border-red-500 focus:outline-none"
                />
              </div>

              <div className="border-t border-slate-200 dark:border-slate-800 pt-3">
                <h4 className="font-extrabold text-red-600 dark:text-red-400 text-xs uppercase tracking-wider mb-2">Initial Organization Super Admin</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-slate-700 dark:text-slate-400 font-bold">Admin Email</label>
                    <input
                      required
                      type="email"
                      placeholder="admin@acme.com"
                      value={createForm.admin_email}
                      onChange={(e) => setCreateForm({ ...createForm, admin_email: e.target.value })}
                      className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:border-red-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="text-slate-700 dark:text-slate-400 font-bold">Initial Password</label>
                    <input
                      required
                      type="text"
                      value={createForm.admin_password}
                      onChange={(e) => setCreateForm({ ...createForm, admin_password: e.target.value })}
                      className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:border-red-500 focus:outline-none"
                    />
                  </div>
                </div>
              </div>

              <div className="flex justify-end space-x-3 pt-4 border-t border-slate-200 dark:border-slate-800">
                <button
                  type="button"
                  onClick={() => setIsCreateModalOpen(false)}
                  className="px-4 py-2 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-xl text-xs font-bold hover:bg-slate-200 dark:hover:bg-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-red-600 text-white rounded-xl text-xs font-bold hover:bg-red-500 shadow-lg shadow-red-600/25"
                >
                  Provision Tenant
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal: Org Detail Inspection */}
      {isOrgDetailModalOpen && selectedOrg && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl w-full max-w-md p-6 space-y-4 shadow-2xl text-slate-900 dark:text-white">
            <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
              <h3 className="text-lg font-black">{selectedOrg.display_name}</h3>
              <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-red-100 text-red-700 dark:bg-red-950/40 dark:text-red-400 border border-red-200 dark:border-red-900/40 font-mono">
                {selectedOrg.organization_code}
              </span>
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <span className="text-slate-500 font-semibold">Legal Name:</span>
                <div className="font-extrabold text-slate-900 dark:text-white">{selectedOrg.legal_name}</div>
              </div>
              <div>
                <span className="text-slate-500 font-semibold">Subscription Plan:</span>
                <div className="font-bold text-slate-900 dark:text-white">{selectedOrg.subscription_plan}</div>
              </div>
              <div>
                <span className="text-slate-500 font-semibold">Status:</span>
                <div className="font-extrabold text-emerald-600 dark:text-emerald-400">{selectedOrg.subscription_status}</div>
              </div>
            </div>

            <div className="flex justify-end pt-4 border-t border-slate-200 dark:border-slate-800">
              <button
                onClick={() => setIsOrgDetailModalOpen(false)}
                className="px-4 py-2 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-xl text-xs font-bold hover:bg-slate-200 dark:hover:bg-slate-700"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal: Provision Admin */}
      {isResetAdminModalOpen && selectedOrg && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl w-full max-w-md p-6 space-y-4 shadow-2xl text-slate-900 dark:text-white">
            <h3 className="text-lg font-black">Provision Org Admin for {selectedOrg.display_name}</h3>
            <form onSubmit={handleProvisionAdmin} className="space-y-3 text-xs">
              <div>
                <label className="text-slate-700 dark:text-slate-400 font-bold">Admin Email</label>
                <input
                  required
                  type="email"
                  placeholder="orgadmin@domain.com"
                  value={adminForm.email}
                  onChange={(e) => setAdminForm({ ...adminForm, email: e.target.value })}
                  className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:border-red-500 focus:outline-none"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-700 dark:text-slate-400 font-bold">First Name</label>
                  <input
                    required
                    type="text"
                    placeholder="Jane"
                    value={adminForm.first_name}
                    onChange={(e) => setAdminForm({ ...adminForm, first_name: e.target.value })}
                    className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:border-red-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="text-slate-700 dark:text-slate-400 font-bold">Last Name</label>
                  <input
                    required
                    type="text"
                    placeholder="Doe"
                    value={adminForm.last_name}
                    onChange={(e) => setAdminForm({ ...adminForm, last_name: e.target.value })}
                    className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:border-red-500 focus:outline-none"
                  />
                </div>
              </div>
              <div>
                <label className="text-slate-700 dark:text-slate-400 font-bold">Temporary Password</label>
                <input
                  required
                  type="text"
                  value={adminForm.password}
                  onChange={(e) => setAdminForm({ ...adminForm, password: e.target.value })}
                  className="w-full mt-1 p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:border-red-500 focus:outline-none"
                />
              </div>

              <div className="flex justify-end space-x-3 pt-4 border-t border-slate-200 dark:border-slate-800">
                <button
                  type="button"
                  onClick={() => setIsResetAdminModalOpen(false)}
                  className="px-4 py-2 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-xl text-xs font-bold hover:bg-slate-200 dark:hover:bg-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-red-600 text-white rounded-xl text-xs font-bold hover:bg-red-500"
                >
                  Confirm Provisioning
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
