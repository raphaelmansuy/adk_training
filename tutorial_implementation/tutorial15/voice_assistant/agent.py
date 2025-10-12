"""
Voice Assistant Agent
Full VoiceAssistant implementation with audio recording, playback, and conversation.
"""

import asyncio
from typing import Optional
from google.adk.agents import Agent, LiveRequestQueue
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.apps import App
from google.adk.runners import Runner
from google.genai import types

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
        model: str = 'gemini-live-2.5-flash-preview',
        voice_name: str = 'Puck',
        sample_rate: int = 16000
    ):
        """
        Initialize voice assistant.
        
        Args:
            model: Live API model to use
            voice_name: Voice configuration (Puck, Charon, Kore, Fenrir, Aoede)
            sample_rate: Audio sample rate in Hz
        """
        
        # Audio configuration
        self.chunk_size = 1024
        self.sample_rate = sample_rate
        self.channels = 1
        self.format = pyaudio.paInt16 if PYAUDIO_AVAILABLE else None
        
        # PyAudio instance (initialized lazily)
        self._audio = None
        
        # Create voice agent
        self.agent = Agent(
            model=model,
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
        
        # Configure for text-only demo (no speech config needed)
        self.run_config = RunConfig(
            streaming_mode=StreamingMode.BIDI,
            
            # Use text modality for demo (audio requires proper audio handling)
            response_modalities=['text']
        )
        
        # Create app (runner created lazily when needed)
        self.app = App(name='voice_assistant_app', root_agent=self.agent)
        self._runner: Optional[Runner] = None
        
        # Session management
        self._session_id: Optional[str] = None
        self._user_id = 'voice_user'
    
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
        
        # Create queue
        queue = LiveRequestQueue()
        
        # Send text using send_content
        queue.send_content(
            types.Content(
                role='user',
                parts=[types.Part.from_text(text=text)]
            )
        )
        
        # Close queue
        queue.close()
        
        # Collect response
        response_text = []
        
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
    model='gemini-live-2.5-flash-preview',
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
