# Tutorial 15 Makefile live audio improvements

- added live_env_check, audio_deps_check, and live_smoke targets to validate Vertex
  AI setup and audio deps
- defaulted Makefile exports for live model and region, enhancing demo instructions
- replaced heredocs with portable python -c invocations to prevent make parsing errors
