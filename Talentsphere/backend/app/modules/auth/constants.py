from enum import Enum

class AccountType(str, Enum):
    PLATFORM_SUPER_ADMIN = "PLATFORM_SUPER_ADMIN"
    ORGANIZATION_SUPER_ADMIN = "ORGANIZATION_SUPER_ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN" # Retained for legacy compatibility
    HR_ADMIN = "HR_ADMIN"
    RECRUITER = "RECRUITER"
    HIRING_MANAGER = "HIRING_MANAGER"
    INTERVIEWER = "INTERVIEWER"
    EXECUTIVE = "EXECUTIVE"
    CANDIDATE = "CANDIDATE"
    SYSTEM = "SYSTEM"

class RoleScope(str, Enum):
    PLATFORM = "PLATFORM"
    ORGANIZATION = "ORGANIZATION"

class AccountStatus(str, Enum):
    PENDING_VERIFICATION = "Pending Verification"
    ACTIVE = "Active"
    LOCKED = "Locked"
    SUSPENDED = "Suspended"
    DISABLED = "Disabled"

# System Permission Catalog Definitions (Categorized by Scope)
SYSTEM_PERMISSIONS = [
    # Platform-Level Permissions (Scope = PLATFORM)
    {"code": "platform:read", "name": "View Platform Metrics", "module": "platform", "scope": "PLATFORM", "description": "Can view platform-wide analytics and health"},
    {"code": "platform:manage", "name": "Manage Platform", "module": "platform", "scope": "PLATFORM", "description": "Can manage global system settings and configuration"},
    {"code": "organization:read:any", "name": "View Any Organization", "module": "platform", "scope": "PLATFORM", "description": "Can view metadata for all tenant organizations"},
    {"code": "organization:create", "name": "Create Organization", "module": "platform", "scope": "PLATFORM", "description": "Can provision new organization tenants"},
    {"code": "organization:update:any", "name": "Update Any Organization", "module": "platform", "scope": "PLATFORM", "description": "Can edit metadata for any tenant organization"},
    {"code": "organization:suspend", "name": "Suspend Organization", "module": "platform", "scope": "PLATFORM", "description": "Can suspend tenant access"},
    {"code": "organization:activate", "name": "Activate Organization", "module": "platform", "scope": "PLATFORM", "description": "Can activate suspended tenants"},
    {"code": "organization:admin:create", "name": "Create Org Admin", "module": "platform", "scope": "PLATFORM", "description": "Can provision initial Organization Super Admin"},
    {"code": "organization:admin:reset", "name": "Reset Org Admin Access", "module": "platform", "scope": "PLATFORM", "description": "Can trigger password reset for Org Super Admin"},
    {"code": "platform:audit:read", "name": "View Platform Audit Logs", "module": "platform", "scope": "PLATFORM", "description": "Can view global platform security and audit logs"},

    # Organization-Level Permissions (Scope = ORGANIZATION)
    {"code": "users:read", "name": "View Users", "module": "auth", "scope": "ORGANIZATION", "description": "Can view user accounts inside organization"},
    {"code": "users:write", "name": "Manage Users", "module": "auth", "scope": "ORGANIZATION", "description": "Can create and edit organization users"},
    {"code": "users:delete", "name": "Delete Users", "module": "auth", "scope": "ORGANIZATION", "description": "Can disable or delete organization users"},
    {"code": "roles:manage", "name": "Manage Roles & Permissions", "module": "auth", "scope": "ORGANIZATION", "description": "Can assign roles and configure tenant permissions"},
    
    # Organization Settings & Master Data
    {"code": "org:read", "name": "View Organization Settings", "module": "organizations", "scope": "ORGANIZATION", "description": "Can view org details"},
    {"code": "org:write", "name": "Update Organization", "module": "organizations", "scope": "ORGANIZATION", "description": "Can update org settings"},
    
    # Candidates
    {"code": "candidates:read", "name": "View Candidates", "module": "candidates", "scope": "ORGANIZATION", "description": "Can view candidate profiles and resumes"},
    {"code": "candidates:write", "name": "Manage Candidates", "module": "candidates", "scope": "ORGANIZATION", "description": "Can create and edit candidates"},
    {"code": "candidates:delete", "name": "Delete Candidates", "module": "candidates", "scope": "ORGANIZATION", "description": "Can soft-delete candidates"},
    
    # Recruitment & Jobs
    {"code": "jobs:read", "name": "View Jobs", "module": "recruitment", "scope": "ORGANIZATION", "description": "Can view job postings"},
    {"code": "jobs:write", "name": "Manage Jobs", "module": "recruitment", "scope": "ORGANIZATION", "description": "Can create and update jobs"},
    {"code": "jobs:publish", "name": "Publish Jobs", "module": "recruitment", "scope": "ORGANIZATION", "description": "Can publish jobs to boards"},
    {"code": "applications:manage", "name": "Manage Applications", "module": "recruitment", "scope": "ORGANIZATION", "description": "Can advance or reject candidate applications"},
    {"code": "hiring_plans:manage", "name": "Manage Hiring Plans", "module": "recruitment", "scope": "ORGANIZATION", "description": "Can create and manage hiring plans & requisitions"},
    {"code": "pipelines:manage", "name": "Manage Pipelines", "module": "recruitment", "scope": "ORGANIZATION", "description": "Can create recruitment pipelines and workflow stages"},
    {"code": "workflow:configure", "name": "Configure Workflows", "module": "recruitment", "scope": "ORGANIZATION", "description": "Can configure workflow rules, transitions, and SLAs"},
    
    # Interviews
    {"code": "interviews:read", "name": "View Interviews", "module": "interviews", "scope": "ORGANIZATION", "description": "Can view interview schedules and panels"},
    {"code": "interviews:schedule", "name": "Schedule Interviews", "module": "interviews", "scope": "ORGANIZATION", "description": "Can schedule and reschedule interviews"},
    {"code": "interviews:evaluate", "name": "Submit Scorecards", "module": "interviews", "scope": "ORGANIZATION", "description": "Can submit interview feedback"},
    
    # Offers & Hiring
    {"code": "offers:read", "name": "View Offers", "module": "offers", "scope": "ORGANIZATION", "description": "Can view offer letters and comp details"},
    {"code": "offers:write", "name": "Create Offers", "module": "offers", "scope": "ORGANIZATION", "description": "Can draft and issue offer letters"},
    {"code": "offers:approve", "name": "Approve Offers", "module": "offers", "scope": "ORGANIZATION", "description": "Can approve offer requests"},
    
    # AI & Knowledge
    {"code": "ai:execute", "name": "Run AI Workflows", "module": "ai", "scope": "ORGANIZATION", "description": "Can execute AI screening, matching, and generation workflows"},
    {"code": "ai:admin", "name": "Manage AI Prompts & Models", "module": "ai", "scope": "ORGANIZATION", "description": "Can edit AI prompts and model hyper-parameters"},
    
    # Reporting
    {"code": "reports:view", "name": "View Analytics", "module": "reporting", "scope": "ORGANIZATION", "description": "Can view dashboards and export reports"}
]

