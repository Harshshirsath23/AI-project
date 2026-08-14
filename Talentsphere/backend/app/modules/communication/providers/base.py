from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseProvider(ABC):
    """Base class for communication providers"""
    
    @abstractmethod
    async def send(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send message via provider"""
        pass
    
    @abstractmethod
    async def validate_recipient(self, recipient: str) -> bool:
        """Validate recipient format"""
        pass
    
    @abstractmethod
    async def validate_message(self, message: str) -> bool:
        """Validate message content"""
        pass


class EmailProvider(BaseProvider):
    """Email provider implementation"""
    
    async def send(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send email message"""
        # Placeholder for actual email provider integration
        # Would integrate with SendGrid, AWS SES, or similar
        return {
            "status": "success",
            "message_id": f"email_{uuid.uuid4()}",
            "provider": "email"
        }
    
    async def validate_recipient(self, recipient: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, recipient))
    
    async def validate_message(self, message: str) -> bool:
        """Validate email content"""
        return len(message) > 0 and len(message) <= 100000  # Basic validation


class SMSProvider(BaseProvider):
    """SMS provider implementation"""
    
    async def send(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send SMS message"""
        # Placeholder for actual SMS provider integration
        # Would integrate with Twilio, AWS SNS, or similar
        return {
            "status": "success",
            "message_id": f"sms_{uuid.uuid4()}",
            "provider": "sms"
        }
    
    async def validate_recipient(self, recipient: str) -> bool:
        """Validate phone number format"""
        import re
        # Basic international phone validation
        pattern = r'^\+?[1-9]\d{1,14}$'
        return bool(re.match(pattern, recipient.replace(" ", "")))
    
    async def validate_message(self, message: str) -> bool:
        """Validate SMS content"""
        return len(message) > 0 and len(message) <= 1600  # SMS limit


class WhatsAppProvider(BaseProvider):
    """WhatsApp provider implementation"""
    
    async def send(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send WhatsApp message"""
        # Placeholder for actual WhatsApp provider integration
        # Would integrate with Twilio WhatsApp, WhatsApp Business API, or similar
        return {
            "status": "success",
            "message_id": f"whatsapp_{uuid.uuid4()}",
            "provider": "whatsapp"
        }
    
    async def validate_recipient(self, recipient: str) -> bool:
        """Validate WhatsApp number format"""
        # WhatsApp uses phone numbers
        import re
        pattern = r'^\+?[1-9]\d{1,14}$'
        return bool(re.match(pattern, recipient.replace(" ", "")))
    
    async def validate_message(self, message: str) -> bool:
        """Validate WhatsApp message content"""
        return len(message) > 0 and len(message) <= 4096  # WhatsApp limit


class ProviderFactory:
    """Factory for creating provider instances"""
    
    @staticmethod
    def get_provider(channel: str) -> BaseProvider:
        """Get provider instance by channel"""
        from app.modules.communication.enums import CommunicationChannel
        
        if channel == CommunicationChannel.EMAIL:
            return EmailProvider()
        elif channel == CommunicationChannel.SMS:
            return SMSProvider()
        elif channel == CommunicationChannel.WHATSAPP:
            return WhatsAppProvider()
        else:
            raise ValueError(f"Unsupported channel: {channel}")