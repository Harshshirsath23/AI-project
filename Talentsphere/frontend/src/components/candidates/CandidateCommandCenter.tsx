import React, { useState } from 'react';
import { useOrganization } from '../../context/OrganizationContext';
import { Candidate } from '../../types';
import { CandidateProfileView } from './CandidateProfileView';
import { ResumeUploadModal } from './ResumeUploadModal';
import { ManualCandidateModal } from './ManualCandidateModal';
import {
  Users,
  Search,
  FileUp,
  UserPlus,
  ChevronRight,
  Filter,
  Sparkles,
  MapPin,
  Briefcase
} from 'lucide-react';

export const CandidateCommandCenter: React.FC = () => {
  const { candidates } = useOrganization();
  const [selectedCandidate, setSelectedCandidate] = useState<Candidate | null>(null);
  const [isResumeModalOpen, setIsResumeModalOpen] = useState(false);
  const [isManualModalOpen, setIsManualModalOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('All');

  if (selectedCandidate) {
    return (
      <CandidateProfileView
        candidate={selectedCandidate}
        onBack={() => setSelectedCandidate(null)}
      />
    );
  }

  const filteredCandidates = candidates.filter((c) => {
    const matchesSearch =
      c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.skills.some((s) => s.toLowerCase().includes(searchQuery.toLowerCase())) ||
      c.currentRole.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.currentCompany.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesStatus = statusFilter === 'All' || c.status === statusFilter;

    return matchesSearch && matchesStatus;
  });

  return (
    <div className="w-full space-y-6 animate-fade-in text-left">
      {/* Top Banner - Executive Styling */}
      <div className="always-dark flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-blue-950 via-slate-900 to-zinc-950 p-6 rounded-2xl border border-red-900/50 shadow-2xl backdrop-blur-md text-white">
        <div className="flex items-center space-x-4">
          <div className="p-3.5 rounded-2xl bg-blue-600/30 text-blue-400 border border-blue-500/40 shadow-lg shadow-blue-600/20">
            <Users className="w-8 h-8" />
          </div>
          <div>
            <div className="flex items-center space-x-3">
              <h1 className="text-2xl font-black text-white tracking-tight">Candidate Command Center</h1>
              <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 flex items-center space-x-1.5">
                <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
                <span>AI-Screened</span>
              </span>
            </div>
            <p className="text-xs text-slate-300 mt-1 font-mono">
              Directory • Real-time skill indexing & match analytics
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2.5 flex-wrap">
          <button
            onClick={() => setIsManualModalOpen(true)}
            className="flex items-center space-x-2 px-4 py-2.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold rounded-xl transition shadow-lg shadow-blue-600/30"
          >
            <UserPlus className="w-4 h-4" /> <span>Add Candidate</span>
          </button>

          <button
            onClick={() => setIsResumeModalOpen(true)}
            className="flex items-center space-x-2 px-4 py-2.5 bg-white hover:bg-slate-100 text-slate-900 text-xs font-bold rounded-xl transition shadow-lg"
          >
            <FileUp className="w-4 h-4" /> <span>Upload AI Resume</span>
          </button>
        </div>
      </div>

      {/* KPI Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition cursor-pointer group">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-500 dark:text-slate-400 font-semibold uppercase tracking-wider">Total Candidates</span>
            <Users className="w-5 h-5 text-red-500 group-hover:scale-110 transition" />
          </div>
          <div className="mt-3 text-3xl font-black text-slate-900 dark:text-white font-mono">{candidates.length}</div>
          <p className="mt-2 text-xs text-emerald-600 dark:text-emerald-400 font-bold">100% Vector Indexed</p>
        </div>
        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition cursor-pointer group">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-500 dark:text-slate-400 font-semibold uppercase tracking-wider">Active Interviewing</span>
            <Briefcase className="w-5 h-5 text-blue-500 group-hover:scale-110 transition" />
          </div>
          <div className="mt-3 text-3xl font-black text-slate-900 dark:text-white font-mono">
            {candidates.filter((c) => c.status === 'Interviewing').length}
          </div>
          <p className="mt-2 text-xs text-slate-500 dark:text-slate-400 font-medium">High Pipeline Velocity</p>
        </div>
        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition cursor-pointer group">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-500 dark:text-slate-400 font-semibold uppercase tracking-wider">Avg Match Score</span>
            <Sparkles className="w-5 h-5 text-emerald-500 group-hover:scale-110 transition" />
          </div>
          <div className="mt-3 text-3xl font-black text-emerald-600 dark:text-emerald-400 font-mono">93.7%</div>
          <p className="mt-2 text-xs text-slate-500 dark:text-slate-400 font-medium">Top Tier Precision</p>
        </div>
        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition cursor-pointer group">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-500 dark:text-slate-400 font-semibold uppercase tracking-wider">Offers Extended</span>
            <UserPlus className="w-5 h-5 text-purple-500 group-hover:scale-110 transition" />
          </div>
          <div className="mt-3 text-3xl font-black text-slate-900 dark:text-white font-mono">
            {candidates.filter((c) => c.status === 'Offered' || c.status === 'Hired').length}
          </div>
          <p className="mt-2 text-xs text-slate-500 dark:text-slate-400 font-medium">Ready for Acceptance</p>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="p-5 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search candidates by name, role, company, or skills..."
            className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-sm font-medium text-slate-900 dark:text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
          />
        </div>

        <div className="flex items-center gap-2 overflow-x-auto w-full md:w-auto">
          <Filter className="w-4 h-4 text-slate-400 mr-2" />
          {['All', 'New', 'Screening', 'Interviewing', 'Offered'].map((status) => (
            <button
              key={status}
              onClick={() => setStatusFilter(status)}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition whitespace-nowrap ${statusFilter === status
                  ? 'bg-blue-600 text-white shadow-md'
                  : 'bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700'
                }`}
            >
              {status}
            </button>
          ))}
        </div>
      </div>

      {/* Candidates List Grid */}
      <div className="space-y-3">
        {filteredCandidates.map((candidate) => (
          <div
            key={candidate.id}
            onClick={() => setSelectedCandidate(candidate)}
            className="p-5 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition cursor-pointer flex flex-col md:flex-row md:items-center justify-between gap-4 group"
          >
            <div className="flex items-center gap-4">
              <img
                src={candidate.avatar}
                alt={candidate.name}
                className="w-14 h-14 rounded-xl object-cover border border-slate-200 dark:border-slate-700 shrink-0"
              />
              <div className="space-y-1">
                <div className="flex flex-wrap items-center gap-2">
                  <h4 className="text-base font-extrabold text-slate-900 dark:text-white">{candidate.name}</h4>
                  <span className="px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 font-mono text-[10px] font-bold border border-slate-200 dark:border-slate-700">
                    {candidate.status}
                  </span>
                </div>
                <p className="text-xs text-slate-600 dark:text-slate-400 font-medium flex items-center gap-1">
                  {candidate.currentRole} • <span className="font-bold text-slate-900 dark:text-slate-300">{candidate.currentCompany}</span>
                  {candidate.location && candidate.location !== 'Not Specified' && (
                    <>
                       • <MapPin className="w-3 h-3 text-slate-400 ml-1" /> {candidate.location}
                    </>
                  )}
                </p>
                <div className="flex flex-wrap items-center gap-2 pt-1">
                  {candidate.skills.slice(0, 5).map((skill, i) => (
                    <span key={i} className="px-2.5 py-1 rounded bg-slate-50 dark:bg-slate-950 text-slate-700 dark:text-slate-300 text-[10px] font-mono font-semibold border border-slate-200 dark:border-slate-800">
                      {skill}
                    </span>
                  ))}
                  {candidate.skills.length > 5 && (
                    <span className="text-[10px] text-slate-500 font-mono font-bold ml-1">+{candidate.skills.length - 5} more</span>
                  )}
                </div>
              </div>
            </div>

            <div className="flex items-center gap-4 self-end md:self-center shrink-0">
              <div className="text-right">
                <span className="text-[10px] font-mono font-bold text-slate-500 block uppercase">AI Match</span>
                <span className="text-xl font-black text-emerald-600 dark:text-emerald-400 font-mono">{candidate.matchScore}%</span>
              </div>
              <div className="p-2 bg-slate-50 dark:bg-slate-800 rounded-lg group-hover:bg-blue-50 dark:group-hover:bg-blue-900/20 transition">
                 <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-blue-500 transition" />
              </div>
            </div>
          </div>
        ))}

        {filteredCandidates.length === 0 && (
          <div className="p-12 text-center rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3">
            <Users className="w-10 h-10 text-slate-400 mx-auto" />
            <h3 className="text-base font-bold text-slate-900 dark:text-white">No candidates match your current search criteria.</h3>
            <p className="text-xs text-slate-500 font-medium">Try adjusting your keyword query or status filters.</p>
          </div>
        )}
      </div>

      {/* Manual Candidate Addition Modal */}
      <ManualCandidateModal
        isOpen={isManualModalOpen}
        onClose={() => setIsManualModalOpen(false)}
      />

      {/* Resume Upload Modal */}
      <ResumeUploadModal
        isOpen={isResumeModalOpen}
        onClose={() => setIsResumeModalOpen(false)}
      />
    </div>
  );
};
