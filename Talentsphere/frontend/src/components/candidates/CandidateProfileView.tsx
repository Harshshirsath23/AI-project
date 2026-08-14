import React, { useState } from 'react';
import { Candidate } from '../../types';
import {
  ArrowLeft,
  Mail,
  Phone,
  MapPin,
  Briefcase,
  GraduationCap,
  FileText,
  Clock,
  Sparkles,
  CheckCircle2,
  Award
} from 'lucide-react';

interface CandidateProfileViewProps {
  candidate: Candidate;
  onBack: () => void;
}

export const CandidateProfileView: React.FC<CandidateProfileViewProps> = ({
  candidate,
  onBack,
}) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'experience' | 'skills' | 'documents' | 'timeline'>('overview');

  return (
    <div className="space-y-6 text-left animate-fade-in">
      {/* Top Navigation */}
      <button
        onClick={onBack}
        className="px-3.5 py-1.5 rounded-xl glass-panel text-zinc-700 dark:text-zinc-300 hover:text-zinc-900 dark:hover:text-white transition flex items-center gap-2 text-xs font-medium"
      >
        <ArrowLeft className="w-3.5 h-3.5" /> Back to Candidate Directory
      </button>

      {/* Hero Header Card */}
      <div className="p-6 rounded-2xl glass-card relative overflow-hidden">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="flex items-center gap-4">
            <img
              src={candidate.avatar}
              alt={candidate.name}
              className="w-20 h-20 rounded-2xl object-cover border border-zinc-300 dark:border-zinc-700 shrink-0"
            />
            <div className="space-y-1">
              <div className="flex flex-wrap items-center gap-2">
                <h2 className="text-xl font-medium dark:text-white light:text-zinc-900">{candidate.name}</h2>
                <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30 text-[10px] font-mono font-medium uppercase">
                  {candidate.status}
                </span>
              </div>
              <p className="text-xs dark:text-zinc-300 light:text-zinc-700 font-medium">{candidate.currentRole} at {candidate.currentCompany}</p>
              <div className="flex flex-wrap items-center gap-4 text-xs dark:text-zinc-400 light:text-zinc-600 pt-1 font-normal">
                <span className="flex items-center gap-1"><Mail className="w-3.5 h-3.5 text-zinc-400" /> {candidate.email}</span>
                <span className="flex items-center gap-1"><Phone className="w-3.5 h-3.5 text-zinc-400" /> {candidate.phone}</span>
                <span className="flex items-center gap-1"><MapPin className="w-3.5 h-3.5 text-zinc-400" /> {candidate.location}</span>
              </div>
            </div>
          </div>

          {/* AI Match Badge & Score */}
          <div className="p-4 rounded-2xl glass-panel text-center space-y-1 shrink-0">
            <span className="text-[10px] font-mono font-medium dark:text-zinc-400 light:text-zinc-500 uppercase tracking-widest block">
              AI Job Match Index
            </span>
            <div className="text-3xl font-medium text-emerald-600 dark:text-emerald-400 font-mono">{candidate.matchScore}%</div>
            <span className="text-[10px] dark:text-zinc-300 light:text-zinc-700 font-medium inline-flex items-center gap-1">
              <Sparkles className="w-3 h-3 text-zinc-400" /> Top Tier Match
            </span>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex items-center gap-2 mt-6 pt-4 border-t border-zinc-200 dark:border-zinc-800 text-xs font-medium overflow-x-auto">
          {[
            { id: 'overview', label: 'Overview & Summary', icon: FileText },
            { id: 'experience', label: 'Experience & Education', icon: Briefcase },
            { id: 'skills', label: 'Skills & Competencies', icon: Award },
            { id: 'documents', label: 'Documents', icon: FileText },
            { id: 'timeline', label: 'Activity Timeline', icon: Clock },
          ].map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`px-4 py-2 rounded-xl transition flex items-center gap-2 whitespace-nowrap ${isActive
                    ? 'bg-zinc-900 text-white shadow-sm'
                    : 'glass-panel text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white'
                  }`}
              >
                <Icon className="w-3.5 h-3.5" />
                {tab.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* Tab Content */}
      <div className="p-6 rounded-2xl glass-card space-y-6">
        {activeTab === 'overview' && (
          <div className="space-y-6">
            <div>
              <h4 className="text-xs font-medium uppercase tracking-wider dark:text-zinc-400 light:text-zinc-500 mb-2 font-mono">Executive Summary</h4>
              <p className="text-sm dark:text-zinc-200 light:text-zinc-800 leading-relaxed glass-panel p-4 rounded-2xl font-normal">
                {candidate.summary}
              </p>
            </div>

            <div>
              <h4 className="text-xs font-medium uppercase tracking-wider dark:text-zinc-400 light:text-zinc-500 mb-3 font-mono">Core Technical Skills</h4>
              <div className="flex flex-wrap gap-2">
                {candidate.skills.map((skill, i) => (
                  <span
                    key={i}
                    className="px-3 py-1.5 rounded-xl glass-panel dark:text-zinc-200 light:text-zinc-800 text-xs font-mono font-medium"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'experience' && (
          <div className="space-y-6">
            <div>
              <h4 className="text-xs font-medium uppercase tracking-wider dark:text-zinc-400 light:text-zinc-500 mb-4 flex items-center gap-2 font-mono">
                <Briefcase className="w-4 h-4 text-zinc-400" /> Work Experience
              </h4>
              <div className="space-y-4">
                {candidate.experiences.map((exp) => (
                  <div key={exp.id} className="p-4 rounded-2xl glass-panel space-y-1">
                    <div className="flex items-center justify-between">
                      <h5 className="text-sm font-medium dark:text-white light:text-zinc-900">{exp.role}</h5>
                      <span className="text-xs font-mono dark:text-zinc-400 light:text-zinc-500">{exp.startDate} - {exp.endDate}</span>
                    </div>
                    <p className="text-xs dark:text-zinc-300 light:text-zinc-700 font-medium">{exp.company}</p>
                    <p className="text-xs dark:text-zinc-300 light:text-zinc-700 leading-relaxed pt-2 font-normal">{exp.description}</p>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h4 className="text-xs font-medium uppercase tracking-wider dark:text-zinc-400 light:text-zinc-500 mb-4 flex items-center gap-2 font-mono">
                <GraduationCap className="w-4 h-4 text-emerald-600 dark:text-emerald-400" /> Education
              </h4>
              <div className="space-y-3">
                {candidate.education.map((edu) => (
                  <div key={edu.id} className="p-4 rounded-2xl glass-panel flex items-center justify-between">
                    <div>
                      <h5 className="text-sm font-medium dark:text-white light:text-zinc-900">{edu.degree} in {edu.fieldOfStudy}</h5>
                      <p className="text-xs dark:text-zinc-400 light:text-zinc-600">{edu.institution}</p>
                    </div>
                    <span className="text-xs font-mono dark:text-zinc-400 light:text-zinc-500">Class of {edu.graduationYear}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'skills' && (
          <div className="space-y-4">
            <h4 className="text-xs font-medium uppercase tracking-wider dark:text-zinc-400 light:text-zinc-500 font-mono">Skill Alignment Rubric</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {candidate.skills.map((skill, i) => (
                <div key={i} className="p-3.5 rounded-2xl glass-panel flex items-center justify-between">
                  <span className="text-xs font-medium dark:text-white light:text-zinc-900">{skill}</span>
                  <span className="text-xs font-mono text-emerald-600 dark:text-emerald-400 font-medium flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Verified
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'documents' && (
          <div className="space-y-4">
            <h4 className="text-xs font-medium uppercase tracking-wider dark:text-zinc-400 light:text-zinc-500 font-mono">Candidate Documents</h4>
            <div className="space-y-3">
              {candidate.documents.map((doc) => (
                <div key={doc.id} className="p-4 rounded-2xl glass-panel flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <FileText className="w-5 h-5 text-zinc-400" />
                    <div>
                      <p className="text-xs font-medium dark:text-white light:text-zinc-900">{doc.name}</p>
                      <p className="text-[11px] dark:text-zinc-400 light:text-zinc-500">{doc.type} • {doc.size} • Uploaded {doc.uploadDate}</p>
                    </div>
                  </div>
                  <button className="px-3 py-1.5 rounded-xl glass-card dark:text-zinc-200 light:text-zinc-800 text-xs font-medium hover:bg-zinc-100 dark:hover:bg-zinc-800">
                    Download
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'timeline' && (
          <div className="space-y-4">
            <h4 className="text-xs font-medium uppercase tracking-wider dark:text-zinc-400 light:text-zinc-500 font-mono">Candidate History &amp; Audit Trail</h4>
            <div className="space-y-3 font-mono text-xs">
              {candidate.timeline.map((ev) => (
                <div key={ev.id} className="p-3.5 rounded-2xl glass-panel flex items-start justify-between gap-4">
                  <div className="space-y-1">
                    <p className="font-medium dark:text-white light:text-zinc-900">{ev.title}</p>
                    <p className="dark:text-zinc-400 light:text-zinc-600 text-[11px] font-sans font-normal">{ev.description}</p>
                    <span className="text-[10px] dark:text-zinc-400 light:text-zinc-500">By {ev.actor}</span>
                  </div>
                  <span className="text-[10px] dark:text-zinc-500 light:text-zinc-400 shrink-0">{ev.timestamp}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
