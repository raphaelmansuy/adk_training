"""
Voice Assistant Agent
Full VoiceAssistant implementation with audio recording, playback, and conversation.
"""

import asyncio
import os
from typing import Optional
from google.adk.agents import Agent, LiveRequestQueue
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.apps import App
from google.adk.runners import Runner
from google.genai import Client, types, errors

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False


class VoiceAssistant:
    """
    Real-time voice assistant using Live API.
    
    Features:
    - Audio recording from microphone
    - Audio playback through speakers
    - Bidirectional streaming conversation
    - Multiple voice configurations
    """
    
    def __init__(
        self,
        model: Optional[str] = None,
        voice_name: str = 'Puck',
        sample_rate: int = 16000,
        audio_mode: bool = False
    ):
        """
        Initialize voice assistant.
        
        Args:
            model: Live API model to use
            voice_name: Voice configuration (Puck, Charon, Kore, Fenrir, Aoede)
            sample_rate: Audio sample rate in Hz
            audio_mode: If True, use audio modality. If False, use text modality.
        """
        
        # Audio configuration
        self.chunk_size = 1024
        self.sample_rate = sample_rate
        self.channels = 1
        self.format = pyaudio.paInt16 if PYAUDIO_AVAILABLE else None
        self.voice_name = voice_name
        self.audio_mode = audio_mode
        
        # PyAudio instance (initialized lazily)
        self._audio = None
        
        # Determine model configuration
        self.live_model = model or os.getenv('VOICE_ASSISTANT_LIVE_MODEL', 'gemini-2.0-flash-live-001')

        # Create voice agent
        self.agent = Agent(
            model=self.live_model,
            name='voice_assistant',
            description='Real-time voice assistant',
            instruction="""
You are a helpful voice assistant. Guidelines:

- Respond naturally and conversationally
- Keep responses concise for voice interaction (2-3 sentences max)
- Ask clarifying questions when needed
- Be friendly and engaging
- Use casual language appropriate for spoken conversation
- Avoid long explanations unless specifically asked
            """.strip(),
            generate_content_config=types.GenerateContentConfig(
                temperature=0.8,  # Natural conversation
                max_output_tokens=150  # Concise for voice
            )
        )
        
        # Configure live streaming settings based on mode
        if audio_mode:
            # Audio mode: receive audio responses
            self.run_config = RunConfig(
                streaming_mode=StreamingMode.BIDI,
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice_name
                        )
                    )
                ),
                response_modalities=['audio']  # Native audio model
            )
        else:
            # Text mode: receive text responses (fallback)
            self.run_config = RunConfig(
                streaming_mode=StreamingMode.BIDI,
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice_name
                        )
                    )
                ),
                response_modalities=['text']  # Text fallback
            )
        
        # Determine authentication strategy
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
        self.vertex_location = (
            os.getenv('GOOGLE_CLOUD_LOCATION')
            or os.getenv('GOOGLE_GENAI_VERTEXAI_LOCATION')
            or 'us-central1'
        )
        self.use_vertex_live = bool(
            os.getenv('GOOGLE_GENAI_USE_VERTEXAI') and self.project_id
        )
        if self.use_vertex_live:
            # Ensure downstream libraries see a location even if user omitted it
            if not os.getenv('GOOGLE_GENAI_VERTEXAI_LOCATION'):
                os.environ['GOOGLE_GENAI_VERTEXAI_LOCATION'] = self.vertex_location
            if not os.getenv('GOOGLE_CLOUD_LOCATION'):
                os.environ['GOOGLE_CLOUD_LOCATION'] = self.vertex_location
        self._api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
        self._client: Optional[Client] = None
        self.text_model = os.getenv('VOICE_ASSISTANT_TEXT_MODEL', 'gemini-2.5-flash')

        # Create app (runner created lazily when needed)
        self.app = App(name='voice_assistant_app', root_agent=self.agent)
        self._runner: Optional[Runner] = None
        
        # Session management
        self._session_id: Optional[str] = None
        self._user_id = 'voice_user'
    
    async def _fallback_generate_text(self, text: str) -> str:
        """Use Responses API when Live API streaming is unavailable."""
        if self._client is None:
            if self.use_vertex_live:
                # Use Vertex AI endpoint with ADC credentials
                self._client = Client(
                    vertexai=True,
                    project=self.project_id,
                    location=self.vertex_location
                )
            elif self._api_key:
                # Direct API key mode (Google hosted endpoint)
                self._client = Client(api_key=self._api_key)
            else:
                self._client = Client()
        
        user_content = types.Content(
            role='user',
            parts=[types.Part.from_text(text=text)]
        )
        model_name = self.text_model
        if not self.use_vertex_live and '/' not in model_name:
            model_name = f"models/{model_name}"

        try:
            response = await asyncio.to_thread(
                self._client.models.generate_content,
                model=model_name,
                contents=[user_content]
            )
        except errors.ClientError as err:
            print(f"❌ Fallback model error ({err}). Check VOICE_ASSISTANT_TEXT_MODEL.")
            return "I'm unable to reach the text model right now. Please verify your API access."
        parts: list[str] = []
        for candidate in getattr(response, 'candidates', []) or []:
            content = getattr(candidate, 'content', None)
            if not content or not getattr(content, 'parts', None):
                continue
            for part in content.parts:
                value = getattr(part, 'text', None)
                if value:
                    parts.append(value)
        return ''.join(parts)
    
    @property
    def runner(self) -> Runner:
        """Lazy initialization of Runner."""
        if self._runner is None:
            from google.adk.sessions import InMemorySessionService
            session_service = InMemorySessionService()
            self._runner = Runner(app=self.app, session_service=session_service)
        return self._runner
    
    @property
    def audio(self):
        """Lazy initialization of PyAudio."""
        if not PYAUDIO_AVAILABLE:
            raise RuntimeError("PyAudio not available. Install with: pip install pyaudio")
        
        if self._audio is None:
            self._audio = pyaudio.PyAudio()
        return self._audio
    
    async def record_audio(self, duration_seconds: int = 5) -> bytes:
        """
        Record audio from microphone.
        
        Args:
            duration_seconds: Recording duration
        
        Returns:
            Audio data as bytes
        """
        
        print(f"🎤 Recording for {duration_seconds} seconds...")
        
        stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        frames = []
        
        for _ in range(0, int(self.sample_rate / self.chunk_size * duration_seconds)):
            data = stream.read(self.chunk_size)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        
        print("✅ Recording complete")
        
        return b''.join(frames)
    
    def play_audio(self, audio_data: bytes):
        """
        Play audio through speakers.
        
        Args:
            audio_data: Audio bytes to play
        """
        
        stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            output=True
        )
        
        stream.write(audio_data)
        stream.stop_stream()
        stream.close()
    
    async def _ensure_session(self):
        """Ensure session is created."""
        if self._session_id is None:
            session = await self.runner.session_service.create_session(
                app_name=self.app.name,
                user_id=self._user_id
            )
            self._session_id = session.id
    
    async def send_text(self, text: str) -> str:
        """
        Send text message and get response.
        
        Args:
            text: User message
        
        Returns:
            Agent's text response
        """
        
        await self._ensure_session()
        
        if not self.use_vertex_live:
            return await self._fallback_generate_text(text)

        # Create queue for live streaming
        queue = LiveRequestQueue()
        queue.send_content(
            types.Content(
                role='user',
                parts=[types.Part.from_text(text=text)]
            )
        )
        queue.close()
        
        response_text: list[str] = []
        try:
            async for event in self.runner.run_live(
                live_request_queue=queue,
                user_id=self._user_id,
                session_id=self._session_id,
                run_config=self.run_config
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            response_text.append(part.text)
        except Exception as exc:
            print(f"⚠️  Live session error ({exc}); falling back to text responses.")
            return await self._fallback_generate_text(text)
        
        # Fallback if stream returns nothing
        if not response_text:
            return await self._fallback_generate_text(text)
        
        return ''.join(response_text)
    
    async def send_audio(self, audio_data: bytes) -> tuple[str, list[bytes]]:
        """
        Send audio and get response.
        
        Args:
            audio_data: Audio bytes
        
        Returns:
            Tuple of (text_response, audio_response_chunks)
        """
        
        await self._ensure_session()
        
        # Create queue
        queue = LiveRequestQueue()
        
        # Send audio using send_realtime
        queue.send_realtime(
            blob=types.Blob(
                data=audio_data,
                mime_type=f'audio/pcm;rate={self.sample_rate}'
            )
        )
        
        # Close queue
        queue.close()
        
        # Collect response
        text_response = []
        audio_response = []
        
        async for event in self.runner.run_live(
            live_request_queue=queue,
            user_id=self._user_id,
            session_id=self._session_id,
            run_config=self.run_config
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        text_response.append(part.text)
                    if part.inline_data:
                        audio_response.append(part.inline_data.data)
        
        return ''.join(text_response), audio_response
    
    async def conversation_turn(self, user_audio: bytes):
        """
        Execute one conversation turn with audio.
        
        Args:
            user_audio: User's audio input
        """
        
        print("\n🤖 Agent responding...")
        
        # Send audio and get response
        text_response, audio_response = await self.send_audio(user_audio)
        
        # Print text response
        print(text_response)
        
        # Play audio response if available
        if audio_response:
            print("🔊 Playing response...")
            combined_audio = b''.join(audio_response)
            self.play_audio(combined_audio)
    
    def cleanup(self):
        """Cleanup resources."""
        if self._audio is not None:
            self._audio.terminate()


# Export root_agent for ADK discovery
root_agent = Agent(
    model=os.getenv('VOICE_ASSISTANT_LIVE_MODEL', 'gemini-2.0-flash-live-001'),
    name='voice_assistant',
    description='Real-time voice assistant with Live API support',
    instruction="""
You are a helpful voice assistant. Guidelines:

- Respond naturally and conversationally
- Keep responses concise for voice interaction (2-3 sentences max)
- Ask clarifying questions when needed
- Be friendly and engaging
- Use casual language appropriate for spoken conversation
- Avoid long explanations unless specifically asked
    """.strip(),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.8,
        max_output_tokens=150
    )
)
