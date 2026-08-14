from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, update, delete
from sqlalchemy.orm import selectinload
import uuid
from datetime import datetime, timedelta

from app.modules.ai.models import (
    AIAgent, AIAgentVersion, AITool, PromptTemplate,
    KnowledgeDocument, DocumentChunk, AIExecution, HITLState,
    AIWorkflow, WorkflowStep, AIUsage, AIGuardrail
)
from app.modules.ai.enums import ExecutionStatus, AgentStatus


class AgentRepository:
    """Repository for AI agent operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_agent(self, agent_data: dict) -> AIAgent:
        """Create AI agent"""
        agent = AIAgent(**agent_data)
        self.db.add(agent)
        await self.db.commit()
        return agent
    
    async def get_agent_by_id(self, agent_id: uuid.UUID) -> Optional[AIAgent]:
        """Get agent by ID"""
        query = select(AIAgent).where(AIAgent.id == agent_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_agents_by_org(self, org_id: uuid.UUID) -> List[AIAgent]:
        """Get agents by organization"""
        query = select(AIAgent).where(
            or_(
                AIAgent.organization_id == org_id,
                AIAgent.is_global == True
            )
        )
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def create_agent_version(self, version_data: dict) -> AIAgentVersion:
        """Create agent version"""
        version = AIAgentVersion(**version_data)
        self.db.add(version)
        await self.db.commit()
        return version


class ToolRepository:
    """Repository for AI tool operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_tool(self, tool_data: dict) -> AITool:
        """Create AI tool"""
        tool = AITool(**tool_data)
        self.db.add(tool)
        await self.db.commit()
        return tool
    
    async def get_tool_by_name(self, tool_name: str) -> Optional[AITool]:
        """Get tool by name"""
        query = select(AITool).where(AITool.tool_name == tool_name)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_all_tools(self) -> List[AITool]:
        """Get all active tools"""
        query = select(AITool).where(AITool.is_active == True)
        result = await self.db.execute(query)
        return result.scalars().all()


class KnowledgeRepository:
    """Repository for knowledge operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_document(self, document_data: dict) -> KnowledgeDocument:
        """Create knowledge document"""
        document = KnowledgeDocument(**document_data)
        self.db.add(document)
        await self.db.commit()
        return document
    
    async def get_document_by_id(self, doc_id: uuid.UUID) -> Optional[KnowledgeDocument]:
        """Get document by ID"""
        query = select(KnowledgeDocument).where(KnowledgeDocument.id == doc_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_documents_by_org(self, org_id: uuid.UUID) -> List[KnowledgeDocument]:
        """Get documents by organization"""
        query = select(KnowledgeDocument).where(
            or_(
                KnowledgeDocument.organization_id == org_id,
                KnowledgeDocument.is_public == True
            )
        )
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def create_chunk(self, chunk_data: dict) -> DocumentChunk:
        """Create document chunk"""
        chunk = DocumentChunk(**chunk_data)
        self.db.add(chunk)
        await self.db.commit()
        return chunk
    
    async def get_chunks_by_document(self, document_id: uuid.UUID) -> List[DocumentChunk]:
        """Get chunks by document"""
        query = select(DocumentChunk).where(
            DocumentChunk.document_id == document_id
        ).order_by(DocumentChunk.chunk_index)
        result = await self.db.execute(query)
        return result.scalars().all()


class ExecutionRepository:
    """Repository for AI execution operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_execution(self, execution_data: dict) -> AIExecution:
        """Create AI execution"""
        execution = AIExecution(**execution_data)
        self.db.add(execution)
        await self.db.commit()
        return execution
    
    async def get_execution_by_id(self, execution_id: uuid.UUID) -> Optional[AIExecution]:
        """Get execution by ID"""
        query = select(AIExecution).where(AIExecution.id == execution_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_execution_status(
        self, 
        execution_id: uuid.UUID, 
        new_status: str,
        output_data: Optional[dict] = None,
        error_message: Optional[str] = None,
        langsmith_trace_id: Optional[str] = None
    ) -> None:
        """Update execution status"""
        update_data = {"status": new_status}
        
        if new_status == ExecutionStatus.RUNNING:
            update_data["started_at"] = datetime.now()
        elif new_status in [ExecutionStatus.COMPLETED, ExecutionStatus.FAILED, ExecutionStatus.TIMED_OUT]:
            update_data["completed_at"] = datetime.now()
        
        if output_data:
            update_data["output_data"] = output_data
        if error_message:
            update_data["error_message"] = error_message
        if langsmith_trace_id:
            update_data["langsmith_trace_id"] = langsmith_trace_id
        
        query = update(AIExecution).where(
            AIExecution.id == execution_id
        ).values(**update_data)
        await self.db.execute(query)
        await self.db.commit()
    
    async def get_executions_by_org(self, org_id: uuid.UUID, limit: int = 100) -> List[AIExecution]:
        """Get executions by organization"""
        query = select(AIExecution).where(
            AIExecution.organization_id == org_id
        ).order_by(AIExecution.created_at.desc()).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()


class HITLRepository:
    """Repository for HITL operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_hitl_state(self, hitl_data: dict) -> HITLState:
        """Create HITL state"""
        hitl = HITLState(**hitl_data)
        self.db.add(hitl)
        await self.db.commit()
        return hitl
    
    async def get_hitl_by_execution(self, execution_id: uuid.UUID) -> Optional[HITLState]:
        """Get HITL state by execution"""
        query = select(HITLState).where(HITLState.execution_id == execution_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_hitl_decision(
        self, 
        hitl_id: uuid.UUID, 
        decision: str,
        decision_reason: Optional[str] = None,
        response_data: Optional[dict] = None
    ) -> None:
        """Update HITL decision"""
        update_data = {
            "decision": decision,
            "responded_at": datetime.now()
        }
        
        if decision_reason:
            update_data["decision_reason"] = decision_reason
        if response_data:
            update_data["response_data"] = response_data
        
        query = update(HITLState).where(
            HITLState.id == hitl_id
        ).values(**update_data)
        await self.db.execute(query)
        await self.db.commit()


class WorkflowRepository:
    """Repository for workflow operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_workflow(self, workflow_data: dict) -> AIWorkflow:
        """Create workflow"""
        workflow = AIWorkflow(**workflow_data)
        self.db.add(workflow)
        await self.db.commit()
        return workflow
    
    async def get_workflow_by_id(self, workflow_id: uuid.UUID) -> Optional[AIWorkflow]:
        """Get workflow by ID"""
        query = select(AIWorkflow).where(AIWorkflow.id == workflow_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


class UsageRepository:
    """Repository for usage tracking"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_usage_record(self, usage_data: dict) -> AIUsage:
        """Create usage record"""
        usage = AIUsage(**usage_data)
        self.db.add(usage)
        await self.db.commit()
        return usage
    
    async def get_usage_stats(
        self, 
        org_id: uuid.UUID, 
        start_date: datetime,
        end_date: datetime
    ) -> List[AIUsage]:
        """Get usage statistics for organization"""
        query = select(AIUsage).where(
            and_(
                AIUsage.organization_id == org_id,
                AIUsage.execution_date >= start_date,
                AIUsage.execution_date <= end_date
            )
        )
        result = await self.db.execute(query)
        return result.scalars().all()