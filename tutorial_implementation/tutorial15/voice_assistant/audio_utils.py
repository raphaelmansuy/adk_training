"""
Audio Utilities for Live API Audio Processing

Handles audio playback, recording, and format conversion for Live API.
"""

import io
import wave
from typing import Optional, Tuple
import numpy as np

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    pyaudio = None


class AudioConfig:
    """Audio configuration constants for Live API."""
    
    # Live API expects 16-bit PCM, 16kHz, mono
    SAMPLE_RATE = 16000
    CHANNELS = 1
    SAMPLE_WIDTH = 2  # 16-bit = 2 bytes
    FORMAT = pyaudio.paInt16 if PYAUDIO_AVAILABLE else None
    CHUNK_SIZE = 1024
    
    # For microphone recording
    DEFAULT_RECORD_SECONDS = 5


class AudioPlayer:
    """Play audio received from Live API."""
    
    def __init__(self):
        """Initialize audio player."""
        if not PYAUDIO_AVAILABLE:
            raise RuntimeError(
                "PyAudio is not installed. Install with: pip install pyaudio\n"
                "See AUDIO_SETUP.md for platform-specific instructions."
            )
        self.audio = pyaudio.PyAudio()
    
    def play_pcm_bytes(self, audio_data: bytes) -> None:
        """
        Play raw PCM audio data.
        
        Args:
            audio_data: Raw PCM bytes (16-bit, 16kHz, mono)
        """
        if not audio_data:
            return
        
        # Open output stream
        stream = self.audio.open(
            format=AudioConfig.FORMAT,
            channels=AudioConfig.CHANNELS,
            rate=AudioConfig.SAMPLE_RATE,
            output=True,
            frames_per_buffer=AudioConfig.CHUNK_SIZE
        )
        
        try:
            # Play audio in chunks
            for i in range(0, len(audio_data), AudioConfig.CHUNK_SIZE * AudioConfig.SAMPLE_WIDTH):
                chunk = audio_data[i:i + AudioConfig.CHUNK_SIZE * AudioConfig.SAMPLE_WIDTH]
                stream.write(chunk)
        finally:
            stream.stop_stream()
            stream.close()
    
    def play_wav_bytes(self, wav_data: bytes) -> None:
        """
        Play WAV file from bytes.
        
        Args:
            wav_data: Complete WAV file as bytes
        """
        # Parse WAV file
        wav_io = io.BytesIO(wav_data)
        with wave.open(wav_io, 'rb') as wav_file:
            # Read audio data
            audio_data = wav_file.readframes(wav_file.getnframes())
            
            # Open output stream with WAV parameters
            stream = self.audio.open(
                format=self.audio.get_format_from_width(wav_file.getsampwidth()),
                channels=wav_file.getnchannels(),
                rate=wav_file.getframerate(),
                output=True
            )
            
            try:
                stream.write(audio_data)
            finally:
                stream.stop_stream()
                stream.close()
    
    def save_to_wav(self, audio_data: bytes, filename: str) -> None:
        """
        Save raw PCM audio to WAV file.
        
        Args:
            audio_data: Raw PCM bytes
            filename: Output WAV filename
        """
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(AudioConfig.CHANNELS)
            wav_file.setsampwidth(AudioConfig.SAMPLE_WIDTH)
            wav_file.setframerate(AudioConfig.SAMPLE_RATE)
            wav_file.writeframes(audio_data)
    
    def close(self):
        """Close audio resources."""
        if hasattr(self, 'audio') and self.audio:
            self.audio.terminate()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


