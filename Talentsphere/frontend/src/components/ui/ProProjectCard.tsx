import React from 'react';
import { MoreVertical } from 'lucide-react';

export type ProCardAccent = 'emerald' | 'amber' | 'rose' | 'blue' | 'purple';

export interface ProCardMember {
  name: string;
  avatar: string;
}

export interface ProProjectCardProps {
  date: string;
  title: string;
  category: string;
  progress: number;
  accent?: ProCardAccent;
  members?: ProCardMember[];
  statusBadge: string;
  onClick?: () => void;
  className?: string;
}

export const ProProjectCard: React.FC<ProProjectCardProps> = ({
  date,
  title,
  category,
  progress,
  accent = 'emerald',
  members = [
    { name: 'Dr. Evelyn', avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80' },
    { name: 'Marcus S.', avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80' },
  ],
  statusBadge,
  onClick,
  className = '',
}) => {
  // Accent color themes for Light and Dark modes
  const accentStyles = {
    emerald: {
      cardBg: 'dark:bg-gradient-to-b dark:from-teal-950/40 dark:via-zinc-900/90 dark:to-zinc-950 dark:border-zinc-800/80 dark:hover:border-emerald-500/50 light:bg-gradient-to-b light:from-emerald-50/60 light:via-white light:to-white light:border-emerald-200/80 light:hover:border-emerald-300',
      progressFill: 'bg-emerald-500 dark:bg-emerald-400 shadow-[0_0_12px_rgba(52,211,153,0.8)]',
      plusBg: 'bg-emerald-500 dark:bg-teal-400 text-white dark:text-zinc-950',
      glowOrb: 'from-emerald-500/15 to-transparent',
      progressText: 'text-emerald-600 dark:text-emerald-400',
      badgeBg: 'bg-emerald-50 dark:bg-zinc-900/90 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-zinc-800',
    },
    amber: {
      cardBg: 'dark:bg-gradient-to-b dark:from-amber-950/40 dark:via-zinc-900/90 dark:to-zinc-950 dark:border-zinc-800/80 dark:hover:border-amber-500/50 light:bg-gradient-to-b light:from-amber-50/60 light:via-white light:to-white light:border-amber-200/80 light:hover:border-amber-300',
      progressFill: 'bg-amber-500 dark:bg-amber-400 shadow-[0_0_12px_rgba(251,191,36,0.8)]',
      plusBg: 'bg-amber-500 dark:bg-amber-400 text-white dark:text-zinc-950',
      glowOrb: 'from-amber-500/15 to-transparent',
      progressText: 'text-amber-600 dark:text-amber-400',
      badgeBg: 'bg-amber-50 dark:bg-zinc-900/90 text-amber-700 dark:text-amber-300 border-amber-200 dark:border-zinc-800',
    },
    rose: {
      cardBg: 'dark:bg-gradient-to-b dark:from-rose-950/40 dark:via-zinc-900/90 dark:to-zinc-950 dark:border-zinc-800/80 dark:hover:border-rose-500/50 light:bg-gradient-to-b light:from-rose-50/60 light:via-white light:to-white light:border-rose-200/80 light:hover:border-rose-300',
      progressFill: 'bg-rose-500 shadow-[0_0_12px_rgba(244,63,94,0.8)]',
      plusBg: 'bg-rose-500 text-white',
      glowOrb: 'from-rose-500/15 to-transparent',
      progressText: 'text-rose-600 dark:text-rose-400',
      badgeBg: 'bg-rose-50 dark:bg-zinc-900/90 text-rose-700 dark:text-rose-300 border-rose-200 dark:border-zinc-800',
    },
    blue: {
      cardBg: 'dark:bg-gradient-to-b dark:from-blue-950/40 dark:via-zinc-900/90 dark:to-zinc-950 dark:border-zinc-800/80 dark:hover:border-blue-500/50 light:bg-gradient-to-b light:from-blue-50/60 light:via-white light:to-white light:border-blue-200/80 light:hover:border-blue-300',
      progressFill: 'bg-blue-500 dark:bg-blue-400 shadow-[0_0_12px_rgba(96,165,250,0.8)]',
      plusBg: 'bg-blue-500 dark:bg-blue-400 text-white dark:text-zinc-950',
      glowOrb: 'from-blue-500/15 to-transparent',
      progressText: 'text-blue-600 dark:text-blue-400',
      badgeBg: 'bg-blue-50 dark:bg-zinc-900/90 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-zinc-800',
    },
    purple: {
      cardBg: 'dark:bg-gradient-to-b dark:from-purple-950/40 dark:via-zinc-900/90 dark:to-zinc-950 dark:border-zinc-800/80 dark:hover:border-purple-500/50 light:bg-gradient-to-b light:from-purple-50/60 light:via-white light:to-white light:border-purple-200/80 light:hover:border-purple-300',
      progressFill: 'bg-purple-500 dark:bg-purple-400 shadow-[0_0_12px_rgba(192,132,252,0.8)]',
      plusBg: 'bg-purple-500 dark:bg-purple-400 text-white dark:text-zinc-950',
      glowOrb: 'from-purple-500/15 to-transparent',
      progressText: 'text-purple-600 dark:text-purple-400',
      badgeBg: 'bg-purple-50 dark:bg-zinc-900/90 text-purple-700 dark:text-purple-300 border-purple-200 dark:border-zinc-800',
    },
  }[accent];

  return (
    <div
      onClick={onClick}
      className={`relative group rounded-[28px] p-6 text-left transition-all duration-300 cursor-pointer shadow-xl hover:shadow-2xl hover:-translate-y-1 border backdrop-blur-md overflow-hidden flex flex-col justify-between space-y-6 ${accentStyles.cardBg} ${className}`}
    >
      {/* Top Ambient Glow Orb */}
      <div
        className={`absolute -top-12 -left-12 w-44 h-44 rounded-full bg-gradient-to-br ${accentStyles.glowOrb} blur-2xl pointer-events-none group-hover:scale-125 transition-transform duration-500`}
      />

      {/* Header Row */}
      <div className="flex items-center justify-between z-10">
        <span className="text-xs font-semibold text-zinc-500 dark:text-zinc-400 tracking-wide font-sans">
          {date}
        </span>
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
          }}
          className="p-1.5 rounded-xl hover:bg-zinc-200/80 dark:hover:bg-zinc-800/80 text-zinc-400 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white transition"
        >
          <MoreVertical className="w-4 h-4" />
        </button>
      </div>

      {/* Title & Category Body */}
      <div className="text-center py-2 space-y-1.5 z-10">
        <h3 className="text-xl sm:text-2xl font-bold dark:text-white light:text-zinc-900 tracking-tight transition">
          {title}
        </h3>
        <p className="text-sm font-medium dark:text-zinc-400 light:text-zinc-600 font-sans">
          {category}
        </p>
      </div>

      {/* Progress Bar Section */}
      <div className="space-y-2 z-10">
        <div className="flex items-center justify-between text-xs">
          <span className="font-bold uppercase text-[11px] tracking-wider dark:text-zinc-300 light:text-zinc-700">
            Progress
          </span>
          <span className={`font-bold font-mono text-xs ${accentStyles.progressText}`}>{progress}%</span>
        </div>
        <div className="w-full h-2.5 rounded-full dark:bg-zinc-800/90 light:bg-zinc-200 overflow-hidden p-0.5 border dark:border-zinc-700/30 light:border-zinc-300/60">
          <div
            className={`h-full rounded-full transition-all duration-700 ease-out ${accentStyles.progressFill}`}
            style={{ width: `${Math.min(100, Math.max(0, progress))}%` }}
          />
        </div>
      </div>

      {/* Footer Row */}
      <div className="flex items-center justify-between pt-2 z-10">
        {/* Avatars Stack */}
        <div className="flex items-center -space-x-2">
          {members.slice(0, 3).map((m, idx) => (
            <img
              key={idx}
              src={m.avatar}
              alt={m.name}
              className="w-8 h-8 rounded-full border-2 dark:border-zinc-900 light:border-white object-cover shadow-sm"
            />
          ))}
          <div
            className={`w-8 h-8 rounded-full font-bold text-xs flex items-center justify-center border-2 dark:border-zinc-900 light:border-white shadow-md ${accentStyles.plusBg}`}
          >
            +
          </div>
        </div>

        {/* Status Pill Badge */}
        <div className={`px-4 py-2 rounded-full border text-xs font-semibold shadow-sm tracking-tight ${accentStyles.badgeBg}`}>
          {statusBadge}
        </div>
      </div>
    </div>
  );
};
