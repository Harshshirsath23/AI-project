from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Date, Float, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.models import Base, AuditMixin

# -------------------------
# Geographic Masters
# -------------------------
class Country(AuditMixin, Base):
    __tablename__ = "countries"
    iso_code: Mapped[str] = mapped_column(String(10), unique=True)
    iso3_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    country_name: Mapped[str] = mapped_column(String(100))
    phone_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    currency_code: Mapped[str | None] = mapped_column(String(10), nullable=True)

class State(AuditMixin, Base):
    __tablename__ = "states"
    country_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("countries.id"))
    state_code: Mapped[str] = mapped_column(String(20))
    state_name: Mapped[str] = mapped_column(String(100))

class City(AuditMixin, Base):
    __tablename__ = "cities"
    state_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("states.id"))
    city_name: Mapped[str] = mapped_column(String(100))

class Currency(AuditMixin, Base):
    __tablename__ = "currencies"
    currency_code: Mapped[str] = mapped_column(String(10), unique=True)
    currency_name: Mapped[str] = mapped_column(String(100))
    currency_symbol: Mapped[str | None] = mapped_column(String(20), nullable=True)

class Language(AuditMixin, Base):
    __tablename__ = "languages"
    language_code: Mapped[str] = mapped_column(String(10), unique=True)
    language_name: Mapped[str] = mapped_column(String(100))

class TimeZone(AuditMixin, Base):
    __tablename__ = "timezones"
    timezone_code: Mapped[str] = mapped_column(String(100), unique=True) # e.g. Asia/Kolkata
    display_name: Mapped[str] = mapped_column(String(255))
    utc_offset: Mapped[str | None] = mapped_column(String(30), nullable=True)

# -------------------------
# Industry & Skill Masters
# -------------------------
class Industry(AuditMixin, Base):
    __tablename__ = "industries"
    industry_code: Mapped[str] = mapped_column(String(50), unique=True)
    industry_name: Mapped[str] = mapped_column(String(150))

class Skill(AuditMixin, Base):
    __tablename__ = "skills"
    skill_name: Mapped[str] = mapped_column(String(150), unique=True)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    aliases: Mapped[str | None] = mapped_column(String(500), nullable=True) # comma separated aliases
    is_ai_generated: Mapped[bool] = mapped_column(default=False)

# -------------------------
# Employment & Experience Masters
# -------------------------
class JobFamily(AuditMixin, Base):
    __tablename__ = "job_families"
    family_code: Mapped[str] = mapped_column(String(50), unique=True)
    family_name: Mapped[str] = mapped_column(String(150))

class EmploymentType(AuditMixin, Base):
    __tablename__ = "employment_types"
    type_name: Mapped[str] = mapped_column(String(50), unique=True) # Full Time, Part Time, Contract, Internship, Consultant

class WorkMode(AuditMixin, Base):
    __tablename__ = "work_modes"
    mode_name: Mapped[str] = mapped_column(String(50), unique=True) # Remote, Hybrid, Office

class ExperienceLevel(AuditMixin, Base):
    __tablename__ = "experience_levels"
    level_name: Mapped[str] = mapped_column(String(50), unique=True) # Fresher, Junior, Mid-Level, Senior, Lead, Architect, Director

# -------------------------
# Education Masters
# -------------------------
class Degree(AuditMixin, Base):
    __tablename__ = "degrees"
    degree_name: Mapped[str] = mapped_column(String(100), unique=True)

class University(AuditMixin, Base):
    __tablename__ = "universities"
    university_name: Mapped[str] = mapped_column(String(255), unique=True)
    country_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("countries.id"), nullable=True)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)

class Certification(AuditMixin, Base):
    __tablename__ = "certifications"
    certification_name: Mapped[str] = mapped_column(String(255), unique=True)
    issuing_organization: Mapped[str] = mapped_column(String(255))
    validity_period: Mapped[int | None] = mapped_column(Integer, nullable=True) # in months

# -------------------------
# Organization Core
# -------------------------
class Organization(AuditMixin, Base):
    __tablename__ = "organizations"
    
    organization_code: Mapped[str] = mapped_column(String(50), unique=True)
    legal_name: Mapped[str] = mapped_column(String(255))
    display_name: Mapped[str] = mapped_column(String(255))
    
    registration_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    tax_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    industry_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("industries.id"))
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    logo_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    employee_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
    subscription_plan: Mapped[str] = mapped_column(String(50))
    subscription_status: Mapped[str] = mapped_column(String(30))
    
    timezone_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("timezones.id"), nullable=True)
    currency_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("currencies.id"), nullable=True)
    language_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("languages.id"), nullable=True)

class Location(AuditMixin, Base):
    __tablename__ = "locations"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    location_name: Mapped[str] = mapped_column(String(150))
    address_line_1: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address_line_2: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("cities.id"), nullable=True)
    state_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("states.id"), nullable=True)
    country_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("countries.id"), nullable=True)
    postal_code: Mapped[str | None] = mapped_column(String(30), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)

class Branch(AuditMixin, Base):
    __tablename__ = "branches"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    branch_code: Mapped[str] = mapped_column(String(30))
    branch_name: Mapped[str] = mapped_column(String(150))
    location_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("locations.id"), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    manager_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # Refers to User/Employee
    is_head_office: Mapped[bool] = mapped_column(default=False)

class BusinessUnit(AuditMixin, Base):
    __tablename__ = "business_units"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    unit_code: Mapped[str] = mapped_column(String(30))
    unit_name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    head_employee_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)

class Department(AuditMixin, Base):
    __tablename__ = "departments"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    business_unit_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("business_units.id"), nullable=True)
    department_code: Mapped[str] = mapped_column(String(50))
    department_name: Mapped[str] = mapped_column(String(150))
    parent_department_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("departments.id"), nullable=True)
    department_head_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)

class Designation(AuditMixin, Base):
    __tablename__ = "designations"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    designation_code: Mapped[str] = mapped_column(String(50))
    designation_name: Mapped[str] = mapped_column(String(150))
    job_family_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("job_families.id"), nullable=True)
    level: Mapped[str | None] = mapped_column(String(30), nullable=True)
    grade: Mapped[str | None] = mapped_column(String(30), nullable=True)

class SalaryBand(AuditMixin, Base):
    __tablename__ = "salary_bands"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    band_code: Mapped[str] = mapped_column(String(50))
    minimum_salary: Mapped[float] = mapped_column(Float, default=0.0)
    maximum_salary: Mapped[float] = mapped_column(Float, default=0.0)
    currency_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("currencies.id"))

# -------------------------
# Holidays & shifts
# -------------------------
class HolidayCalendar(AuditMixin, Base):
    __tablename__ = "holiday_calendars"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    calendar_name: Mapped[str] = mapped_column(String(150))
    year: Mapped[int] = mapped_column(Integer)

class Holiday(AuditMixin, Base):
    __tablename__ = "holidays"
    holiday_calendar_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("holiday_calendars.id"))
    holiday_date: Mapped[Date] = mapped_column(Date)
    holiday_name: Mapped[str] = mapped_column(String(150))

class Shift(AuditMixin, Base):
    __tablename__ = "shifts"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    shift_name: Mapped[str] = mapped_column(String(100))
    start_time: Mapped[str] = mapped_column(String(30)) # e.g. "09:00:00"
    end_time: Mapped[str] = mapped_column(String(30)) # e.g. "18:00:00"
    is_flexible: Mapped[bool] = mapped_column(default=False)
