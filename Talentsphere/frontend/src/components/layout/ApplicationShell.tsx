import React from 'react';
import { SidebarNav } from './SidebarNav';
import { TopContextBar } from './TopContextBar';

interface ApplicationShellProps {
  activeTab: string;
  onNavigate: (tabId: string) => void;
  onOpenQuickAIModal: () => void;
  children: React.ReactNode;
}

export const ApplicationShell: React.FC<ApplicationShellProps> = ({
  activeTab,
  onNavigate,
  onOpenQuickAIModal,
  children,
}) => {
  return (
    <div className="min-h-screen bg-black dark:bg-black light:bg-white text-zinc-100 dark:text-zinc-100 light:text-zinc-900 flex font-sans relative overflow-x-hidden transition-colors">
      {/* Sidebar Navigation */}
      <SidebarNav activeTab={activeTab} onNavigate={onNavigate} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 z-10 relative">
        <TopContextBar onNavigate={onNavigate} onOpenQuickAIModal={onOpenQuickAIModal} />

        <main className="flex-1 p-4 sm:p-6 lg:p-8 overflow-y-auto bg-black dark:bg-black light:bg-slate-50 transition-colors w-full">
          <div className="w-full space-y-6 animate-fade-in">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};
