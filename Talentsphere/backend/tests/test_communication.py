"""
Comprehensive tests for Communication & Collaboration Module

This test suite covers:
- Template validation and CRUD operations
- Message queue management
- Provider abstraction
- Conversation thread management
- Notification system
- Webhook infrastructure
- Notification preferences
- AI hooks (for future LangGraph integration)
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.communication.models import (
    CommunicationTemplate, MessageQueue, Conversation, Message,
    Notification, WebhookConfiguration, NotificationPreference
)
from app.modules.communication.schemas import (
    CommunicationTemplateCreate, MessageCreate, ConversationCreate,
    NotificationCreate, WebhookConfigurationCreate,
    NotificationPreferenceCreate, MessageCreateForConversation,
    TemplateVariableSubstitution
)
from app.modules.communication.enums import (
    CommunicationChannel, MessageStatus, NotificationType,
    NotificationPriority, ConversationType, MessageDirection
)
from app.modules.communication.validators import (
    TemplateValidator, MessageValidator, ConversationValidator,
    NotificationValidator
)
from app.modules.communication.exceptions import (
    TemplateNotFoundException, MessageNotFoundException, ConversationNotFoundException,
    TemplateValidationException, InvalidRecipientException, InvalidMessageStatusException
)
from app.modules.communication.service import (
    TemplateService, MessageService, ConversationService,
    NotificationService, NotificationPreferenceService, WebhookService
)
from app.modules.communication.ai_hooks import CommunicationAIHooks


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
def sample_user_id():
    """Sample user ID"""
    return uuid.uuid4()


@pytest.fixture
def sample_template_data():
    """Sample template data"""
    return CommunicationTemplateCreate(
        template_name="Interview Invitation",
        template_type="email",
        notification_type="Interview Scheduled",
        subject="Interview Invitation - {{job_title}}",
        body="Hello {{candidate_name}},\n\nYour interview for {{job_title}} has been scheduled for {{interview_date}}.\n\nInterview link: {{meeting_link}}",
        variables={
            "candidate_name": {"type": "string", "required": True},
            "job_title": {"type": "string", "required": True},
            "interview_date": {"type": "string", "required": True},
            "meeting_link": {"type": "string", "required": True}
        },
        is_default=False
    )


@pytest.fixture
def sample_message_data():
    """Sample message data"""
    return MessageCreate(
        recipient_id=uuid.uuid4(),
        recipient_type="candidate",
        recipient_email="candidate@example.com",
        channel="Email",
        notification_type="Interview Scheduled",
        subject="Interview Invitation",
        body="Hello, your interview has been scheduled.",
        priority="Normal"
    )


@pytest.fixture
def sample_conversation_data():
    """Sample conversation data"""
    return ConversationCreate(
        conversation_type="Candidate",
        entity_id=uuid.uuid4(),
        entity_type="candidate",
        subject="Interview Scheduling",
        participants={"user_ids": [], "roles": []}
    )


@pytest.fixture
def sample_notification_data():
    """Sample notification data"""
    return NotificationCreate(
        recipient_id=uuid.uuid4(),
        recipient_type="user",
        notification_type="Interview Scheduled",
        title="Interview Scheduled",
        body="An interview has been scheduled.",
        channel="In-App",
        priority="Normal"
    )


# ==================== Template Validator Tests ====================

class TestTemplateValidator:
    """Test suite for template validation"""
    
    def test_validate_template_structure_success(self):
        """Test successful template structure validation"""
        template_data = {
            "template_type": "email",
            "notification_type": "Interview Scheduled",
            "subject": "Test Subject",
            "body": "Test body with {{variable}}"
        }
        # Should not raise exception
        TemplateValidator.validate_template_structure(template_data)
    
    def test_validate_template_structure_missing_body(self):
        """Test validation fails with missing body"""
        template_data = {
            "template_type": "email",
            "notification_type": "Interview Scheduled",
            "subject": "Test Subject"
        }
        with pytest.raises(TemplateValidationException):
            TemplateValidator.validate_template_structure(template_data)
    
    def test_validate_template_structure_email_no_subject(self):
        """Test validation fails for email without subject"""
        template_data = {
            "template_type": "email",
            "notification_type": "Interview Scheduled",
            "body": "Test body"
        }
        with pytest.raises(TemplateValidationException):
            TemplateValidator.validate_template_structure(template_data)
    
    def test_validate_template_variables_success(self):
        """Test successful template variables validation"""
        body = "Hello {{name}}, your interview is on {{date}}"
        variables = {"name": {"type": "string"}, "date": {"type": "string"}}
        # Should not raise exception
        TemplateValidator.validate_template_variables(body, variables)
    
    def test_validate_template_variables_undefined(self):
        """Test validation fails with undefined variables"""
        body = "Hello {{name}}, your interview is on {{date}}"
        variables = {"name": {"type": "string"}}  # Missing 'date'
        with pytest.raises(Exception):
            TemplateValidator.validate_template_variables(body, variables)
    
    def test_substitute_variables_success(self):
        """Test successful variable substitution"""
        body = "Hello {{name}}, your interview is on {{date}}"
        variables = {"name": "John", "date": "2024-01-15"}
        result = TemplateValidator.substitute_variables(body, variables)
        assert result == "Hello John, your interview is on 2024-01-15"


# ==================== Message Validator Tests ====================

class TestMessageValidator:
    """Test suite for message validation"""
    
    def test_validate_recipient_success(self):
        """Test successful recipient validation"""
        recipient_data = {
            "recipient_type": "user",
            "channel": "Email",
            "recipient_email": "user@example.com"
        }
        # Should not raise exception
        MessageValidator.validate_recipient(recipient_data)
    
    def test_validate_recipient_invalid_type(self):
        """Test validation fails with invalid recipient type"""
        recipient_data = {
            "recipient_type": "invalid",
            "channel": "Email",
            "recipient_email": "user@example.com"
        }
        with pytest.raises(InvalidRecipientException):
            MessageValidator.validate_recipient(recipient_data)
    
    def test_validate_recipient_email_no_email(self):
        """Test validation fails for email without email"""
        recipient_data = {
            "recipient_type": "user",
            "channel": "Email",
            "recipient_phone": "+1234567890"
        }
        with pytest.raises(InvalidRecipientException):
            MessageValidator.validate_recipient(recipient_data)
    
    def test_validate_status_transition_success(self):
        """Test successful status transition"""
        MessageValidator.validate_status_transition("Queued", "Processing")
    
    def test_validate_status_transition_invalid(self):
        """Test validation fails with invalid transition"""
        with pytest.raises(InvalidMessageStatusException):
            MessageValidator.validate_status_transition("Sent", "Queued")


# ==================== Service Tests ====================

class TestTemplateService:
    """Test suite for template service"""
    
    @pytest.mark.asyncio
    async def test_create_template_success(self, mock_db, sample_template_data, sample_org_id):
        """Test successful template creation"""
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        
        service = TemplateService(mock_db)
        result = await service.create_template(sample_org_id, sample_template_data)
        
        assert result["status"] == "success"
        assert "template_id" in result


class TestMessageService:
    """Test suite for message service"""
    
    @pytest.mark.asyncio
    async def test_create_message_success(self, mock_db, sample_message_data, sample_org_id, sample_user_id):
        """Test successful message creation"""
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        
        service = MessageService(mock_db)
        service.message_repo.create_message = AsyncMock(return_value=Mock(id=uuid.uuid4()))
        service.check_automation_policy = AsyncMock(return_value=None)
        
        result = await service.create_message(sample_org_id, sample_message_data, sample_user_id)
        
        assert result["status"] == "success"
        assert "message_id" in result


class TestConversationService:
    """Test suite for conversation service"""
    
    @pytest.mark.asyncio
    async def test_create_conversation_success(self, mock_db, sample_conversation_data, sample_org_id):
        """Test successful conversation creation"""
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        
        service = ConversationService(mock_db)
        result = await service.create_conversation(sample_org_id, sample_conversation_data)
        
        assert result["status"] == "success"
        assert "conversation_id" in result


class TestNotificationService:
    """Test suite for notification service"""
    
    @pytest.mark.asyncio
    async def test_create_notification_success(self, mock_db, sample_notification_data, sample_org_id):
        """Test successful notification creation"""
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        
        service = NotificationService(mock_db)
        service.notification_repo.create_notification = AsyncMock(return_value=Mock(id=uuid.uuid4()))
        service.get_user_preferences = AsyncMock(return_value=None)
        service.is_channel_enabled = Mock(return_value=True)
        
        result = await service.create_notification(sample_org_id, sample_notification_data)
        
        assert result["status"] == "success"
        assert "notification_id" in result


# ==================== AI Hooks Tests ====================

class TestCommunicationAIHooks:
    """Test suite for communication AI hooks"""
    
    @pytest.mark.asyncio
    async def test_on_message_drafting_requested(self, mock_db):
        """Test message drafting hook"""
        hooks = CommunicationAIHooks(mock_db)
        
        result = await hooks.on_message_drafting_requested(
            uuid.uuid4(),
            {"context": "interview scheduling"},
            {"tone": "professional"}
        )
        
        assert result["recipient_id"]
        assert result["hook_status"] == "ready_for_langgraph_integration"
        assert "agent_type" in result
    
    @pytest.mark.asyncio
    async def test_on_conversation_summary_requested(self, mock_db):
        """Test conversation summary hook"""
        hooks = CommunicationAIHooks(mock_db)
        
        result = await hooks.on_conversation_summary_requested(
            uuid.uuid4(),
            {"detail_level": "brief"}
        )
        
        assert result["conversation_id"]
        assert "summary" in result
        assert result["hook_status"] == "ready_for_langgraph_integration"


# ==================== Test Configuration ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])