class AudioRecorder:
    """Record audio from microphone for Live API."""
    
    def __init__(self):
        """Initialize audio recorder."""
        if not PYAUDIO_AVAILABLE:
            raise RuntimeError(
                "PyAudio is not installed. Install with: pip install pyaudio\n"
                "See AUDIO_SETUP.md for platform-specific instructions."
            )
        self.audio = pyaudio.PyAudio()
    
    def record_audio(
        self,
        duration_seconds: int = AudioConfig.DEFAULT_RECORD_SECONDS,
        show_progress: bool = True
    ) -> bytes:
        """
        Record audio from microphone.
        
        Args:
            duration_seconds: Recording duration in seconds
            show_progress: Show recording progress
            
        Returns:
            Raw PCM audio bytes (16-bit, 16kHz, mono)
        """
        if show_progress:
            print(f"🎤 Recording for {duration_seconds} seconds...")
        
        # Open input stream
        stream = self.audio.open(
            format=AudioConfig.FORMAT,
            channels=AudioConfig.CHANNELS,
            rate=AudioConfig.SAMPLE_RATE,
            input=True,
            frames_per_buffer=AudioConfig.CHUNK_SIZE
        )
        
        frames = []
        num_chunks = int(AudioConfig.SAMPLE_RATE / AudioConfig.CHUNK_SIZE * duration_seconds)
        
        try:
            for i in range(num_chunks):
                data = stream.read(AudioConfig.CHUNK_SIZE)
                frames.append(data)
                
                if show_progress and i % 10 == 0:
                    progress = (i / num_chunks) * 100
                    print(f"\r🎤 Recording: {progress:.0f}%", end='', flush=True)
            
            if show_progress:
                print("\r🎤 Recording complete!     ")
        finally:
            stream.stop_stream()
            stream.close()
        
        return b''.join(frames)
    
    def close(self):
        """Close audio resources."""
        if hasattr(self, 'audio') and self.audio:
            self.audio.terminate()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def check_audio_available() -> Tuple[bool, Optional[str]]:
    """
    Check if audio functionality is available.
    
    Returns:
        Tuple of (is_available, error_message)
    """
    if not PYAUDIO_AVAILABLE:
        return False, (
            "PyAudio is not installed.\n"
            "Install with: pip install pyaudio\n"
            "See AUDIO_SETUP.md for platform-specific instructions."
        )
    
    # Try to initialize PyAudio
    try:
        audio = pyaudio.PyAudio()
        
        # Check for input devices
        has_input = False
        has_output = False
        
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                has_input = True
            if device_info['maxOutputChannels'] > 0:
                has_output = True
        
        audio.terminate()
        
        if not has_input:
            return False, "No microphone detected. Please connect a microphone."
        
        if not has_output:
            return False, "No audio output detected. Please connect speakers/headphones."
        
        return True, None
        
    except Exception as e:
        return False, f"Audio initialization failed: {str(e)}"


def print_audio_devices():
    """Print available audio devices for debugging."""
    if not PYAUDIO_AVAILABLE:
        print("❌ PyAudio is not installed")
        return
    
    try:
        audio = pyaudio.PyAudio()
        
        print("\n" + "=" * 70)
        print("AVAILABLE AUDIO DEVICES")
        print("=" * 70)
        
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            print(f"\nDevice {i}: {device_info['name']}")
            print(f"  Max Input Channels: {device_info['maxInputChannels']}")
            print(f"  Max Output Channels: {device_info['maxOutputChannels']}")
            print(f"  Default Sample Rate: {device_info['defaultSampleRate']}")
        
        print("\n" + "=" * 70)
        
        audio.terminate()
        
    except Exception as e:
        print(f"❌ Error listing audio devices: {e}")


def pcm_to_numpy(pcm_data: bytes) -> np.ndarray:
    """
    Convert PCM bytes to numpy array.
    
    Args:
        pcm_data: Raw PCM bytes (16-bit)
        
    Returns:
        Numpy array of audio samples
    """
    return np.frombuffer(pcm_data, dtype=np.int16)


def numpy_to_pcm(audio_array: np.ndarray) -> bytes:
    """
    Convert numpy array to PCM bytes.
    
    Args:
        audio_array: Numpy array of audio samples
        
    Returns:
        Raw PCM bytes (16-bit)
    """
    return audio_array.astype(np.int16).tobytes()


def adjust_volume(audio_data: bytes, volume_factor: float) -> bytes:
    """
    Adjust audio volume.
    
    Args:
        audio_data: Raw PCM bytes
        volume_factor: Volume multiplier (1.0 = original, 2.0 = double, 0.5 = half)
        
    Returns:
        Adjusted PCM bytes
    """
    audio_array = pcm_to_numpy(audio_data)
    adjusted = np.clip(audio_array * volume_factor, -32768, 32767)
    return numpy_to_pcm(adjusted)


if __name__ == '__main__':
    # Test audio availability
    available, error = check_audio_available()
    
    if available:
        print("✅ Audio functionality is available!")
        print_audio_devices()
    else:
        print(f"❌ Audio not available: {error}")
