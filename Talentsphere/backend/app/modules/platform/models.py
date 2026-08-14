from sqlalchemy import Column, String, Integer, ForeignKey, Date, Float, TEXT, Boolean, DateTime, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.models import Base, AuditMixin

# -------------------------
# Platform Configuration
# -------------------------
class SystemSetting(AuditMixin, Base):
    __tablename__ = "system_settings"
    setting_key: Mapped[str] = mapped_column(String(150), unique=True)
    setting_value: Mapped[str] = mapped_column(TEXT)

class OrganizationSetting(AuditMixin, Base):
    __tablename__ = "organization_settings"
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # references organizations
    setting_key: Mapped[str] = mapped_column(String(150))
    setting_value: Mapped[str] = mapped_column(TEXT)
    __table_args__ = (UniqueConstraint('organization_id', 'setting_key', name='uq_org_setting_key'),)

class FeatureFlag(AuditMixin, Base):
    __tablename__ = "feature_flags"
    flag_code: Mapped[str] = mapped_column(String(100), unique=True)
    is_enabled: Mapped[bool] = mapped_column(default=False)

class TenantPreference(AuditMixin, Base):
    __tablename__ = "tenant_preferences"
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    preference_key: Mapped[str] = mapped_column(String(100))
    preference_value: Mapped[str] = mapped_column(TEXT)
    __table_args__ = (UniqueConstraint('organization_id', 'preference_key', name='uq_tenant_pref_key'),)

# -------------------------
# File Metadata
# -------------------------
class FileMetadata(AuditMixin, Base):
    __tablename__ = "file_metadata"
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(500))
    file_size: Mapped[int] = mapped_column(Integer)
    mime_type: Mapped[str] = mapped_column(String(100))

class FileVersion(AuditMixin, Base):
    __tablename__ = "file_versions"
    file_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("file_metadata.id"))
    version_number: Mapped[int] = mapped_column(Integer, default=1)
    file_path: Mapped[str] = mapped_column(String(500))
    __table_args__ = (UniqueConstraint('file_id', 'version_number', name='uq_file_version_num'),)

class ObjectStorage(AuditMixin, Base):
    __tablename__ = "object_storage"
    provider: Mapped[str] = mapped_column(String(50)) # e.g. Local, AWS S3, Azure Blob
    bucket_name: Mapped[str] = mapped_column(String(255))

class StorageQuota(AuditMixin, Base):
    __tablename__ = "storage_quotas"
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True)
    max_bytes: Mapped[float] = mapped_column(Float, default=10737418240.0) # default 10GB
    used_bytes: Mapped[float] = mapped_column(Float, default=0.0)

# -------------------------
# Background Jobs
# -------------------------
class BackgroundJob(AuditMixin, Base):
    __tablename__ = "background_jobs"
    job_type: Mapped[str] = mapped_column(String(100)) # e.g. ResumeParsing, EmailBlast
    status: Mapped[str] = mapped_column(String(30)) # Pending, Running, Completed, Failed
    payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)

class JobQueue(AuditMixin, Base):
    __tablename__ = "job_queues"
    queue_name: Mapped[str] = mapped_column(String(100), unique=True)

class ScheduledJob(AuditMixin, Base):
    __tablename__ = "scheduled_jobs"
    job_name: Mapped[str] = mapped_column(String(150), unique=True)
    cron_expression: Mapped[str] = mapped_column(String(50)) # e.g. "0 0 * * *"
    is_active: Mapped[bool] = mapped_column(default=True)

class SchedulerHistory(AuditMixin, Base):
    __tablename__ = "scheduler_history"
    scheduled_job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scheduled_jobs.id"))
    run_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(30)) # Success, Failure
    error_log: Mapped[str | None] = mapped_column(TEXT, nullable=True)

# -------------------------
# Integration Registry
# -------------------------
class IntegrationRegistry(AuditMixin, Base):
    __tablename__ = "integration_registries"
    integration_name: Mapped[str] = mapped_column(String(150), unique=True)
    status: Mapped[str] = mapped_column(String(30)) # Active, Inactive

class IntegrationConfiguration(AuditMixin, Base):
    __tablename__ = "integration_configurations"
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    integration_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("integration_registries.id"))
    config_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    __table_args__ = (UniqueConstraint('organization_id', 'integration_id', name='uq_org_integration_config'),)

class ApiCredential(AuditMixin, Base):
    __tablename__ = "api_credentials"
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    credential_name: Mapped[str] = mapped_column(String(150))
    credential_value: Mapped[str] = mapped_column(TEXT)

class WebhookRegistry(AuditMixin, Base):
    __tablename__ = "webhook_registries"
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    target_url: Mapped[str] = mapped_column(String(500))

class WebhookLog(AuditMixin, Base):
    __tablename__ = "webhook_logs"
    webhook_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("webhook_registries.id"))
    response_code: Mapped[int] = mapped_column(Integer)
    response_body: Mapped[str | None] = mapped_column(TEXT, nullable=True)

# -------------------------
# Infrastructure Settings
# -------------------------
class EnvironmentVariable(AuditMixin, Base):
    __tablename__ = "environment_variables"
    variable_key: Mapped[str] = mapped_column(String(150), unique=True)
    variable_value: Mapped[str] = mapped_column(TEXT)
