# Audio Setup Guide for Tutorial 15

This guide helps you set up audio functionality for the Live API audio demos.

## Quick Check

Before installing, verify audio is needed:

```bash
# Check if audio utilities are available
make check_audio
```

## Requirements

- **Python 3.8+**
- **PyAudio** for audio I/O
- **Microphone** (for interactive demo)
- **Speakers/Headphones** (for audio playback)

## Platform-Specific Installation

### macOS

#### Option 1: Using Homebrew (Recommended)

```bash
# Install portaudio (PyAudio dependency)
brew install portaudio

# Install PyAudio
pip install pyaudio

# Verify installation
python -c "import pyaudio; print('✅ PyAudio installed successfully!')"
```

#### Option 2: Pre-built Wheels

```bash
# Install pre-built PyAudio wheel
pip install pyaudio

# If above fails, try:
pip install --upgrade pip
pip install pyaudio
```

#### Troubleshooting macOS

**Issue**: `fatal error: 'portaudio.h' file not found`

```bash
# Solution: Install portaudio first
brew install portaudio

# Then reinstall PyAudio with explicit paths
pip install --global-option="build_ext" \
  --global-option="-I/opt/homebrew/include" \
  --global-option="-L/opt/homebrew/lib" \
  pyaudio
```

**Issue**: Microphone permission denied

```bash
# macOS requires microphone permission
# Go to: System Preferences → Security & Privacy → Privacy → Microphone
# Enable microphone access for Terminal or your Python IDE
```

### Linux (Ubuntu/Debian)

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y portaudio19-dev python3-pyaudio

# Install PyAudio
pip install pyaudio

# Verify installation
python -c "import pyaudio; print('✅ PyAudio installed successfully!')"
```

#### Alternative: Build from Source

```bash
# Install build dependencies
sudo apt-get install -y python3-dev portaudio19-dev

# Install PyAudio
pip install pyaudio
```

#### Troubleshooting Linux

**Issue**: No audio devices detected

```bash
# Check audio devices
aplay -l   # List playback devices
arecord -l # List recording devices

# Install ALSA utilities if missing
sudo apt-get install alsa-utils

# Test microphone
arecord -d 5 test.wav  # Record 5 seconds
aplay test.wav         # Play back
```

**Issue**: Permission denied for audio devices

```bash
# Add user to audio group
sudo usermod -a -G audio $USER

# Log out and log back in for changes to take effect
```

### Windows

#### Option 1: Pre-built Wheels (Easiest)

```powershell
# Install PyAudio from pre-built wheel
pip install pyaudio

# If above fails, try unofficial binaries:
# Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Then: pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl
```

#### Option 2: Using pipwin

```powershell
# Install pipwin
pip install pipwin

# Install PyAudio using pipwin
pipwin install pyaudio
```

#### Troubleshooting Windows

**Issue**: Microsoft Visual C++ 14.0 required

```powershell
# Install Visual Studio Build Tools
# Download from: https://visualstudio.microsoft.com/downloads/
# Select "Desktop development with C++"

# Or use pre-built wheels (Option 1)
```

**Issue**: No microphone detected

```powershell
# Check Windows sound settings
# Settings → System → Sound → Input
# Ensure microphone is enabled and set as default
```

## Verify Installation

After installing PyAudio:

```bash
# Check audio devices
make check_audio

# Or manually:
python -m voice_assistant.audio_utils
```

Expected output:
```
✅ Audio functionality is available!

======================================================================
AVAILABLE AUDIO DEVICES
======================================================================

Device 0: Built-in Microphone
  Max Input Channels: 2
  Max Output Channels: 0
  Default Sample Rate: 48000.0

Device 1: Built-in Output
  Max Input Channels: 0
  Max Output Channels: 2
  Default Sample Rate: 48000.0
```

## Testing Audio

### Test Audio Playback

```bash
# Run basic demo with audio output
make basic_demo_audio
```

This will:
1. Send a text message to the agent
2. Receive audio response
3. Play audio through speakers
4. Save audio to `response.wav`

### Test Full Interactive Audio

```bash
# Run interactive demo (microphone + speakers)
make audio_demo
```

This will:
1. Record from your microphone (5 seconds)
2. Send audio to Live API
3. Receive audio response
4. Play response through speakers

## Common Issues

### "PyAudio is not installed"

```bash
# Follow platform-specific installation above
pip install pyaudio
```

### "No microphone detected"

**macOS**: Check System Preferences → Security & Privacy → Microphone

**Linux**: 
```bash
arecord -l  # List recording devices
# If empty, check hardware connection
```

**Windows**: Settings → System → Sound → Input

### "No audio output detected"

Ensure speakers/headphones are:
- Connected
- Powered on
- Set as default audio output device
- Not muted

### Audio Quality Issues

The Live API expects specific audio format:
- **Format**: 16-bit PCM
- **Sample Rate**: 16kHz
- **Channels**: Mono (1 channel)

If audio quality is poor:

```bash
# Check if your device supports 16kHz
python -c "
import pyaudio
p = pyaudio.PyAudio()
info = p.get_default_input_device_info()
print(f'Default Sample Rate: {info[\"defaultSampleRate\"]}')
p.terminate()
"
```

Most devices support 16kHz, but audio utils will resample if needed.

## Alternative: Text-Only Mode

If audio setup is too complex, use text-only demos:

```bash
# Basic demo with text responses (no audio)
make basic_demo_text

# Or regular demo (text conversation)
make demo
```

## Docker/Container Environments

Audio in containers requires special configuration:

### Docker on macOS/Linux

```dockerfile
# In your Dockerfile, add:
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    alsa-utils \
    && pip install pyaudio

# Run with audio device access:
docker run --device /dev/snd:/dev/snd your-image
```

### Docker on Windows with WSL2

Audio support in WSL2 is limited. Consider:
- Running demos directly on Windows
- Using text-only mode
- Connecting to a remote machine with audio

## CI/CD Environments

For testing without audio hardware:

```python
# Mock audio in tests
from unittest.mock import patch

with patch('voice_assistant.audio_utils.PYAUDIO_AVAILABLE', False):
    # Run tests in text-only mode
    pass
```

Or use text-only demos:

```bash
# In CI pipeline
make basic_demo_text  # No audio required
```

## Getting Help

If you encounter issues:

1. **Check audio devices**: `make check_audio`
2. **Test microphone**: Use system sound settings
3. **Verify PyAudio**: `python -c "import pyaudio; print(pyaudio.__version__)"`
4. **Check documentation**: [PyAudio docs](https://people.csail.mit.edu/hubert/pyaudio/)
5. **Use text mode**: Fall back to text-only demos

## Next Steps

Once audio is working:

```bash
# 1. Test basic audio playback
make basic_demo_audio

# 2. Try interactive conversation
make audio_demo

# 3. Explore advanced features
make advanced_demo
```

## Additional Resources

- **PyAudio Documentation**: https://people.csail.mit.edu/hubert/pyaudio/
- **PortAudio**: http://www.portaudio.com/
- **Live API Docs**: https://ai.google.dev/gemini-api/docs/live
- **Tutorial 15**: [Full documentation](../../docs/tutorial/15_live_api_audio.md)
