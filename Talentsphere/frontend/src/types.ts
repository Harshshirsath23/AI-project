export type LoginMode = 'password' | 'sso' | 'passkey';

export interface UserPreset {
  id: string;
  name: string;
  email: string;
  role: string;
  avatar: string;
  company: string;
  region: string;
  badge: string;
  scope?: 'PLATFORM' | 'ORGANIZATION';
  is_platform_admin?: boolean;
  is_organization_admin?: boolean;
  permissions?: string[];
  roles?: string[];
}

export interface PlatformMetrics {
  total_organizations: number;
  active_organizations: number;
  suspended_organizations: number;
  total_users: number;
  recent_security_events: {
    id: string;
    event_type: string;
    severity: string;
    description: string;
    event_time: string;
  }[];
}

export interface RegionOption {
  id: string;
  name: string;
  location: string;
  flag: string;
  latency: string;
  status: 'Operational' | 'Degraded';
}

export interface SecurityAuditItem {
  id?: string;
  timestamp: string;
  event: string;
  ip: string;
  location: string;
  status: 'SUCCESS' | 'WARNING' | 'VERIFIED' | 'FAILED';
  user?: string;
}

export interface AIAgentStatus {
  id: string;
  name: string;
  category: string;
  status: 'active' | 'standby' | 'processing';
  metric: string;
  uptime: string;
  lastAction?: string;
}

// --- Enterprise TalentSphere Domain Models ---

export type Permission = 
  | 'candidate:read'
  | 'candidate:write'
  | 'candidate:delete'
  | 'job:read'
  | 'job:write'
  | 'job:delete'
  | 'application:read'
  | 'application:write'
  | 'workflow:read'
  | 'workflow:write'
  | 'interview:read'
  | 'interview:write'
  | 'org:read'
  | 'org:write'
  | 'iam:admin'
  | 'audit:read';

export interface Role {
  id: string;
  name: string;
  description: string;
  permissions: Permission[];
  isSystem?: boolean;
  memberCount?: number;
}

export interface CandidateExperience {
  id: string;
  company: string;
  role: string;
  startDate: string;
  endDate: string;
  description: string;
  isCurrent?: boolean;
}

export interface CandidateEducation {
  id: string;
  institution: string;
  degree: string;
  fieldOfStudy: string;
  graduationYear: string;
}

export interface CandidateDocument {
  id: string;
  name: string;
  type: 'Resume' | 'Cover Letter' | 'Portfolio' | 'Certificate';
  uploadDate: string;
  size: string;
  url?: string;
}

export interface CandidateTimelineEvent {
  id: string;
  title: string;
  description: string;
  timestamp: string;
  actor: string;
  type: 'stage_change' | 'note' | 'interview_scheduled' | 'scorecard_submitted' | 'resume_uploaded';
}

export interface Candidate {
  id: string;
  name: string;
  email: string;
  phone: string;
  location: string;
  currentRole: string;
  currentCompany: string;
  avatar: string;
  status: 'New' | 'Screening' | 'Interviewing' | 'Offered' | 'Hired' | 'Rejected';
  matchScore: number;
  skills: string[];
  summary: string;
  experiences: CandidateExperience[];
  education: CandidateEducation[];
  documents: CandidateDocument[];
  timeline: CandidateTimelineEvent[];
  createdAt: string;
  updatedAt: string;
}

export interface Job {
  id: string;
  title: string;
  department: string;
  branch: string;
  location: string;
  type: 'Full-Time' | 'Part-Time' | 'Contract' | 'Remote';
  status: 'Draft' | 'Active' | 'On Hold' | 'Closed';
  salaryRange: string;
  openings: number;
  filled: number;
  recruiter: string;
  hiringManager: string;
  description: string;
  requirements: string[];
  skillsRequired: string[];
  createdAt: string;
  updatedAt: string;
}

export interface Application {
  id: string;
  candidateId: string;
  candidateName: string;
  candidateAvatar: string;
  jobId: string;
  jobTitle: string;
  stageId: string;
  stageName: string;
  status: 'In Progress' | 'Shortlisted' | 'Rejected' | 'Offered' | 'Accepted';
  appliedDate: string;
  matchScore: number;
  recruiterNotes: string;
  aiRecommendation: string;
}

export interface HiringPlan {
  id: string;
  title: string;
  department: string;
  targetQuarter: string;
  positionsCount: number;
  allocatedBudget: string;
  status: 'Draft' | 'Pending Approval' | 'Approved' | 'Active' | 'Completed';
  owner: string;
  approvedBy?: string;
  createdAt: string;
}

