"""
Direct Live API Audio Example
Using google.genai.Client directly for true bidirectional audio streaming.

This bypasses the ADK Runner framework and uses the low-level Live API
for microphone input → audio output workflow.

Based on official documentation:
https://ai.google.dev/gemini-api/docs/live
"""

import asyncio
import os

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("❌ google-genai not installed. Run: pip install google-genai")

try:
    from voice_assistant.audio_utils import AudioRecorder, AudioPlayer, check_audio_available
    AUDIO_UTILS_AVAILABLE = True
except ImportError:
    AUDIO_UTILS_AVAILABLE = False
    print("❌ Audio utils not available")


async def direct_audio_conversation():
    """
    Run bidirectional audio conversation using direct Live API.
    
    This demonstrates:
    - True audio input from microphone
    - Audio output to speakers
    - Direct genai.Client usage (bypasses ADK framework)
    - Real-time streaming
    """
    
    # Check dependencies
    if not GENAI_AVAILABLE:
        print("❌ google-genai package is required")
        return
        
    if not AUDIO_UTILS_AVAILABLE:
        print("❌ Audio utilities not available")
        return
    
    # Check audio availability
    audio_ok, error_msg = check_audio_available()
    if not audio_ok:
        print(f"❌ {error_msg}")
        return
    
    print("=" * 70)
    print("DIRECT LIVE API - BIDIRECTIONAL AUDIO CONVERSATION")
    print("=" * 70)
    print()
    print("This demo uses google.genai.Client directly for true audio input.")
    print("Unlike ADK Runner, this supports microphone → agent → speakers.")
    print()
    print("⚠️  Note: This bypasses ADK agent framework (no tools/state)")
    print()
    
        # Get model name
    model = os.getenv(
        'VOICE_ASSISTANT_LIVE_MODEL',
        'gemini-2.0-flash-live-preview-04-09'
    )
    print(f"Using model: {model}")
    print()
    
    # Initialize audio recorder and player
    recorder = AudioRecorder()
    player = AudioPlayer()
    
    # Create client
    client = genai.Client(
        vertexai=os.getenv('GOOGLE_GENAI_USE_VERTEXAI', '1') == '1',
        project=os.getenv('GOOGLE_CLOUD_PROJECT'),
        location=os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
    )
    
    # Configure session
    config = {
        "response_modalities": ["AUDIO"],  # Audio output
        "speech_config": types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name='Puck'
                )
            )
        ),
        "system_instruction": (
            "You are a helpful voice assistant. "
            "Keep responses concise (2-3 sentences) for voice interaction. "
            "Be friendly and conversational."
        ),
    }
    
    try:
        print("🔌 Connecting to Live API...")
        async with client.aio.live.connect(model=model, config=config) as session:
            print("✅ Connected to Live API")
            print()
            
            max_turns = 3
            for turn in range(1, max_turns + 1):
                print(f"\n{'='*70}")
                print(f"TURN {turn}/{max_turns}")
                print(f"{'='*70}\n")
                
                # Record audio from user
                print("🎤 Recording your message (5 seconds)...")
                print("   Speak now!")
                audio_data = recorder.record_audio(duration_seconds=5, show_progress=True)
                
                if not audio_data or len(audio_data) < 1000:
                    print("⚠️  No audio detected. Please check your microphone.")
                    continue
                
                print(f"✅ Recorded {len(audio_data)} bytes")
                print("   (Audio already in correct format: 16-bit PCM, 16kHz, mono)")
                
                # Send audio to agent
                print("📤 Sending audio to agent...")
                await session.send_realtime_input(
                    audio=types.Blob(
                        data=audio_data,
                        mime_type="audio/pcm;rate=16000"  # IMPORTANT: Include rate
                    )
                )
                print("✅ Audio sent")
                
                # Receive and play response
                print("🔊 Agent responding...")
                audio_chunks = []
                chunk_count = 0
                
                try:
                    # Process response with timeout
                    async def receive_with_timeout():
                        nonlocal chunk_count
                        async for response in session.receive():
                            # Check for audio data
                            if response.data is not None:
                                chunk_count += 1
                                audio_chunks.append(response.data)
                                # Play in real-time
                                player.play_pcm_bytes(response.data)
                                print(f"   🔊 Playing chunk {chunk_count}...", end='\r', flush=True)
                            
                            # Check for text (sometimes included)
                            if hasattr(response, 'text') and response.text:
                                print(f"\n   💬 Text: {response.text}")
                            
                            # Check for turn completion
                            if hasattr(response, 'server_content'):
                                server_content = response.server_content
                                if server_content and hasattr(server_content, 'turn_complete'):
                                    if server_content.turn_complete:
                                        print("\n   ✅ Turn complete")
                                        break
                    
                    # Run with 30 second timeout
                    await asyncio.wait_for(receive_with_timeout(), timeout=30.0)
                    
                    print(f"\n✅ Received {chunk_count} audio chunks")
                    
                    # Save complete response
                    if audio_chunks:
                        complete_audio = b''.join(audio_chunks)
                        filename = f'direct_response_turn_{turn}.wav'
                        player.save_to_wav(complete_audio, filename)
                        print(f"💾 Saved response to: {filename}")
                    else:
                        print("⚠️  No audio response received")
                        
                except asyncio.TimeoutError:
                    print("\n⏱️  Response timeout (30 seconds)")
                    if audio_chunks:
                        print(f"   Received {chunk_count} chunks before timeout")
                except Exception as e:
                    print(f"\n❌ Error receiving response: {e}")
                
                # Ask to continue
                if turn < max_turns:
                    print("\n❓ Continue conversation? (y/n) ", end='', flush=True)
                    response = input().strip().lower()
                    if response != 'y':
                        print("👋 Goodbye!")
                        break
            
            print("\n" + "="*70)
            print("CONVERSATION COMPLETE")
            print("="*70)
            
    except Exception as e:
        print(f"\n❌ Error during conversation: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main entry point."""
    
    # Check if running with correct authentication
    if os.getenv('GOOGLE_GENAI_USE_VERTEXAI') == '1':
        if not os.getenv('GOOGLE_CLOUD_PROJECT'):
            print("❌ GOOGLE_CLOUD_PROJECT environment variable required")
            print("   Set it in your .env file or export it:")
            print("   export GOOGLE_CLOUD_PROJECT=your-project-id")
            return
        print("✓ Using Vertex AI authentication")
    else:
        if not os.getenv('GOOGLE_API_KEY'):
            print("❌ GOOGLE_API_KEY environment variable required")
            print("   Get one from: https://aistudio.google.com/apikey")
            return
        print("✓ Using AI Studio API key")
    
    print()
    
    try:
        asyncio.run(direct_audio_conversation())
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
