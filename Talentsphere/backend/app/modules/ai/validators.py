from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status

from app.modules.ai.enums import (
    AgentStatus, ExecutionStatus, ToolRisk, HITLRequirement,
    PromptStatus, DocumentType, GuardrailType
)
from app.modules.ai.exceptions import (
    InvalidExecutionStatusException, ToolAuthorizationException,
    GuardrailViolationException
)


class AgentValidator:
    """Validator for AI agent operations"""
    
    @staticmethod
    def validate_agent_status_transition(current_status: str, new_status: str) -> None:
        """Validate agent status transitions"""
        valid_transitions = {
            AgentStatus.DRAFT: [AgentStatus.ACTIVE, AgentStatus.ARCHIVED],
            AgentStatus.ACTIVE: [AgentStatus.DEPRECATED, AgentStatus.ARCHIVED],
            AgentStatus.DEPRECATED: [AgentStatus.ARCHIVED],
            AgentStatus.ARCHIVED: []  # Terminal state
        }
        
        if current_status not in valid_transitions:
            raise Exception(f"Invalid current status: {current_status}")
        
        if new_status not in valid_transitions[current_status]:
            raise Exception(f"Invalid status transition from {current_status} to {new_status}")


class ExecutionValidator:
    """Validator for AI execution operations"""
    
    @staticmethod
    def validate_execution_status_transition(current_status: str, new_status: str) -> None:
        """Validate execution status transitions"""
        valid_transitions = {
            ExecutionStatus.QUEUED: [ExecutionStatus.RUNNING, ExecutionStatus.CANCELLED],
            ExecutionStatus.RUNNING: [ExecutionStatus.WAITING_HITL, ExecutionStatus.COMPLETED, ExecutionStatus.FAILED, ExecutionStatus.TIMED_OUT],
            ExecutionStatus.WAITING_HITL: [ExecutionStatus.RUNNING, ExecutionStatus.CANCELLED, ExecutionStatus.COMPLETED, ExecutionStatus.FAILED],
            ExecutionStatus.COMPLETED: [],  # Terminal state
            ExecutionStatus.FAILED: [ExecutionStatus.QUEUED, ExecutionStatus.CANCELLED],
            ExecutionStatus.CANCELLED: [],  # Terminal state
            ExecutionStatus.TIMED_OUT: [ExecutionStatus.QUEUED, ExecutionStatus.CANCELLED]
        }
        
        if current_status not in valid_transitions:
            raise InvalidExecutionStatusException(current_status, "Unknown current status")
        
        if new_status not in valid_transitions[current_status]:
            raise InvalidExecutionStatusException(current_status, new_status)
    
    @staticmethod
    def validate_execution_input(input_data: Dict[str, Any]) -> None:
        """Validate execution input data"""
        if not input_data:
            raise Exception("Execution input data cannot be empty")
        
        # Add more specific validation as needed


class ToolValidator:
    """Validator for AI tool operations"""
    
    @staticmethod
    def validate_tool_authorization(
        tool_permissions: List[str],
        user_permissions: List[str],
        hitl_requirement: str,
        tool_risk: str
    ) -> Dict[str, Any]:
        """Validate tool authorization"""
        # Check permissions
        missing_permissions = set(tool_permissions) - set(user_permissions)
        if missing_permissions:
            raise ToolAuthorizationException(
                "Tool authorization",
                f"Missing permissions: {missing_permissions}"
            )
        
        # Check HITL requirement
        if hitl_requirement == HITLRequirement.REQUIRED:
            return {"authorized": True, "requires_hitl": True}
        elif hitl_requirement == HITLRequirement.ALWAYS:
            return {"authorized": True, "requires_hitl": True}
        
        # Check risk level
        if tool_risk in [ToolRisk.HIGH, ToolRisk.CRITICAL]:
            return {"authorized": True, "requires_hitl": True}
        
        return {"authorized": True, "requires_hitl": False}


class KnowledgeValidator:
    """Validator for knowledge operations"""
    
    @staticmethod
    def validate_document_content(content: str) -> None:
        """Validate document content"""
        if not content or len(content.strip()) < 10:
            raise Exception("Document content is too short")
        
        if len(content) > 10000000:  # 10MB limit
            raise Exception("Document content exceeds maximum size")
    
    @staticmethod
    def validate_retrieval_query(query: str) -> None:
        """Validate retrieval query"""
        if not query or len(query.strip()) < 3:
            raise Exception("Query is too short")
        
        if len(query) > 1000:
            raise Exception("Query exceeds maximum length")


class GuardrailValidator:
    """Validator for AI guardrails"""
    
    @staticmethod
    def validate_input_for_injection(input_data: Dict[str, Any]) -> None:
        """Validate input for potential injection attacks"""
        # Basic validation - can be extended
        for key, value in input_data.items():
            if isinstance(value, str):
                # Check for common injection patterns
                dangerous_patterns = ["<script", "javascript:", "eval(", "exec("]
                for pattern in dangerous_patterns:
                    if pattern.lower() in value.lower():
                        raise GuardrailViolationException(
                            GuardrailType.INPUT_VALIDATION,
                            f"Potential injection detected in field: {key}"
                        )
    
    @staticmethod
    def validate_output_structure(output_data: Dict[str, Any], output_schema: Dict[str, Any]) -> None:
        """Validate output against schema"""
        # Basic schema validation
        if output_schema:
            required_fields = output_schema.get("required", [])
            for field in required_fields:
                if field not in output_data:
                    raise GuardrailViolationException(
                        GuardrailType.OUTPUT_VALIDATION,
                        f"Missing required field in output: {field}"
                    )