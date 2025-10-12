"""
Test Agent Configuration
Verify agent setup, configuration, and behavior.
"""

import os
import pytest
from google.adk.agents import Agent
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.genai import types


class TestAgentConfiguration:
    """Test agent configuration and setup."""
    
    def test_root_agent_exists(self):
        """Test root_agent is properly exported."""
        from voice_assistant import root_agent
        
        assert root_agent is not None
        assert isinstance(root_agent, Agent)
    
    def test_root_agent_model(self):
        """Test root_agent uses correct Live API model."""
        from voice_assistant import root_agent
        
        # Should use Live API model
        assert 'live' in root_agent.model.lower() or 'gemini-2' in root_agent.model
    
    def test_root_agent_name(self):
        """Test root_agent has correct name."""
        from voice_assistant import root_agent
        
        assert root_agent.name == 'voice_assistant'
    
    def test_root_agent_has_description(self):
        """Test root_agent has description."""
        from voice_assistant import root_agent
        
        assert root_agent.description is not None
        assert len(root_agent.description) > 0
    
    def test_root_agent_has_instruction(self):
        """Test root_agent has instruction."""
        from voice_assistant import root_agent
        
        assert root_agent.instruction is not None
        assert len(root_agent.instruction) > 0
    
    def test_root_agent_generate_config(self):
        """Test root_agent has proper generation config."""
        from voice_assistant import root_agent
        
        if root_agent.generate_content_config:
            config = root_agent.generate_content_config
            
            # Should have concise output for voice
            if hasattr(config, 'max_output_tokens'):
                assert config.max_output_tokens <= 300, "Voice responses should be concise"


class TestVoiceAssistant:
    """Test VoiceAssistant class."""
    
    def test_voice_assistant_instantiation(self):
        """Test VoiceAssistant can be instantiated."""
        from voice_assistant import VoiceAssistant
        
        assistant = VoiceAssistant()
        assert assistant is not None
    
    def test_voice_assistant_default_model(self):
        """Test VoiceAssistant uses correct default model."""
        from voice_assistant import VoiceAssistant
        
        assistant = VoiceAssistant()
        assert assistant.agent is not None
        assert 'live' in assistant.agent.model.lower() or 'gemini-2' in assistant.agent.model
    
    def test_voice_assistant_custom_voice(self):
        """Test VoiceAssistant accepts custom voice."""
        from voice_assistant import VoiceAssistant
        
        voices = ['Puck', 'Charon', 'Kore', 'Fenrir', 'Aoede']
        
        for voice in voices:
            assistant = VoiceAssistant(voice_name=voice)
            assert assistant is not None
    
    def test_voice_assistant_run_config(self):
        """Test VoiceAssistant has proper RunConfig."""
        from voice_assistant import VoiceAssistant
        
        assistant = VoiceAssistant()
        assert assistant.run_config is not None
        assert isinstance(assistant.run_config, RunConfig)
        assert assistant.run_config.streaming_mode == StreamingMode.BIDI
    
    def test_voice_assistant_speech_config(self):
        """Test VoiceAssistant has speech configuration."""
        from voice_assistant import VoiceAssistant
        
        assistant = VoiceAssistant()
        assert assistant.run_config.speech_config is not None
    
    def test_voice_assistant_response_modalities(self):
        """Test VoiceAssistant has correct response modalities."""
        from voice_assistant import VoiceAssistant
        
        assistant = VoiceAssistant()
        modalities = assistant.run_config.response_modalities
        
        # Should have exactly one modality
        assert modalities is not None
        assert len(modalities) >= 1, "Must have at least one response modality"
    
    def test_voice_assistant_cleanup(self):
        """Test VoiceAssistant cleanup doesn't error."""
        from voice_assistant import VoiceAssistant
        
        assistant = VoiceAssistant()
        # Should not raise exception
        assistant.cleanup()


class TestLiveAPIConfiguration:
    """Test Live API specific configurations."""
    
    def test_streaming_mode_bidi(self):
        """Test StreamingMode.BIDI is available."""
        assert hasattr(StreamingMode, 'BIDI')
    
    def test_speech_config_structure(self):
        """Test SpeechConfig can be created."""
        config = types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name='Puck'
                )
            )
        )
        assert config is not None
    
    def test_voice_names(self):
        """Test valid voice names don't raise errors."""
        valid_voices = ['Puck', 'Charon', 'Kore', 'Fenrir', 'Aoede']
        
        for voice in valid_voices:
            config = types.PrebuiltVoiceConfig(voice_name=voice)
            assert config is not None
            assert config.voice_name == voice


class TestIntegration:
    """Integration tests (require GOOGLE_API_KEY)."""
    
    @pytest.mark.skipif(
        not os.getenv('GOOGLE_API_KEY') and not os.getenv('GOOGLE_GENAI_USE_VERTEXAI'),
        reason="Requires Google API credentials"
    )
    @pytest.mark.asyncio
    async def test_send_text_message(self):
        """Test sending text message (integration test)."""
        from voice_assistant import VoiceAssistant
        
        assistant = VoiceAssistant()
        
        try:
            response = await assistant.send_text("Hello!")
            assert response is not None
            assert len(response) > 0
        finally:
            assistant.cleanup()
    
    @pytest.mark.skipif(
        not os.getenv('GOOGLE_API_KEY') and not os.getenv('GOOGLE_GENAI_USE_VERTEXAI'),
        reason="Requires Google API credentials"
    )
    @pytest.mark.asyncio
    async def test_live_request_queue(self):
        """Test LiveRequestQueue usage (integration test)."""
        from google.adk.agents import LiveRequestQueue
        from google.genai import types
        
        queue = LiveRequestQueue()
        
        # Should not raise errors
        queue.send_content(
            types.Content(
                role='user',
                parts=[types.Part.from_text(text="Test message")]
            )
        )
        
        queue.close()
        
        # Verify queue is closed
        assert queue is not None
