---
id: live_api_audio
title: "Tutorial 15: Live API and Audio - Real-Time Voice Interactions"
description: "Create voice-enabled agents using Gemini's Live API for real-time audio streaming and voice-to-voice conversations."
sidebar_label: "15. Live API & Audio"
sidebar_position: 15
tags: ["advanced", "live-api", "audio", "voice", "real-time"]
keywords: ["live api", "audio streaming", "voice interaction", "real-time conversation", "voice agents"]
status: "draft"
difficulty: "advanced"
estimated_time: "2 hours"
prerequisites: ["Tutorial 01: Hello World Agent", "Tutorial 14: Streaming & SSE", "Gemini 2.0+ Live API access"]
learning_objectives:
  - "Configure Gemini Live API for audio streaming"
  - "Build voice-enabled conversation agents"
  - "Handle real-time audio processing"
  - "Implement voice interruption and turn-taking"
implementation_link: "https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial15"
---

# Tutorial 15: Live API & Bidirectional Streaming with Audio

**Goal**: Master the Live API for bidirectional streaming, enabling real-time voice conversations, audio input/output, and interactive multimodal experiences with your AI agents.

**Prerequisites**:
- Tutorial 01 (Hello World Agent)
- Tutorial 14 (Streaming with SSE)
- Basic understanding of async/await
- Microphone access for audio examples

**What You'll Learn**:
- Implementing bidirectional streaming with `StreamingMode.BIDI`
- Using `LiveRequestQueue` for real-time communication
- Configuring audio input/output with speech recognition
- Building voice assistants
- Handling video streaming
- Understanding proactivity and affective dialog
- Live API model selection and compatibility

**Time to Complete**: 60-75 minutes

---

## Why Live API Matters

Traditional agents are **turn-based** - send message, wait for complete response. The **Live API** enables **real-time, bidirectional** communication:

**Turn-Based (Traditional)**:
```
User speaks → [Complete audio uploaded]
              ↓
Agent thinks → [Processing complete audio]
              ↓
Agent speaks → [Complete response generated]
              ↓
User speaks again...
```

**Live API (Bidirectional)**:
```
User speaks ⟷ Agent hears in real-time
              ⟷ Agent can interrupt
              ⟷ Agent responds while listening
              ⟷ Natural conversation flow
```

**Benefits**:
- 🎙️ **Real-Time Audio**: Stream audio as you speak
- 🗣️ **Natural Conversations**: Interruptions, turn-taking
- 🎭 **Affective Dialog**: Emotion detection in voice
- 📹 **Video Streaming**: Real-time video analysis
- ⚡ **Low Latency**: Immediate responses
- 🤖 **Proactivity**: Agent can initiate conversation

---

## 1. Live API Basics

### What is Bidirectional Streaming?

**BIDI streaming** enables **simultaneous** two-way communication between user and agent. Unlike SSE (one-way), BIDI allows:

- User sends data while agent responds
- Agent can respond before user finishes
- Real-time interaction without turn-taking

**Source**: `google/adk/models/gemini_llm_connection.py`, `google/adk/agents/live_request_queue.py`

### Basic Live API Setup

```python
import asyncio
from google.adk.agents import Agent, Runner, RunConfig, StreamingMode, LiveRequestQueue
from google.genai import types

# Create agent for live interaction
agent = Agent(
    model='gemini-2.0-flash-live-preview-04-09',  # Live API model (Vertex)
    name='live_assistant',
    instruction='You are a helpful voice assistant. Respond naturally to user queries.'
)

# Configure live streaming
run_config = RunConfig(
    streaming_mode=StreamingMode.BIDI,
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name='Puck'  # Available voices: Puck, Charon, Kore, Fenrir, Aoede
            )
        )
    )
)

async def live_session():
    """Run live bidirectional session."""
    
    # Create request queue for live communication
    queue = LiveRequestQueue()
    
    runner = Runner()
    
    # Start live session
    async for event in runner.run_live(queue, agent=agent, run_config=run_config):
        if event.content and event.content.parts:
            # Process agent responses
            for part in event.content.parts:
                if part.text:
                    print(f"Agent: {part.text}")

asyncio.run(live_session())
```

### Live API Models

**VertexAI API**:
```python
# ✅ Vertex Live API model
agent = Agent(model='gemini-2.0-flash-live-preview-04-09')
```

