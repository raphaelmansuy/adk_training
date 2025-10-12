# 2025-10-12 07:33:02 Tutorial 15 text fallback model fix
- Prefixed fallback model with "models/" when missing so API-key runs succeed
- Added ClientError handling that returns a friendly message instead of crashing
- Demo remains text-only under API key but now completes without exceptions
