import React, { createContext, useContext, useState, useEffect } from 'react';
import {
  Candidate,
  Job,
  Application,
  HiringPlan,
  RecruitmentWorkflow,
  Interview,
  Branch,
  Department,
  Designation,
  Organization,
  SecurityAuditItem,
  HITLTask,
  Scorecard
} from '../types';
import { MOCK_ORGANIZATION } from '../data/mockData';
import { backendApi } from '../api/client';

interface OrganizationContextType {
  organization: Organization;
  candidates: Candidate[];
  jobs: Job[];
  applications: Application[];
  hiringPlans: HiringPlan[];
  workflows: RecruitmentWorkflow[];
  interviews: Interview[];
  branches: Branch[];
  departments: Department[];
  designations: Designation[];
  auditLogs: SecurityAuditItem[];
  hitlTasks: HITLTask[];
  
  // Handlers
  addCandidate: (candidate: Omit<Candidate, 'id' | 'createdAt' | 'updatedAt'>) => void;
  updateCandidateStatus: (id: string, status: Candidate['status']) => void;
  addJob: (job: Omit<Job, 'id' | 'createdAt' | 'updatedAt' | 'filled'>) => void;
  updateJobStatus: (id: string, status: Job['status']) => void;
  addHiringPlan: (plan: Omit<HiringPlan, 'id' | 'createdAt'>) => void;
  updateApplicationStage: (appId: string, stageId: string, stageName: string) => void;
  addInterview: (interview: Omit<Interview, 'id'>) => void;
  submitScorecard: (interviewId: string, scorecard: Omit<Scorecard, 'id' | 'submittedAt'>) => void;
  updateWorkflow: (workflow: RecruitmentWorkflow) => void;
  resolveHITLTask: (taskId: string, action: 'Approved' | 'Rejected') => void;
  addBranch: (branch: Omit<Branch, 'id'>) => void;
  addDepartment: (department: Omit<Department, 'id'>) => void;
  addDesignation: (designation: Omit<Designation, 'id'>) => void;
  createOrganization: (orgData: any) => Promise<void>;
}

const OrganizationContext = createContext<OrganizationContextType | undefined>(undefined);