**AI Studio API**:
```python
# ✅ AI Studio Live API model
agent = Agent(model='gemini-live-2.5-flash-preview')
```

**Important**: Regular Gemini models don't support Live API:
```python
# ❌ These DON'T support Live API
agent = Agent(model='gemini-2.0-flash')  # Regular model
agent = Agent(model='gemini-1.5-flash')  # Older model
```

---

## 2. LiveRequestQueue: Real-Time Communication

### Understanding LiveRequestQueue

`LiveRequestQueue` manages bidirectional communication - sending user input and receiving agent responses simultaneously.

**Source**: `google/adk/agents/live_request_queue.py`

### Sending Text

```python
from google.adk.agents import LiveRequestQueue
from google.genai import types

queue = LiveRequestQueue()

# Send text message
queue.send_realtime(text="Hello, how are you?")

# Continue conversation
queue.send_realtime(text="Tell me about quantum computing")

# End session
queue.send_end()
```

### Sending Audio

```python
import wave

# Load audio file
with wave.open('audio_input.wav', 'rb') as audio_file:
    audio_data = audio_file.readframes(audio_file.getnframes())

# Send audio to agent
queue.send_realtime(
    blob=types.Blob(
        data=audio_data,
        mime_type='audio/pcm'  # Or 'audio/wav', 'audio/mp3'
    )
)
```

### Sending Video

```python
# Send video frame
queue.send_realtime(
    blob=types.Blob(
        data=video_frame_bytes,
        mime_type='video/mp4'
    )
)
```

### Queue Management

```python
# Check queue status
is_closed = queue.is_closed()

# Close queue when done
queue.send_end()

# Queue automatically manages:
# - Buffering
# - Synchronization
# - Backpressure
```

---

## 3. Audio Configuration

### Speech Recognition (Input)

```python
from google.genai import types

run_config = RunConfig(
    streaming_mode=StreamingMode.BIDI,
    
    # Audio input configuration
    speech_config=types.SpeechConfig(
        # Voice output configuration
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name='Puck'  # Agent's voice
            )
        ),
        
        # Optional: Audio transcription
        audio_transcription_config=types.AudioTranscriptionConfig(
            model='chirp',
            enable_word_timestamps=True,
            language_codes=['en-US']
        )
    ),
    
    # Response format
    response_modalities=['TEXT', 'AUDIO']  # Return both text and audio
)
```

### Available Voices

```python
# Available prebuilt voices:
voices = [
    'Puck',    # Friendly, conversational
    'Charon',  # Deep, authoritative
    'Kore',    # Warm, professional
    'Fenrir',  # Energetic, dynamic
    'Aoede'    # Calm, soothing
]

# Set voice
run_config = RunConfig(
    streaming_mode=StreamingMode.BIDI,
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name='Charon'  # Choose voice
            )
        )
    )
)
```

### Response Modalities

```python
# Text only
response_modalities=['TEXT']

# Audio only
response_modalities=['AUDIO']

# Both text and audio
response_modalities=['TEXT', 'AUDIO']

# With images (multimodal)
response_modalities=['TEXT', 'AUDIO', 'IMAGE']
```

---

## 4. Real-World Example: Voice Assistant

Let's build a complete voice assistant with Live API.

### Complete Implementation

