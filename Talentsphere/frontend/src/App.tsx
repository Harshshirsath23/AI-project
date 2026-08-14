import React, { useState } from 'react';
import { useAuth } from './context/AuthContext';
import { BackgroundCanvas } from './components/BackgroundCanvas';
import { RedesignedLoginPortal } from './components/RedesignedLoginPortal';
import { MfaModal } from './components/MfaModal';
import { ForgotPasswordModal } from './components/ForgotPasswordModal';
import { EnterpriseComplianceModal } from './components/EnterpriseComplianceModal';
import { ApplicationShell } from './components/layout/ApplicationShell';

// Views
import { DashboardOverview } from './components/dashboard/DashboardOverview';
import { AICommandCenterHub } from './components/ai/AICommandCenterHub';
import { CandidateCommandCenter } from './components/candidates/CandidateCommandCenter';
import { JobManagementView } from './components/recruitment/JobManagementView';
import { HiringPlansView } from './components/recruitment/HiringPlansView';
import { RecruitmentPipelineView } from './components/recruitment/RecruitmentPipelineView';
import { InterviewCalendarView } from './components/interviews/InterviewCalendarView';
import { InterviewDashboardView } from './components/interviews/InterviewDashboardView';
import { WorkflowBuilderView } from './components/recruitment/WorkflowBuilderView';
import { OrganizationOverviewView } from './components/org/OrganizationOverviewView';
import { BranchesView } from './components/org/BranchesView';
import { DepartmentsView } from './components/org/DepartmentsView';
import { DesignationsView } from './components/org/DesignationsView';
import { UsersManagementView } from './components/iam/UsersManagementView';
import { RolesManagementView } from './components/iam/RolesManagementView';
import { AuditLogsView } from './components/iam/AuditLogsView';
import { QuickAIAssistantModal } from './components/ai/QuickAIAssistantModal';

// Milestones 8-13 Views
import { OffersDashboardView } from './components/offers/OffersDashboardView';
import { CommunicationCenterView } from './components/communication/CommunicationCenterView';
import { IntelligentSourcingView } from './components/sourcing/IntelligentSourcingView';
import { AICopilotView } from './components/ai/AICopilotView';
import { AIObservabilityView } from './components/ai/AIObservabilityView';
import { AIAgentsRegistryView } from './components/ai/AIAgentsRegistryView';
import { AIToolsRegistryView } from './components/ai/AIToolsRegistryView';
import { KnowledgeCenterView } from './components/ai/KnowledgeCenterView';
import { WorkflowVisualizerView } from './components/workflows/WorkflowVisualizerView';
import { AgentRuntimeView } from './components/workflows/AgentRuntimeView';
import { HITLCenterView } from './components/ai/HITLCenterView';
import { PlatformAdminDashboardView } from './components/platform/PlatformAdminDashboardView';
import { OrgAdminUsersRolesView } from './components/org/OrgAdminUsersRolesView';

import { LoginMode, UserPreset } from './types';
import { AsciiPalette, AsciiMode } from './components/ui/AsciiNumberCanvas';

