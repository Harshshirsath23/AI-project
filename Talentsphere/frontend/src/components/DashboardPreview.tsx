import React, { useState } from 'react';
import { 
  LogOut, 
  Cpu, 
  ShieldCheck, 
  CheckCircle2, 
  Users, 
  TrendingUp, 
  Briefcase, 
  Activity, 
  Clock, 
  Sparkles
} from 'lucide-react';
import { UserPreset, AIAgentStatus } from '../types';
import confetti from 'canvas-confetti';

interface DashboardPreviewProps {
  user: UserPreset;
  onLogout: () => void;
  region: string;
}

export const DashboardPreview: React.FC<DashboardPreviewProps> = ({
  user,
  onLogout,
  region,
}) => {
  const [agents] = useState<AIAgentStatus[]>([
    {
      id: 'ag-1',
      name: 'Executive Sourcing Agent',
      category: 'Headhunting & Outreach',
      status: 'active',
      metric: '142 Candidates Screened/hr',
      uptime: '99.99%',
    },
    {
      id: 'ag-2',
      name: 'Technical Skill & Code Matcher',
      category: 'Competency Evaluation',
      status: 'processing',
      metric: '89% Precision Alignment',
      uptime: '99.98%',
    },
    {
      id: 'ag-3',
      name: 'EEOC & Diversity Sentinel',
      category: 'Compliance & Audit',
      status: 'active',
      metric: '100% Bias Shield Active',
      uptime: '100%',
    },
    {
      id: 'ag-4',
      name: 'Offer Negotiation & Insights',
      category: 'Compensation Intelligence',
      status: 'standby',
      metric: 'Real-time Benchmark',
      uptime: '99.95%',
    },
  ]);

  const triggerConfettiEffect = () => {
    confetti({
      particleCount: 80,
      spread: 70,
      origin: { y: 0.6 },
      colors: ['#ffffff', '#27272a', '#10b981'],
    });
  };

  React.useEffect(() => {
    triggerConfettiEffect();
  }, []);

  return (
    <div className="w-full space-y-6 animate-fade-in text-left">
      {/* Top Banner - Executive Styling */}
      <div className="always-dark flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-emerald-950 via-slate-900 to-zinc-950 p-6 rounded-2xl border border-emerald-900/50 shadow-2xl backdrop-blur-md text-white">
        <div className="flex items-center space-x-4">
          <div className="p-3.5 rounded-2xl bg-emerald-600/30 text-emerald-400 border border-emerald-500/40 shadow-lg shadow-emerald-600/20">
            <Cpu className="w-8 h-8" />
          </div>
          <div>
            <div className="flex items-center space-x-3">
              <h1 className="text-2xl font-black text-white tracking-tight">TalentSphere Command Center</h1>
              <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 flex items-center space-x-1.5">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                <span>Live Session</span>
              </span>
            </div>
            <p className="text-xs text-slate-300 mt-1 font-mono flex items-center space-x-2">
              <span>Tenant: {user.company}</span>
              <span>•</span>
              <span>Data Region: {region}</span>
              <span>•</span>
              <span className="flex items-center space-x-1"><Sparkles className="w-3 h-3"/> Authenticated via Okta SAML 2.0</span>
            </p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-3">
            <img
              src={user.avatar}
              alt={user.name}
              className="w-10 h-10 rounded-full object-cover border-2 border-emerald-500/40 shadow-md"
            />
            <div className="hidden sm:block text-left">
              <p className="text-sm font-bold text-white flex items-center gap-1">
                {user.name}
              </p>
              <p className="text-[11px] text-emerald-300 font-mono">{user.role}</p>
            </div>
          </div>
          <button
            onClick={onLogout}
            className="px-3 py-1.5 rounded-xl bg-white/10 hover:bg-white/20 text-white border border-white/20 transition flex items-center gap-1.5 text-xs font-bold"
            title="Log out of session"
          >
            <LogOut className="w-4 h-4" />
            <span className="hidden md:inline">Sign Out</span>
          </button>
        </div>
      </div>

      <div className="p-6 bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-2xl space-y-4 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900 dark:text-white flex items-center space-x-2">
             Welcome back, {user.name}
          </h2>
          <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
            Your autonomous recruitment agents are active across 18 executive pipelines with 0 compliance flags.
          </p>
        </div>
        <button
          onClick={triggerConfettiEffect}
          className="px-5 py-2.5 rounded-xl bg-slate-900 dark:bg-slate-800 text-white font-bold text-xs tracking-wide transition flex items-center gap-2 shrink-0 shadow-md border border-slate-700"
        >
          <Activity className="w-4 h-4 text-emerald-400" /> System Health Check
        </button>
      </div>

      {/* Metrics Overview */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition cursor-pointer group">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-500 dark:text-slate-400 font-semibold uppercase tracking-wider">Active Openings</span>
            <Briefcase className="w-5 h-5 text-red-500 group-hover:scale-110 transition" />
          </div>
          <div className="mt-3 text-3xl font-black text-slate-900 dark:text-white font-mono">24</div>
          <p className="text-xs text-emerald-600 dark:text-emerald-400 font-bold mt-2 flex items-center gap-1">
            <TrendingUp className="w-3.5 h-3.5" /> +12% AI match velocity
          </p>
        </div>

        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition cursor-pointer group">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-500 dark:text-slate-400 font-semibold uppercase tracking-wider">Candidates Screened</span>
            <Users className="w-5 h-5 text-blue-500 group-hover:scale-110 transition" />
          </div>
          <div className="mt-3 text-3xl font-black text-slate-900 dark:text-white font-mono">1,420</div>
          <p className="text-xs text-slate-600 dark:text-slate-400 font-bold mt-2">94% Precision score</p>
        </div>

        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition cursor-pointer group">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-500 dark:text-slate-400 font-semibold uppercase tracking-wider">Offer Acceptance</span>
            <CheckCircle2 className="w-5 h-5 text-emerald-500 group-hover:scale-110 transition" />
          </div>
          <div className="mt-3 text-3xl font-black text-slate-900 dark:text-white font-mono">91.8%</div>
          <p className="text-xs text-slate-600 dark:text-slate-400 font-bold mt-2">Enterprise Leader</p>
        </div>

        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition cursor-pointer group">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-500 dark:text-slate-400 font-semibold uppercase tracking-wider">Security Status</span>
            <ShieldCheck className="w-5 h-5 text-emerald-500 group-hover:scale-110 transition" />
          </div>
          <div className="mt-3 text-2xl font-black text-emerald-600 dark:text-emerald-400 font-mono">SOC 2 Type II</div>
          <p className="text-xs text-slate-600 dark:text-slate-400 font-bold mt-2">0 Security Alerts</p>
        </div>
      </div>

      {/* AI Agents Grid */}
      <div className="p-6 bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
            <Cpu className="w-5 h-5 text-red-500" />
            <span>Autonomous Recruitment Agents</span>
          </h3>
          <span className="text-xs text-slate-500 dark:text-slate-400 font-bold">4 Operational Agents</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {agents.map((agent) => (
            <div
              key={agent.id}
              className="p-5 rounded-xl bg-slate-50 dark:bg-slate-950/80 border border-slate-200 dark:border-slate-800 flex items-center justify-between shadow-sm hover:shadow-md transition"
            >
              <div className="space-y-1.5">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-extrabold text-slate-900 dark:text-white">{agent.name}</span>
                  <span
                    className={`text-[10px] font-mono font-bold uppercase px-2 py-0.5 rounded border ${
                      agent.status === 'active'
                        ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/30'
                        : 'bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-700'
                    }`}
                  >
                    {agent.status}
                  </span>
                </div>
                <p className="text-xs text-slate-600 dark:text-slate-400 font-medium">{agent.category}</p>
                <p className="text-xs text-slate-800 dark:text-slate-200 font-mono font-bold">{agent.metric}</p>
              </div>
              <div className="text-right text-xs text-slate-500 dark:text-slate-400 font-mono font-bold">
                Uptime {agent.uptime}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Audit Trail Log */}
      <div className="p-6 bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
            <Clock className="w-5 h-5 text-red-500" />
            <span>Identity & Access Log</span>
          </h3>
          <span className="text-[11px] text-emerald-600 dark:text-emerald-400 font-mono font-bold bg-emerald-500/10 px-2 py-1 rounded border border-emerald-500/30">AES-256 Encrypted</span>
        </div>
        <div className="space-y-3 text-xs font-mono">
          <div className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-950/80 border border-slate-200 dark:border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-2">
            <span className="text-emerald-600 dark:text-emerald-400 font-bold">[VERIFIED] SAML2_SSO_AUTHENTICATION</span>
            <span className="text-slate-700 dark:text-slate-300 font-semibold">User: {user.email}</span>
            <span className="text-slate-500">Just now</span>
          </div>
          <div className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-950/80 border border-slate-200 dark:border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-2">
            <span className="text-slate-700 dark:text-slate-300 font-bold">[SUCCESS] MFA_CHALLENGE_PASSED</span>
            <span className="text-slate-600 dark:text-slate-400 font-semibold">TOTP Auth Token Generated</span>
            <span className="text-slate-500">1 min ago</span>
          </div>
        </div>
      </div>
    </div>
  );
};
