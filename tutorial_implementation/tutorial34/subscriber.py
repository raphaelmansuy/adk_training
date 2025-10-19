import os
import sys
import json
import asyncio
import logging
from google.cloud import pubsub_v1
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pubsub_agent.agent import root_agent

# Suppress noisy debug messages from libraries
logging.getLogger('google.auth').setLevel(logging.WARNING)
logging.getLogger('google.cloud').setLevel(logging.WARNING)
logging.getLogger('google.genai').setLevel(logging.WARNING)
logging.getLogger('absl').setLevel(logging.ERROR)

project_id = os.environ.get("GCP_PROJECT")
subscription_id = "document-processor"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

async def process_document_with_agent(document_id: str, content: str):
    """Process document using the ADK root_agent coordinator."""
    try:
        # Create a runner for the agent with required session service
        session_service = InMemorySessionService()
        runner = Runner(
            app_name="pubsub_processor",
            agent=root_agent,
            session_service=session_service
        )
        
        # Create a session for this document processing
        session = await session_service.create_session(
            app_name="pubsub_processor",
            user_id="pubsub_subscriber"
        )
        
        # Prepare the message for the agent
        prompt_text = f"""Analyze this document and route it to the appropriate analyzer:

Document ID: {document_id}

Content:
{content}

Analyze the document type and extract relevant information."""
        
        # Create a proper Content object for the agent
        prompt = types.Content(
            role="user",
            parts=[types.Part(text=prompt_text)]
        )
        
        # Run the agent and collect the result
        final_result = None
        async for event in runner.run_async(
            user_id="pubsub_subscriber",
            session_id=session.id,
            new_message=prompt
        ):
            # Events are streamed, capture the final one
            final_result = event
        
        return final_result
        
    except Exception as e:
        print(f"❌ Agent processing error: {e}")
        raise

def process_message(message):
    """Process Pub/Sub message with async agent processing."""
    try:
        data = json.loads(message.data.decode("utf-8"))
        document_id = data.get("document_id")
        content = data.get("content")

        print(f"\n� Processing: {document_id}")

        # Run the async agent processing
        result = asyncio.run(process_document_with_agent(document_id, content))

        if result:
            # Extract text from the event's content
            response_text = ""
            if hasattr(result, 'content') and result.content and result.content.parts:
                for part in result.content.parts:
                    if part.text:
                        response_text += part.text
            
            if response_text:
                # Clean up the response text for display
                display_text = response_text.strip()[:200]
                print(f"✅ Success: {document_id}")
                print(f"   └─ {display_text}...")
            else:
                print(f"✅ Completed {document_id} (no text response)")
        else:
            print(f"✅ Completed {document_id}")

        # Acknowledge message (remove from queue)
        message.ack()

    except Exception as e:
        print(f"❌ Error: {document_id} - {str(e)[:100]}")
        message.nack()

# Subscribe and process
print("\n" + "="*70)
print("🚀 Document Processing Coordinator")
print("="*70)
print(f"Subscription: {subscription_id}")
print(f"Project:      {project_id or '(not set - local mode)'}")
print(f"Agent:        root_agent (multi-analyzer coordinator)")
print("="*70)
print("Waiting for messages...\n")

streaming_pull_future = subscriber.subscribe(
    subscription_path,
    callback=process_message
)

try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
    print("\n" + "="*70)
    print("✋ Processor stopped")
    print("="*70)
