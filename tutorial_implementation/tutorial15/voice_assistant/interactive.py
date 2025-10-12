"""
Interactive Voice Mode
Requires microphone for audio input.
"""

import asyncio
import os
from voice_assistant.agent import VoiceAssistant, PYAUDIO_AVAILABLE


async def run_interactive():
    """
    Run interactive voice conversation.
    Requires microphone and speakers.
    """
    
    if not PYAUDIO_AVAILABLE:
        print("❌ PyAudio not installed!")
        print("   Install with: pip install pyaudio")
        print()
        print("   On macOS: brew install portaudio && pip install pyaudio")
        print("   On Ubuntu: sudo apt-get install portaudio19-dev && pip install pyaudio")
        return
    
    print("=" * 70)
    print("VOICE ASSISTANT - INTERACTIVE VOICE MODE")
    print("=" * 70)
    print()
    print("This mode uses your microphone for voice input.")
    print("Press Enter to start recording, or type 'quit' to exit.")
    print()
    print("=" * 70)
    print()
    
    assistant = VoiceAssistant(
        model='gemini-live-2.5-flash-preview',
        voice_name='Puck',
        sample_rate=16000
    )
    
    try:
        while True:
            # Get user input
            command = input("\nPress Enter to speak (or 'quit' to exit): ").strip()
            
            if command.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Goodbye!")
                break
            
            # Record audio
            user_audio = await assistant.record_audio(duration_seconds=5)
            
            # Process conversation turn
            await assistant.conversation_turn(user_audio)
    
    finally:
        assistant.cleanup()


def main():
    """Main entry point."""
    
    # Check environment
    if not os.getenv('GOOGLE_GENAI_USE_VERTEXAI') and not os.getenv('GOOGLE_API_KEY'):
        print("⚠️  Please configure environment variables:")
        print("   Set GOOGLE_GENAI_USE_VERTEXAI=1 and GOOGLE_CLOUD_PROJECT")
        print("   OR set GOOGLE_API_KEY")
        return
    
    asyncio.run(run_interactive())


if __name__ == '__main__':
    main()
