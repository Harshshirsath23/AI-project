import React, { useState } from 'react';
import { usePermission } from '../../context/PermissionContext';
import { useAuth } from '../../context/AuthContext';
import {
  LayoutDashboard,
  Cpu,
  Users,
  Briefcase,
  FileText,
  TrendingUp,
  GitMerge,
  Calendar,
  Video,
  ClipboardCheck,
  Award,
  Workflow,
  Sparkles,
  Building2,
  GitBranch,
  Layers,
  Award as DesgIcon,
  Settings,
  Shield,
  Lock,
  History,
  Bot,
  Globe,
  ShieldAlert,
  ChevronRight,
  ChevronLeft
} from 'lucide-react';

interface SidebarNavProps {
  activeTab: string;
  onNavigate: (tabId: string) => void;
}

export const SidebarNav: React.FC<SidebarNavProps> = ({ activeTab, onNavigate }) => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const { hasPermission } = usePermission();
  const { currentUser } = useAuth();

  const isPlatformAdmin = currentUser?.is_platform_admin || currentUser?.scope === 'PLATFORM';

  const platformGroups = [
    {
      title: 'Platform Governance',
      items: [
        { id: 'platform-dashboard', label: 'Platform Control Center', icon: Globe, badge: 'Global' },
        { id: 'platform-orgs', label: 'Organizations Directory', icon: Building2 },
        { id: 'platform-audit', label: 'Platform Security & Audit', icon: ShieldAlert },
      ],
    },
    {
      title: 'Global Administration',
      items: [
        { id: 'platform-roles', label: 'Global Roles & Permissions', icon: Shield },
      ],
    },
  ];

  const orgGroups = [
    {
      title: 'Command Center',
      items: [
        { id: 'dashboard', label: 'Overview', icon: LayoutDashboard },
        { id: 'ai-copilot', label: 'AI Recruitment Copilot', icon: Bot, badge: 'M13' },
        { id: 'ai-activity', label: 'AI Activity', icon: Cpu, badge: 'Live' },
        { id: 'ai-observability', label: 'AI Observability', icon: Sparkles, badge: 'RAG' },
      ],
    },
    {
      title: 'Recruitment & Sourcing',
      items: [
        { id: 'sourcing', label: 'Intelligent Sourcing', icon: Sparkles, badge: 'Nemotron' },
        { id: 'candidates', label: 'Candidates', icon: Users, permission: 'candidate:read' },
        { id: 'jobs', label: 'Jobs', icon: Briefcase, permission: 'job:read' },
        { id: 'applications', label: 'Applications', icon: FileText, permission: 'application:read' },
        { id: 'offers', label: 'Offers & Onboarding', icon: Award, badge: 'M8' },
        { id: 'communications', label: 'Inbox & Comms', icon: FileText, badge: 'M9' },
        { id: 'hiring-plans', label: 'Hiring Plans', icon: TrendingUp },
        { id: 'pipelines', label: 'Pipelines (Kanban)', icon: GitMerge },
      ],
    },
    {
      title: 'Interviews',
      items: [
        { id: 'interview-calendar', label: 'Interview Calendar', icon: Calendar },
        { id: 'interviews-list', label: 'Interviews', icon: Video },
        { id: 'scorecards', label: 'Scorecards', icon: ClipboardCheck },
      ],
    },
    {
      title: 'AI Intelligence & Runtime',
      items: [
        { id: 'ai-agents', label: 'Agents Registry', icon: Cpu },
        { id: 'ai-tools', label: 'Tools Registry', icon: Layers },
        { id: 'knowledge', label: 'Knowledge Base (RAG)', icon: Building2 },
        { id: 'workflow-builder', label: 'Workflow Visualizer', icon: Workflow, badge: 'Visual' },
        { id: 'agent-runtime', label: 'Agent Runtime Traces', icon: History },
        { id: 'hitl-tasks', label: 'HITL Approvals', icon: Sparkles, badge: 'Action' },
      ],
    },
    {
      title: 'Organization',
      items: [
        { id: 'org-admin-panel', label: 'Org Super Admin Panel', icon: Shield, badge: 'Tenant' },
        { id: 'org-overview', label: 'Organization Profile', icon: Building2 },
        { id: 'org-settings', label: 'Settings', icon: Settings },
      ],
    },
    {
      title: 'Administration',
      permission: 'iam:admin',
      items: [
        { id: 'iam-users', label: 'Users & Accounts', icon: Users, permission: 'iam:admin' },
        { id: 'iam-roles', label: 'Roles & RBAC', icon: Shield, permission: 'iam:admin' },
        { id: 'iam-audit', label: 'Security & Audit Logs', icon: History, permission: 'audit:read' },
      ],
    },
  ];

  const groups = isPlatformAdmin ? platformGroups : orgGroups;

  return (
    <aside
      className={`bg-black dark:bg-black light:bg-white border-r border-zinc-800 dark:border-zinc-800 light:border-zinc-200 text-zinc-300 dark:text-zinc-300 light:text-zinc-700 flex flex-col justify-between transition-all duration-300 shrink-0 sticky top-0 h-screen z-30 ${
        isCollapsed ? 'w-16' : 'w-64'
      }`}
    >
      {/* Brand Header */}
      <div className="p-4 border-b border-zinc-800 dark:border-zinc-800 light:border-zinc-200 flex items-center justify-between">
        {!isCollapsed && (
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-zinc-800 dark:bg-zinc-800 light:bg-zinc-900 flex items-center justify-center text-white">
              <Cpu className="w-4 h-4 text-white" />
            </div>
            <div>
              <span className="text-sm font-medium dark:text-white light:text-zinc-900 tracking-tight block">TalentSphere</span>
              <span className="text-[9px] font-mono font-medium text-zinc-400 dark:text-zinc-400 light:text-zinc-500 uppercase tracking-widest block">AI Recruitment OS</span>
            </div>
          </div>
        )}
        {isCollapsed && (
          <div className="w-8 h-8 mx-auto rounded-xl bg-zinc-800 dark:bg-zinc-800 light:bg-zinc-900 flex items-center justify-center text-white">
            <Cpu className="w-4 h-4 text-white" />
          </div>
        )}
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="btn-secondary p-1.5 rounded-lg text-xs font-medium transition"
          title={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {/* Navigation Links */}
      <div className="flex-1 overflow-y-auto p-3 space-y-5 custom-scrollbar">
        {groups.map((group, gIdx) => {
          if (group.permission && !hasPermission(group.permission as any)) {
            return null;
          }

          return (
            <div key={gIdx} className="space-y-1">
              {!isCollapsed && (
                <span className="px-3 text-[10px] font-mono font-medium uppercase tracking-widest text-zinc-500 dark:text-zinc-500 light:text-zinc-400 block mb-1">
                  {group.title}
                </span>
              )}
              {group.items.map((item) => {
                if (item.permission && !hasPermission(item.permission as any)) {
                  return null;
                }

                const isActive = activeTab === item.id;
                const Icon = item.icon;

                return (
                  <button
                    key={item.id}
                    onClick={() => onNavigate(item.id)}
                    className={`w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium transition group ${
                      isActive
                        ? 'active-tab-btn'
                        : 'inactive-tab-btn border border-transparent'
                    }`}
                    title={item.label}
                  >
                    <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-white dark:text-white light:text-white' : 'text-zinc-500 dark:text-zinc-400 light:text-zinc-500'}`} />
                    {!isCollapsed && <span className="truncate flex-1 text-left">{item.label}</span>}
                    {!isCollapsed && item.badge && (
                      <span className="px-1.5 py-0.5 rounded glass-panel text-[9px] font-mono font-medium uppercase">
                        {item.badge}
                      </span>
                    )}
                  </button>
                );
              })}
            </div>
          );
        })}
      </div>

      {/* Footer / System Status */}
      {!isCollapsed && (
        <div className="p-3 border-t border-zinc-800 dark:border-zinc-800 light:border-zinc-200 bg-black dark:bg-black light:bg-white text-left">
          <div className="p-2.5 rounded-xl glass-panel flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              <span className="text-[10px] font-mono dark:text-zinc-300 light:text-zinc-700 font-medium">SOC 2 Type II Shield</span>
            </div>
            <Lock className="w-3 h-3 text-zinc-400" />
          </div>
        </div>
      )}
    </aside>
  );
};
