import {
  Candidate,
  Job,
  Application,
  HiringPlan,
  RecruitmentWorkflow,
  Interview,
  InterviewTemplate,
  Branch,
  Department,
  Designation,
  Organization,
  Role,
  SecurityAuditItem,
  HITLTask,
  AIAgentStatus,
  Offer,
  BackgroundVerification,
  OnboardingPlan,
  CommMessage,
  CommTemplate,
  NotificationItem,
  WebhookLog,
  AIAgentDetail,
  AIToolItem,
  KnowledgeDoc,
  AIExecutionItem,
  SourcingCandidateResult,
  ObservabilityTrace
} from '../types';

export const MOCK_ORGANIZATION: Organization = {
  id: 'org-ts-01',
  name: 'TalentSphere Systems Inc.',
  domain: 'talentsphere.ai',
  logo: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=120&auto=format&fit=crop&q=80',
  plan: 'Enterprise Tier 1',
  headquarters: 'San Francisco, CA & London, UK',
  totalEmployees: 0,
  ssoEnabled: true,
  ssoProvider: 'Okta SAML 2.0 / Entra ID',
  mfaEnforced: true,
};

export const MOCK_ROLES: Role[] = [
  {
    id: 'role-admin',
    name: 'Enterprise Admin',
    description: 'Full access to organization settings, IAM, security audit logs, and billing.',
    permissions: [
      'candidate:read', 'candidate:write', 'candidate:delete',
      'job:read', 'job:write', 'job:delete',
      'application:read', 'application:write',
      'workflow:read', 'workflow:write',
      'interview:read', 'interview:write',
      'org:read', 'org:write',
      'iam:admin', 'audit:read'
    ],
    isSystem: true,
    memberCount: 4,
  },
  {
    id: 'role-recruiter',
    name: 'Lead Recruiter',
    description: 'Manage candidates, post jobs, run recruitment workflows, and schedule interviews.',
    permissions: [
      'candidate:read', 'candidate:write',
      'job:read', 'job:write',
      'application:read', 'application:write',
      'workflow:read', 'workflow:write',
      'interview:read', 'interview:write',
      'org:read'
    ],
    isSystem: true,
    memberCount: 18,
  },
  {
    id: 'role-hiring-manager',
    name: 'Hiring Manager',
    description: 'Review candidate applications, score interview rounds, and approve offers.',
    permissions: [
      'candidate:read',
      'job:read',
      'application:read', 'application:write',
      'interview:read', 'interview:write'
    ],
    isSystem: true,
    memberCount: 42,
  },
  {
    id: 'role-interviewer',
    name: 'Technical Interviewer',
    description: 'Conduct assigned candidate interviews and submit scorecards.',
    permissions: [
      'candidate:read',
      'interview:read', 'interview:write'
    ],
    isSystem: true,
    memberCount: 85,
  }
];
export const MOCK_CANDIDATES: Candidate[] = [];
export const MOCK_JOBS: Job[] = [];
export const MOCK_APPLICATIONS: Application[] = [];
export const MOCK_HIRING_PLANS: HiringPlan[] = [];
export const MOCK_WORKFLOWS: RecruitmentWorkflow[] = [];
export const MOCK_INTERVIEWS: Interview[] = [];
export const MOCK_BRANCHES: Branch[] = [];
export const MOCK_DEPARTMENTS: Department[] = [];
export const MOCK_DESIGNATIONS: Designation[] = [];
export const MOCK_AUDIT_LOGS: SecurityAuditItem[] = [];
export const MOCK_HITL_TASKS: HITLTask[] = [];
export const MOCK_AI_AGENTS_DETAILED: AIAgentDetail[] = [];
export const MOCK_AI_TOOLS: AIToolItem[] = [];
export const MOCK_KNOWLEDGE_DOCS: KnowledgeDoc[] = [];
export const MOCK_AI_EXECUTIONS: AIExecutionItem[] = [];
export const MOCK_SOURCING_RESULTS: SourcingCandidateResult[] = [];
export const MOCK_OBSERVABILITY_TRACES: ObservabilityTrace[] = [];
export const MOCK_OFFERS: Offer[] = [];
export const MOCK_BGV: BackgroundVerification[] = [];
export const MOCK_ONBOARDING: OnboardingPlan[] = [];
export const MOCK_COMM_MESSAGES: CommMessage[] = [];
export const MOCK_COMM_TEMPLATES: CommTemplate[] = [];
export const MOCK_NOTIFICATIONS: NotificationItem[] = [];
export const MOCK_WEBHOOK_LOGS: WebhookLog[] = [];
export const MOCK_INTERVIEW_TEMPLATES: InterviewTemplate[] = [];
export const MOCK_AGENT_STATUSES: AIAgentStatus[] = [];
export const MOCK_AI_AGENTS_STATUS: AIAgentStatus[] = [];
export const USER_PRESETS = [
  {
    id: 'usr-admin',
    name: 'Harsh Shirsath',
    email: 'harsh.shirsath.amp@gmail.com',
    role: 'Enterprise Admin',
    avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80',
    company: 'TalentSphere Systems Inc.',
    region: 'us-east-1 (N. Virginia)',
    badge: 'SECURE_SHELL_ACTIVE'
  }
];
export const REGION_OPTIONS = [
  { id: 'us-east-1', name: 'US East (N. Virginia)', location: 'AWS us-east-1', flag: '🇺🇸', latency: '12ms', status: 'Operational' }
];
