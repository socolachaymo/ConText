import cv2
import time
import pyaudio
import wave
import threading
import subprocess
import os

def record_video(output_file, duration=10):
    """
    Records video and audio simultaneously from the default devices.
    """
    temp_video_file = "temp_video.mp4"
    temp_audio_file = "temp_audio.wav"

    # --- Audio Recording Thread ---
    def record_audio_thread_func(audio_file, record_duration):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        
        p = pyaudio.PyAudio()
        
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        
        print("Recording audio...")
        
        frames = []
        
        for _ in range(0, int(RATE / CHUNK * record_duration)):
            data = stream.read(CHUNK)
            frames.append(data)
            
        print("Finished recording audio.")
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        wf = wave.open(audio_file, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    # --- Video Recording ---
    def record_video_thread_func(video_file, record_duration):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return

        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_file, fourcc, 20.0, (frame_width, frame_height))

        print(f"Recording video for {record_duration} seconds...")
        start_time = time.time()
        while (time.time() - start_time) < record_duration:
            ret, frame = cap.read()
            if ret:
                out.write(frame)
            else:
                break
        
        cap.release()
        out.release()
        print("Finished recording video.")

    # --- Start Recording Threads ---
    audio_thread = threading.Thread(target=record_audio_thread_func, args=(temp_audio_file, duration))
    video_thread = threading.Thread(target=record_video_thread_func, args=(temp_video_file, duration))

    audio_thread.start()
    video_thread.start()

    audio_thread.join()
    video_thread.join()

    # --- Merge Audio and Video using ffmpeg ---
    print("Merging audio and video...")
    # Using -nostdin to prevent ffmpeg from consuming stdin, which can cause issues when run from a web server
    command = [
        'ffmpeg',
        '-y',  # Overwrite output file if it exists
        '-i', temp_video_file,
        '-i', temp_audio_file,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        output_file
    ]
    
    try:
        # Using DEVNULL to avoid hanging on some systems
        process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print("Error during ffmpeg merging:")
            print(stderr.decode())
        else:
            print(f"Video saved to {output_file}")
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please ensure ffmpeg is installed and in your system's PATH.")
    except Exception as e:
        print(f"An error occurred during merging: {e}")
    finally:
        # --- Clean up temporary files ---
        if os.path.exists(temp_video_file):
            os.remove(temp_video_file)
        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)

if __name__ == '__main__':
    record_video('test_recording_with_audio.mp4', duration=5)