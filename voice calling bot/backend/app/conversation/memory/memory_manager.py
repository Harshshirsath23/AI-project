from typing import Optional, Dict, Any, List
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.models.conversation import ConversationMemory, ConversationTurn

logger = get_logger(__name__)


class MemoryManager:
    """
    Manager for conversation memory.
    
    This manager handles two memory layers:
    - Short-Term Memory: Conversation-only memory (turns, context)
    - Long-Term Memory: Persistent customer preferences and summaries
    
    The long-term memory architecture is prepared for future implementation
    of customer preference persistence and conversation summarization.
    """

    def __init__(self):
        """Initialize the memory manager."""
        self._short_term_memory: Dict[str, List[Dict[str, Any]]] = {}

    async def add_turn_to_memory(
        self,
        session_id: str,
        turn: ConversationTurn,
        db: Optional[AsyncSession] = None,
    ) -> None:
        """
        Add a conversation turn to short-term memory.
        
        Args:
            session_id: Session ID
            turn: Conversation turn to add
            db: Database session
        """
        if session_id not in self._short_term_memory:
            self._short_term_memory[session_id] = []
        
        turn_data = {
            "turn_number": turn.turn_number,
            "turn_type": turn.turn_type,
            "content": turn.content,
            "content_type": turn.content_type,
            "state": turn.state,
            "tool_name": turn.tool_name,
            "tool_result": turn.tool_result,
            "start_time": turn.start_time,
            "end_time": turn.end_time,
            "duration": turn.duration,
            "metadata": turn.metadata,
        }
        
        self._short_term_memory[session_id].append(turn_data)
        
        logger.debug("Turn added to short-term memory", session_id=session_id, turn_number=turn.turn_number)

    async def get_conversation_history(
        self,
        session_id: str,
        limit: Optional[int] = None,
        db: AsyncSession = None,
    ) -> List[Dict[str, Any]]:
        """
        Get conversation history from short-term memory.
        
        Args:
            session_id: Session ID
            limit: Optional limit on number of turns
            db: Database session
        
        Returns:
            List of conversation turns
        """
        # Check memory first
        if session_id in self._short_term_memory:
            history = self._short_term_memory[session_id]
            if limit:
                return history[-limit:]
            return history.copy()
        
        # Check database
        if db:
            result = await db.execute(
                select(ConversationTurn)
                .where(ConversationTurn.session_id == session_id)
                .order_by(ConversationTurn.turn_number)
            )
            turns = result.scalars().all()
            
            history = [
                {
                    "turn_number": turn.turn_number,
                    "turn_type": turn.turn_type,
                    "content": turn.content,
                    "content_type": turn.content_type,
                    "state": turn.state,
                    "tool_name": turn.tool_name,
                    "tool_result": turn.tool_result,
                    "start_time": turn.start_time,
                    "end_time": turn.end_time,
                    "duration": turn.duration,
                    "metadata": turn.metadata,
                }
                for turn in turns
            ]
            
            # Load into memory
            self._short_term_memory[session_id] = history
            
            if limit:
                return history[-limit:]
            return history
        
        return []

    async def get_recent_turns(
        self,
        session_id: str,
        count: int = 5,
        db: AsyncSession = None,
    ) -> List[Dict[str, Any]]:
        """
        Get the most recent conversation turns.
        
        Args:
            session_id: Session ID
            count: Number of recent turns to retrieve
            db: Database session
        
        Returns:
            List of recent conversation turns
        """
        history = await self.get_conversation_history(session_id, db=db)
        return history[-count:] if history else []

    async def clear_short_term_memory(
        self,
        session_id: str,
    ) -> None:
        """
        Clear short-term memory for a session.
        
        Args:
            session_id: Session ID
        """
        if session_id in self._short_term_memory:
            del self._short_term_memory[session_id]
            logger.debug("Short-term memory cleared", session_id=session_id)

    async def get_long_term_memory(
        self,
        organization_id: str,
        lead_id: str,
        db: AsyncSession,
    ) -> Optional[ConversationMemory]:
        """
        Get long-term memory for a customer.
        
        Args:
            organization_id: Organization ID
            lead_id: Lead ID
            db: Database session
        
        Returns:
            Conversation memory or None if not found
        """
        result = await db.execute(
            select(ConversationMemory)
            .where(ConversationMemory.organization_id == organization_id)
            .where(ConversationMemory.lead_id == lead_id)
        )
        return result.scalar_one_or_none()

    async def create_long_term_memory(
        self,
        organization_id: str,
        lead_id: str,
        db: AsyncSession,
    ) -> ConversationMemory:
        """
        Create long-term memory for a customer.
        
        Args:
            organization_id: Organization ID
            lead_id: Lead ID
            db: Database session
        
        Returns:
            Created conversation memory
        """
        memory = ConversationMemory(
            organization_id=organization_id,
            lead_id=lead_id,
            preferences={},
            last_conversation_summary=None,
            conversation_count=0,
            key_topics=[],
            sentiment_history=[],
            last_conversation_date=None,
            last_agent_id=None,
        )
        
        db.add(memory)
        await db.commit()
        await db.refresh(memory)
        
        logger.info("Long-term memory created", organization_id=organization_id, lead_id=lead_id)
        
        return memory

    async def update_preferences(
        self,
        organization_id: str,
        lead_id: str,
        preferences: Dict[str, Any],
        db: AsyncSession,
    ) -> Optional[ConversationMemory]:
        """
        Update customer preferences in long-term memory.
        
        Args:
            organization_id: Organization ID
            lead_id: Lead ID
            preferences: Preferences dictionary
            db: Database session
        
        Returns:
            Updated memory or None if not found
        """
        memory = await self.get_long_term_memory(organization_id, lead_id, db)
        
        if not memory:
            memory = await self.create_long_term_memory(organization_id, lead_id, db)
        
        memory.preferences.update(preferences)
        
        await db.commit()
        await db.refresh(memory)
        
        logger.debug("Preferences updated", organization_id=organization_id, lead_id=lead_id)
        
        return memory

    async def get_preferences(
        self,
        organization_id: str,
        lead_id: str,
        db: AsyncSession,
    ) -> Dict[str, Any]:
        """
        Get customer preferences from long-term memory.
        
        Args:
            organization_id: Organization ID
            lead_id: Lead ID
            db: Database session
        
        Returns:
            Preferences dictionary
        """
        memory = await self.get_long_term_memory(organization_id, lead_id, db)
        
        if not memory:
            return {}
        
        return memory.preferences.copy()

    async def update_conversation_summary(
        self,
        organization_id: str,
        lead_id: str,
        summary: str,
        agent_id: Optional[str] = None,
        db: AsyncSession = None,
    ) -> Optional[ConversationMemory]:
        """
        Update the conversation summary in long-term memory.
        
        Args:
            organization_id: Organization ID
            lead_id: Lead ID
            summary: Conversation summary
            agent_id: Optional agent ID
            db: Database session
        
        Returns:
            Updated memory or None if not found
        """
        memory = await self.get_long_term_memory(organization_id, lead_id, db)
        
        if not memory:
            memory = await self.create_long_term_memory(organization_id, lead_id, db)
        
        memory.last_conversation_summary = summary
        memory.last_conversation_date = datetime.utcnow()
        memory.conversation_count += 1
        
        if agent_id:
            memory.last_agent_id = agent_id
        
        if db:
            await db.commit()
            await db.refresh(memory)
        
        logger.debug("Conversation summary updated", organization_id=organization_id, lead_id=lead_id)
        
        return memory

    async def add_key_topic(
        self,
        organization_id: str,
        lead_id: str,
        topic: str,
        db: AsyncSession,
    ) -> Optional[ConversationMemory]:
        """
        Add a key topic to long-term memory.
        
        Args:
            organization_id: Organization ID
            lead_id: Lead ID
            topic: Topic to add
            db: Database session
        
        Returns:
            Updated memory or None if not found
        """
        memory = await self.get_long_term_memory(organization_id, lead_id, db)
        
        if not memory:
            memory = await self.create_long_term_memory(organization_id, lead_id, db)
        
        if topic not in memory.key_topics:
            memory.key_topics.append(topic)
        
        await db.commit()
        await db.refresh(memory)
        
        logger.debug("Key topic added", organization_id=organization_id, lead_id=lead_id, topic=topic)
        
        return memory

    async def add_sentiment_record(
        self,
        organization_id: str,
        lead_id: str,
        sentiment: str,
        confidence: float,
        db: AsyncSession,
    ) -> Optional[ConversationMemory]:
        """
        Add a sentiment record to long-term memory.
        
        Args:
            organization_id: Organization ID
            lead_id: Lead ID
            sentiment: Sentiment value (positive, negative, neutral)
            confidence: Confidence score
            db: Database session
        
        Returns:
            Updated memory or None if not found
        """
        memory = await self.get_long_term_memory(organization_id, lead_id, db)
        
        if not memory:
            memory = await self.create_long_term_memory(organization_id, lead_id, db)
        
        sentiment_record = {
            "sentiment": sentiment,
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        memory.sentiment_history.append(sentiment_record)
        
        # Keep only last 50 sentiment records
        if len(memory.sentiment_history) > 50:
            memory.sentiment_history = memory.sentiment_history[-50:]
        
        await db.commit()
        await db.refresh(memory)
        
        logger.debug("Sentiment record added", organization_id=organization_id, lead_id=lead_id, sentiment=sentiment)
        
        return memory

    async def get_sentiment_history(
        self,
        organization_id: str,
        lead_id: str,
        limit: int = 10,
        db: AsyncSession = None,
    ) -> List[Dict[str, Any]]:
        """
        Get sentiment history from long-term memory.
        
        Args:
            organization_id: Organization ID
            lead_id: Lead ID
            limit: Number of records to retrieve
            db: Database session
        
        Returns:
            List of sentiment records
        """
        memory = await self.get_long_term_memory(organization_id, lead_id, db)
        
        if not memory:
            return []
        
        return memory.sentiment_history[-limit:] if memory.sentiment_history else []

    def remove_from_memory(self, session_id: str) -> None:
        """
        Remove session from short-term memory.
        
        Args:
            session_id: Session ID
        """
        if session_id in self._short_term_memory:
            del self._short_term_memory[session_id]
            logger.debug("Session removed from memory", session_id=session_id)


# Global memory manager instance
_memory_manager: Optional[MemoryManager] = None


def get_memory_manager() -> MemoryManager:
    """
    Get the global memory manager instance.
    
    Returns:
        MemoryManager: The global memory manager
    """
    global _memory_manager
    if _memory_manager is None:
        _memory_manager = MemoryManager()
    return _memory_manager
