import React, { useState } from 'react';
import { useOrganization } from '../../context/OrganizationContext';
import { useNotification } from '../../context/NotificationContext';
import {
  Briefcase,
  Plus,
  Sparkles,
  X
} from 'lucide-react';

export const JobManagementView: React.FC = () => {
  const { jobs, addJob } = useOrganization();
  const { showSuccess } = useNotification();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isAiGenerating, setIsAiGenerating] = useState(false);

  // Form state
  const [formData, setFormData] = useState({
    title: '',
    department: 'AI & Core Engineering',
    branch: 'Global HQ - Silicon Valley',
    location: 'San Francisco, CA (Hybrid)',
    type: 'Full-Time' as const,
    status: 'Active' as const,
    salaryRange: '$220,000 - $280,000 + Equity',
    openings: 2,
    recruiter: 'Alex Mercer',
    hiringManager: 'Dr. Elena Rostova',
    description: '',
    skillsRequired: 'React, TypeScript, AI Agents, Python, Distributed Systems',
  });

  const handleAiGenerateDescription = () => {
    if (!formData.title) {
      alert('Please enter a Job Title first.');
      return;
    }
    setIsAiGenerating(true);
    setTimeout(() => {
      setFormData((prev) => ({
        ...prev,
        description: `We are looking for a ${prev.title} to join our high-impact team. You will lead technical direction, design resilient scalable architectures, and collaborate closely with cross-functional AI product leads.`,
        skillsRequired: prev.skillsRequired || 'Python, PyTorch, System Design, Distributed Systems, Communication',
      }));
      setIsAiGenerating(false);
      showSuccess('AI Job Description Generated!', 'Drafted requirements based on enterprise benchmarking.');
    }, 1200);
  };

  const handleCreateJob = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.title) return;

    addJob({
      title: formData.title,
      department: formData.department,
      branch: formData.branch,
      location: formData.location,
      type: formData.type,
      status: formData.status,
      salaryRange: formData.salaryRange,
      openings: Number(formData.openings),
      recruiter: formData.recruiter,
      hiringManager: formData.hiringManager,
      description: formData.description || 'Enterprise role description.',
      requirements: [
        '5+ years relevant experience in tech / engineering leadership',
        'Proven ability to work with enterprise teams',
      ],
      skillsRequired: formData.skillsRequired.split(',').map((s) => s.trim()),
    });

    showSuccess('Job Position Posted!', `${formData.title} is now active.`);
    setIsModalOpen(false);
    setFormData({
      title: '',
      department: 'AI & Core Engineering',
      branch: 'Global HQ - Silicon Valley',
      location: 'San Francisco, CA (Hybrid)',
      type: 'Full-Time',
      status: 'Active',
      salaryRange: '$220,000 - $280,000 + Equity',
      openings: 2,
      recruiter: 'Alex Mercer',
      hiringManager: 'Dr. Elena Rostova',
      description: '',
      skillsRequired: 'React, TypeScript, AI Agents, Python, Distributed Systems',
    });
  };

  return (
    <div className="w-full space-y-6 animate-fade-in text-left">
      {/* Top Banner - Executive Styling */}
      <div className="always-dark flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-purple-950 via-slate-900 to-zinc-950 p-6 rounded-2xl border border-red-900/50 shadow-2xl backdrop-blur-md text-white">
        <div className="flex items-center space-x-4">
          <div className="p-3.5 rounded-2xl bg-purple-600/30 text-purple-400 border border-purple-500/40 shadow-lg shadow-purple-600/20">
            <Briefcase className="w-8 h-8" />
          </div>
          <div>
            <div className="flex items-center space-x-3">
              <h1 className="text-2xl font-black text-white tracking-tight">Job Openings & Requisitions</h1>
              <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 flex items-center space-x-1.5">
                <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
                <span>AI-Powered</span>
              </span>
            </div>
            <p className="text-xs text-slate-300 mt-1 font-mono">
              Enterprise position directory • AI job description generation & skill requirement indexing
            </p>
          </div>
        </div>

        <button
          onClick={() => setIsModalOpen(true)}
          className="flex items-center space-x-2 px-4 py-2.5 bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold rounded-xl transition shadow-lg shadow-purple-600/30 shrink-0"
        >
          <Plus className="w-4 h-4" /> <span>Post New Job Requisition</span>
        </button>
      </div>

      {/* Jobs Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {jobs.map((job) => (
          <div
            key={job.id}
            className="p-5 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition flex flex-col justify-between group space-y-4"
          >
            <div className="flex items-start justify-between gap-2">
              <div className="space-y-1.5">
                <div className="flex items-center gap-2">
                  <h3 className="text-lg font-extrabold text-slate-900 dark:text-white group-hover:text-purple-600 dark:group-hover:text-purple-400 transition">{job.title}</h3>
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase border ${job.status === 'Active'
                        ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/30'
                        : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border-slate-200 dark:border-slate-700'
                      }`}
                  >
                    {job.status}
                  </span>
                </div>
                <p className="text-xs text-slate-600 dark:text-slate-400 font-bold">{job.department} • {job.type}</p>
              </div>

              <div className="text-right text-xs font-mono font-bold text-slate-500 bg-slate-50 dark:bg-slate-950 px-2 py-1 rounded border border-slate-200 dark:border-slate-800">
                <span className="text-slate-900 dark:text-white font-black">{job.filled}</span> / {job.openings} Filled
              </div>
            </div>

            <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed line-clamp-2 font-medium">
              {job.description}
            </p>

            <div className="flex flex-wrap gap-1.5">
              {job.skillsRequired.map((skill, i) => (
                <span key={i} className="px-2.5 py-1 rounded bg-slate-50 dark:bg-slate-950 text-slate-700 dark:text-slate-300 text-[10px] font-mono font-bold border border-slate-200 dark:border-slate-800">
                  {skill}
                </span>
              ))}
            </div>

            <div className="pt-4 border-t border-slate-200 dark:border-slate-800 flex flex-wrap items-center justify-between text-xs text-slate-600 dark:text-slate-400 font-semibold">
              <span>{job.location}</span>
              <span className="text-emerald-600 dark:text-emerald-400 font-mono font-black">{job.salaryRange}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Create Job Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-150">
          <div className="w-full max-w-xl rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 text-left relative space-y-5 shadow-2xl max-h-[90vh] overflow-y-auto custom-scrollbar">
            <button
              onClick={() => setIsModalOpen(false)}
              className="absolute top-5 right-5 p-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition"
            >
              <X className="w-4 h-4" />
            </button>

            <div>
              <h3 className="text-lg font-black text-slate-900 dark:text-white">Create New Job Requisition</h3>
              <p className="text-xs font-medium text-slate-500 mt-1">Fill in details or use AI to draft description.</p>
            </div>

            <form onSubmit={handleCreateJob} className="space-y-4 text-xs font-medium">
              <div>
                <label className="text-slate-700 dark:text-slate-300 font-bold block mb-1">Job Title</label>
                <input
                  type="text"
                  required
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  placeholder="e.g. Principal AI Systems Engineer"
                  className="w-full px-3 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-white focus:outline-none focus:border-purple-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-slate-700 dark:text-slate-300 font-bold block mb-1">Department</label>
                  <input
                    type="text"
                    value={formData.department}
                    onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                    className="w-full px-3 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-white focus:outline-none focus:border-purple-500"
                  />
                </div>
                <div>
                  <label className="text-slate-700 dark:text-slate-300 font-bold block mb-1">Salary Band</label>
                  <input
                    type="text"
                    value={formData.salaryRange}
                    onChange={(e) => setFormData({ ...formData, salaryRange: e.target.value })}
                    className="w-full px-3 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-white focus:outline-none focus:border-purple-500 font-mono"
                  />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="text-slate-700 dark:text-slate-300 font-bold">Job Description</label>
                  <button
                    type="button"
                    onClick={handleAiGenerateDescription}
                    disabled={isAiGenerating}
                    className="text-[11px] text-slate-700 dark:text-slate-300 font-bold flex items-center gap-1.5 hover:text-purple-500 dark:hover:text-purple-400 transition"
                  >
                    <Sparkles className="w-3.5 h-3.5 text-amber-500" /> Auto-Draft with AI
                  </button>
                </div>
                <textarea
                  rows={4}
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Role summary, responsibilities..."
                  className="w-full px-3 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-white focus:outline-none focus:border-purple-500 leading-relaxed"
                />
              </div>

              <div>
                <label className="text-slate-700 dark:text-slate-300 font-bold block mb-1">Skills Required (comma-separated)</label>
                <input
                  type="text"
                  value={formData.skillsRequired}
                  onChange={(e) => setFormData({ ...formData, skillsRequired: e.target.value })}
                  className="w-full px-3 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-white focus:outline-none focus:border-purple-500 font-mono"
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-200 dark:border-slate-800">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold hover:bg-slate-200 dark:hover:bg-slate-700 transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold transition shadow-md"
                >
                  Publish Requisition
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
