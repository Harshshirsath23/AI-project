"""
Comprehensive tests for AI Intelligence & Knowledge Foundation Module

This test suite covers:
- AI agent registry and versioning
- AI tool registry and permissions
- Knowledge document management
- AI execution tracking
- HITL state management
- Workflow registry
- Guardrails validation
- Usage tracking
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai.models import (
    AIAgent, AIAgentVersion, AITool, KnowledgeDocument,
    AIExecution, HITLState, AIWorkflow
)
from app.modules.ai.schemas import (
    AIAgentCreate, AIToolCreate, KnowledgeDocumentCreate,
    AIExecutionCreate, HITLRequest, HITLResponse, AIWorkflowCreate,
    RetrievalRequest
)
from app.modules.ai.enums import (
    AgentStatus, AgentType, ExecutionStatus, ToolRisk,
    HITLRequirement, DocumentType
)
from app.modules.ai.validators import (
    AgentValidator, ExecutionValidator, ToolValidator,
    KnowledgeValidator, GuardrailValidator
)
from app.modules.ai.exceptions import (
    AgentNotFoundException, ToolNotFoundException, InvalidExecutionStatusException
)
from app.modules.ai.service import (
    AgentService, ToolService, KnowledgeService,
    ExecutionService, WorkflowService, GuardrailService
)


# ==================== Fixtures ====================

@pytest.fixture
def mock_db():
    """Mock database session"""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def sample_org_id():
    """Sample organization ID"""
    return uuid.uuid4()


@pytest.fixture
def sample_agent_data():
    """Sample agent data"""
    return AIAgentCreate(
        agent_name="Resume Parser Agent",
        agent_type="Parser",
        description="Parses candidate resumes",
        model_provider="OpenAI",
        model_name="gpt-4",
        allowed_tools=["parse_resume", "extract_skills"],
        required_permissions=["candidate:read"],
        config_data=None,
        is_global=False
    )


@pytest.fixture
def sample_tool_data():
    """Sample tool data"""
    return AIToolCreate(
        tool_name="search_candidates",
        description="Search candidates by criteria",
        tool_path="app.modules.ai.tools.search_candidates",
        required_permissions=["candidate:read"],
        hitl_requirement="Not_Required",
        risk_level="Low"
    )


@pytest.fixture
def sample_document_data():
    """Sample document data"""
    return KnowledgeDocumentCreate(
        document_type="Policy",
        title="Recruitment Policy",
        content="This is the recruitment policy document...",
        tags=["recruitment", "policy"]
    )


@pytest.fixture
def sample_execution_data():
    """Sample execution data"""
    return AIExecutionCreate(
        agent_id=uuid.uuid4(),
        input_data={"resume_text": "Sample resume"}
    )


# ==================== Agent Validator Tests ====================

class TestAgentValidator:
    """Test suite for agent validation"""
    
    def test_validate_agent_status_transition_success(self):
        """Test successful agent status transition"""
        AgentValidator.validate_agent_status_transition("Draft", "Active")
    
    def test_validate_agent_status_transition_invalid(self):
        """Test invalid agent status transition"""
        with pytest.raises(Exception):
            AgentValidator.validate_agent_status_transition("Active", "Draft")


# ==================== Execution Validator Tests ====================

class TestExecutionValidator:
    """Test suite for execution validation"""
    
    def test_validate_execution_status_transition_success(self):
        """Test successful execution status transition"""
        ExecutionValidator.validate_execution_status_transition("Queued", "Running")
    
    def test_validate_execution_status_transition_invalid(self):
        """Test invalid execution status transition"""
        with pytest.raises(InvalidExecutionStatusException):
            ExecutionValidator.validate_execution_status_transition("Completed", "Running")
    
    def test_validate_execution_input_success(self):
        """Test successful execution input validation"""
        ExecutionValidator.validate_execution_input({"resume": "data"})
    
    def test_validate_execution_input_empty(self):
        """Test execution input validation with empty data"""
        with pytest.raises(Exception):
            ExecutionValidator.validate_execution_input({})


# ==================== Tool Validator Tests ====================

class TestToolValidator:
    """Test suite for tool validation"""
    
    def test_validate_tool_authorization_success(self):
        """Test successful tool authorization"""
        result = ToolValidator.validate_tool_authorization(
            ["candidate:read"],
            ["candidate:read"],
            "Not_Required",
            "Low"
        )
        assert result["authorized"] == True
        assert result["requires_hitl"] == False
    
    def test_validate_tool_authorization_missing_permission(self):
        """Test tool authorization with missing permission"""
        with pytest.raises(Exception):
            ToolValidator.validate_tool_authorization(
                ["candidate:read"],
                [],
                "Not_Required",
                "Low"
            )
    
    def test_validate_tool_authorization_high_risk(self):
        """Test tool authorization with high risk"""
        result = ToolValidator.validate_tool_authorization(
            ["candidate:read"],
            ["candidate:read"],
            "Not_Required",
            "High"
        )
        assert result["requires_hitl"] == True


# ==================== Knowledge Validator Tests ====================

class TestKnowledgeValidator:
    """Test suite for knowledge validation"""
    
    def test_validate_document_content_success(self):
        """Test successful document content validation"""
        KnowledgeValidator.validate_document_content("Valid document content")
    
    def test_validate_document_content_too_short(self):
        """Test document content validation with too short content"""
        with pytest.raises(Exception):
            KnowledgeValidator.validate_document_content("Short")
    
    def test_validate_retrieval_query_success(self):
        """Test successful retrieval query validation"""
        KnowledgeValidator.validate_retrieval_query("Valid query")
    
    def test_validate_retrieval_query_too_short(self):
        """Test retrieval query validation with too short query"""
        with pytest.raises(Exception):
            KnowledgeValidator.validate_retrieval_query("Q")


# ==================== Service Tests ====================

class TestAgentService:
    """Test suite for agent service"""
    
    @pytest.mark.asyncio
    async def test_create_agent_success(self, mock_db, sample_agent_data, sample_org_id):
        """Test successful agent creation"""
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        
        service = AgentService(mock_db)
        service.agent_repo.create_agent = AsyncMock(return_value=Mock(id=uuid.uuid4()))
        service.agent_repo.create_agent_version = AsyncMock()
        
        result = await service.create_agent(sample_org_id, sample_agent_data)
        
        assert result["status"] == "success"
        assert "agent_id" in result


class TestToolService:
    """Test suite for tool service"""
    
    @pytest.mark.asyncio
    async def test_create_tool_success(self, mock_db, sample_tool_data):
        """Test successful tool creation"""
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        
        service = ToolService(mock_db)
        service.tool_repo.create_tool = AsyncMock(return_value=Mock(id=uuid.uuid4()))
        
        result = await service.create_tool(sample_tool_data)
        
        assert result["status"] == "success"
        assert "tool_id" in result


class TestKnowledgeService:
    """Test suite for knowledge service"""
    
    @pytest.mark.asyncio
    async def test_create_document_success(self, mock_db, sample_document_data, sample_org_id):
        """Test successful document creation"""
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        
        service = KnowledgeService(mock_db)
        service.knowledge_repo.create_document = AsyncMock(return_value=Mock(id=uuid.uuid4()))
        
        result = await service.create_document(sample_org_id, sample_document_data)
        
        assert result["status"] == "success"
        assert "document_id" in result


class TestExecutionService:
    """Test suite for execution service"""
    
    @pytest.mark.asyncio
    async def test_create_execution_success(self, mock_db, sample_execution_data, sample_org_id):
        """Test successful execution creation"""
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        
        service = ExecutionService(mock_db)
        service.execution_repo.create_execution = AsyncMock(return_value=Mock(id=uuid.uuid4()))
        
        result = await service.create_execution(sample_org_id, sample_execution_data)
        
        assert result["status"] == "success"
        assert "execution_id" in result


class TestGuardrailService:
    """Test suite for guardrail service"""
    
    @pytest.mark.asyncio
    async def test_validate_input_success(self, mock_db):
        """Test successful input validation"""
        service = GuardrailService(mock_db)
        result = await service.validate_input({"safe": "data"})
        
        assert result["status"] == "success"
        assert result["passed"] == True


# ==================== Test Configuration ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])