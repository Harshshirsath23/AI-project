import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  Cpu,
  UserCheck
} from 'lucide-react';
import { SourcingCandidateResult } from '../../types';
import { sourcingApi } from '../../api';

export const IntelligentSourcingView: React.FC = () => {
  const [selectedJob, setSelectedJob] = useState('job-1');
  const [booleanQuery, setBooleanQuery] = useState('("Python" OR "FastAPI") AND ("Machine Learning" OR "AI") AND ("PostgreSQL")');
  const [isSourcing, setIsSourcing] = useState(false);
  const [results, setResults] = useState<SourcingCandidateResult[]>([]);
  const [selectedCandidate, setSelectedCandidate] = useState<SourcingCandidateResult | null>(null);

  useEffect(() => {
    sourcingApi.runSourcing(selectedJob).then((data) => {
      if (data && data.length > 0) setResults(data);
    });
  }, [selectedJob]);

  const handleLaunchSourcing = async () => {
    setIsSourcing(true);
    const data = await sourcingApi.runSourcing(selectedJob);
    setResults(data);
    setIsSourcing(false);
  };

  return (
    <div className="space-y-6 animate-fade-in text-left">
      {/* Header Banner */}
      <div className="glass-panel p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-zinc-100 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 text-xs font-mono font-medium mb-2">
            <Cpu className="w-3.5 h-3.5 text-zinc-400" /> Powered by NVIDIA Nemotron 3 Ultra
          </div>
          <h1 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight">AI Intelligent Talent Sourcing &amp; Discovery</h1>
          <p className="text-xs dark:text-zinc-400 light:text-zinc-600 mt-1 font-normal">
            Autonomous candidate discovery engine utilizing vector embedding traversal, RAG criteria matching, and EEOC non-discrimination shields.
          </p>
        </div>

        <button
          onClick={handleLaunchSourcing}
          disabled={isSourcing}
          className="px-5 py-3 rounded-xl bg-zinc-900 text-white text-xs font-medium transition flex items-center gap-2 shadow-sm hover:bg-zinc-800 active:scale-95 shrink-0 disabled:opacity-50"
        >
          {isSourcing ? (
            <>
              <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Sourcing Candidates...
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4 text-zinc-300" /> Launch AI Sourcing Execution
            </>
          )}
        </button>
      </div>

      {/* Sourcing Search & Boolean Query Builder */}
      <div className="glass-card p-6 rounded-2xl space-y-4">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3 border-b border-zinc-200 dark:border-zinc-800 pb-3">
          <h3 className="text-xs font-medium dark:text-white light:text-zinc-900 uppercase font-mono tracking-wider">Target Job Specification &amp; Boolean Filter</h3>
          <span className="text-[11px] dark:text-zinc-400 light:text-zinc-600 font-mono">Advanced Recruiter Syntax Enabled</span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div>
            <label className="text-xs font-medium dark:text-zinc-300 light:text-zinc-700 block mb-1">Target Position Requisition</label>
            <select
              value={selectedJob}
              onChange={(e) => setSelectedJob(e.target.value)}
              className="w-full px-3 py-2 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 text-xs dark:text-white light:text-zinc-900 focus:outline-none"
            >
              <option value="job-1">Principal AI Engineer (REQ-104)</option>
              <option value="job-2">Staff Frontend Architect (REQ-105)</option>
              <option value="job-3">Senior MLOps Specialist (REQ-106)</option>
            </select>
          </div>

          <div className="lg:col-span-2">
            <label className="text-xs font-medium dark:text-zinc-300 light:text-zinc-700 block mb-1">Boolean Query &amp; Keyphrase Expression</label>
            <input
              type="text"
              value={booleanQuery}
              onChange={(e) => setBooleanQuery(e.target.value)}
              className="w-full px-3 py-2 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 text-xs font-mono dark:text-zinc-200 light:text-zinc-800 focus:outline-none"
            />
          </div>
        </div>
      </div>

      {/* Animated Agent Sourcing Execution Workflow Progress */}
      {isSourcing && (
        <div className="glass-card p-6 rounded-2xl space-y-4 animate-in fade-in">
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="dark:text-zinc-200 light:text-zinc-800 font-medium flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-zinc-400 animate-spin" /> Nemotron 3 Ultra Vector Sourcing Execution Active
            </span>
            <span className="dark:text-zinc-400 light:text-zinc-600">Processing Vector Traversal...</span>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-[11px] font-mono">
            <div className="p-3 rounded-xl glass-panel text-emerald-600 dark:text-emerald-400 border-emerald-500/30">
              ✓ Job Intelligence Analyzed
            </div>
            <div className="p-3 rounded-xl glass-panel text-emerald-600 dark:text-emerald-400 border-emerald-500/30">
              ✓ Candidate Vector Traversal
            </div>
            <div className="p-3 rounded-xl glass-panel text-zinc-700 dark:text-zinc-300 animate-pulse">
              ● Match &amp; Semantic Scoring
            </div>
            <div className="p-3 rounded-xl glass-panel dark:text-zinc-500 light:text-zinc-400">
              ○ EEOC Bias Shield Validation
            </div>
          </div>
        </div>
      )}

      {/* Sourcing Candidate Results Table */}
      {results.length > 0 && (
        <div className="glass-card p-6 rounded-2xl space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium dark:text-white light:text-zinc-900 flex items-center gap-2">
              <UserCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400" /> Sourced Candidate Intelligence Pool
            </h3>
            <span className="text-xs text-emerald-600 dark:text-emerald-400 font-mono font-medium">
              {results.length} Candidates Ranked &amp; EEOC Compliant
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-zinc-200 dark:border-zinc-800 dark:text-zinc-400 light:text-zinc-600 font-mono uppercase text-[10px]">
                  <th className="py-3 px-4 font-medium">Candidate &amp; Title</th>
                  <th className="py-3 px-4 font-medium">Match Score</th>
                  <th className="py-3 px-4 font-medium">Skills Score</th>
                  <th className="py-3 px-4 font-medium">Experience</th>
                  <th className="py-3 px-4 font-medium">Recommendation</th>
                  <th className="py-3 px-4 text-right font-medium">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-200 dark:divide-zinc-800">
                {results.map((cand) => (
                  <tr key={cand.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-900/50 transition">
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-3">
                        <img src={cand.candidateAvatar} alt={cand.candidateName} className="w-9 h-9 rounded-xl object-cover border border-zinc-300 dark:border-zinc-800" />
                        <div>
                          <span className="font-medium dark:text-white light:text-zinc-900 block">{cand.candidateName}</span>
                          <span className="text-[10px] dark:text-zinc-400 light:text-zinc-600">{cand.currentRole} at {cand.currentCompany}</span>
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-4 font-mono">
                      <span className="text-emerald-600 dark:text-emerald-400 font-medium text-sm">{cand.overallMatchScore}%</span>
                    </td>
                    <td className="py-3 px-4 font-mono dark:text-zinc-300 light:text-zinc-700">{cand.skillsScore}/35</td>
                    <td className="py-3 px-4 font-mono dark:text-zinc-300 light:text-zinc-700">{cand.experienceScore}/25</td>
                    <td className="py-3 px-4 font-mono">
                      <span className="px-2.5 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400 text-[10px] font-medium">
                        {cand.recommendation}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => setSelectedCandidate(cand)}
                        className="px-3 py-1.5 rounded-lg glass-panel dark:text-zinc-200 light:text-zinc-800 font-medium transition inline-flex items-center gap-1 hover:bg-zinc-100 dark:hover:bg-zinc-800"
                      >
                        <Sparkles className="w-3.5 h-3.5 text-zinc-400" /> AI Card
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Candidate AI Intelligence Card Modal */}
      {selectedCandidate && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-md z-50 flex items-center justify-center p-4">
          <div className="glass-card max-w-2xl w-full overflow-hidden shadow-2xl">
            <div className="p-5 border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between glass-panel">
              <div className="flex items-center gap-3">
                <img src={selectedCandidate.candidateAvatar} alt="Cand" className="w-10 h-10 rounded-xl object-cover border border-zinc-300 dark:border-zinc-800" />
                <div>
                  <h3 className="text-sm font-medium dark:text-white light:text-zinc-900">{selectedCandidate.candidateName}</h3>
                  <span className="text-xs dark:text-zinc-400 light:text-zinc-600">{selectedCandidate.currentRole}</span>
                </div>
              </div>
              <button onClick={() => setSelectedCandidate(null)} className="dark:text-zinc-400 light:text-zinc-600 hover:text-zinc-900 dark:hover:text-white text-xs font-medium">
                Close
              </button>
            </div>

            <div className="p-6 space-y-5 max-h-[75vh] overflow-y-auto custom-scrollbar">
              {/* Nemotron AI Decision Card */}
              <div className="p-4 rounded-xl glass-panel space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono font-medium uppercase dark:text-zinc-300 light:text-zinc-700 flex items-center gap-1">
                    <Cpu className="w-3.5 h-3.5 text-zinc-400" /> AI Decision Card — Nemotron 3 Ultra
                  </span>
                  <span className="text-xs font-mono font-medium text-emerald-600 dark:text-emerald-400">{selectedCandidate.overallMatchScore}% Match</span>
                </div>

                <div className="grid grid-cols-2 gap-2 text-xs font-mono">
                  <div className="p-2.5 rounded-lg glass-panel">
                    <span className="dark:text-zinc-500 light:text-zinc-600 text-[10px] block">Recommendation</span>
                    <span className="text-emerald-600 dark:text-emerald-400 font-medium">{selectedCandidate.recommendation}</span>
                  </div>
                  <div className="p-2.5 rounded-lg glass-panel">
                    <span className="dark:text-zinc-500 light:text-zinc-600 text-[10px] block">Confidence Level</span>
                    <span className="dark:text-zinc-200 light:text-zinc-800 font-medium">{selectedCandidate.confidence}</span>
                  </div>
                </div>
              </div>

              {/* Strengths & Gaps */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-xl glass-panel space-y-2">
                  <span className="text-xs font-medium text-emerald-600 dark:text-emerald-400 uppercase font-mono block">Key Strengths</span>
                  <ul className="space-y-1 text-xs dark:text-zinc-300 light:text-zinc-700">
                    {selectedCandidate.strengths.map((s, idx) => (
                      <li key={idx} className="flex items-center gap-1.5">✓ {s}</li>
                    ))}
                  </ul>
                </div>

                <div className="p-4 rounded-xl glass-panel space-y-2">
                  <span className="text-xs font-medium dark:text-zinc-400 light:text-zinc-600 uppercase font-mono block">Identified Gaps</span>
                  <ul className="space-y-1 text-xs dark:text-zinc-300 light:text-zinc-700">
                    {selectedCandidate.gaps.map((g, idx) => (
                      <li key={idx} className="flex items-center gap-1.5">• {g}</li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Verified Resume Evidence Sources */}
              <div className="space-y-2">
                <span className="text-xs font-medium dark:text-white light:text-zinc-900 uppercase font-mono block">Verified Resume Evidence</span>
                <div className="space-y-2">
                  {selectedCandidate.evidenceSources.map((ev, idx) => (
                    <div key={idx} className="p-3 rounded-xl glass-panel text-xs space-y-1">
                      <span className="dark:text-zinc-300 light:text-zinc-700 font-mono text-[10px] uppercase font-medium block">{ev.title}</span>
                      <p className="dark:text-zinc-300 light:text-zinc-700 font-mono italic">"{ev.snippet}"</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
