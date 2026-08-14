import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useOrganization } from '../../context/OrganizationContext';
import { useTheme } from '../../context/ThemeContext';
import {
  Search,
  Bell,
  Globe,
  ChevronDown,
  ShieldCheck,
  LogOut,
  User as UserIcon,
  Sparkles,
  Command,
  Sun,
  Moon
} from 'lucide-react';

interface TopContextBarProps {
  onNavigate: (tabId: string) => void;
  onOpenQuickAIModal: () => void;
}

export const TopContextBar: React.FC<TopContextBarProps> = ({
  onNavigate,
  onOpenQuickAIModal,
}) => {
  const { currentUser, selectedRegion, logout } = useAuth();
  const { organization } = useOrganization();
  const { theme, toggleTheme } = useTheme();
  const [searchQuery, setSearchQuery] = useState('');
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);

  return (
    <header className="h-16 px-6 bg-black dark:bg-black light:bg-white border-b border-zinc-800 dark:border-zinc-800 light:border-zinc-200 flex items-center justify-between gap-4 sticky top-0 z-40 transition-colors">
      {/* Search Input */}
      <div className="flex items-center gap-3 flex-1 max-w-md">
        <div className="relative w-full">
          <Search className="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search candidates, jobs, pipelines... (Cmd+K)"
            className="w-full pl-10 pr-12 py-1.5 rounded-xl bg-zinc-950 dark:bg-zinc-950 light:bg-zinc-50 border border-zinc-800 dark:border-zinc-800 light:border-zinc-200 text-xs dark:text-white light:text-zinc-900 placeholder-zinc-500 focus:outline-none focus:border-zinc-500 transition font-sans"
          />
          <span className="absolute right-3 top-1/2 -translate-y-1/2 px-1.5 py-0.5 rounded bg-zinc-900 dark:bg-zinc-900 light:bg-zinc-200 text-[10px] font-mono text-zinc-400 light:text-zinc-600 flex items-center gap-0.5">
            <Command className="w-2.5 h-2.5" /> K
          </span>
        </div>
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-3">
        {/* Quick AI Command Center Trigger */}
        <button
          onClick={onOpenQuickAIModal}
          className="btn-primary px-3.5 py-1.5 rounded-xl text-xs font-medium transition flex items-center gap-2 active:scale-95 shadow-sm"
        >
          <Sparkles className="w-3.5 h-3.5 text-zinc-300 dark:text-zinc-300 light:text-white" />
          <span className="hidden sm:inline">Ask AI Assistant</span>
        </button>

        {/* Theme Toggle Button */}
        <button
          onClick={toggleTheme}
          className="btn-secondary p-2 rounded-xl text-xs font-medium transition relative flex items-center gap-1.5"
          title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Theme`}
        >
          {theme === 'dark' ? (
            <>
              <Sun className="w-4 h-4 text-zinc-300" />
              <span className="hidden md:inline text-[11px] text-zinc-300">Light</span>
            </>
          ) : (
            <>
              <Moon className="w-4 h-4 text-zinc-700" />
              <span className="hidden md:inline text-[11px] text-zinc-700">Dark</span>
            </>
          )}
        </button>

        {/* Region Indicator */}
        <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-xl glass-panel text-xs dark:text-zinc-300 light:text-zinc-700 font-medium">
          <Globe className="w-3.5 h-3.5 text-zinc-400" />
          <span>{selectedRegion.name}</span>
          <span className="w-2 h-2 rounded-full bg-emerald-400" />
        </div>

        {/* Notifications Bell */}
        <button
          onClick={() => onNavigate('hitl-tasks')}
          className="btn-secondary p-2 rounded-xl transition relative"
          title="HITL Approvals & Notifications"
        >
          <Bell className="w-4 h-4" />
          <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-sky-400" />
        </button>

        {/* User Profile Dropdown */}
        <div className="relative">
          <button
            onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
            className="flex items-center gap-2.5 p-1 rounded-xl hover:bg-zinc-900 dark:hover:bg-zinc-900 light:hover:bg-zinc-100 border border-transparent hover:border-zinc-800 transition"
          >
            <img
              src={currentUser?.avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80'}
              alt={currentUser?.name || 'User'}
              className="w-8 h-8 rounded-full object-cover border border-zinc-700"
            />
            <div className="hidden sm:block text-left">
              <p className="text-xs font-medium dark:text-white light:text-zinc-900 flex items-center gap-1">
                {currentUser?.name || 'Recruiter'}
                <ShieldCheck className="w-3 h-3 text-emerald-400" />
              </p>
              <p className="text-[10px] dark:text-zinc-400 light:text-zinc-500 font-medium">{organization.name}</p>
            </div>
            <ChevronDown className="w-3.5 h-3.5 text-zinc-400 hidden sm:block" />
          </button>

          {/* User Dropdown Menu */}
          {isUserMenuOpen && (
            <div className="absolute right-0 mt-2 w-56 rounded-xl glass-card shadow-2xl p-2 text-left space-y-1 z-50 animate-in fade-in duration-150">
              <div className="px-3 py-2 border-b border-zinc-200 dark:border-zinc-800">
                <p className="text-xs font-medium dark:text-white light:text-zinc-900">{currentUser?.name}</p>
                <p className="text-[11px] dark:text-zinc-400 light:text-zinc-500">{currentUser?.email}</p>
                <span className="inline-block mt-1 px-2 py-0.5 rounded glass-panel text-zinc-700 dark:text-zinc-300 text-[10px] font-mono font-medium">
                  {currentUser?.role || 'Enterprise Admin'}
                </span>
              </div>

              <button
                onClick={() => {
                  setIsUserMenuOpen(false);
                  onNavigate('iam-profile');
                }}
                className="w-full px-3 py-2 rounded-lg text-xs dark:text-zinc-300 light:text-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition flex items-center gap-2 font-medium"
              >
                <UserIcon className="w-3.5 h-3.5 text-zinc-400" />
                My Profile &amp; Security
              </button>

              <button
                onClick={() => {
                  setIsUserMenuOpen(false);
                  onNavigate('org-settings');
                }}
                className="w-full px-3 py-2 rounded-lg text-xs dark:text-zinc-300 light:text-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition flex items-center gap-2 font-medium"
              >
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                Organization Settings
              </button>

              <button
                onClick={() => {
                  setIsUserMenuOpen(false);
                  logout();
                }}
                className="w-full px-3 py-2 rounded-lg text-xs text-red-500 hover:bg-red-500/10 transition flex items-center gap-2 font-medium border-t border-zinc-200 dark:border-zinc-800 mt-1"
              >
                <LogOut className="w-3.5 h-3.5" />
                Sign Out
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
