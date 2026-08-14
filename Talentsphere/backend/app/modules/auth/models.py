from sqlalchemy import Column, String, Boolean, ForeignKey, TEXT, UniqueConstraint, DateTime, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.models import Base, AuditMixin

class User(AuditMixin, Base):
    __tablename__ = "users"
    
    organization_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("organizations.id"), nullable=True)
    employee_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # Link to internal employee if applicable
    candidate_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # Link to candidate if applicable
    
    username: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    password_hash: Mapped[str] = mapped_column(TEXT)
    
    account_type: Mapped[str] = mapped_column(String(50)) # PLATFORM_SUPER_ADMIN, ORGANIZATION_SUPER_ADMIN, HR_ADMIN, RECRUITER, etc.
    account_status: Mapped[str] = mapped_column(String(30)) # Pending Verification, Active, Locked, Suspended, Disabled
    account_scope: Mapped[str] = mapped_column(String(30), default="ORGANIZATION") # PLATFORM, ORGANIZATION
    
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    email_verified: Mapped[bool] = mapped_column(default=False)
    phone_verified: Mapped[bool] = mapped_column(default=False)
    mfa_enabled: Mapped[bool] = mapped_column(default=False)

class UserProfile(AuditMixin, Base):
    __tablename__ = "user_profiles"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), unique=True)
    first_name: Mapped[str] = mapped_column(String(100))
    middle_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100))
    profile_photo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    gender: Mapped[str | None] = mapped_column(String(20), nullable=True)
    date_of_birth: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True) # Stored as timestamp or date
    timezone_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # References TimeZone
    language_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # References Language

class Role(AuditMixin, Base):
    __tablename__ = "roles"
    organization_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("organizations.id"), nullable=True)
    role_code: Mapped[str] = mapped_column(String(50))
    role_name: Mapped[str] = mapped_column(String(100))
    scope: Mapped[str] = mapped_column(String(30), default="ORGANIZATION") # PLATFORM, ORGANIZATION
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_system_role: Mapped[bool] = mapped_column(default=False)

class Permission(AuditMixin, Base):
    __tablename__ = "permissions"
    permission_code: Mapped[str] = mapped_column(String(100), unique=True) # e.g. platform:read, candidate.read
    permission_name: Mapped[str] = mapped_column(String(100))
    module: Mapped[str] = mapped_column(String(50))
    scope: Mapped[str] = mapped_column(String(30), default="ORGANIZATION") # PLATFORM, ORGANIZATION
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

class PermissionGroup(AuditMixin, Base):
    __tablename__ = "permission_groups"
    group_name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

class RolePermission(AuditMixin, Base):
    __tablename__ = "role_permissions"
    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roles.id"))
    permission_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("permissions.id"))
    __table_args__ = (UniqueConstraint('role_id', 'permission_id', name='uq_role_permission'),)

class UserRole(AuditMixin, Base):
    __tablename__ = "user_roles"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roles.id"))
    assigned_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    __table_args__ = (UniqueConstraint('user_id', 'role_id', name='uq_user_role'),)

class Session(AuditMixin, Base):
    __tablename__ = "sessions"
    session_token: Mapped[str] = mapped_column(String(500), unique=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    device_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    device_type: Mapped[str | None] = mapped_column(String(50), nullable=True) # Mobile, Desktop, Tablet
    operating_system: Mapped[str | None] = mapped_column(String(500), nullable=True)
    browser: Mapped[str | None] = mapped_column(String(500), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    login_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class RefreshToken(AuditMixin, Base):
    __tablename__ = "refresh_tokens"
    token_hash: Mapped[str] = mapped_column(String(500), unique=True)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sessions.id"))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked: Mapped[bool] = mapped_column(default=False)

class MfaConfiguration(AuditMixin, Base):
    __tablename__ = "mfa_configurations"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), unique=True)
    mfa_type: Mapped[str] = mapped_column(String(30)) # TOTP, Email OTP, SMS OTP
    secret_key: Mapped[str] = mapped_column(TEXT)
    enabled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class MfaRecoveryCode(AuditMixin, Base):
    __tablename__ = "mfa_recovery_codes"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    recovery_code_hash: Mapped[str] = mapped_column(String(255))
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class PasswordHistory(AuditMixin, Base):
    __tablename__ = "password_history"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    password_hash: Mapped[str] = mapped_column(TEXT)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class PasswordResetToken(AuditMixin, Base):
    __tablename__ = "password_reset_tokens"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    token_hash: Mapped[str] = mapped_column(String(255), unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class EmailVerification(AuditMixin, Base):
    __tablename__ = "email_verifications"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    verification_token: Mapped[str] = mapped_column(String(255), unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class ApiKey(AuditMixin, Base):
    __tablename__ = "api_keys"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    key_name: Mapped[str] = mapped_column(String(100))
    key_hash: Mapped[str] = mapped_column(String(255), unique=True)
    permissions: Mapped[str | None] = mapped_column(TEXT, nullable=True) # Comma separated or JSON permission rules
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class UserPreference(AuditMixin, Base):
    __tablename__ = "user_preferences"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), unique=True)
    language: Mapped[str | None] = mapped_column(String(10), nullable=True)
    timezone: Mapped[str | None] = mapped_column(String(100), nullable=True)
    theme: Mapped[str | None] = mapped_column(String(30), nullable=True) # light, dark, system
    notification_preferences: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    dashboard_layout: Mapped[dict | None] = mapped_column(JSON, nullable=True)

class LoginHistory(AuditMixin, Base):
    __tablename__ = "login_history"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    login_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    logout_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    browser: Mapped[str | None] = mapped_column(String(500), nullable=True)
    operating_system: Mapped[str | None] = mapped_column(String(500), nullable=True)
    login_status: Mapped[str] = mapped_column(String(30)) # Success, Failed
    failure_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)

class ActivityLog(AuditMixin, Base):
    __tablename__ = "activity_logs"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    module: Mapped[str] = mapped_column(String(50)) # e.g. recruitment, candidates
    action: Mapped[str] = mapped_column(String(100)) # e.g. Created Job, Updated Candidate
    entity_type: Mapped[str | None] = mapped_column(String(100), nullable=True) # e.g. Job, Candidate
    entity_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)

class AuditLog(AuditMixin, Base):
    __tablename__ = "audit_logs"
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    entity_type: Mapped[str] = mapped_column(String(100))
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    action: Mapped[str] = mapped_column(String(50)) # INSERT, UPDATE, DELETE
    previous_values: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    new_values: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class SecurityEvent(AuditMixin, Base):
    __tablename__ = "security_events"
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    event_type: Mapped[str] = mapped_column(String(100)) # e.g. Failed Login, Password Reset, MFA Disabled
    severity: Mapped[str] = mapped_column(String(30)) # Low, Medium, High, Critical
    description: Mapped[str] = mapped_column(TEXT)
    event_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
