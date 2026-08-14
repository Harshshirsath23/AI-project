from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional, List, Dict, Any
import uuid
from datetime import date, datetime

# -------------------------
# Core Candidate
# -------------------------
class CandidateBase(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=30)

class CandidateCreate(CandidateBase):
    pass

class CandidateCreateFromStaged(BaseModel):
    candidate: CandidateCreate
    staged_file_path: str
    original_filename: str
    file_size: int
    mime_type: str
    location: Optional[str] = "Not Specified"
    current_role: Optional[str] = "Candidate"
    current_company: Optional[str] = "Organization"
    summary: Optional[str] = ""
    raw_skills: Optional[List[str]] = []
    education: Optional[List['CandidateEducationCreate']] = []
    experience: Optional[List['CandidateExperienceCreate']] = []
    skills: Optional[List['CandidateSkillCreate']] = []

class CandidateResponse(CandidateBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# -------------------------
# Candidate Profile
# -------------------------
class CandidateProfileBase(BaseModel):
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    marital_status: Optional[str] = None
    nationality: Optional[str] = None
    summary: Optional[str] = None

class CandidateProfileCreate(CandidateProfileBase):
    pass

class CandidateProfileResponse(CandidateProfileBase):
    candidate_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

# -------------------------
# Professional Info
# -------------------------
class CandidateEducationBase(BaseModel):
    degree_name: str
    university_name: str
    field_of_study: Optional[str] = None
    start_year: int
    end_year: Optional[int] = None
    grade: Optional[str] = None
    is_completed: bool = True

class CandidateEducationCreate(CandidateEducationBase):
    pass

class CandidateEducationResponse(CandidateEducationBase):
    id: uuid.UUID
    candidate_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

class CandidateExperienceBase(BaseModel):
    company_name: str
    designation_name: str
    start_date: date
    end_date: Optional[date] = None
    is_current: bool = False
    description: Optional[str] = None
    location: Optional[str] = None

class CandidateExperienceCreate(CandidateExperienceBase):
    pass

class CandidateExperienceResponse(CandidateExperienceBase):
    id: uuid.UUID
    candidate_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

class CandidateSkillBase(BaseModel):
    skill_id: uuid.UUID
    proficiency_level: Optional[str] = None

class CandidateSkillCreate(CandidateSkillBase):
    pass

class CandidateSkillResponse(CandidateSkillBase):
    id: uuid.UUID
    candidate_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

class CandidateCertificationBase(BaseModel):
    certification_name: str
    issuing_organization: str
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    credential_id: Optional[str] = None

class CandidateCertificationCreate(CandidateCertificationBase):
    pass

class CandidateCertificationResponse(CandidateCertificationBase):
    id: uuid.UUID
    candidate_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

# -------------------------
# Resumes & Documents
# -------------------------
class ResumeResponse(BaseModel):
    id: uuid.UUID
    candidate_id: uuid.UUID
    file_name: str
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    is_primary: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# -------------------------
# AI & Completion
# -------------------------
class CandidateAiProfileResponse(BaseModel):
    candidate_id: uuid.UUID
    ai_profile_completeness: Optional[float] = None
    ai_calculated_experience_years: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)

# -------------------------
# Search & Filters
# -------------------------
class CandidateSearchRequest(BaseModel):
    query: Optional[str] = None
    skills: Optional[List[uuid.UUID]] = None
    min_experience_years: Optional[float] = None
    notice_period_days: Optional[int] = None
    limit: int = 50
    offset: int = 0

class FullCandidateProfileResponse(BaseModel):
    candidate: CandidateResponse
    profile: Optional[CandidateProfileResponse] = None
    education: List[CandidateEducationResponse] = []
    experience: List[CandidateExperienceResponse] = []
    skills: List[CandidateSkillResponse] = []
    certifications: List[CandidateCertificationResponse] = []
    resumes: List[ResumeResponse] = []
    ai_profile: Optional[CandidateAiProfileResponse] = None

class FullCandidateSummaryResponse(CandidateBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    location: Optional[str] = "Not Specified"
    current_role: Optional[str] = "Candidate"
    current_company: Optional[str] = "Organization"
    summary: Optional[str] = ""
    skills: List[str] = []
    match_score: int = 85
    experiences: List[CandidateExperienceResponse] = []
    education: List[CandidateEducationResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CandidateSemanticSearchRequest(BaseModel):
    query: str = Field(..., min_length=2, description="Natural language search query or required job skills")
    top_k: int = Field(default=10, ge=1, le=100, description="Max candidate results")
    threshold: float = Field(default=0.4, ge=0.0, le=1.0, description="Minimum cosine similarity threshold")

CandidateCreateFromStaged.model_rebuild()
FullCandidateSummaryResponse.model_rebuild()
