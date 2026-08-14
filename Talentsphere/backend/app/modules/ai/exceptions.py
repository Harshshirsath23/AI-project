from typing import Optional
from fastapi import HTTPException, status


class AIException(Exception):
    """Base exception for AI module"""
    pass


class AgentNotFoundException(HTTPException):
    def __init__(self, agent_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AI agent with ID {agent_id} not found"
        )


class AgentVersionNotFoundException(HTTPException):
    def __init__(self, agent_id: str, version: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent version {version} for agent {agent_id} not found"
        )


class ToolNotFoundException(HTTPException):
    def __init__(self, tool_name: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AI tool {tool_name} not found"
        )


class ToolAuthorizationException(HTTPException):
    def __init__(self, tool_name: str, reason: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Tool authorization failed for {tool_name}: {reason}"
        )


class KnowledgeDocumentNotFoundException(HTTPException):
    def __init__(self, document_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Knowledge document with ID {document_id} not found"
        )


class EmbeddingException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Embedding processing failed: {message}"
        )


class RetrievalException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Knowledge retrieval failed: {message}"
        )


class ExecutionNotFoundException(HTTPException):
    def __init__(self, execution_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AI execution with ID {execution_id} not found"
        )


class InvalidExecutionStatusException(HTTPException):
    def __init__(self, current_status: str, new_status: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid execution status transition. Current: {current_status}, New: {new_status}"
        )


class HITLException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"HITL operation failed: {message}"
        )


class WorkflowNotFoundException(HTTPException):
    def __init__(self, workflow_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow with ID {workflow_id} not found"
        )


class GuardrailViolationException(HTTPException):
    def __init__(self, guardrail_type: str, message: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Guardrail violation [{guardrail_type}]: {message}"
        )


class PromptNotFoundException(HTTPException):
    def __init__(self, prompt_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prompt template with ID {prompt_id} not found"
        )


class ModelProviderException(HTTPException):
    def __init__(self, provider: str, message: str):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Model provider {provider} error: {message}"
        )


class UsageTrackingException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Usage tracking failed: {message}"
        )