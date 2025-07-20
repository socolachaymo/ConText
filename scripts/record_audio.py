# This script records audio from the microphone for a specified duration
# and saves it as a WAV file.
import pyaudio
import wave
import os

def record_audio(output_filename="output_audio/recorded_audio.wav", duration=10, sample_rate=44100, chunk=1024, channels=1):
    """
    Records audio from the microphone for a specified duration and saves it to a file.
    """
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    audio_format = pyaudio.paInt16
    p = pyaudio.PyAudio()

    print(f"Recording for {duration} seconds...")

    stream = p.open(format=audio_format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []

    for i in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a WAV file
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(audio_format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))
    
    print(f"Audio saved to {output_filename}")

if __name__ == "__main__":
    record_audio()