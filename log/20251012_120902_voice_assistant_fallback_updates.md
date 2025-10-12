# Update Notes

- rebuilt `tutorial_implementation/tutorial15/voice_assistant/advanced.py`
  around the `_resolve_live_model` helper so every advanced demo selects a
  text-friendly Live model and keeps the examples readable
- fixed the `RunConfig` blocks in
  `tutorial_implementation/tutorial15/voice_assistant/basic_demo.py` and
  `tutorial_implementation/tutorial15/voice_assistant/basic_live.py` so
  `response_modalities` stays inside the call
- ran `python -m compileall` on the updated scripts to confirm they parse
  cleanly
