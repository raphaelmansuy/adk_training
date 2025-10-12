# 2025-10-12 07:31:17 Tutorial 15 Live API fallback and messaging update
- Added Responses API fallback in voice_assistant/agent.py when Vertex Live is unavailable or fails
- Restored speech configuration in RunConfig so tests reference non-null speech_config
- Updated make demo messaging to explain text-only fallback for API-key auth
- Demo script now warns users when fallback mode triggers