export const OrganizationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [organization, setOrganization] = useState<Organization>(MOCK_ORGANIZATION);
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [applications, setApplications] = useState<Application[]>([]);
  const [hiringPlans, setHiringPlans] = useState<HiringPlan[]>([]);
  const [workflows, setWorkflows] = useState<RecruitmentWorkflow[]>([]);
  const [interviews, setInterviews] = useState<Interview[]>([]);
  const [branches, setBranches] = useState<Branch[]>([]);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [designations, setDesignations] = useState<Designation[]>([]);
  const [auditLogs, setAuditLogs] = useState<SecurityAuditItem[]>([]);
  const [hitlTasks, setHitlTasks] = useState<HITLTask[]>([]);

  // Load datasets from Live Backend on mount
  useEffect(() => {
    const fetchBackendData = async () => {
      try {
        const [
          liveCand,
          liveJobs,
          liveApps,
          livePlans,
          liveBranches,
          liveDepts,
          liveDesgs,
          liveOrg,
          liveExecs,
          liveInterviews
        ] = await Promise.all([
          backendApi.getCandidates(),
          backendApi.getJobs(),
          backendApi.getApplications(),
          backendApi.getHiringPlans(),
          backendApi.getBranches(),
          backendApi.getDepartments(),
          backendApi.getDesignations(),
          backendApi.getOrganization(),
          backendApi.getExecutions(),
          backendApi.getInterviews()
        ]);

        if (liveCand && Array.isArray(liveCand)) {
          setCandidates(liveCand.map((c: any) => ({
            id: c.id,
            name: `${c.first_name || ''} ${c.last_name || ''}`.trim() || 'Candidate',
            email: c.email,
            phone: c.phone || 'N/A',
            location: c.location || 'Not Specified',
            currentRole: c.current_role || 'Candidate',
            currentCompany: c.current_company || 'Organization',
            avatar: `https://ui-avatars.com/api/?name=${encodeURIComponent(c.first_name || 'U')}&background=random`,
            status: 'New',
            matchScore: c.match_score || 85,
            skills: Array.isArray(c.skills) ? c.skills : [],
            summary: c.summary || '',
            experiences: (c.experiences || []).map((exp: any) => ({
              id: exp.id || `exp-${Date.now()}`,
              company: exp.company_name || 'Company',
              role: exp.designation_name || 'Role',
              startDate: exp.start_date || 'Recent',
              endDate: exp.end_date || 'Present',
              isCurrent: exp.is_current,
              description: exp.description || ''
            })),
            education: (c.education || []).map((edu: any) => ({
              id: edu.id || `edu-${Date.now()}`,
              institution: edu.university_name || 'University',
              degree: edu.degree_name || 'Degree',
              fieldOfStudy: edu.field_of_study || 'General',
              graduationYear: edu.end_year || edu.start_year || 2024
            })),
            documents: (c.documents || []).map((doc: any) => ({
              id: doc.id || `doc-${Date.now()}`,
              name: doc.file_name || 'Resume.pdf',
              type: 'Resume',
              uploadDate: doc.created_at || 'Recently',
              size: doc.file_size ? `${Math.round(doc.file_size / 1024)} KB` : 'Uploaded'
            })),
            timeline: [],
            createdAt: c.created_at || new Date().toISOString(),
            updatedAt: c.updated_at || new Date().toISOString()
          })));
        }
        if (liveJobs && Array.isArray(liveJobs)) setJobs(liveJobs);
        if (liveApps && Array.isArray(liveApps)) setApplications(liveApps);
        if (livePlans && Array.isArray(livePlans)) setHiringPlans(livePlans);
        if (liveBranches && Array.isArray(liveBranches)) {
          setBranches(liveBranches.map((b: any) => ({
            id: b.id,
            name: b.branch_name,
            location: b.location_id || 'Unknown',
            country: 'Unknown',
            headcount: 0,
            status: b.is_active ? 'Active' : 'Inactive'
          })));
        }
        if (liveDepts && Array.isArray(liveDepts)) {
          setDepartments(liveDepts.map((d: any) => ({
            id: d.id,
            name: d.department_name,
            headName: d.department_head_id || 'N/A',
            branchName: 'Headquarters',
            openPositions: 0,
            totalMembers: 0
          })));
        }
        if (liveDesgs && Array.isArray(liveDesgs)) {
          setDesignations(liveDesgs.map((d: any) => ({
            id: d.id,
            title: d.designation_name,
            department: 'N/A',
            level: d.level || 'Standard',
            payGrade: d.grade || 'Band 1'
          })));
        }
        if (liveOrg) {
          setOrganization({
            id: liveOrg.id,
            name: liveOrg.display_name || liveOrg.legal_name || 'Organization',
            domain: liveOrg.website || `${liveOrg.organization_code?.toLowerCase() || 'org'}.com`,
            logo: liveOrg.logo_path || '',
            plan: (liveOrg.subscription_plan as any) || 'Enterprise Tier 1',
            headquarters: 'N/A',
            totalEmployees: liveOrg.employee_count || 0,
            ssoEnabled: false,
            ssoProvider: 'None',
            mfaEnforced: false,
            taxId: liveOrg.tax_number || liveOrg.registration_number || 'N/A'
          });
        }
        if (liveInterviews && Array.isArray(liveInterviews)) setInterviews(liveInterviews);

        // Map executions to HITL tasks if status is Waiting_HITL
        if (liveExecs && Array.isArray(liveExecs)) {
          const formattedHitl: HITLTask[] = liveExecs
            .filter((e) => e.status === 'Waiting_HITL' || e.status === 'Waiting for Human')
            .map((e) => ({
              id: e.id || e.execution_id,
              title: `Approve Candidate Screening Decision`,
              candidateName: e.candidate_name || 'System Candidate',
              jobTitle: e.job_title || 'General Opening',
              agentName: e.agent_name || 'Screening Agent',
              recommendation: 'SHORTLIST',
              confidenceScore: 0.92,
              evidence: ['Resume matches key tech skills', 'Required experience criteria passed.'],
              status: 'Pending',
              timestamp: new Date().toISOString()
            }));
          setHitlTasks(formattedHitl);
        }
      } catch (err) {
        console.error('[OrganizationProvider] Failed loading active backend records:', err);
      }
    };

    fetchBackendData();
  }, []);

  const addCandidate = async (candidateData: Omit<Candidate, 'id' | 'createdAt' | 'updatedAt'>) => {
    try {
      let saved: any = null;
      const stagedPayload = (candidateData as any).stagedPayload;
      
      if (stagedPayload) {
        saved = await backendApi.createCandidateFromStaged(stagedPayload);
      } else {
        const nameParts = candidateData.name.split(' ');
        const firstName = nameParts[0];
        const lastName = nameParts.slice(1).join(' ');
        const backendPayload = {
          first_name: firstName,
          last_name: lastName || 'User',
          email: candidateData.email,
          phone: candidateData.phone || null
        };
        saved = await backendApi.createCandidate(backendPayload);
      }

      if (saved) {
        const candObj = saved.candidate || saved;
        const candId = saved.candidate_id || saved.id || `cand-${Date.now()}`;
        const fullSaved: Candidate = {
          ...candidateData,
          id: candId,
          name: candObj.first_name ? `${candObj.first_name} ${candObj.last_name || ''}`.trim() : candidateData.name,
          email: candObj.email || candidateData.email,
          phone: candObj.phone || candidateData.phone,
          location: candObj.location || candidateData.location,
          currentRole: candObj.current_role || candidateData.currentRole,
          currentCompany: candObj.current_company || candidateData.currentCompany,
          summary: candObj.summary || candidateData.summary,
          skills: Array.isArray(candObj.skills) ? candObj.skills : candidateData.skills,
          matchScore: candObj.match_score || candidateData.matchScore || 85,
          createdAt: candObj.created_at || new Date().toISOString().split('T')[0],
          updatedAt: candObj.updated_at || new Date().toISOString().split('T')[0]
        };
        setCandidates((prev) => [fullSaved, ...prev]);
      } else {
        // Safe local state fallback if backend isn't ready
        const localCand: Candidate = {
          ...candidateData,
          id: `cand-${Date.now()}`,
          createdAt: new Date().toISOString().split('T')[0],
          updatedAt: new Date().toISOString().split('T')[0]
        };
        setCandidates((prev) => [localCand, ...prev]);
      }
    } catch (err) {
      console.error('[addCandidate] Failed:', err);
    }
  };

  const updateCandidateStatus = (id: string, status: Candidate['status']) => {
    setCandidates((prev) =>
      prev.map((c) => (c.id === id ? { ...c, status, updatedAt: new Date().toISOString().split('T')[0] } : c))
    );
  };

  const addJob = async (jobData: Omit<Job, 'id' | 'createdAt' | 'updatedAt' | 'filled'>) => {
    try {
      const saved = await backendApi.createJob(jobData);
      if (saved) {
        setJobs((prev) => [saved, ...prev]);
      } else {
        const localJob: Job = {
          ...jobData,
          id: `job-${Date.now()}`,
          filled: 0,
          createdAt: new Date().toISOString().split('T')[0],
          updatedAt: new Date().toISOString().split('T')[0]
        };
        setJobs((prev) => [localJob, ...prev]);
      }
    } catch (err) {
      console.error('[addJob] Failed:', err);
    }
  };

  const updateJobStatus = (id: string, status: Job['status']) => {
    setJobs((prev) =>
      prev.map((j) => (j.id === id ? { ...j, status, updatedAt: new Date().toISOString().split('T')[0] } : j))
    );
  };

  const addHiringPlan = async (planData: Omit<HiringPlan, 'id' | 'createdAt'>) => {
    try {
      const saved = await backendApi.createHiringPlan(planData);
      if (saved) {
        setHiringPlans((prev) => [saved, ...prev]);
      } else {
        const localPlan: HiringPlan = {
          ...planData,
          id: `plan-${Date.now()}`,
          createdAt: new Date().toISOString().split('T')[0]
        };
        setHiringPlans((prev) => [localPlan, ...prev]);
      }
    } catch (err) {
      console.error('[addHiringPlan] Failed:', err);
    }
  };

  const updateApplicationStage = (appId: string, stageId: string, stageName: string) => {
    setApplications((prev) =>
      prev.map((app) => (app.id === appId ? { ...app, stageId, stageName } : app))
    );
  };

  const addInterview = async (interviewData: Omit<Interview, 'id'>) => {
    try {
      const saved = await backendApi.createInterview(interviewData);
      if (saved) {
        setInterviews((prev) => [saved, ...prev]);
      } else {
        const localInt: Interview = {
          ...interviewData,
          id: `int-${Date.now()}`,
        };
        setInterviews((prev) => [localInt, ...prev]);
      }
    } catch (err) {
      console.error('[addInterview] Failed:', err);
    }
  };

  const submitScorecard = (interviewId: string, scorecardData: Omit<Scorecard, 'id' | 'submittedAt'>) => {
    setInterviews((prev) =>
      prev.map((int) =>
        int.id === interviewId
          ? {
              ...int,
              scorecardSubmitted: true,
              overallScore: scorecardData.overallScore,
              status: 'Completed',
            }
          : int
      )
    );
  };

  const updateWorkflow = (workflow: RecruitmentWorkflow) => {
    setWorkflows((prev) =>
      prev.map((wf) => (wf.id === workflow.id ? { ...workflow, updatedAt: new Date().toISOString().split('T')[0] } : wf))
    );
  };

  const resolveHITLTask = (taskId: string, action: 'Approved' | 'Rejected') => {
    setHitlTasks((prev) =>
      prev.map((t) => (t.id === taskId ? { ...t, status: action } : t))
    );
  };

  const addBranch = (branchData: Omit<Branch, 'id'>) => {
    setBranches((prev) => [...prev, { ...branchData, id: `br-${Date.now()}` }]);
  };

  const addDepartment = (deptData: Omit<Department, 'id'>) => {
    setDepartments((prev) => [...prev, { ...deptData, id: `dept-${Date.now()}` }]);
  };

  const addDesignation = (desgData: Omit<Designation, 'id'>) => {
    setDesignations((prev) => [...prev, { ...desgData, id: `desg-${Date.now()}` }]);
  };

  const createOrganization = async (orgData: any) => {
    try {
      const saved = await backendApi.createOrganization(orgData);
      if (saved && saved.status === 'success') {
        setOrganization({
          id: saved.organization_id,
          name: orgData.display_name,
          domain: orgData.legal_name,
          logo: '',
          plan: orgData.subscription_plan || 'Enterprise Tier 1',
          headquarters: 'N/A',
          totalEmployees: 0,
          ssoEnabled: false,
          ssoProvider: 'None',
          mfaEnforced: false,
          taxId: 'N/A'
        });
      }
    } catch (err) {
      console.error('[createOrganization] Failed:', err);
    }
  };

  return (
    <OrganizationContext.Provider
      value={{
        organization,
        candidates,
        jobs,
        applications,
        hiringPlans,
        workflows,
        interviews,
        branches,
        departments,
        designations,
        auditLogs,
        hitlTasks,
        addCandidate,
        updateCandidateStatus,
        addJob,
        updateJobStatus,
        addHiringPlan,
        updateApplicationStage,
        addInterview,
        submitScorecard,
        updateWorkflow,
        resolveHITLTask,
        addBranch,
        addDepartment,
        addDesignation,
        createOrganization,
      }}
    >
      {children}
    </OrganizationContext.Provider>
  );
};

export const useOrganization = () => {
  const context = useContext(OrganizationContext);
  if (!context) {
    throw new Error('useOrganization must be used within an OrganizationProvider');
  }
  return context;
};
