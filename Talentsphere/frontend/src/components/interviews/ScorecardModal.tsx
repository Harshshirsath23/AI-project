import React, { useState } from 'react';
import { Interview } from '../../types';
import { useOrganization } from '../../context/OrganizationContext';
import { useNotification } from '../../context/NotificationContext';
import { ClipboardCheck, CheckCircle2, X } from 'lucide-react';

interface ScorecardModalProps {
  isOpen: boolean;
  interview: Interview | null;
  onClose: () => void;
}

export const ScorecardModal: React.FC<ScorecardModalProps> = ({
  isOpen,
  interview,
  onClose,
}) => {
  const { submitScorecard } = useOrganization();
  const { showSuccess } = useNotification();

  // Criteria evaluation state
  const [techScore, setTechScore] = useState(9);
  const [systemDesignScore, setSystemDesignScore] = useState(8);
  const [commScore, setCommScore] = useState(8);
  const [notes, setNotes] = useState('Candidate demonstrated exceptional architectural clarity when scaling LLM agent tool calling under heavy concurrency.');
  const [recommendation, setRecommendation] = useState<'Strong Hire' | 'Hire' | 'Hold' | 'Reject'>('Strong Hire');

  if (!isOpen || !interview) return null;

  const overallScore = Number(((techScore * 0.4 + systemDesignScore * 0.4 + commScore * 0.2)).toFixed(1));

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    submitScorecard(interview.id, {
      interviewId: interview.id,
      candidateId: interview.candidateId,
      interviewerName: interview.interviewerName,
      overallScore,
      recommendation,
      evaluations: [
        { id: 'eval-1', category: 'Technical Skills & Algorithms', score: techScore, weight: 0.4, comments: 'Solid CS fundamentals' },
        { id: 'eval-2', category: 'System Design & Scalability', score: systemDesignScore, weight: 0.4, comments: 'Understands high-throughput architectures' },
        { id: 'eval-3', category: 'Communication & Alignment', score: commScore, weight: 0.2, comments: 'Clear communicator' },
      ],
      summaryNotes: notes,
      status: 'Final',
    });

    showSuccess('Scorecard Submitted!', `Evaluation for ${interview.candidateName} recorded.`);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-md animate-in fade-in duration-150">
      <div className="w-full max-w-2xl rounded-2xl glass-card p-6 text-left relative space-y-5 max-h-[90vh] overflow-y-auto custom-scrollbar">
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-xl glass-panel dark:text-zinc-400 light:text-zinc-600 hover:text-zinc-900 dark:hover:text-white transition"
        >
          <X className="w-4 h-4" />
        </button>

        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full glass-panel dark:text-zinc-300 light:text-zinc-700 text-xs font-mono font-medium mb-1">
            <ClipboardCheck className="w-3.5 h-3.5" /> Structured Evaluation Scorecard
          </div>
          <h3 className="text-xl font-medium dark:text-white light:text-zinc-900">Interview Evaluation: {interview.candidateName}</h3>
          <p className="text-xs dark:text-zinc-400 light:text-zinc-600">
            {interview.roundName} • Position: <span className="dark:text-white light:text-zinc-900 font-medium">{interview.jobTitle}</span>
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          {/* Rating Sliders */}
          <div className="p-4 rounded-xl glass-panel space-y-4">
            <div>
              <div className="flex justify-between font-medium mb-1 dark:text-zinc-300 light:text-zinc-700">
                <span>Technical Skills &amp; AI Algorithms</span>
                <span className="font-mono">{techScore} / 10</span>
              </div>
              <input
                type="range"
                min="1"
                max="10"
                value={techScore}
                onChange={(e) => setTechScore(Number(e.target.value))}
                className="w-full accent-zinc-700 cursor-pointer"
              />
            </div>

            <div>
              <div className="flex justify-between font-medium mb-1 dark:text-zinc-300 light:text-zinc-700">
                <span>System Design &amp; Architecture</span>
                <span className="font-mono">{systemDesignScore} / 10</span>
              </div>
              <input
                type="range"
                min="1"
                max="10"
                value={systemDesignScore}
                onChange={(e) => setSystemDesignScore(Number(e.target.value))}
                className="w-full accent-zinc-700 cursor-pointer"
              />
            </div>

            <div>
              <div className="flex justify-between font-medium mb-1 dark:text-zinc-300 light:text-zinc-700">
                <span>Communication &amp; Leadership</span>
                <span className="font-mono">{commScore} / 10</span>
              </div>
              <input
                type="range"
                min="1"
                max="10"
                value={commScore}
                onChange={(e) => setCommScore(Number(e.target.value))}
                className="w-full accent-zinc-700 cursor-pointer"
              />
            </div>
          </div>

          {/* Overall Computed Score & Recommendation */}
          <div className="p-4 rounded-xl glass-panel flex items-center justify-between gap-4">
            <div>
              <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-600 uppercase block">Calculated Rating</span>
              <span className="text-2xl font-medium text-emerald-600 dark:text-emerald-400 font-mono">{overallScore} / 10</span>
            </div>

            <div>
              <label className="dark:text-zinc-300 light:text-zinc-700 font-medium block mb-1">Recommendation</label>
              <select
                value={recommendation}
                onChange={(e) => setRecommendation(e.target.value as any)}
                className="px-3 py-1.5 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 dark:text-white light:text-zinc-900 font-medium"
              >
                <option value="Strong Hire">Strong Hire</option>
                <option value="Hire">Hire</option>
                <option value="Hold">Hold</option>
                <option value="Reject">Reject</option>
              </select>
            </div>
          </div>

          {/* Detailed Comments */}
          <div>
            <label className="dark:text-zinc-300 light:text-zinc-700 font-medium block mb-1">Interviewer Feedback &amp; Evidence Notes</label>
            <textarea
              rows={3}
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              className="w-full px-3 py-2 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 dark:text-white light:text-zinc-900"
            />
          </div>

          {/* Submit */}
          <div className="flex items-center justify-end gap-3 pt-3 border-t border-zinc-200 dark:border-zinc-800">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl glass-panel text-zinc-700 dark:text-zinc-300 font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-5 py-2 rounded-xl bg-zinc-900 text-white font-medium flex items-center gap-2 shadow-sm hover:bg-zinc-800"
            >
              <CheckCircle2 className="w-4 h-4" /> Finalize Scorecard
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
