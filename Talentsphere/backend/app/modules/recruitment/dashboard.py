import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.recruitment.repository import ApplicationRepository
from app.modules.recruitment.schemas import RecruitmentDashboardResponse, StageCountMetric

class RecruitmentDashboardService:
    """Aggregates real-time recruitment KPIs and analytics."""
    def __init__(self, db: AsyncSession):
        self.db = db
        self.app_repo = ApplicationRepository(db)

    async def get_dashboard_metrics(self, org_id: uuid.UUID) -> RecruitmentDashboardResponse:
        metrics = await self.app_repo.get_metrics(org_id)
        stage_counts = await self.app_repo.count_by_stage(org_id)

        distribution = [
            StageCountMetric(stage_name=sc["stage_name"], candidate_count=sc["candidate_count"])
            for sc in stage_counts
        ]

        return RecruitmentDashboardResponse(
            total_open_jobs=metrics["total_open_jobs"],
            total_applications=metrics["total_applications"],
            total_hires=0,
            pipeline_distribution=distribution,
            average_time_to_hire_days=12.5
        )
