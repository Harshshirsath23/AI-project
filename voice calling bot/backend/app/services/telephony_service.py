import logging
from abc import ABC, abstractmethod
from typing import Optional

from app.config.settings import get_settings

logger = logging.getLogger(__name__)


class TelephonyProvider(ABC):
    @abstractmethod
    async def initiate_call(self, from_number: str, to_number: str, webhook_url: str) -> str:
        """Initiates an outbound call and returns the provider's call ID."""
        pass

    @abstractmethod
    def generate_twiml(self, websocket_url: str) -> str:
        """Generates TwiML to connect the call to a bidirectional WebSocket Media Stream."""
        pass


class TwilioProvider(TelephonyProvider):
    """
    Twilio Telephony Provider implementation.
    Uses the real Twilio client if credentials are configured in settings/env,
    otherwise gracefully falls back to mock mode for development and testing.
    """

    def __init__(self):
        settings = get_settings()
        self.account_sid = settings.twilio_account_sid
        self.auth_token = settings.twilio_auth_token
        self.client = None

        if self.account_sid and self.auth_token:
            try:
                from twilio.rest import Client
                self.client = Client(self.account_sid, self.auth_token)
                logger.info("Twilio client initialized with provided credentials.")
            except ImportError:
                logger.warning(
                    "twilio package is not installed. TwilioProvider will operate in mock mode. "
                    "Run 'pip install twilio' to enable live calls."
                )
            except Exception as e:
                logger.error(f"Failed to initialize Twilio client: {e}. Falling back to mock mode.")

    async def initiate_call(
        self,
        from_number: str,
        to_number: str,
        webhook_url: str,
        status_callback_url: str = None,
        inline_twiml: str = None
    ) -> str:
        """
        Initiates an outbound call via Twilio.
        Works on both Trial and paid accounts.
        """
        if self.client:
            try:
                create_kwargs = dict(
                    to=to_number,
                    from_=from_number,
                    url=webhook_url,  # TwiML URL — must be public (use ngrok)
                )

                # status_callback_event is NOT available on Twilio Trial accounts
                # Only add status_callback (URL only, no event list) — this is allowed
                if status_callback_url:
                    create_kwargs["status_callback"] = status_callback_url

                logger.info(f"Twilio: Calling {to_number} from {from_number} → TwiML: {webhook_url}")
                call = self.client.calls.create(**create_kwargs)
                logger.info(f"Twilio Call initiated. SID: {call.sid}")
                return call.sid
            except Exception as e:
                logger.error(f"Error initiating Twilio call: {e}")
                raise e
        else:
            logger.info(f"Twilio Mock Call: {from_number} → {to_number}")
            return "mock_twilio_call_id_12345"






    def generate_twiml(self, websocket_url: str) -> str:
        """Generates TwiML to connect the call to a bidirectional WebSocket Media Stream."""
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <Stream url="{websocket_url}" />
    </Connect>
    <Pause length="60"/>
</Response>'''




telephony_provider = TwilioProvider()

