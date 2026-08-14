import React from 'react';
import { useOrganization } from '../../context/OrganizationContext';
import {
  Users,
  Briefcase,
  Sparkles,
  TrendingUp,
  FileUp,
  ShieldAlert,
  ChevronRight,
  ArrowUpRight,
  Kanban
} from 'lucide-react';
import { ProProjectCard } from '../ui/ProProjectCard';

interface DashboardOverviewProps {
  onNavigate: (tabId: string) => void;
}

export const DashboardOverview: React.FC<DashboardOverviewProps> = ({ onNavigate }) => {
  const { candidates, jobs, hitlTasks } = useOrganization();

  const pendingHitlCount = hitlTasks.filter((t) => t.status === 'Pending').length;

  return (
    <div className="space-y-8 text-left animate-fade-in w-full">
      {/* Welcome Hero Banner */}
      <div className="p-6 sm:p-8 rounded-3xl glass-card flex flex-col md:flex-row md:items-center justify-between gap-6 relative overflow-hidden border border-zinc-200/80 dark:border-zinc-800/80 shadow-2xl bg-white dark:bg-gradient-to-r dark:from-zinc-950 dark:via-zinc-900 dark:to-zinc-950">
        <div className="space-y-2 z-10">
          <div className="inline-flex items-center gap-1.5 px-3.5 py-1 rounded-full bg-zinc-100 dark:bg-zinc-800/80 border border-zinc-200 dark:border-zinc-700/80 text-zinc-800 dark:text-zinc-200 text-xs font-mono font-medium">
            <Sparkles className="w-3.5 h-3.5 text-amber-500 dark:text-amber-400" /> TalentSphere Executive Portal
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-zinc-900 dark:text-white tracking-tight">
            AI Recruitment Operating System
          </h1>
          <p className="text-xs sm:text-sm text-zinc-600 dark:text-zinc-400 max-w-2xl leading-relaxed font-normal">
            Streamlining candidate sourcing, automated skill extraction, structured scorecards, and human-governed AI workflows across your entire organization.
          </p>
        </div>

        {/* Quick Actions */}
        <div className="flex flex-wrap items-center gap-3 shrink-0 z-10">
          <button
            onClick={() => onNavigate('candidates')}
            className="px-5 py-3 rounded-2xl bg-zinc-900 dark:bg-white text-white dark:text-zinc-950 hover:bg-zinc-800 dark:hover:bg-zinc-200 text-xs font-semibold transition flex items-center gap-2 shadow-lg active:scale-95"
          >
            <FileUp className="w-4 h-4 text-white dark:text-zinc-900" /> Upload Resume
          </button>
          <button
            onClick={() => onNavigate('jobs')}
            className="px-5 py-3 rounded-2xl glass-panel text-zinc-800 dark:text-zinc-200 hover:text-zinc-950 dark:hover:text-white text-xs font-semibold transition flex items-center gap-2 border border-zinc-300 dark:border-zinc-700/80 hover:bg-zinc-100 dark:hover:bg-zinc-800/80"
          >
            <Briefcase className="w-4 h-4 text-zinc-500 dark:text-zinc-400" /> Post Job
          </button>
        </div>
      </div>



      {/* Primary KPI Summary Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 w-full">
        <div
          onClick={() => onNavigate('candidates')}
          className="p-5 rounded-2xl glass-card transition cursor-pointer space-y-2 group hover:border-zinc-400 dark:hover:border-zinc-500 bg-white dark:bg-zinc-950/80 border border-zinc-200 dark:border-zinc-800 shadow-md"
        >
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-mono font-medium uppercase text-zinc-500 dark:text-zinc-400 tracking-wider">Candidate Pool</span>
            <Users className="w-4 h-4 text-zinc-400 group-hover:scale-110 transition" />
          </div>
          <p className="text-3xl font-bold text-zinc-900 dark:text-white font-mono">{candidates.length}</p>
          <p className="text-xs text-emerald-600 dark:text-emerald-400 font-medium flex items-center gap-1">
            <ArrowUpRight className="w-3.5 h-3.5" /> 100% Parsed &amp; Indexed
          </p>
        </div>

        <div
          onClick={() => onNavigate('jobs')}
          className="p-5 rounded-2xl glass-card transition cursor-pointer space-y-2 group hover:border-zinc-400 dark:hover:border-zinc-500 bg-white dark:bg-zinc-950/80 border border-zinc-200 dark:border-zinc-800 shadow-md"
        >
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-mono font-medium uppercase text-zinc-500 dark:text-zinc-400 tracking-wider">Active Requisitions</span>
            <Briefcase className="w-4 h-4 text-zinc-400 group-hover:scale-110 transition" />
          </div>
          <p className="text-3xl font-bold text-zinc-900 dark:text-white font-mono">{jobs.length}</p>
          <p className="text-xs text-zinc-600 dark:text-zinc-300 font-medium flex items-center gap-1">
            <ArrowUpRight className="w-3.5 h-3.5" /> Benchmarked Compensation
          </p>
        </div>

        <div
          onClick={() => onNavigate('hitl-tasks')}
          className="p-5 rounded-2xl glass-card transition cursor-pointer space-y-2 group hover:border-zinc-400 dark:hover:border-zinc-500 bg-white dark:bg-zinc-950/80 border border-zinc-200 dark:border-zinc-800 shadow-md"
        >
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-mono font-medium uppercase text-zinc-500 dark:text-zinc-400 tracking-wider">HITL Approvals Queue</span>
            <ShieldAlert className="w-4 h-4 text-zinc-400 group-hover:scale-110 transition" />
          </div>
          <p className="text-3xl font-bold text-zinc-900 dark:text-white font-mono">{pendingHitlCount}</p>
          <p className="text-xs text-rose-600 dark:text-rose-400 font-medium">Requires Action</p>
        </div>

        <div
          onClick={() => onNavigate('pipelines')}
          className="p-5 rounded-2xl glass-card transition cursor-pointer space-y-2 group hover:border-zinc-400 dark:hover:border-zinc-500 bg-white dark:bg-zinc-950/80 border border-zinc-200 dark:border-zinc-800 shadow-md"
        >
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-mono font-medium uppercase text-zinc-500 dark:text-zinc-400 tracking-wider">Avg Time-to-Hire</span>
            <TrendingUp className="w-4 h-4 text-emerald-600 dark:text-emerald-400 group-hover:scale-110 transition" />
          </div>
          <p className="text-3xl font-bold text-emerald-600 dark:text-emerald-400 font-mono">14.2 Days</p>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 font-normal">68% Faster than Industry</p>
        </div>
      </div>

      {/* Candidate Pipeline Spotlight */}
      <div className="p-6 rounded-3xl glass-card space-y-4 bg-white dark:bg-zinc-950/90 border border-zinc-200 dark:border-zinc-800/80 shadow-lg w-full">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-zinc-900 dark:text-white flex items-center gap-2">
            <Users className="w-4 h-4 text-teal-600 dark:text-teal-400" /> High-Match Candidates Spotlight
          </h3>
          <button
            onClick={() => onNavigate('candidates')}
            className="text-xs font-semibold text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white transition flex items-center gap-1"
          >
            View All <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="space-y-3 w-full">
          {candidates.slice(0, 3).map((cand) => (
            <div
              key={cand.id}
              onClick={() => onNavigate('candidates')}
              className="p-4 rounded-2xl bg-zinc-50 dark:bg-zinc-900/60 hover:bg-zinc-100 dark:hover:bg-zinc-900 border border-zinc-200 dark:border-zinc-800/80 hover:border-zinc-300 dark:hover:border-zinc-700 transition cursor-pointer flex flex-col sm:flex-row sm:items-center justify-between gap-3 w-full"
            >
              <div className="flex items-center gap-3">
                <img src={cand.avatar} alt={cand.name} className="w-10 h-10 rounded-xl object-cover border border-zinc-200 dark:border-zinc-700 shadow-sm" />
                <div>
                  <h4 className="text-sm font-bold text-zinc-900 dark:text-white">{cand.name}</h4>
                  <p className="text-xs text-zinc-500 dark:text-zinc-400">{cand.currentRole} at {cand.currentCompany}</p>
                </div>
              </div>

              <div className="flex items-center gap-4 text-xs">
                <div className="text-right">
                  <span className="text-[10px] font-mono text-zinc-400 dark:text-zinc-500 block uppercase">Match Score</span>
                  <span className="font-mono font-bold text-emerald-600 dark:text-emerald-400 text-sm">{cand.matchScore}%</span>
                </div>
                <span className="px-3.5 py-1.5 rounded-full bg-zinc-200 dark:bg-zinc-800/90 border border-zinc-300 dark:border-zinc-700 font-mono text-xs font-medium text-zinc-800 dark:text-zinc-200">
                  {cand.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

