"""
PostgreSQL LangGraph State Checkpointer Implementation

This module provides a PostgreSQL-backed checkpointer for LangGraph workflows,
enabling state persistence, recovery, and HITL (Human-in-the-Loop) pause/resume functionality.
"""

import uuid
import json
import structlog
from typing import Dict, Any, Optional, TypedDict, Iterator
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from langgraph.checkpoint import BaseCheckpointSaver, Checkpoint
from langgraph.checkpoint.id import uuid6
from app.modules.ai.models import AIExecution
from app.core.observability import trace_span

logger = structlog.get_logger(__name__)


class PostgresCheckpointSaver(BaseCheckpointSaver):
    """
    PostgreSQL-backed LangGraph CheckpointSaver implementation.
    
    Stores workflow state in the AIExecution table, enabling:
    - Workflow pause/resume for HITL gates
    - State recovery after failures
    - Execution history tracking
    - Multi-tenant state isolation
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def put(
        self,
        config: Dict[str, Any],
        checkpoint: Checkpoint,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Save checkpoint to PostgreSQL.
        
        Args:
            config: LangGraph configuration dict containing thread_id and checkpoint_id
            checkpoint: The checkpoint state to persist
            metadata: Optional metadata about the checkpoint
        """
        thread_id = config.get("thread_id")
        checkpoint_id = config.get("checkpoint_id") or str(uuid6())
        
        try:
            async with trace_span(
                name="PostgresCheckpointSaver.put",
                inputs={"thread_id": thread_id, "checkpoint_id": checkpoint_id}
            ) as span:
                # Check if execution exists
                execution = await self.db.execute(
                    select(AIExecution).where(
                        AIExecution.execution_id == thread_id
                    )
                )
                execution_record = execution.scalar_one_or_none()
                
                # Serialize checkpoint state
                checkpoint_data = self._serialize_checkpoint(checkpoint)
                
                if execution_record:
                    # Update existing execution
                    await self.db.execute(
                        update(AIExecution)
                        .where(AIExecution.execution_id == thread_id)
                        .values(
                            output_data=checkpoint_data,
                            status=checkpoint.get("status", "RUNNING"),
                            updated_at=datetime.utcnow()
                        )
                    )
                    logger.debug(
                        "Updated checkpoint in PostgreSQL",
                        execution_id=thread_id,
                        checkpoint_id=checkpoint_id
                    )
                else:
                    # This shouldn't happen in normal flow as execution is created in runtime
                    logger.warning(
                        "Attempted to save checkpoint for non-existent execution",
                        execution_id=thread_id
                    )
                
                await self.db.commit()
                span.end(outputs={"checkpoint_saved": True})
                
        except Exception as exc:
            logger.error(
                "Failed to save checkpoint to PostgreSQL",
                execution_id=thread_id,
                error=str(exc)
            )
            await self.db.rollback()
            raise

    async def get(self, config: Dict[str, Any]) -> Optional[Checkpoint]:
        """
        Retrieve checkpoint from PostgreSQL.
        
        Args:
            config: LangGraph configuration dict containing thread_id
            
        Returns:
            Checkpoint dict if found, None otherwise
        """
        thread_id = config.get("thread_id")
        
        try:
            async with trace_span(
                name="PostgresCheckpointSaver.get",
                inputs={"thread_id": thread_id}
            ) as span:
                execution = await self.db.execute(
                    select(AIExecution).where(
                        AIExecution.execution_id == thread_id
                    )
                )
                execution_record = execution.scalar_one_or_none()
                
                if not execution_record:
                    logger.debug("No checkpoint found", execution_id=thread_id)
                    span.end(outputs={"checkpoint_found": False})
                    return None
                
                checkpoint = self._deserialize_checkpoint(execution_record.output_data)
                
                logger.debug(
                    "Retrieved checkpoint from PostgreSQL",
                    execution_id=thread_id,
                    status=execution_record.status
                )
                
                span.end(outputs={"checkpoint_found": True, "status": execution_record.status})
                return checkpoint
                
        except Exception as exc:
            logger.error(
                "Failed to retrieve checkpoint from PostgreSQL",
                execution_id=thread_id,
                error=str(exc)
            )
            raise

    async def list(
        self,
        config: Optional[Dict[str, Any]] = None,
        before: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Iterator[Checkpoint]:
        """
        List checkpoints from PostgreSQL.
        
        Args:
            config: Optional configuration filter
            before: Optional checkpoint ID to list before
            limit: Optional limit on number of checkpoints
            
        Returns:
            Iterator of checkpoint dicts
        """
        try:
            query = select(AIExecution)
            
            if config and config.get("thread_id"):
                query = query.where(AIExecution.execution_id == config["thread_id"])
            
            if before:
                query = query.where(AIExecution.created_at < before)
            
            if limit:
                query = query.limit(limit)
            
            query = query.order_by(AIExecution.created_at.desc())
            
            result = await self.db.execute(query)
            executions = result.scalars().all()
            
            for execution in executions:
                if execution.output_data:
                    yield self._deserialize_checkpoint(execution.output_data)
                    
        except Exception as exc:
            logger.error("Failed to list checkpoints", error=str(exc))
            raise

    async def delete(self, config: Dict[str, Any]) -> None:
        """
        Delete checkpoint from PostgreSQL.
        
        Args:
            config: LangGraph configuration dict containing thread_id
        """
        thread_id = config.get("thread_id")
        
        try:
            async with trace_span(
                name="PostgresCheckpointSaver.delete",
                inputs={"thread_id": thread_id}
            ) as span:
                await self.db.execute(
                    delete(AIExecution).where(
                        AIExecution.execution_id == thread_id
                    )
                )
                await self.db.commit()
                
                logger.debug("Deleted checkpoint", execution_id=thread_id)
                span.end(outputs={"checkpoint_deleted": True})
                
        except Exception as exc:
            logger.error(
                "Failed to delete checkpoint",
                execution_id=thread_id,
                error=str(exc)
            )
            await self.db.rollback()
            raise

    def _serialize_checkpoint(self, checkpoint: Checkpoint) -> Dict[str, Any]:
        """
        Serialize checkpoint for database storage.
        
        Args:
            checkpoint: LangGraph checkpoint dict
            
        Returns:
            Serialized dict suitable for JSON storage
        """
        # Convert to dict if it's not already
        if hasattr(checkpoint, 'model_dump'):
            checkpoint_dict = checkpoint.model_dump()
        elif hasattr(checkpoint, 'dict'):
            checkpoint_dict = checkpoint.dict()
        else:
            checkpoint_dict = dict(checkpoint)
        
        # Handle UUID serialization
        def serialize_value(value):
            if isinstance(value, uuid.UUID):
                return str(value)
            elif isinstance(value, datetime):
                return value.isoformat()
            elif isinstance(value, dict):
                return {k: serialize_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [serialize_value(item) for item in value]
            else:
                return value
        
        return serialize_value(checkpoint_dict)

    def _deserialize_checkpoint(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deserialize checkpoint from database storage.
        
        Args:
            data: Serialized checkpoint data
            
        Returns:
            Deserialized checkpoint dict
        """
        if not data:
            return {}
        
        def deserialize_value(value):
            if isinstance(value, dict):
                return {k: deserialize_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [deserialize_value(item) for item in value]
            else:
                return value
        
        return deserialize_value(data)


class CheckpointManager:
    """
    High-level checkpoint management interface.
    
    Provides convenient methods for workflow state management
    without direct LangGraph dependency.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.checkpointer = PostgresCheckpointSaver(db)

    async def save_workflow_state(
        self,
        execution_id: str,
        state: Dict[str, Any],
        status: str = "RUNNING"
    ) -> None:
        """
        Save workflow state checkpoint.
        
        Args:
            execution_id: Unique execution identifier
            state: Current workflow state
            status: Current workflow status
        """
        config = {
            "thread_id": execution_id,
            "checkpoint_id": str(uuid6())
        }
        
        checkpoint = {
            **state,
            "status": status,
            "checkpointed_at": datetime.utcnow().isoformat()
        }
        
        await self.checkpointer.put(config, checkpoint)

    async def load_workflow_state(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """
        Load workflow state checkpoint.
        
        Args:
            execution_id: Unique execution identifier
            
        Returns:
            Workflow state dict if found, None otherwise
        """
        config = {"thread_id": execution_id}
        checkpoint = await self.checkpointer.get(config)
        return checkpoint

    async def delete_workflow_state(self, execution_id: str) -> None:
        """
        Delete workflow state checkpoint.
        
        Args:
            execution_id: Unique execution identifier
        """
        config = {"thread_id": execution_id}
        await self.checkpointer.delete(config)

    async def list_workflow_states(
        self,
        execution_id: Optional[str] = None,
        limit: int = 10
    ) -> list[Dict[str, Any]]:
        """
        List workflow state checkpoints.
        
        Args:
            execution_id: Optional execution identifier filter
            limit: Maximum number of checkpoints to return
            
        Returns:
            List of workflow state dicts
        """
        config = {"thread_id": execution_id} if execution_id else None
        checkpoints = []
        
        async for checkpoint in self.checkpointer.list(config=config, limit=limit):
            checkpoints.append(checkpoint)
            
        return checkpoints
