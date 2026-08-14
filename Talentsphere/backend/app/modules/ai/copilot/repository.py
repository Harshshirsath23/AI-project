import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.modules.ai.copilot.models import (
    CopilotConversation, CopilotMessage, CopilotExecutionContext, 
    CopilotToolCall, CopilotPreference
)

class CopilotRepository:
    """
    Persistence Repository for Copilot conversations and messages.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_conversation(self, org_id: uuid.UUID, user_id: str, conversation_id: Optional[str] = None) -> CopilotConversation:
        if conversation_id:
            try:
                cid = uuid.UUID(conversation_id)
                stmt = select(CopilotConversation).where(
                    CopilotConversation.id == cid,
                    CopilotConversation.organization_id == org_id
                )
                result = await self.db.execute(stmt)
                conv = result.scalar_one_or_none()
                if conv:
                    return conv
            except ValueError:
                pass

        # Create new
        conv = CopilotConversation(
            organization_id=org_id,
            user_id=uuid.UUID(user_id) if isinstance(user_id, str) else user_id,
            title="Recruitment Copilot Session"
        )
        self.db.add(conv)
        await self.db.commit()
        await self.db.refresh(conv)
        return conv

    async def add_message(
        self,
        conversation_id: uuid.UUID,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> CopilotMessage:
        msg = CopilotMessage(
            conversation_id=conversation_id,
            role=role,
            content=content,
            meta_data=metadata or {}
        )
        self.db.add(msg)
        await self.db.commit()
        await self.db.refresh(msg)
        return msg

    async def get_messages(self, conversation_id: uuid.UUID) -> List[CopilotMessage]:
        stmt = select(CopilotMessage).where(
            CopilotMessage.conversation_id == conversation_id
        ).order_by(CopilotMessage.created_at.asc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def list_conversations(self, org_id: uuid.UUID, user_id: str) -> List[CopilotConversation]:
        uid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
        stmt = select(CopilotConversation).where(
            CopilotConversation.organization_id == org_id,
            CopilotConversation.user_id == uid
        ).order_by(CopilotConversation.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_execution_context(
        self, 
        conversation_id: uuid.UUID, 
        execution_id: str
    ) -> CopilotExecutionContext:
        ctx = CopilotExecutionContext(
            conversation_id=conversation_id,
            execution_id=execution_id,
            status="running"
        )
        self.db.add(ctx)
        await self.db.commit()
        await self.db.refresh(ctx)
        return ctx
    
    async def update_execution_context(
        self, 
        execution_id: str,
        status: str,
        intent: Optional[str] = None,
        intent_confidence: Optional[float] = None,
        final_response: Optional[Dict[str, Any]] = None
    ):
        stmt = select(CopilotExecutionContext).where(CopilotExecutionContext.execution_id == execution_id)
        result = await self.db.execute(stmt)
        ctx = result.scalar_one_or_none()
        if ctx:
            ctx.status = status
            if intent:
                ctx.intent = intent
            if intent_confidence is not None:
                ctx.intent_confidence = intent_confidence
            if final_response is not None:
                ctx.final_response = final_response
            await self.db.commit()
