#!/usr/bin/env python3
"""Check if audio dependencies are available."""

import importlib.util
import sys

missing = [m for m in ('pyaudio', 'numpy') if importlib.util.find_spec(m) is None]

if missing:
    print('   ❌ Missing audio packages: ' + ', '.join(missing))
    print('   👉 Install with: pip install pyaudio numpy')
    print('   👉 See AUDIO_SETUP.md for platform-specific instructions')
    sys.exit(1)

print('   ✅ Audio dependencies available.')