export default function App() {
  const { isLoggedIn, currentUser, login, selectedRegion, setSelectedRegion } = useAuth();

  const isPlatformAdmin = currentUser?.is_platform_admin || currentUser?.scope === 'PLATFORM';

  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [isQuickAiModalOpen, setIsQuickAiModalOpen] = useState(false);

  // Set default tab for platform admin on mount / login
  React.useEffect(() => {
    if (isPlatformAdmin && (activeTab === 'dashboard' || !activeTab)) {
      setActiveTab('platform-dashboard');
    }
  }, [isPlatformAdmin]);

  // Modals for login screen
  const [isMfaOpen, setIsMfaOpen] = useState(false);
  const [isForgotPasswordOpen, setIsForgotPasswordOpen] = useState(false);
  const [isComplianceOpen, setIsComplianceOpen] = useState(false);
  const [pendingEmail, setPendingEmail] = useState('');
  const [pendingLoginPreset, setPendingLoginPreset] = useState<UserPreset | undefined>();
  const [pendingLoginMode, setPendingLoginMode] = useState<LoginMode>('password');

  // ASCII Background Customization state
  const [asciiPalette, setAsciiPalette] = useState<AsciiPalette>('mono');
  const [asciiMode, setAsciiMode] = useState<AsciiMode>('waves');

  // Accessibility / motion preference
  const [reducedMotion] = useState(false);

  const handleLoginSubmit = (
    email: string,
    pass: string,
    mode: LoginMode,
    preset?: UserPreset
  ) => {
    login(email, pass, mode, preset);
  };

  const handleMfaVerifySuccess = async () => {
    setIsMfaOpen(false);
    await login(pendingEmail, 'password', pendingLoginMode, pendingLoginPreset);
  };

  const renderActiveView = () => {
    switch (activeTab) {
      case 'platform-dashboard':
      case 'platform-orgs':
      case 'platform-roles':
      case 'platform-audit':
        return <PlatformAdminDashboardView activeTab={activeTab} onNavigate={(tab) => setActiveTab(tab)} />;
      case 'org-admin-panel':
        return <OrgAdminUsersRolesView />;
      case 'dashboard':
        return isPlatformAdmin ? <PlatformAdminDashboardView activeTab={activeTab} onNavigate={(tab) => setActiveTab(tab)} /> : <DashboardOverview onNavigate={(tab) => setActiveTab(tab)} />;
      case 'ai-activity':
        return <AICommandCenterHub />;
      case 'ai-copilot':
        return <AICopilotView />;
      case 'ai-observability':
        return <AIObservabilityView />;
      case 'sourcing':
        return <IntelligentSourcingView />;
      case 'candidates':
        return <CandidateCommandCenter />;
      case 'jobs':
        return <JobManagementView />;
      case 'applications':
      case 'pipelines':
        return <RecruitmentPipelineView />;
      case 'offers':
        return <OffersDashboardView />;
      case 'communications':
        return <CommunicationCenterView />;
      case 'hiring-plans':
        return <HiringPlansView />;
      case 'interview-calendar':
        return <InterviewCalendarView />;
      case 'interviews-list':
      case 'scorecards':
        return <InterviewDashboardView />;
      case 'ai-agents':
        return <AIAgentsRegistryView />;
      case 'ai-tools':
        return <AIToolsRegistryView />;
      case 'knowledge':
        return <KnowledgeCenterView />;
      case 'workflow-builder':
        return <WorkflowVisualizerView />;
      case 'agent-runtime':
        return <AgentRuntimeView />;
      case 'hitl-tasks':
        return <HITLCenterView />;
      case 'org-overview':
      case 'org-settings':
        return <OrganizationOverviewView />;
      case 'org-branches':
        return <BranchesView />;
      case 'org-departments':
        return <DepartmentsView />;
      case 'org-designations':
        return <DesignationsView />;
      case 'iam-users':
      case 'iam-profile':
        return <UsersManagementView />;
      case 'iam-roles':
        return <RolesManagementView />;
      case 'iam-audit':
        return <AuditLogsView />;
      default:
        return isPlatformAdmin ? <PlatformAdminDashboardView activeTab={activeTab} onNavigate={(tab) => setActiveTab(tab)} /> : <DashboardOverview onNavigate={(tab) => setActiveTab(tab)} />;
    }
  };

  return (
    <>
      {!isLoggedIn ? (
        <div className="min-h-screen bg-black text-slate-100 flex flex-col justify-between font-sans selection:bg-red-500/20 selection:text-red-700 relative overflow-x-hidden">
          <BackgroundCanvas reducedMotion={reducedMotion} palette={asciiPalette} mode={asciiMode} />

          <main className="relative z-10 flex-1 flex flex-col items-center justify-center px-4 py-8 md:py-12 w-full max-w-7xl mx-auto my-auto">
            <RedesignedLoginPortal
              onLoginSubmit={handleLoginSubmit}
              onOpenForgotPassword={(email) => {
                setPendingEmail(email);
                setIsForgotPasswordOpen(true);
              }}
              onOpenComplianceModal={() => setIsComplianceOpen(true)}
              selectedRegion={selectedRegion}
              onSelectRegion={setSelectedRegion}
              asciiPalette={asciiPalette}
              onSelectPalette={setAsciiPalette}
              asciiMode={asciiMode}
              onSelectMode={setAsciiMode}
            />
          </main>

          {/* Login Modals */}
          <MfaModal
            isOpen={isMfaOpen}
            userEmail={pendingEmail}
            onVerifySuccess={handleMfaVerifySuccess}
            onCancel={() => setIsMfaOpen(false)}
          />

          <ForgotPasswordModal
            isOpen={isForgotPasswordOpen}
            initialEmail={pendingEmail}
            onClose={() => setIsForgotPasswordOpen(false)}
          />

          <EnterpriseComplianceModal
            isOpen={isComplianceOpen}
            onClose={() => setIsComplianceOpen(false)}
          />
        </div>
      ) : (
        /* Authenticated Application Shell */
        <ApplicationShell
          activeTab={activeTab}
          onNavigate={(tab) => setActiveTab(tab)}
          onOpenQuickAIModal={() => setIsQuickAiModalOpen(true)}
        >
          {renderActiveView()}

          <QuickAIAssistantModal
            isOpen={isQuickAiModalOpen}
            onClose={() => setIsQuickAiModalOpen(false)}
          />
        </ApplicationShell>
      )}
    </>
  );
}
