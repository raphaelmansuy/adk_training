"""Quick debug script to test audio response."""
import asyncio
import os
from google.adk.agents import Agent, LiveRequestQueue
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.apps import App
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

async def test():
    model = 'gemini-2.0-flash-live-preview-04-09'
    agent = Agent(
        model=model,
        name='test_agent',
        instruction='Keep response very short - just say hello.'
    )
    
    run_config = RunConfig(
        streaming_mode=StreamingMode.BIDI,
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Puck')
            )
        ),
        response_modalities=[types.Modality.AUDIO],
    )
    
    queue = LiveRequestQueue()
    app = App(name='test_app', root_agent=agent)
    session_service = InMemorySessionService()
    runner = Runner(app=app, session_service=session_service)
    session = await runner.session_service.create_session(app_name=app.name, user_id='test')
    
    queue.send_content(types.Content(role='user', parts=[types.Part.from_text(text='Hello')]))
    queue.close()
    
    print('Starting run_live...')
    event_count = 0
    async for event in runner.run_live(
        live_request_queue=queue,
        user_id='test',
        session_id=session.id,
        run_config=run_config
    ):
        event_count += 1
        print(f'Event {event_count}: {type(event).__name__}')
        if hasattr(event, 'server_content') and event.server_content:
            print(f'  Has server_content with {len(event.server_content.parts)} parts')
            for i, part in enumerate(event.server_content.parts):
                has_text = bool(getattr(part, 'text', None))
                has_inline = bool(getattr(part, 'inline_data', None))
                print(f'  Part {i}: text={has_text}, inline_data={has_inline}')
                if has_inline:
                    print(f'    Audio data size: {len(part.inline_data.data)} bytes')
        if event_count > 50:
            print('Stopping after 50 events')
            break
    print(f'Total events: {event_count}')

if __name__ == '__main__':
    asyncio.run(test())
