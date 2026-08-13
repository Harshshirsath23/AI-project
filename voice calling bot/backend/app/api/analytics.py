from datetime import datetime, timedelta, UTC
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.connection import get_db
from app.models.call import Call
from app.models.campaign import Campaign
from app.models.agent import Agent
from app.models.lead import Lead
from app.models.audit_log import AuditLog

router = APIRouter()


@router.get("/overview")
async def get_analytics_overview(db: Session = Depends(get_db)):
    """Get dashboard analytics overview data generated dynamically from the database."""
    total_calls = db.query(Call).count()
    completed_calls = db.query(Call).filter(Call.status == "completed").count()
    active_campaigns = db.query(Campaign).filter(Campaign.status == "running", Campaign.deleted_at.is_(None)).count()
    total_agents = db.query(Agent).filter(Agent.deleted_at.is_(None)).count()
    total_leads = db.query(Lead).filter(Lead.deleted_at.is_(None)).count()

    success_rate = (completed_calls / total_calls * 100) if total_calls > 0 else 0.0

    # Calculate average call duration
    try:
        avg_duration_res = db.query(func.avg(Call.duration_seconds)).scalar()
        avg_duration_seconds = int(avg_duration_res) if avg_duration_res else 0
    except Exception:
        avg_duration_seconds = 0

    # Generate real daily call volume breakdown for past 7 days
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    now = datetime.now(UTC)
    chart_data = []

    for i in range(6, -1, -1):
        day_date = (now - timedelta(days=i)).date()
        day_name = days[day_date.weekday()]

        day_total = db.query(Call).filter(func.date(Call.created_at) == day_date).count()
        day_success = db.query(Call).filter(
            func.date(Call.created_at) == day_date,
            Call.status == "completed"
        ).count()

        chart_data.append({
            "name": day_name,
            "calls": day_total,
            "success": day_success,
        })

    # Fetch recent audit logs or recent call activities
    recent_activity = []
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(5).all()

    for log in logs:
        time_diff = now - log.created_at.replace(tzinfo=UTC) if log.created_at.tzinfo is None else now - log.created_at
        mins = int(time_diff.total_seconds() // 60)
        time_str = "Just now" if mins < 1 else f"{mins} mins ago"

        recent_activity.append({
            "id": str(log.id),
            "message": f"{log.action.capitalize()} {log.resource_type}: {log.resource_id or ''}".strip(),
            "time": time_str,
            "status": "success" if log.status == "success" else "warning",
        })

    # Fallback to recent calls if audit log is empty
    if not recent_activity:
        calls = db.query(Call).order_by(Call.created_at.desc()).limit(5).all()
        for c in calls:
            time_diff = now - c.created_at.replace(tzinfo=UTC) if c.created_at.tzinfo is None else now - c.created_at
            mins = int(time_diff.total_seconds() // 60)
            time_str = "Just now" if mins < 1 else f"{mins} mins ago"

            recent_activity.append({
                "id": str(c.id),
                "message": f"Call to {c.to_number or 'Target'} ({c.status})",
                "time": time_str,
                "status": "success" if c.status == "completed" else "info",
            })

    # Calculate real sentiment distribution from PostgreSQL
    pos_count = db.query(Call).filter(Call.sentiment.in_(["positive", "interested"])).count()
    neu_count = db.query(Call).filter((Call.sentiment == "neutral") | (Call.sentiment.is_(None))).count()
    neg_count = db.query(Call).filter(Call.sentiment.in_(["negative", "not-interested"])).count()
    total_analyzed = total_calls or 1

    pos_pct = round((pos_count / total_analyzed) * 100, 1)
    neu_pct = round((neu_count / total_analyzed) * 100, 1)
    neg_pct = round((neg_count / total_analyzed) * 100, 1)

    return {
        "metrics": {
            "total_calls": total_calls,
            "completed_calls": completed_calls,
            "success_rate": round(success_rate, 1),
            "active_campaigns": active_campaigns,
            "total_agents": total_agents,
            "total_leads": total_leads,
            "avg_duration_seconds": avg_duration_seconds,
        },
        "chart_data": chart_data,
        "sentiment_breakdown": {
            "positive": pos_pct,
            "neutral": neu_pct,
            "negative": neg_pct,
        },
        "recent_activity": recent_activity,
    }
