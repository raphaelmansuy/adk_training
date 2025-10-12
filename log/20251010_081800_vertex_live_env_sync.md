# Tutorial 15 Vertex Live environment sync update

- ensured Vertex demos export both `GOOGLE_CLOUD_LOCATION` and `GOOGLE_GENAI_VERTEXAI_LOCATION`
- updated `voice_assistant.agent` to propagate the region env vars automatically
- refreshed demo scripts to warn about missing `GOOGLE_CLOUD_LOCATION`
- verified `make demo` now loads Vertex client and
  falls back cleanly when the live model is unavailable