```python
"""
Voice Assistant with Live API
Real-time voice conversation with audio input/output.
"""

import asyncio
import os
import wave
import pyaudio
from google.adk.agents import Agent, Runner, RunConfig, StreamingMode, LiveRequestQueue
from google.genai import types

# Environment setup
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = '1'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'your-project-id'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'


class VoiceAssistant:
    """Real-time voice assistant using Live API."""
    
    def __init__(self):
        """Initialize voice assistant."""
        
        # Audio configuration
        self.chunk_size = 1024
        self.sample_rate = 16000
        self.channels = 1
        self.format = pyaudio.paInt16
        
        # PyAudio instance
        self.audio = pyaudio.PyAudio()
        
        # Create voice agent
        self.agent = Agent(
            model='gemini-2.0-flash-live-preview-04-09',
            name='voice_assistant',
            description='Real-time voice assistant',
            instruction="""
You are a helpful voice assistant. Guidelines:

- Respond naturally and conversationally
- Keep responses concise for voice interaction
- Ask clarifying questions when needed
- Be friendly and engaging
- Use casual language appropriate for spoken conversation
            """.strip(),
            generate_content_config=types.GenerateContentConfig(
                temperature=0.8,  # Natural conversation
                max_output_tokens=150  # Concise for voice
            )
        )
        
        # Configure live streaming with audio
        self.run_config = RunConfig(
            streaming_mode=StreamingMode.BIDI,
            
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name='Puck'
                    )
                ),
                audio_transcription_config=types.AudioTranscriptionConfig(
                    model='chirp',
                    language_codes=['en-US']
                )
            ),
            
            response_modalities=['TEXT', 'AUDIO']
        )
        
        self.runner = Runner()
    
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
    
    async def conversation_turn(self, user_audio: bytes):
        """
        Execute one conversation turn.
        
        Args:
            user_audio: User's audio input
        """
        
        # Create queue
        queue = LiveRequestQueue()
        
        # Send user audio
        queue.send_realtime(
            blob=types.Blob(
                data=user_audio,
                mime_type='audio/pcm'
            )
        )
        
        # Signal end of user input
        queue.send_end()
        
        print("\n🤖 Agent responding...")
        
        # Collect response
        text_response = []
        audio_response = []
        
        async for event in self.runner.run_live(
            queue,
            agent=self.agent,
            run_config=self.run_config
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    # Text response
                    if part.text:
                        text_response.append(part.text)
                        print(part.text, end='', flush=True)
                    
                    # Audio response
                    if part.inline_data:
                        audio_response.append(part.inline_data.data)
        
        print("\n")
        
        # Play agent's audio response
        if audio_response:
            print("🔊 Playing response...")
            combined_audio = b''.join(audio_response)
            self.play_audio(combined_audio)
    
    async def run_interactive(self):
        """Run interactive voice conversation."""
        
        print("="*70)
        print("VOICE ASSISTANT - LIVE API")
        print("="*70)
        print("Press Enter to start recording, or 'quit' to exit")
        print("="*70)
        
        try:
            while True:
                command = input("\nPress Enter to speak (or 'quit'): ").strip()
                
                if command.lower() == 'quit':
                    print("Goodbye!")
                    break
                
                # Record user audio
                user_audio = await self.record_audio(duration_seconds=5)
                
                # Process conversation turn
                await self.conversation_turn(user_audio)
        
        finally:
            self.audio.terminate()
    
    async def run_demo(self):
        """Run demo with simulated audio."""
        
        print("="*70)
        print("VOICE ASSISTANT DEMO")
        print("="*70)
        
        # Demo messages (in production, these would be actual audio)
        demo_messages = [
            "Hello, what's the weather like today?",
            "Can you tell me a fun fact about space?",
            "Thank you, that's interesting!"
        ]
        
        queue = LiveRequestQueue()
        
        for message in demo_messages:
            print(f"\n🎤 User: {message}")
            
            # Send as text (in production, send audio)
            queue.send_realtime(text=message)
            
            await asyncio.sleep(0.5)
        
        queue.send_end()
        
        print("\n🤖 Agent:")
        
        async for event in self.runner.run_live(
            queue,
            agent=self.agent,
            run_config=self.run_config
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(part.text, end='', flush=True)
        
        print("\n")


async def main():
    """Main entry point."""
    
    assistant = VoiceAssistant()
    
    # Run demo (no microphone needed)
    await assistant.run_demo()
    
    # Uncomment for interactive mode (requires microphone):
    # await assistant.run_interactive()


if __name__ == '__main__':
    asyncio.run(main())
```

### Expected Output

```
======================================================================
VOICE ASSISTANT DEMO
======================================================================

🎤 User: Hello, what's the weather like today?

🤖 Agent: Hello! I don't have access to real-time weather data, but I can help 
you find that information. You could check weather.com or use a weather app on 
your phone. What city are you interested in?

🎤 User: Can you tell me a fun fact about space?

🤖 Agent: Sure! Here's a cool one: One day on Venus is longer than one year on 
Venus! Venus takes about 243 Earth days to rotate once on its axis, but only 
about 225 Earth days to orbit the Sun. So a Venusian day is actually longer 
than a Venusian year. Pretty wild, right?

🎤 User: Thank you, that's interesting!

🤖 Agent: You're welcome! I'm glad you found it interesting. Feel free to ask 
if you'd like to know more fun facts about space or anything else!
```

