#!/usr/bin/env python3
"""Quick smoke test for Vertex AI text API connectivity."""

import os
import sys
from google.genai import Client, types

project = os.environ['GOOGLE_CLOUD_PROJECT']
location = os.environ.get('GOOGLE_CLOUD_LOCATION', 'us-central1')
model = os.environ.get('VOICE_ASSISTANT_TEXT_MODEL', 'gemini-2.5-flash')

try:
    client = Client(vertexai=True, project=project, location=location)
    response = client.models.generate_content(
        model=model,
        contents=[types.Content(role='user', parts=[types.Part.from_text(text='ping')])]
    )
except Exception as exc:
    print(f'   ❌ Live smoke test failed: {exc}')
    sys.exit(1)

text = ''
for candidate in getattr(response, 'candidates', []) or []:
    content = getattr(candidate, 'content', None)
    if not content:
        continue
    for part in getattr(content, 'parts', []) or []:
        value = getattr(part, 'text', None)
        if value:
            text += value
    if text:
        break

print('   ✅ Vertex text API reachable.')
if text:
    preview = text.replace('\n', ' ')[:120]
    print(f'   ↪ Sample response: {preview}')
