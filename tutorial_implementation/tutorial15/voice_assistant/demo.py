"""
Demo Script - Text-Based Conversation
Demonstrates Live API without requiring microphone.
"""

import asyncio
import os
from voice_assistant.agent import VoiceAssistant


async def run_demo():
    """
    Run demo with text messages.
    No microphone required - uses send_text() method.
    """
    
    print("=" * 70)
    print("VOICE ASSISTANT DEMO - TEXT MODE")
    print("=" * 70)
    print()
    print("This demo uses text messages to simulate conversation.")
    print("No microphone required!")
    print()
    print("=" * 70)
    print()
    
    # Create assistant
    assistant = VoiceAssistant(
        model='gemini-live-2.5-flash-preview',
        voice_name='Puck'
    )
    
    # Demo conversation
    demo_messages = [
        "Hello! How are you today?",
        "Can you tell me a fun fact about space?",
        "That's fascinating! Tell me more about Venus.",
        "Thank you for the information!"
    ]
    
    try:
        for message in demo_messages:
            print(f"🎤 User: {message}")
            print("🤖 Agent: ", end='', flush=True)
            
            # Send text and get response
            response = await assistant.send_text(message)
            print(response)
            print()
            
            # Small delay for readability
            await asyncio.sleep(0.5)
        
        print("=" * 70)
        print("DEMO COMPLETE")
        print("=" * 70)
        
    finally:
        assistant.cleanup()


async def run_interactive_demo():
    """
    Run interactive text-based demo.
    User can type messages.
    """
    
    print("=" * 70)
    print("VOICE ASSISTANT - INTERACTIVE TEXT MODE")
    print("=" * 70)
    print()
    print("Type your messages (or 'quit' to exit)")
    print()
    print("=" * 70)
    print()
    
    assistant = VoiceAssistant(
        model='gemini-live-2.5-flash-preview',
        voice_name='Puck'
    )
    
    try:
        while True:
            # Get user input
            user_message = input("🎤 You: ").strip()
            
            if not user_message:
                continue
            
            if user_message.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Goodbye!")
                break
            
            print("🤖 Agent: ", end='', flush=True)
            
            # Send text and get response
            response = await assistant.send_text(user_message)
            print(response)
            print()
    
    finally:
        assistant.cleanup()


def main():
    """Main entry point."""
    
    # Check environment - support both Vertex AI and API keys for Live API
    has_vertex = os.getenv('GOOGLE_GENAI_USE_VERTEXAI') and os.getenv('GOOGLE_CLOUD_PROJECT')
    has_api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
    
    if not has_vertex and not has_api_key:
        print("⚠️  Live API requires authentication:")
        print()
        print("   Option 1 - Vertex AI (recommended for Live API):")
        print("   • GOOGLE_GENAI_USE_VERTEXAI=1")
        print("   • GOOGLE_CLOUD_PROJECT=your-project-id")
        print()
        print("   Option 2 - API Key (may have limitations):")
        print("   • GOOGLE_API_KEY=your-api-key")
        print("   • GEMINI_API_KEY=your-api-key")
        print()
        print("   Setup instructions:")
        print("   1. Copy .env.example to .env")
        print("   2. Edit .env with your credentials")
        print()
        print("💡 Alternative: Try 'make basic_demo' for a simpler example")
        return
    
    print(f"🔑 Using authentication: {'Vertex AI' if has_vertex else 'API Key'}")
    
    # Run automated demo by default
    # Uncomment the interactive version if you want to chat
    asyncio.run(run_demo())
    
    # For interactive mode:
    # asyncio.run(run_interactive_demo())


if __name__ == '__main__':
    main()