export interface WorkflowStage {
  id: string;
  name: string;
  type: 'source' | 'screen' | 'interview' | 'assessment' | 'offer' | 'hire';
  slaHours: number;
  autoAssignRole?: string;
  requireScorecard?: boolean;
  color: string;
}

export interface RecruitmentWorkflow {
  id: string;
  name: string;
  department: string;
  description: string;
  isDefault: boolean;
  stages: WorkflowStage[];
  updatedAt: string;
}

export interface CriteriaEvaluation {
  id: string;
  category: string;
  score: number; // 1 - 10
  weight: number;
  comments: string;
}

export interface Scorecard {
  id: string;
  interviewId: string;
  candidateId: string;
  interviewerName: string;
  overallScore: number;
  recommendation: 'Strong Hire' | 'Hire' | 'Hold' | 'Reject';
  evaluations: CriteriaEvaluation[];
  summaryNotes: string;
  submittedAt: string;
  status: 'Draft' | 'Submitted' | 'Final';
}

export interface Interview {
  id: string;
  candidateId: string;
  candidateName: string;
  candidateAvatar: string;
  jobId: string;
  jobTitle: string;
  roundName: string;
  interviewerName: string;
  interviewerRole: string;
  date: string;
  time: string;
  durationMinutes: number;
  location: string;
  meetingLink: string;
  status: 'Scheduled' | 'Completed' | 'Cancelled' | 'Rescheduled';
  scorecardSubmitted?: boolean;
  overallScore?: number;
}

export interface InterviewTemplate {
  id: string;
  name: string;
  department: string;
  roundsCount: number;
  rounds: {
    roundName: string;
    durationMinutes: number;
    focusAreas: string[];
  }[];
}

export interface Branch {
  id: string;
  name: string;
  location: string;
  country: string;
  headcount: number;
  status: 'Active' | 'Inactive';
}

export interface Department {
  id: string;
  name: string;
  headName: string;
  branchName: string;
  openPositions: number;
  totalMembers: number;
}

export interface Designation {
  id: string;
  title: string;
  department: string;
  level: string;
  payGrade: string;
}

export interface Organization {
  id: string;
  name: string;
  domain: string;
  logo: string;
  plan: 'Enterprise Tier 1' | 'Scale' | 'Government';
  headquarters: string;
  totalEmployees: number;
  ssoEnabled: boolean;
  ssoProvider: string;
  mfaEnforced: boolean;
  taxId?: string;
}

export interface HITLTask {
  id: string;
  title: string;
  candidateName: string;
  jobTitle: string;
  agentName: string;
  recommendation: string;
  confidenceScore: number;
  evidence: string[];
  status: 'Pending' | 'Approved' | 'Rejected';
  timestamp: string;
  riskLevel?: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  impact?: string;
}

// --- Milestone 8: Offers, BGV & Onboarding ---
export type OfferStatus = 'Draft' | 'Pending Approval' | 'Approved' | 'Sent' | 'Negotiating' | 'Accepted' | 'Rejected' | 'Expired';

export interface Offer {
  id: string;
  candidateId: string;
  candidateName: string;
  candidateAvatar: string;
  jobId: string;
  jobTitle: string;
  department: string;
  baseSalary: number;
  bonus: number;
  equity: string;
  currency: string;
  joiningDate: string;
  location: string;
  status: OfferStatus;
  owner: string;
  createdAt: string;
  approvalStatus: 'Approved' | 'Pending' | 'Rejected';
  benefits: string[];
  documents: { id: string; name: string; type: string; url: string }[];
  approvalHistory: { approver: string; role: string; decision: string; date: string; comments: string }[];
  negotiationLogs: { date: string; party: string; note: string; proposedSalary: number }[];
}

export interface BackgroundVerification {
  id: string;
  candidateId: string;
  candidateName: string;
  jobTitle: string;
  status: 'Passed' | 'In Progress' | 'Flagged' | 'Pending Documents';
  identityCheck: 'Verified' | 'Pending' | 'Failed';
  educationCheck: 'Verified' | 'Pending' | 'Failed';
  employmentCheck: 'Verified' | 'Pending' | 'Failed';
  criminalCheck: 'Verified' | 'Pending' | 'Failed';
  referenceCheck: 'Verified' | 'Pending' | 'Failed';
  riskIndicator: 'Low' | 'Medium' | 'High';
  updatedAt: string;
}

export interface OnboardingTask {
  id: string;
  title: string;
  category: 'HR Docs' | 'IT Setup' | 'Compliance' | 'Training';
  owner: string;
  dueDate: string;
  completed: boolean;
}

export interface OnboardingPlan {
  id: string;
  candidateId: string;
  candidateName: string;
  jobTitle: string;
  department: string;
  joiningDate: string;
  progressPercent: number;
  status: 'Scheduled' | 'Active' | 'Completed';
  tasks: OnboardingTask[];
}

