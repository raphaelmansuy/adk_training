"""
Test Imports
Verify all package imports work correctly.
"""

import pytest


def test_import_package():
    """Test importing main package."""
    import voice_assistant

    assert voice_assistant is not None
    assert hasattr(voice_assistant, "__version__")


def test_import_voice_assistant():
    """Test importing VoiceAssistant class."""
    from voice_assistant import VoiceAssistant

    assert VoiceAssistant is not None


def test_import_root_agent():
    """Test importing root_agent."""
    from voice_assistant import root_agent

    assert root_agent is not None


# Removed: basic_live.py (duplicate of basic_demo.py)


# Removed demo scripts: demo.py, basic_demo.py, advanced.py, multi_agent.py, 
# direct_live_audio.py, interactive.py
# Use 'adk web' for Live API interaction instead


def test_pyaudio_availability():
    """Test PyAudio availability flag."""
    from voice_assistant.agent import PYAUDIO_AVAILABLE

    assert isinstance(PYAUDIO_AVAILABLE, bool)


def test_adk_imports():
    """Test Google ADK imports."""
    from google.adk.agents import Agent, LiveRequestQueue
    from google.adk.agents.run_config import RunConfig, StreamingMode
    from google.adk.apps import App
    from google.adk.runners import Runner
    from google.genai import types

    assert Agent is not None
    assert Runner is not None
    assert RunConfig is not None
    assert StreamingMode is not None
    assert LiveRequestQueue is not None
    assert App is not None
    assert types is not None
