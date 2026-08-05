import * as React from "react"
import { createBrowserRouter, Navigate } from "react-router-dom"
import { AppLayout } from "@/components/layout/app-layout"
import { AuthLayout } from "@/pages/auth/auth-layout"
import { LoginPage } from "@/pages/auth/login"
import { ForgotPasswordPage } from "@/pages/auth/forgot-password"
import { ResetPasswordPage } from "@/pages/auth/reset-password"
import { DashboardPage } from "@/pages/dashboard"
import { LoadingSpinner } from "@/components/ui/loading-spinner"

// Helper for Suspense wrapper
const Loadable = (Component: React.LazyExoticComponent<any>) => (props: any) => (
  <React.Suspense fallback={<div className="flex h-[50vh] items-center justify-center"><LoadingSpinner /></div>}>
    <Component {...props} />
  </React.Suspense>
)

// Lazy load feature modules
const AgentsListPage = React.lazy(() => import("@/pages/agents").then(m => ({ default: m.AgentsListPage })))
const AgentDetailPage = React.lazy(() => import("@/pages/agents/detail").then(m => ({ default: m.AgentDetailPage })))
const NewAgentPage = React.lazy(() => import("@/pages/agents/new").then(m => ({ default: m.NewAgentPage })))

const CampaignsListPage = React.lazy(() => import("@/pages/campaigns").then(m => ({ default: m.CampaignsListPage })))
const CampaignDetailPage = React.lazy(() => import("@/pages/campaigns/detail").then(m => ({ default: m.CampaignDetailPage })))
const NewCampaignPage = React.lazy(() => import("@/pages/campaigns/new").then(m => ({ default: m.NewCampaignPage })))

const LeadsListPage = React.lazy(() => import("@/pages/leads").then(m => ({ default: m.LeadsListPage })))
const ImportLeadsPage = React.lazy(() => import("@/pages/leads/import").then(m => ({ default: m.ImportLeadsPage })))

// Phase 2 Modules
// Phase 2 Modules
const LiveMonitorPage = React.lazy(() => import("@/pages/live").then(m => ({ default: m.LiveMonitorPage })))
const CallHistoryPage = React.lazy(() => import("@/pages/calls").then(m => ({ default: m.CallHistoryPage })))
const PlaygroundPage = React.lazy(() => import("@/pages/playground").then(m => ({ default: m.PlaygroundPage })))
const AnalyticsPage = React.lazy(() => import("@/pages/analytics").then(m => ({ default: m.AnalyticsPage })))
const KnowledgeBasePage = React.lazy(() => import("@/pages/knowledge-base").then(m => ({ default: m.KnowledgeBasePage })))
const SettingsPage = React.lazy(() => import("@/pages/settings").then(m => ({ default: m.SettingsPage })))

// Core Infrastructure
const PhoneNumbersPage = React.lazy(() => import("@/pages/phone-numbers").then(m => ({ default: m.PhoneNumbersPage })))

export const router = createBrowserRouter([
  // Auth routes
  {
    element: <AuthLayout />,
    children: [
      { path: "/login", element: <LoginPage /> },
      { path: "/forgot-password", element: <ForgotPasswordPage /> },
      { path: "/reset-password", element: <ResetPasswordPage /> },
    ],
  },

  // App routes (protected)
  {
    element: <AppLayout />,
    children: [
      { path: "/", element: <DashboardPage /> },
      
      // Agents
      { path: "/agents", element: Loadable(AgentsListPage)({}) },
      { path: "/agents/new", element: Loadable(NewAgentPage)({}) },
      { path: "/agents/:id", element: Loadable(AgentDetailPage)({}) },
      
      // Phone Numbers
      { path: "/phone-numbers", element: Loadable(PhoneNumbersPage)({}) },

      // Campaigns
      { path: "/campaigns", element: Loadable(CampaignsListPage)({}) },
      { path: "/campaigns/new", element: Loadable(NewCampaignPage)({}) },
      { path: "/campaigns/:id", element: Loadable(CampaignDetailPage)({}) },
      
      // Leads
      { path: "/leads", element: Loadable(LeadsListPage)({}) },
      { path: "/leads/import", element: Loadable(ImportLeadsPage)({}) },
      
      // Phase 2 Modules
      { path: "/live", element: Loadable(LiveMonitorPage)({}) },
      { path: "/calls", element: Loadable(CallHistoryPage)({}) },
      { path: "/playground", element: Loadable(PlaygroundPage)({}) },
      { path: "/analytics", element: Loadable(AnalyticsPage)({}) },
      { path: "/knowledge-base", element: Loadable(KnowledgeBasePage)({}) },
      { path: "/settings", element: Loadable(SettingsPage)({}) },
    ],
  },

  // Catch-all
  { path: "*", element: <Navigate to="/" replace /> },
])
