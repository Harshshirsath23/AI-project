from sqlalchemy import Column, String, Integer, ForeignKey, Date, Float, TEXT, Boolean, DateTime, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.models import Base, AuditMixin

# -------------------------
# Dashboard Definitions
# -------------------------
class Dashboard(AuditMixin, Base):
    __tablename__ = "dashboards"
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # references organizations
    dashboard_name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)

class DashboardLayout(AuditMixin, Base):
    __tablename__ = "dashboard_layouts"
    dashboard_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("dashboards.id"), unique=True)
    layout_json: Mapped[dict | None] = mapped_column(JSON, nullable=True) # Grid layout properties

class DashboardWidget(AuditMixin, Base):
    __tablename__ = "dashboard_widgets"
    dashboard_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("dashboards.id"))
    widget_name: Mapped[str] = mapped_column(String(150))
    widget_type: Mapped[str] = mapped_column(String(50)) # BarChart, PieChart, MetricCard

class WidgetConfiguration(AuditMixin, Base):
    __tablename__ = "widget_configurations"
    widget_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("dashboard_widgets.id"), unique=True)
    config_json: Mapped[dict | None] = mapped_column(JSON, nullable=True) # visual preferences

class WidgetDataQuery(AuditMixin, Base):
    __tablename__ = "widget_data_queries"
    widget_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("dashboard_widgets.id"), unique=True)
    query_text: Mapped[str] = mapped_column(TEXT) # SQL query or JSON aggregation rules

# -------------------------
# Report Definitions
# -------------------------
class ReportDefinition(AuditMixin, Base):
    __tablename__ = "report_definitions"
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    report_name: Mapped[str] = mapped_column(String(150))
    query_template: Mapped[str] = mapped_column(TEXT) # SQL or aggregation template with place holders

class ReportParameter(AuditMixin, Base):
    __tablename__ = "report_parameters"
    report_definition_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("report_definitions.id"))
    parameter_name: Mapped[str] = mapped_column(String(100)) # e.g. start_date, end_date
    parameter_type: Mapped[str] = mapped_column(String(50)) # Date, Integer, String

class ScheduledReport(AuditMixin, Base):
    __tablename__ = "scheduled_reports"
    report_definition_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("report_definitions.id"))
    cron_expression: Mapped[str] = mapped_column(String(50)) # e.g. "0 9 * * 1" (Every Monday at 9AM)
    recipient_emails: Mapped[str] = mapped_column(TEXT) # Comma separated list of emails
    is_active: Mapped[bool] = mapped_column(default=True)

class ReportExecutionLog(AuditMixin, Base):
    __tablename__ = "report_execution_logs"
    scheduled_report_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scheduled_reports.id"))
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(30)) # Success, Failure
    file_path: Mapped[str | None] = mapped_column(String(500), nullable=True) # Link to exported PDF/Excel
