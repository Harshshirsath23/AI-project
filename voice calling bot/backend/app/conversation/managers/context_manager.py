from typing import Optional, Dict, Any, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.models.conversation import ConversationContext

logger = get_logger(__name__)


class ContextManager:
    """
    Manager for conversation context.
    
    This manager maintains the context for a conversation including:
    - Conversation history
    - Temporary variables
    - Customer information
    - Agent information
    - Campaign information
    - Session metadata
    - Future RAG context
    - Future NLP context
    - Future tool outputs
    
    The Context Manager exposes a clean API for other modules to access
    and manipulate conversation context.
    """

    def __init__(self):
        """Initialize the context manager."""
        self._memory_contexts: Dict[str, Dict[str, Any]] = {}

    async def get_context(
        self,
        session_id: str,
        db: AsyncSession,
    ) -> Optional[ConversationContext]:
        """
        Get the context for a session.
        
        Args:
            session_id: Session ID
            db: Database session
        
        Returns:
            Conversation context or None if not found
        """
        # Check memory first
        if session_id in self._memory_contexts:
            return self._memory_contexts[session_id]
        
        # Check database
        result = await db.execute(
            select(ConversationContext)
            .where(ConversationContext.session_id == session_id)
        )
        context = result.scalar_one_or_none()
        
        if context:
            # Load into memory
            self._memory_contexts[session_id] = context
        
        return context

    async def create_context(
        self,
        session_id: str,
        db: AsyncSession,
    ) -> ConversationContext:
        """
        Create a new context for a session.
        
        Args:
            session_id: Session ID
            db: Database session
        
        Returns:
            Created conversation context
        """
        context = ConversationContext(
            session_id=session_id,
            variables={},
            customer_info={},
            agent_info={},
            campaign_info={},
            rag_context={},
            nlp_context={},
            tool_outputs={},
        )
        
        db.add(context)
        await db.commit()
        await db.refresh(context)
        
        # Store in memory
        self._memory_contexts[session_id] = context
        
        logger.info("Context created", session_id=session_id)
        
        return context

    async def update_context(
        self,
        session_id: str,
        variables: Optional[Dict[str, Any]] = None,
        customer_info: Optional[Dict[str, Any]] = None,
        agent_info: Optional[Dict[str, Any]] = None,
        campaign_info: Optional[Dict[str, Any]] = None,
        rag_context: Optional[Dict[str, Any]] = None,
        nlp_context: Optional[Dict[str, Any]] = None,
        tool_outputs: Optional[Dict[str, Any]] = None,
        db: Optional[AsyncSession] = None,
    ) -> Optional[ConversationContext]:
        """
        Update the context for a session.
        
        Args:
            session_id: Session ID
            variables: Session variables to update
            customer_info: Customer information to update
            agent_info: Agent information to update
            campaign_info: Campaign information to update
            rag_context: RAG context to update
            nlp_context: NLP context to update
            tool_outputs: Tool outputs to update
            db: Database session
        
        Returns:
            Updated context or None if not found
        """
        context = await self.get_context(session_id, db)
        
        if not context:
            logger.warning("Context not found for update", session_id=session_id)
            return None
        
        # Update fields
        if variables is not None:
            context.variables.update(variables)
        
        if customer_info is not None:
            context.customer_info = {**(context.customer_info or {}), **customer_info}
        
        if agent_info is not None:
            context.agent_info = {**(context.agent_info or {}), **agent_info}
        
        if campaign_info is not None:
            context.campaign_info = {**(context.campaign_info or {}), **campaign_info}
        
        if rag_context is not None:
            context.rag_context = {**(context.rag_context or {}), **rag_context}
        
        if nlp_context is not None:
            context.nlp_context = {**(context.nlp_context or {}), **nlp_context}
        
        if tool_outputs is not None:
            context.tool_outputs = {**(context.tool_outputs or {}), **tool_outputs}
        
        if db:
            await db.commit()
            await db.refresh(context)
        
        logger.debug("Context updated", session_id=session_id)
        
        return context

    async def set_variable(
        self,
        session_id: str,
        key: str,
        value: Any,
        db: Optional[AsyncSession] = None,
    ) -> bool:
        """
        Set a variable in the context.
        
        Args:
            session_id: Session ID
            key: Variable key
            value: Variable value
            db: Database session
        
        Returns:
            True if variable was set successfully
        """
        context = await self.get_context(session_id, db)
        
        if not context:
            return False
        
        context.variables[key] = value
        
        if db:
            await db.commit()
        
        logger.debug("Variable set", session_id=session_id, key=key)
        
        return True

    async def get_variable(
        self,
        session_id: str,
        key: str,
        default: Any = None,
        db: AsyncSession = None,
    ) -> Any:
        """
        Get a variable from the context.
        
        Args:
            session_id: Session ID
            key: Variable key
            default: Default value if key not found
            db: Database session
        
        Returns:
            Variable value or default
        """
        context = await self.get_context(session_id, db)
        
        if not context:
            return default
        
        return context.variables.get(key, default)

    async def delete_variable(
        self,
        session_id: str,
        key: str,
        db: Optional[AsyncSession] = None,
    ) -> bool:
        """
        Delete a variable from the context.
        
        Args:
            session_id: Session ID
            key: Variable key
            db: Database session
        
        Returns:
            True if variable was deleted successfully
        """
        context = await self.get_context(session_id, db)
        
        if not context or key not in context.variables:
            return False
        
        del context.variables[key]
        
        if db:
            await db.commit()
        
        logger.debug("Variable deleted", session_id=session_id, key=key)
        
        return True

    async def get_all_variables(
        self,
        session_id: str,
        db: AsyncSession = None,
    ) -> Dict[str, Any]:
        """
        Get all variables from the context.
        
        Args:
            session_id: Session ID
            db: Database session
        
        Returns:
            Dictionary of all variables
        """
        context = await self.get_context(session_id, db)
        
        if not context:
            return {}
        
        return context.variables.copy()

    async def set_customer_info(
        self,
        session_id: str,
        customer_info: Dict[str, Any],
        db: Optional[AsyncSession] = None,
    ) -> bool:
        """
        Set customer information in the context.
        
        Args:
            session_id: Session ID
            customer_info: Customer information dictionary
            db: Database session
        
        Returns:
            True if customer info was set successfully
        """
        context = await self.get_context(session_id, db)
        
        if not context:
            return False
        
        context.customer_info = customer_info
        
        if db:
            await db.commit()
        
        logger.debug("Customer info set", session_id=session_id)
        
        return True

    async def get_customer_info(
        self,
        session_id: str,
        db: AsyncSession = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Get customer information from the context.
        
        Args:
            session_id: Session ID
            db: Database session
        
        Returns:
            Customer information dictionary or None
        """
        context = await self.get_context(session_id, db)
        
        if not context:
            return None
        
        return context.customer_info

    async def set_agent_info(
        self,
        session_id: str,
        agent_info: Dict[str, Any],
        db: Optional[AsyncSession] = None,
    ) -> bool:
        """
        Set agent information in the context.
        
        Args:
            session_id: Session ID
            agent_info: Agent information dictionary
            db: Database session
        
        Returns:
            True if agent info was set successfully
        """
        context = await self.get_context(session_id, db)
        
        if not context:
            return False
        
        context.agent_info = agent_info
        
        if db:
            await db.commit()
        
        logger.debug("Agent info set", session_id=session_id)
        
        return True

    async def get_agent_info(
        self,
        session_id: str,
        db: AsyncSession = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Get agent information from the context.
        
        Args:
            session_id: Session ID
            db: Database session
        
        Returns:
            Agent information dictionary or None
        """
        context = await self.get_context(session_id, db)
        
        if not context:
            return None
        
        return context.agent_info

    async def set_campaign_info(
        self,
        session_id: str,
        campaign_info: Dict[str, Any],
        db: Optional[AsyncSession] = None,
    ) -> bool:
        """
        Set campaign information in the context.
        
        Args:
            session_id: Session ID
            campaign_info: Campaign information dictionary
            db: Database session
        
        Returns:
            True if campaign info was set successfully
        """
        context = await self.get_context(session_id, db)
        
        if not context:
            return False
        
        context.campaign_info = campaign_info
        
        if db:
            await db.commit()
        
        logger.debug("Campaign info set", session_id=session_id)
        
        return True

    async def get_campaign_info(
        self,
        session_id: str,
        db: AsyncSession = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Get campaign information from the context.
        
        Args:
            session_id: Session ID
            db: Database session
        
        Returns:
            Campaign information dictionary or None
        """
        context = await self.get_context(session_id, db)
        
        if not context:
            return None
        
        return context.campaign_info

    async def set_rag_context(
        self,
        session_id: str,
        rag_context: Dict[str, Any],
        db: Optional[AsyncSession] = None,
    ) -> bool:
        """
        Set RAG context in the context.
        
        Args:
            session_id: Session ID
            rag_context: RAG context dictionary
            db: Database session
        
        Returns:
            True if RAG context was set successfully
        """
        context = await self.get_context(session_id, db)
        
        if not context:
            return False
        
        context.rag_context = rag_context
        
        if db:
            await db.commit()
        
        logger.debug("RAG context set", session_id=session_id)
        
        return True

    async def get_rag_context(
        self,
        session_id: str,
        db: AsyncSession = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Get RAG context from the context.
        
        Args:
            session_id: Session ID
            db: Database session
        
        Returns:
            RAG context dictionary or None
        """
        context = await self.get_context(session_id, db)
        
        if not context:
            return None
        
        return context.rag_context

    async def set_nlp_context(
        self,
        session_id: str,
        nlp_context: Dict[str, Any],
        db: Optional[AsyncSession] = None,
    ) -> bool:
        """
        Set NLP context in the context.
        
        Args:
            session_id: Session ID
            nlp_context: NLP context dictionary
            db: Database session
        
        Returns:
            True if NLP context was set successfully
        """
        context = await self.get_context(session_id, db)
        
        if not context:
            return False
        
        context.nlp_context = nlp_context
        
        if db:
            await db.commit()
        
        logger.debug("NLP context set", session_id=session_id)
        
        return True

    async def get_nlp_context(
        self,
        session_id: str,
        db: AsyncSession = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Get NLP context from the context.
        
        Args:
            session_id: Session ID
            db: Database session
        
        Returns:
            NLP context dictionary or None
        """
        context = await self.get_context(session_id, db)
        
        if not context:
            return None
        
        return context.nlp_context

    async def record_tool_output(
        self,
        session_id: str,
        tool_name: str,
        output: Any,
        db: Optional[AsyncSession] = None,
    ) -> bool:
        """
        Record a tool output in the context.
        
        Args:
            session_id: Session ID
            tool_name: Tool name
            output: Tool output
            db: Database session
        
        Returns:
            True if tool output was recorded successfully
        """
        context = await self.get_context(session_id, db)
        
        if not context:
            return False
        
        context.tool_outputs[tool_name] = output
        
        if db:
            await db.commit()
        
        logger.debug("Tool output recorded", session_id=session_id, tool_name=tool_name)
        
        return True

    async def get_tool_output(
        self,
        session_id: str,
        tool_name: str,
        default: Any = None,
        db: AsyncSession = None,
    ) -> Any:
        """
        Get a tool output from the context.
        
        Args:
            session_id: Session ID
            tool_name: Tool name
            default: Default value if not found
            db: Database session
        
        Returns:
            Tool output or default
        """
        context = await self.get_context(session_id, db)
        
        if not context:
            return default
        
        return context.tool_outputs.get(tool_name, default)

    async def clear_context(
        self,
        session_id: str,
        db: Optional[AsyncSession] = None,
    ) -> bool:
        """
        Clear all context data for a session.
        
        Args:
            session_id: Session ID
            db: Database session
        
        Returns:
            True if context was cleared successfully
        """
        context = await self.get_context(session_id, db)
        
        if not context:
            return False
        
        context.variables.clear()
        context.customer_info = {}
        context.agent_info = {}
        context.campaign_info = {}
        context.rag_context = {}
        context.nlp_context = {}
        context.tool_outputs.clear()
        
        if db:
            await db.commit()
        
        logger.info("Context cleared", session_id=session_id)
        
        return True

    def remove_from_memory(self, session_id: str) -> None:
        """
        Remove context from memory cache.
        
        Args:
            session_id: Session ID
        """
        if session_id in self._memory_contexts:
            del self._memory_contexts[session_id]
            logger.debug("Context removed from memory", session_id=session_id)


# Global context manager instance
_context_manager: Optional[ContextManager] = None


def get_context_manager() -> ContextManager:
    """
    Get the global context manager instance.
    
    Returns:
        ContextManager: The global context manager
    """
    global _context_manager
    if _context_manager is None:
        _context_manager = ContextManager()
    return _context_manager
