import React, { useState } from 'react';
import { useOrganization } from '../../context/OrganizationContext';
import { Interview } from '../../types';
import { ScorecardModal } from './ScorecardModal';
import { Video, ClipboardCheck, ExternalLink } from 'lucide-react';

export const InterviewDashboardView: React.FC = () => {
  const { interviews } = useOrganization();
  const [selectedInterviewForScorecard, setSelectedInterviewForScorecard] = useState<Interview | null>(null);

  return (
    <div className="space-y-6 text-left animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight flex items-center gap-2">
            <Video className="w-5 h-5 dark:text-zinc-300 light:text-zinc-700" /> Interview Management &amp; Scorecards
          </h2>
          <p className="text-xs dark:text-zinc-400 light:text-zinc-600 font-normal mt-0.5">
            Scheduled rounds, candidate evaluation rubrics &amp; AI transcript summaries
          </p>
        </div>
      </div>

      {/* Interviews Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {interviews.map((int) => (
          <div
            key={int.id}
            className="p-5 rounded-2xl glass-card space-y-4"
          >
            <div className="flex items-start justify-between gap-2">
              <div className="space-y-1">
                <span className="text-[10px] font-mono font-medium dark:text-zinc-400 light:text-zinc-500 uppercase tracking-wider block">
                  {int.roundName}
                </span>
                <h3 className="text-base font-medium dark:text-white light:text-zinc-900">{int.candidateName}</h3>
                <p className="text-xs dark:text-zinc-400 light:text-zinc-600 font-medium">Position: {int.jobTitle}</p>
              </div>

              <span
                className={`px-2.5 py-0.5 rounded-full text-[10px] font-mono font-medium uppercase ${int.status === 'Completed'
                    ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30'
                    : 'glass-panel text-zinc-700 dark:text-zinc-300'
                  }`}
              >
                {int.status}
              </span>
            </div>

            <div className="p-3 rounded-xl glass-panel text-xs space-y-1 font-mono dark:text-zinc-300 light:text-zinc-700">
              <div className="flex justify-between">
                <span className="dark:text-zinc-500 light:text-zinc-400">Scheduled:</span>
                <span className="dark:text-white light:text-zinc-900 font-medium">{int.scheduledTime}</span>
              </div>
              <div className="flex justify-between">
                <span className="dark:text-zinc-500 light:text-zinc-400">Interviewer:</span>
                <span className="dark:text-zinc-200 light:text-zinc-800">{int.interviewerName}</span>
              </div>
              <div className="flex justify-between">
                <span className="dark:text-zinc-500 light:text-zinc-400">Location/Link:</span>
                <a href={int.meetingUrl} target="_blank" rel="noreferrer" className="dark:text-zinc-300 light:text-zinc-700 underline flex items-center gap-1">
                  Join Room <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            </div>

            <div className="pt-2 flex items-center justify-between">
              {int.scorecardSubmitted ? (
                <div className="text-xs text-emerald-600 dark:text-emerald-400 font-mono font-medium flex items-center gap-1.5">
                  <ClipboardCheck className="w-4 h-4" /> Scorecard Submitted ({int.overallScore}/10)
                </div>
              ) : (
                <button
                  onClick={() => setSelectedInterviewForScorecard(int)}
                  className="px-4 py-2 rounded-xl bg-zinc-900 text-white text-xs font-medium transition flex items-center gap-2 shadow-sm hover:bg-zinc-800"
                >
                  <ClipboardCheck className="w-3.5 h-3.5" /> Submit Evaluation Scorecard
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Scorecard Modal */}
      <ScorecardModal
        isOpen={!!selectedInterviewForScorecard}
        interview={selectedInterviewForScorecard}
        onClose={() => setSelectedInterviewForScorecard(null)}
      />
    </div>
  );
};
