import logging
from typing import Optional, List, Dict
from app.config.settings import get_settings

logger = logging.getLogger(__name__)


class AIProviderService:
    """Abstraction for STT, LLM, and TTS providers for the voice pipeline."""

    def __init__(self):
        settings = get_settings()
        self.gemini_api_key = settings.gemini_api_key
        self.gemini_client = None

        if self.gemini_api_key:
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=self.gemini_api_key)
                logger.info("Gemini AI Provider initialized with API Key.")
            except Exception as e:
                logger.warning(f"Could not initialize Gemini Client: {e}")

    async def transcribe_audio(self, audio_bytes: bytes, provider: str = "gemini") -> str:
        """
        Transcribe incoming mu-law audio buffer from Twilio into text.
        Converts 8kHz mu-law to PCM16 WAV and uses Gemini 2.5 Flash audio transcription.
        """
        if not audio_bytes or len(audio_bytes) < 1000:
            return ""

        if self.gemini_client:
            try:
                import io
                import wave
                from google.genai import types
                from app.services.audio_utils import mulaw_to_pcm16

                # Convert 8kHz mu-law bytes to 16-bit PCM bytes
                pcm_bytes = mulaw_to_pcm16(audio_bytes)

                # Wrap PCM bytes into an in-memory WAV container
                wav_io = io.BytesIO()
                with wave.open(wav_io, 'wb') as wav_file:
                    wav_file.setnchannels(1)       # Mono
                    wav_file.setsampwidth(2)      # 16-bit (2 bytes per sample)
                    wav_file.setframerate(8000)   # 8kHz
                    wav_file.writeframes(pcm_bytes)
                
                wav_data = wav_io.getvalue()

                # Call Gemini for audio transcription
                for model_name in ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]:
                    try:
                        response = self.gemini_client.models.generate_content(
                            model=model_name,
                            contents=[
                                types.Part.from_bytes(data=wav_data, mime_type="audio/wav"),
                                "Transcribe exact spoken user words. If silent, noise, or unclear, output EMPTY."
                            ]
                        )
                        if response and response.text:
                            text = response.text.strip()
                            if text and text.lower() not in ["empty", "silent", "none", "[noise]", "nothing"]:
                                logger.info(f"STT Transcribed Audio ({model_name}): '{text}'")
                                return text
                            break
                    except Exception as err:
                        if "404" in str(err) or "429" in str(err) or "RESOURCE_EXHAUSTED" in str(err):
                            continue
                        break


            except Exception as e:
                logger.error(f"Error transcribing audio with Gemini: {e}")

        return ""


    async def generate_response(
        self, 
        system_prompt: str, 
        script: str, 
        conversation_history: List[Dict[str, str]], 
        user_input: str,
        provider: str = "gemini",
        temperature: float = 0.7
    ) -> str:
        """
        Generates the next AI response based on context, script, and user input.
        temperature: float 0.0-1.0 (controls creativity/randomness)
        """
        if self.gemini_client:
            try:
                # Construct system prompt context
                full_system_prompt = (
                    f"{system_prompt}\n\n"
                    f"Additional Script Context: {script}\n"
                    f"Instructions: You are participating in a live telephone call. "
                    f"Keep responses concise, natural, friendly, and under 2-3 sentences."
                )
                
                # Add conversation history
                messages_context = [f"System: {full_system_prompt}"]
                for msg in conversation_history[-6:]:  # Keep last 6 messages
                    role = "User" if msg.get("role") == "user" else "Assistant"
                    messages_context.append(f"{role}: {msg.get('content', '')}")
                
                messages_context.append(f"User: {user_input}")
                prompt_text = "\n".join(messages_context)

                from google.genai import types as genai_types
                config = genai_types.GenerateContentConfig(
                    temperature=float(temperature),
                    max_output_tokens=200,
                )

                for model_name in ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]:
                    try:
                        response = self.gemini_client.models.generate_content(
                            model=model_name,
                            contents=prompt_text,
                            config=config,
                        )
                        if response and response.text:
                            return response.text.strip()
                    except Exception as err:
                        if "404" in str(err) or "429" in str(err) or "RESOURCE_EXHAUSTED" in str(err):
                            continue
                        raise err
            except Exception as e:
                logger.error(f"Error calling Gemini LLM: {e}")




        # Return None if LLM is unavailable so conversation service uses script stage progression
        return None

    async def analyze_call_transcript(self, history: List[Dict[str, str]]) -> Dict[str, str]:
        """
        Analyzes a completed call transcript history using Gemini LLM.
        Returns a dict with 'sentiment' (positive, neutral, negative, interested, not-interested) and 'summary'.
        """
        if not history:
            return {"sentiment": "neutral", "summary": "Call ended without speech turns."}

        formatted_turns = []
        for turn in history:
            role = "Lead" if turn.get("role") == "user" else "AI Agent"
            content = turn.get("content", "")
            if content:
                formatted_turns.append(f"{role}: {content}")

        if not formatted_turns:
            return {"sentiment": "neutral", "summary": "Call completed with zero dialogue turns."}

        transcript_text = "\n".join(formatted_turns)
        prompt = (
            f"Analyze this phone call transcript between an AI sales agent and a customer:\n\n"
            f"{transcript_text}\n\n"
            f"Respond ONLY in valid JSON format with two keys:\n"
            f"1. \"sentiment\": strictly one of [\"positive\", \"neutral\", \"negative\", \"interested\", \"not-interested\"]\n"
            f"2. \"summary\": a concise 2-sentence executive summary of the conversation and outcome.\n"
            f"Do not include markdown code block formatting."
        )

        if self.gemini_client:
            try:
                import json
                for model_name in ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]:
                    try:
                        response = self.gemini_client.models.generate_content(
                            model=model_name,
                            contents=prompt,
                        )
                        if response and response.text:
                            raw_text = response.text.strip().replace("```json", "").replace("```", "").strip()
                            data = json.loads(raw_text)
                            sentiment = data.get("sentiment", "neutral").lower()
                            summary = data.get("summary", "Call completed successfully.")
                            return {"sentiment": sentiment, "summary": summary}
                    except Exception as err:
                        if "404" in str(err) or "429" in str(err) or "RESOURCE_EXHAUSTED" in str(err):
                            continue
                        break
            except Exception as e:
                logger.error(f"Error performing AI transcript analysis: {e}")

        # Fallback heuristic analysis if Gemini API is unreachable
        user_words = " ".join([t.get("content", "").lower() for t in history if t.get("role") == "user"])
        sentiment = "neutral"
        if any(w in user_words for w in ["yes", "interested", "sure", "great", "send", "book", "demo", "love"]):
            sentiment = "interested"
        elif any(w in user_words for w in ["no", "stop", "not interested", "busy", "don't", "wrong"]):
            sentiment = "not-interested"

        summary = f"Call processed with {len(history)} conversation turns."
        return {"sentiment": sentiment, "summary": summary}


    async def generate_speech(self, text: str, provider: str = "gtts", voice: Optional[str] = None) -> bytes:
        """
        Converts text to speech using free gTTS (Google Text-to-Speech)
        and converts it into 8kHz 8-bit mu-law audio bytes for Twilio Media Stream.
        """
        try:
            from io import BytesIO
            from gtts import gTTS
            import miniaudio
            from app.services.audio_utils import pcm16_to_mulaw

            lang = "hi" if voice and ("hi" in voice.lower() or "hindi" in voice.lower()) else "en"
            tts = gTTS(text=text, lang=lang, slow=False)
            fp = BytesIO()
            tts.write_to_fp(fp)
            mp3_bytes = fp.getvalue()

            # Decode MP3 to 8kHz mono PCM 16-bit
            decoded = miniaudio.decode(mp3_bytes, sample_rate=8000, nchannels=1)
            # Encode PCM 16-bit to 8kHz 8-bit mu-law for Twilio
            mulaw_bytes = pcm16_to_mulaw(decoded.samples.tobytes())
            
            logger.info(f"gTTS synthesized speech ({len(text)} chars) -> {len(mulaw_bytes)} bytes 8kHz mu-law")
            return mulaw_bytes
        except Exception as e:
            logger.error(f"Error generating gTTS audio speech: {e}")
            return b""



ai_provider = AIProviderService()



ai_provider_service = AIProviderService()