---

## 5. Advanced Live API Features

### Proactivity

Allow agent to initiate conversation:

```python
from google.genai import types

run_config = RunConfig(
    streaming_mode=StreamingMode.BIDI,
    
    # Enable proactive responses
    proactivity=types.ProactivityConfig(
        threshold=0.7  # 0.0 to 1.0, higher = more proactive
    ),
    
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name='Puck'
            )
        )
    )
)

# Agent can now speak without waiting for user input
# Useful for: notifications, reminders, suggestions
```

### Affective Dialog (Emotion Detection)

Detect user emotions from voice:

```python
run_config = RunConfig(
    streaming_mode=StreamingMode.BIDI,
    
    # Enable emotion detection
    enable_affective_dialog=True,
    
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name='Kore'  # Empathetic voice
            )
        )
    )
)

# Agent receives emotion signals:
# - Happy, Sad, Angry, Neutral, etc.
# - Can adjust response tone accordingly
```

### Video Streaming

Stream video for real-time analysis:

```python
import cv2

# Capture video
cap = cv2.VideoCapture(0)

queue = LiveRequestQueue()

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Convert frame to bytes
    _, buffer = cv2.imencode('.jpg', frame)
    frame_bytes = buffer.tobytes()
    
    # Send frame to agent
    queue.send_realtime(
        blob=types.Blob(
            data=frame_bytes,
            mime_type='image/jpeg'
        )
    )
    
    await asyncio.sleep(0.1)  # ~10 FPS

queue.send_end()

# Agent can analyze video in real-time
# Use cases: gesture recognition, object detection, surveillance
```

---

## 6. Multi-Agent Live Sessions

Combine multiple agents in live conversation:

```python
"""
Multi-agent voice conversation.
"""

from google.adk.agents import Agent, Runner, RunConfig, StreamingMode, LiveRequestQueue
from google.genai import types

# Create specialized agents
greeter = Agent(
    model='gemini-2.0-flash-live-preview-04-09',
    name='greeter',
    instruction='Greet users warmly and ask how you can help.'
)

expert = Agent(
    model='gemini-2.0-flash-live-preview-04-09',
    name='expert',
    instruction='Provide detailed expert answers to questions.'
)

# Orchestrator agent
orchestrator = Agent(
    model='gemini-2.0-flash-live-preview-04-09',
    name='orchestrator',
    instruction="""
You coordinate between multiple agents:
- Use 'greeter' for initial contact
- Use 'expert' for detailed questions
- Ensure smooth conversation flow
    """,
    sub_agents=[greeter, expert],
    flow='sequential'
)

run_config = RunConfig(
    streaming_mode=StreamingMode.BIDI,
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name='Puck'
            )
        )
    )
)

async def multi_agent_voice():
    """Run multi-agent voice session."""
    
    queue = LiveRequestQueue()
    runner = Runner()
    
    # User speaks
    queue.send_realtime(text="Hello, I have a question about quantum computing")
    queue.send_end()
    
    # Orchestrator coordinates agents
    async for event in runner.run_live(queue, agent=orchestrator, run_config=run_config):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(f"{event.author}: {part.text}")

asyncio.run(multi_agent_voice())
```

---

## 7. Best Practices

### ✅ DO: Use Live API Models

```python
# ✅ Good - Live API models
agent = Agent(model='gemini-2.0-flash-live-preview-04-09')  # Vertex
agent = Agent(model='gemini-live-2.5-flash-preview')  # AI Studio

# ❌ Bad - Regular models don't support Live API
agent = Agent(model='gemini-2.0-flash')
agent = Agent(model='gemini-1.5-flash')
```

### ✅ DO: Keep Voice Responses Concise

```python
# ✅ Good - Concise for voice
agent = Agent(
    model='gemini-2.0-flash-live-preview-04-09',
    instruction='Keep responses brief and conversational for voice interaction.',
    generate_content_config=types.GenerateContentConfig(
        max_output_tokens=150
    )
)

# ❌ Bad - Too verbose for voice
agent = Agent(
    model='gemini-2.0-flash-live-preview-04-09',
    generate_content_config=types.GenerateContentConfig(
        max_output_tokens=4096  # Too long for voice
    )
)
```

