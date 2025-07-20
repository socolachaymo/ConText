# This script converts an audio file to a video file with a black screen using ffmpeg.
# This is useful for processing audio files with tools that expect video input.
import os
import subprocess

def convert_audio_to_video(audio_path, output_path):
    """
    Converts an audio file to a video file with a black screen using ffmpeg.
    """
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found at {audio_path}")
        return False

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Construct the ffmpeg command
    command = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', 'color=c=black:s=1280x720:r=30', # Black screen input
        '-i', audio_path,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-shortest',
        '-y', # Overwrite output file if it exists
        output_path
    ]

    print(f"Converting {audio_path} to {output_path}...")
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print("Conversion successful.")
        return True
    except subprocess.CalledProcessError as e:
        print("Error during ffmpeg conversion:")
        print(e.stderr)
        return False

if __name__ == '__main__':
    audio_file = "audio_clips/KES WOTLESS Music Video.mp3"
    video_file = "temp_videos/KES_WOTLESS_video.mp4"
    convert_audio_to_video(audio_file, video_file)