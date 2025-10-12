"""
Advanced Live API Features
Demonstrations for proactivity, affective dialog, and video streaming patterns.
"""

import asyncio
import os
from typing import AsyncIterable

from google.adk.agents import Agent, LiveRequestQueue
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.apps import App
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

LIVE_MODEL = (os.getenv("VOICE_ASSISTANT_LIVE_MODEL") or "").strip()


def _resolve_live_model() -> str:
    """Use the configured Live model for demos."""

    model = LIVE_MODEL
    if not model:
        raise RuntimeError(
            "Set VOICE_ASSISTANT_LIVE_MODEL to a Live API model. "
            "Example: gemini-live-2.5-flash-preview-native-audio-09-2025"
        )

    print(f"ℹ️  Using Live API model: {model}")
    return model


def _print_header(title: str) -> None:
    print("=" * 70)
    print(title)
    print("=" * 70)


async def _collect_text_events(events: AsyncIterable) -> None:
    """Stream and display events from Live API (audio or text)."""

    async for event in events:
        content = getattr(event, "content", None)
        if not content or not getattr(content, "parts", None):
            continue
        for part in content.parts:
            # Check for text content
            text = getattr(part, "text", None)
            if text:
                print(text, end="", flush=True)
                continue
            
            # Check for audio content
            inline_data = getattr(part, "inline_data", None)
            if inline_data:
                mime_type = getattr(inline_data, "mime_type", "")
                if "audio" in mime_type:
                    print("[🔊 Audio response received]", end="", flush=True)


async def proactivity_example() -> None:
    """Demonstrate proactive follow-ups from an assistant."""

    model_to_use = _resolve_live_model()
    _print_header("PROACTIVITY EXAMPLE")
    print(f"Configured live model: {model_to_use}")
    print()
    print("The agent keeps context and offers proactive follow-up options.")
    print()

    agent = Agent(
        model=model_to_use,
        name="proactive_planner",
        instruction="""
You are a proactive planning assistant.
Respond conversationally and offer helpful follow-up suggestions.
If the user describes a goal, anticipate next steps and check if they want reminders.
        """.strip(),
    )

    run_config = RunConfig(
        streaming_mode=StreamingMode.BIDI,
        response_modalities=[types.Modality.AUDIO],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Aoede")
            )
        ),
    )

    app = App(name="proactivity_app", root_agent=agent)
    session_service = InMemorySessionService()
    runner = Runner(app=app, session_service=session_service)

    user_id = "proactivity_user"
    session = await runner.session_service.create_session(
        app_name=app.name,
        user_id=user_id,
    )

    scripted_turns = [
        "I need to plan a birthday party for my friend this weekend.",
        "Yes, please draft a quick checklist and ask if I need reminders.",
    ]

    for turn in scripted_turns:
        queue = LiveRequestQueue()
        print(f"🎤 User: {turn}")
        queue.send_content(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=turn)],
            )
        )
        queue.close()

        print("🤖 Agent: ", end="", flush=True)
        await _collect_text_events(
            runner.run_live(
                live_request_queue=queue,
                user_id=user_id,
                session_id=session.id,
                run_config=run_config,
            )
        )
        print("\n")
        await asyncio.sleep(0.5)


async def affective_dialog_example() -> None:
    """Show emotion-aware responses using affective dialog."""

    model_to_use = _resolve_live_model()
    _print_header("AFFECTIVE DIALOG EXAMPLE")
    print(f"Configured live model: {model_to_use}")
    print()
    print("Emotion detection steers response tone for different user moods.")
    print()

    agent = Agent(
        model=model_to_use,
        name="empathetic_assistant",
        instruction="""
You are an empathetic assistant that adapts tone to the user's emotion.
Keep responses concise, supportive, and emotionally aware.
        """.strip(),
    )

    run_config = RunConfig(
        streaming_mode=StreamingMode.BIDI,
        enable_affective_dialog=True,
        response_modalities=[types.Modality.AUDIO],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Kore")
            )
        ),
    )

    app = App(name="affective_app", root_agent=agent)
    session_service = InMemorySessionService()
    runner = Runner(app=app, session_service=session_service)

    user_id = "affective_user"
    session = await runner.session_service.create_session(
        app_name=app.name,
        user_id=user_id,
    )

    test_messages = [
        ("I just got promoted at work!", "Happy"),
        ("I'm having a really tough day...", "Sad"),
        ("What's the weather forecast?", "Neutral"),
    ]

    for message, emotion in test_messages:
        queue = LiveRequestQueue()
        print(f"🎤 User ({emotion}): {message}")
        queue.send_content(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=message)],
            )
        )
        queue.close()

        print("🤖 Agent: ", end="", flush=True)
        await _collect_text_events(
            runner.run_live(
                live_request_queue=queue,
                user_id=user_id,
                session_id=session.id,
                run_config=run_config,
            )
        )
        print("\n")
        await asyncio.sleep(0.5)


async def video_streaming_example() -> None:
    """Outline a conceptual pattern for video streaming."""

    model_to_use = _resolve_live_model()
    _print_header("VIDEO STREAMING EXAMPLE (CONCEPTUAL)")
    print(f"Configured live model: {model_to_use}")
    print()
    print("Video streaming requires camera capture and binary frame uploads.")
    print("Below is a conceptual snippet showing the integration points.")
    print()

    agent = Agent(
        model=model_to_use,
        name="vision_assistant",
        instruction="""
You analyze live video streams and describe notable objects, actions, and context.
Keep observations brief and update as the scene changes.
        """.strip(),
    )

    run_config = RunConfig(
        streaming_mode=StreamingMode.BIDI,
        response_modalities=[types.Modality.AUDIO],
    )

    _ = (agent, run_config)  # Placeholder to highlight configuration reuse

    print("Sample integration code:\n")
    print("""python
import cv2
from google.genai import types
from google.adk.agents import LiveRequestQueue

cap = cv2.VideoCapture(0)
queue = LiveRequestQueue()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        queue.send_realtime(
            blob=types.Blob(data=frame_bytes, mime_type='image/jpeg')
        )

        await asyncio.sleep(0.1)  # ~10 FPS pacing
finally:
    queue.close()
    cap.release()
""")
    print()


async def main() -> None:
    """Run all advanced examples sequentially."""

    if not os.getenv("GOOGLE_GENAI_USE_VERTEXAI") and not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Configure GOOGLE_GENAI_USE_VERTEXAI + GOOGLE_CLOUD_PROJECT or GOOGLE_API_KEY.")
        return

    print()
    print("=" * 70)
    print("ADVANCED LIVE API FEATURES - CONCEPTUAL OVERVIEW")
    print("=" * 70)
    print()
    print("This demo showcases advanced Live API patterns:")
    print("  • Proactivity: Context-aware follow-ups and suggestions")
    print("  • Affective Dialog: Emotion detection and adaptive responses")
    print("  • Video Streaming: Real-time video analysis patterns")
    print()
    print("⚠️  NOTE: Full Live API execution requires:")
    print("  1. Native audio model (e.g., gemini-live-2.5-flash-preview-native-audio-09-2025)")
    print("  2. Audio I/O infrastructure (microphone, speakers)")
    print("  3. PyAudio for audio capture and playback")
    print()
    print("For interactive voice demos, use: make interactive_demo")
    print()
    print("=" * 70)
    print()
    
    # Show conceptual patterns only
    await video_streaming_example()


if __name__ == "__main__":
    asyncio.run(main())