### ✅ DO: Handle Audio Formats Properly

```python
# ✅ Good - Correct audio format
queue.send_realtime(
    blob=types.Blob(
        data=audio_data,
        mime_type='audio/pcm'  # Or 'audio/wav'
    )
)

# ❌ Bad - Wrong format
queue.send_realtime(
    blob=types.Blob(
        data=audio_data,
        mime_type='text/plain'  # Wrong type
    )
)
```

### ✅ DO: Always Close Queue

```python
# ✅ Good - Properly close queue
queue = LiveRequestQueue()

try:
    queue.send_realtime(text="Hello")
    # ... process responses
finally:
    queue.send_end()  # Always close

# ❌ Bad - Forgot to close
queue = LiveRequestQueue()
queue.send_realtime(text="Hello")
# Queue left open
```

### ✅ DO: Use Appropriate Voices

```python
# ✅ Good - Voice matches use case
customer_service = Agent(
    model='gemini-2.0-flash-live-preview-04-09',
    instruction='Helpful customer service agent'
)

run_config = RunConfig(
    streaming_mode=StreamingMode.BIDI,
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name='Kore'  # Warm, professional
            )
        )
    )
)
```

---

## 8. Troubleshooting

### Error: "Model doesn't support Live API"

**Problem**: Using non-Live API model

**Solution**:
```python
# ❌ Wrong model
agent = Agent(model='gemini-2.0-flash')

# ✅ Use Live API model
agent = Agent(model='gemini-2.0-flash-live-preview-04-09')  # Vertex
# Or
agent = Agent(model='gemini-live-2.5-flash-preview')  # AI Studio
```

### Issue: "No audio in response"

**Problem**: Audio not configured properly

**Solutions**:

1. **Set response modalities**:
```python
run_config = RunConfig(
    streaming_mode=StreamingMode.BIDI,
    response_modalities=['TEXT', 'AUDIO'],  # Include AUDIO
    speech_config=types.SpeechConfig(...)
)
```

2. **Configure voice**:
```python
speech_config=types.SpeechConfig(
    voice_config=types.VoiceConfig(
        prebuilt_voice_config=types.PrebuiltVoiceConfig(
            voice_name='Puck'  # Must set voice
        )
    )
)
```

### Issue: "Queue timeout"

**Problem**: Queue not properly closed

**Solution**:
```python
# ✅ Always send_end()
queue = LiveRequestQueue()
queue.send_realtime(text="Hello")
queue.send_end()  # Important!
```

---

## Summary

You've mastered the Live API for real-time voice interactions:

**Key Takeaways**:
- ✅ `StreamingMode.BIDI` enables bidirectional streaming
- ✅ `LiveRequestQueue` manages real-time communication
- ✅ Audio input/output with `speech_config`
- ✅ Multiple voices available (Puck, Charon, Kore, etc.)
- ✅ Proactivity for agent-initiated conversation
- ✅ Affective dialog for emotion detection
- ✅ Video streaming support
- ✅ Live API models: `gemini-2.0-flash-live-preview-04-09` (Vertex), `gemini-live-2.5-flash-preview` (AI Studio)

**Production Checklist**:
- [ ] Using Live API compatible model
- [ ] `StreamingMode.BIDI` configured
- [ ] Speech config with voice selection
- [ ] Audio format properly set (audio/pcm or audio/wav)
- [ ] Queue properly closed with `send_end()`
- [ ] Concise responses for voice (max_output_tokens=150-200)
- [ ] Error handling for audio/network issues
- [ ] Testing with actual audio devices

**Next Steps**:
- **Tutorial 16**: Learn MCP Integration for extended tool ecosystem
- **Tutorial 17**: Implement Agent-to-Agent (A2A) communication
- **Tutorial 18**: Master Events & Observability

**Resources**:
- [Live API Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/gemini-live)
- [Audio Configuration Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/speech)
- [Sample: live_bidi_streaming_single_agent](research/adk-python/contributing/samples/live_bidi_streaming_single_agent/)

---

**🎉 Tutorial 15 Complete!** You now know how to build real-time voice assistants with the Live API. Continue to Tutorial 16 to learn about MCP integration for extended capabilities.