DEFAULT_ROLES = [
    {
        "code": "PLATFORM_SUPER_ADMIN",
        "name": "Platform Super Administrator",
        "scope": "PLATFORM",
        "description": "Full platform administration across all tenants, global configuration, and audit",
        "is_system_role": True,
        "permissions": [
            "platform:read", "platform:manage", "organization:read:any", "organization:create",
            "organization:update:any", "organization:suspend", "organization:activate",
            "organization:admin:create", "organization:admin:reset", "platform:audit:read"
        ]
    },
    {
        "code": "ORGANIZATION_SUPER_ADMIN",
        "name": "Organization Super Administrator",
        "scope": "ORGANIZATION",
        "description": "Full tenant-scoped administration over organization users, roles, settings, and workflows",
        "is_system_role": True,
        "permissions": [
            "users:read", "users:write", "users:delete", "roles:manage", "org:read", "org:write",
            "candidates:read", "candidates:write", "candidates:delete",
            "jobs:read", "jobs:write", "jobs:publish", "applications:manage",
            "hiring_plans:manage", "pipelines:manage", "workflow:configure",
            "interviews:read", "interviews:schedule", "interviews:evaluate",
            "offers:read", "offers:write", "offers:approve",
            "ai:execute", "ai:admin", "reports:view"
        ]
    },
    {
        "code": "SUPER_ADMIN",
        "name": "Super Administrator (Legacy)",
        "scope": "PLATFORM",
        "description": "Legacy wildcard admin access",
        "is_system_role": True,
        "permissions": ["*"]
    },
    {
        "code": "HR_ADMIN",
        "name": "HR Administrator",
        "scope": "ORGANIZATION",
        "description": "Access to manage organization users, jobs, candidates, offers, and settings",
        "is_system_role": True,
        "permissions": [
            "users:read", "users:write", "roles:manage", "org:read", "org:write",
            "candidates:read", "candidates:write", "candidates:delete",
            "jobs:read", "jobs:write", "jobs:publish", "applications:manage",
            "hiring_plans:manage", "pipelines:manage", "workflow:configure",
            "interviews:read", "interviews:schedule", "interviews:evaluate",
            "offers:read", "offers:write", "offers:approve",
            "ai:execute", "reports:view"
        ]
    },
    {
        "code": "RECRUITER",
        "name": "Recruiter",
        "scope": "ORGANIZATION",
        "description": "Manages job postings, sources candidates, screens applications, and schedules interviews",
        "is_system_role": True,
        "permissions": [
            "candidates:read", "candidates:write",
            "jobs:read", "jobs:write", "applications:manage",
            "hiring_plans:manage", "pipelines:manage", "workflow:configure",
            "interviews:read", "interviews:schedule",
            "offers:read", "offers:write",
            "ai:execute", "reports:view"
        ]
    },
    {
        "code": "HIRING_MANAGER",
        "name": "Hiring Manager",
        "scope": "ORGANIZATION",
        "description": "Reviews applicants, approves job requisitions, conducts interviews, and approves offers",
        "is_system_role": True,
        "permissions": [
            "candidates:read", "jobs:read", "applications:manage",
            "interviews:read", "interviews:schedule", "interviews:evaluate",
            "offers:read", "offers:approve", "ai:execute"
        ]
    },
    {
        "code": "INTERVIEWER",
        "name": "Interviewer",
        "scope": "ORGANIZATION",
        "description": "Views assigned candidates and submits interview feedback and scorecards",
        "is_system_role": True,
        "permissions": [
            "candidates:read", "interviews:read", "interviews:evaluate"
        ]
    },
    {
        "code": "CANDIDATE",
        "name": "Candidate / Applicant",
        "scope": "ORGANIZATION",
        "description": "External candidate portal user submitting applications and tracking progress",
        "is_system_role": True,
        "permissions": [
            "jobs:read"
        ]
    }
]

