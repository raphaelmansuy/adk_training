"""
Streaming Chat Application with SSE - Tutorial 14

Real-time interactive chat with progressive responses.
Complete implementation of the StreamingChatApp class from the tutorial.
"""

import asyncio
import os
from datetime import datetime
from typing import AsyncIterator
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Environment setup
os.environ.setdefault('GOOGLE_GENAI_USE_VERTEXAI', 'FALSE')


class StreamingChatApp:
    """Interactive streaming chat application."""

    def __init__(self):
        """Initialize chat application."""

        # Create chat agent
        self.agent = Agent(
            model='gemini-2.0-flash',
            name='chat_assistant',
            description='An assistant that engages in natural conversation.',
            instruction="""
You are a helpful, friendly assistant engaging in natural conversation.

Guidelines:
- Be conversational and engaging
- Provide detailed explanations when asked
- Ask clarifying questions if needed
- Remember conversation context
- Be concise for simple queries, detailed for complex ones
            """.strip(),
            generate_content_config=types.GenerateContentConfig(
                temperature=0.7,  # Conversational
                max_output_tokens=2048
            )
        )

        # Create session for conversation context
        self.session_service = InMemorySessionService()
        self.session = None
        self.runner = Runner(app_name="streaming_chat", agent=self.agent, session_service=self.session_service)

        # Configure streaming
        self.run_config = RunConfig(
            streaming_mode=StreamingMode.SSE,
            max_llm_calls=50
        )

    async def initialize_session(self):
        """Initialize or get existing session."""
        if self.session is None:
            self.session = await self.session_service.create_session(
                app_name="streaming_chat",
                user_id="chat_user"
            )

    async def stream_response(self, user_message: str) -> AsyncIterator[str]:
        """
        Stream agent response to user message.

        Args:
            user_message: User's input message

        Yields:
            Text chunks as they're generated
        """
        await self.initialize_session()

        # Run agent with streaming
        async for event in self.runner.run_async(
            user_id="chat_user",
            session_id=self.session.id,
            new_message=types.Content(role="user", parts=[types.Part(text=user_message)]),
            run_config=self.run_config
        ):
            # Extract text from event
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        yield part.text

            # Check for completion
            if event.turn_complete:
                break

    async def chat_turn(self, user_message: str):
        """
        Execute one chat turn with streaming display.

        Args:
            user_message: User's input message
        """

        # Display user message
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"\n[{timestamp}] User: {user_message}")

        # Display agent response with streaming
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] Agent: ", end='', flush=True)

        # Stream response chunks
        async for chunk in self.stream_response(user_message):
            print(chunk, end='', flush=True)

        print()  # New line after complete response

    async def run_interactive(self):
        """Run interactive chat loop."""

        print("="*70)
        print("STREAMING CHAT APPLICATION")
        print("="*70)
        print("Type 'exit' or 'quit' to end conversation")
        print("="*70)

        while True:
            try:
                # Get user input
                user_input = input("\nYou: ").strip()

                if not user_input:
                    continue

                # Check for exit
                if user_input.lower() in ['exit', 'quit']:
                    print("\nGoodbye!")
                    break

                # Process chat turn
                await self.chat_turn(user_input)

            except KeyboardInterrupt:
                print("\n\nInterrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")

    async def run_demo(self):
        """Run demo conversation."""

        print("="*70)
        print("STREAMING CHAT DEMO")
        print("="*70)

        demo_messages = [
            "Hello! What can you help me with?",
            "Explain quantum computing in simple terms",
            "What are the practical applications?",
            "How does it compare to classical computing?"
        ]

        for message in demo_messages:
            await self.chat_turn(message)
            await asyncio.sleep(1)  # Pause between turns


async def main():
    """Main entry point."""

    chat = StreamingChatApp()

    # Run demo
    await chat.run_demo()

    # Uncomment for interactive mode:
    # await chat.run_interactive()


if __name__ == '__main__':
    asyncio.run(main())