// --- Milestone 9: Communication & Collaboration ---
export type CommChannel = 'Email' | 'SMS' | 'WhatsApp' | 'In-App' | 'Push';

export interface CommMessage {
  id: string;
  candidateId: string;
  candidateName: string;
  candidateAvatar: string;
  channel: CommChannel;
  direction: 'inbound' | 'outbound';
  sender: string;
  recipient: string;
  subject?: string;
  body: string;
  timestamp: string;
  status: 'Sent' | 'Queued' | 'Processing' | 'Delivered' | 'Failed' | 'Read';
  attachments?: string[];
}

export interface CommTemplate {
  id: string;
  name: string;
  channel: CommChannel;
  subject?: string;
  body: string;
  variables: string[];
  active: boolean;
  version: string;
  updatedAt: string;
}

export interface NotificationItem {
  id: string;
  title: string;
  message: string;
  category: 'Offer' | 'Interview' | 'Sourcing' | 'Compliance' | 'System';
  priority: 'Low' | 'Medium' | 'High' | 'Critical';
  timestamp: string;
  read: boolean;
  actionTab?: string;
}

export interface WebhookLog {
  id: string;
  provider: 'SendGrid' | 'Twilio' | 'WhatsApp Business' | 'Greenhouse Sync' | 'Workday HR';
  endpoint: string;
  status: 'Success' | 'Failure' | 'Retrying';
  retryCount: number;
  payloadSummary: string;
  timestamp: string;
  messageId: string;
}

// --- Milestone 10: AI Intelligence & Knowledge ---
export interface AIAgentDetail {
  id: string;
  name: string;
  category: string;
  version: string;
  status: 'active' | 'standby' | 'processing' | 'paused';
  description: string;
  prompt: string;
  tools: string[];
  permissions: string[];
  riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  executionCount: number;
  successRate: number;
  avgLatencyMs: number;
  costEstimate: string;
}

export interface AIToolItem {
  id: string;
  name: string;
  category: string;
  description: string;
  riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  requiredPermissions: string[];
  hitlRequired: boolean;
  usageCount: number;
  status: 'Active' | 'Deprecated' | 'Disabled';
}

export interface KnowledgeDoc {
  id: string;
  title: string;
  category: 'Company Policy' | 'Engineering Benchmarks' | 'Compensation Bands' | 'Interview Guidelines';
  tags: string[];
  size: string;
  uploadDate: string;
  status: 'Processing' | 'Indexed' | 'Failed';
  chunksCount: number;
  embeddingModel: string;
  retentionDays: number;
}

export interface AIExecutionItem {
  id: string;
  executionId: string;
  agentName: string;
  workflowName: string;
  status: 'Queued' | 'Running' | 'Waiting for Human' | 'Completed' | 'Failed' | 'Cancelled';
  durationMs: number;
  tokensUsed: number;
  costUSD: number;
  traceId: string;
  timestamp: string;
  error?: string;
  reasoningSummary?: string;
}

// --- Milestone 11: Agentic Orchestration & Workflows ---
export interface WorkflowCanvasNode {
  id: string;
  label: string;
  type: 'trigger' | 'agent' | 'tool' | 'hitl' | 'condition' | 'output';
  status: 'idle' | 'running' | 'completed' | 'failed';
  duration: string;
  risk: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  inputOutput: string;
}

// --- Milestone 12: Intelligent Sourcing & Observability ---
export interface SourcingCandidateResult {
  id: string;
  candidateName: string;
  candidateAvatar: string;
  currentRole: string;
  currentCompany: string;
  overallMatchScore: number;
  skillsScore: number;
  experienceScore: number;
  roleFitScore: number;
  educationScore: number;
  semanticFitScore: number;
  confidence: 'High' | 'Medium' | 'Low';
  risk: 'Low' | 'Medium' | 'High';
  recommendation: 'Strongly Recommend' | 'Recommend' | 'Consider' | 'Do Not Recommend';
  strengths: string[];
  gaps: string[];
  evidenceSources: { title: string; snippet: string }[];
  compliancePassed: boolean;
  hitlApproved?: boolean;
}

export interface TraceNode {
  id: string;
  name: string;
  type: 'workflow' | 'agent' | 'llm' | 'tool' | 'rag' | 'hitl';
  durationMs: number;
  status: 'ok' | 'error';
  model?: string;
  tokens?: number;
  children?: TraceNode[];
}

export interface ObservabilityTrace {
  id: string;
  traceName: string;
  timestamp: string;
  totalDurationMs: number;
  totalTokens: number;
  totalCostUSD: number;
  errorCount: number;
  rootNode: TraceNode;
}


