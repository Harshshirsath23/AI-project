import React from 'react';
import { ShieldCheck, Lock } from 'lucide-react';

interface FooterSecurityBarProps {
  onOpenCompliance: () => void;
  reducedMotion: boolean;
  onToggleReducedMotion: () => void;
}

export const FooterSecurityBar: React.FC<FooterSecurityBarProps> = ({
  onOpenCompliance,
}) => {
  return (
    <footer className="w-full py-3.5 px-4 border-t border-zinc-200 dark:border-zinc-800 dark:bg-black/80 light:bg-white/80 backdrop-blur-md relative z-10 select-none text-zinc-600 dark:text-zinc-400 text-xs">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-3">
        {/* Left: System Status */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-2.5 py-1 rounded-full glass-panel">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="font-medium dark:text-zinc-200 light:text-zinc-800 text-[11px]">All Systems Operational</span>
          </div>
          <span className="hidden sm:inline text-zinc-300 dark:text-zinc-700">•</span>
          <span className="hidden sm:inline font-mono dark:text-zinc-400 light:text-zinc-500 text-[11px]">SLA 99.99%</span>
        </div>

        {/* Center: Compliance & Security Links */}
        <div className="flex flex-wrap items-center justify-center gap-4 dark:text-zinc-400 light:text-zinc-600 font-normal text-[11px]">
          <button
            onClick={onOpenCompliance}
            className="hover:text-zinc-900 dark:hover:text-white transition flex items-center gap-1.5"
          >
            <ShieldCheck className="w-3.5 h-3.5" /> Security Portal
          </button>
          <span className="text-zinc-300 dark:text-zinc-700">•</span>
          <a href="#privacy" onClick={(e) => { e.preventDefault(); onOpenCompliance(); }} className="hover:text-zinc-900 dark:hover:text-white transition">
            Privacy Policy
          </a>
          <span className="text-zinc-300 dark:text-zinc-700">•</span>
          <a href="#terms" onClick={(e) => { e.preventDefault(); onOpenCompliance(); }} className="hover:text-zinc-900 dark:hover:text-white transition">
            Terms of Service
          </a>
          <span className="text-zinc-300 dark:text-zinc-700">•</span>
          <a href="#trust" onClick={(e) => { e.preventDefault(); onOpenCompliance(); }} className="hover:text-zinc-900 dark:hover:text-white transition">
            SOC 2 Report
          </a>
        </div>

        {/* Right: Copyright & Security Note */}
        <div className="flex items-center gap-3 text-[11px]">
          <span className="dark:text-zinc-400 light:text-zinc-500 font-mono flex items-center gap-1">
            <Lock className="w-3 h-3 text-emerald-600 dark:text-emerald-400" /> AES-256 Validated
          </span>
          <span className="text-zinc-300 dark:text-zinc-700">•</span>
          <span className="dark:text-zinc-400 light:text-zinc-500 font-mono">© 2026 TalentSphere OS</span>
        </div>
      </div>
    </footer>
  );
};
